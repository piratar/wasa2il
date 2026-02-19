import base64
import hashlib
import requests
import secrets
import urllib.parse

from jose import jwt

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.shortcuts import render

from core.models import UserProfile, event_register
from core.signals import user_verified
from core.utils import is_ssn_human_or_institution
from core.utils import calculate_age_from_ssn

from kenniclient import constants
from kenniclient import forms as kenniforms

AUTH_ENDPOINT = f"{constants.ISSUER}/oidc/auth"
TOKEN_ENDPOINT = f"{constants.ISSUER}/oidc/token"
JWKS_ENDPOINT = f"{constants.ISSUER}/oidc/jwks"

def generate_code_verifier(length=64):
    return secrets.token_urlsafe(length)

def generate_code_challenge(verifier):
    """Generate a code challenge from the code verifier."""
    sha256_verifier = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(sha256_verifier).rstrip(b"=").decode()

def exchange_code_for_tokens(code: str, code_verifier: str):
    """
    Exchange the code for an access token by posting the code to the token endpoint
    """

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "redirect_uri": constants.REDIRECT_URL,
        "code": code,
        "client_id": constants.CLIENT_ID,
        "client_secret": constants.CLIENT_SECRET,
        "code_verifier": code_verifier,
    }

    # POST the code to the oidc server's token endpoint
    response = requests.post(TOKEN_ENDPOINT, headers=headers, data=data)

    access_token = response.json().get("access_token", None)
    id_token = response.json().get("id_token", None)

    return {"access_token": access_token, "id_token": id_token}

def get_key_from_oidc_provider(kid: str):
    """
    Get the JSON Web Key Set from the oidc provider

    Return the key that matches the key identifier (kid)
    """
    response = requests.get(JWKS_ENDPOINT)
    jwks = response.json()
    desired_key = {}

    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            desired_key = key

    return desired_key

@login_required
def redirect(request):
    code_verifier = generate_code_verifier()
    request.session['code_verifier'] = code_verifier
    query_params = {
        'client_id':constants.CLIENT_ID,
        'redirect_uri':constants.REDIRECT_URL,
        'response_type':"code",
        'response_mode':"query",
        'scope':constants.SCOPE,
        'state':secrets.token_urlsafe(32),
        'nonce':secrets.token_urlsafe(32),
        'code_challenge':generate_code_challenge(code_verifier),
        'code_challenge_method':"S256",
    }
    authentication_request_url = (
        f"{AUTH_ENDPOINT}?{urllib.parse.urlencode(query_params)}"
    )
    return HttpResponseRedirect(authentication_request_url)

@login_required
def receive(request):
    query_params = request.GET
    code_verifier = request.session["code_verifier"]
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "redirect_uri": constants.REDIRECT_URL,
        "code": query_params.get("code", None),
        "client_id": constants.CLIENT_ID,
        "client_secret": constants.CLIENT_SECRET,
        "code_verifier": code_verifier,
    }

    response = requests.post(TOKEN_ENDPOINT, headers=headers, data=data)

    access_token = response.json().get("access_token", None)
    id_token = response.json().get("id_token", None)    
    decoded_header = jwt.get_unverified_header(id_token)
    kid = decoded_header.get("kid", "")  # get the key id
    alg = decoded_header.get("alg", "")  # get the signing algorithm
    key = get_key_from_oidc_provider(kid)
    payload = jwt.decode(
        id_token,
        key,
        algorithms=[alg],
        audience=constants.CLIENT_ID,
        options={"verify_at_hash": False},
    )

    ssn = payload["national_id"]
    name = payload["name"]

    if is_ssn_human_or_institution(ssn) != 'human':
        ctx = {
            "ssn": ssn,
            "name": name,
        }
        return render(request, 'registration/verification_invalid_entity.html', ctx)

    # Make sure that user has reached the minimum required age, if applicable.
    if hasattr(settings, 'AGE_LIMIT') and settings.AGE_LIMIT > 0:
        age = calculate_age_from_ssn(ssn)
        if age < settings.AGE_LIMIT:
            logout(request)
            ctx = {
                'age': age,
                'age_limit': settings.AGE_LIMIT,
            }
            return render(request, 'registration/verification_age_limit.html', ctx)

    if UserProfile.objects.filter(verified_ssn=ssn).exists():
        taken_user = UserProfile.objects.select_related('user').get(verified_ssn=ssn).user
        ctx = {
            'taken_user': taken_user,
        }
        
        logout(request)

        return render(request, 'registration/verification_duplicate.html', ctx)

    profile = request.user.userprofile  # It shall exist at this point
    profile.verified_ssn = ssn
    profile.verified_name = name
    profile.verified_signature = str(payload)
    profile.verified_timing = timezone.now()
    profile.save()
    event_register('user_verified', user=request.user)
    
    user_verified.send(
        sender=request.user.__class__,
        user=request.user,
        request=request
    )

    return HttpResponseRedirect("/")
