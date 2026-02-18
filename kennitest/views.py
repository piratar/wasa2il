import base64
import hashlib
import requests
import secrets
import urllib.parse

from jose import jwt

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from kennitest import constants
from kennitest import forms as kenniforms

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
def handler(request):
    if request.method == "GET":
        form = kenniforms.Kennitala
    elif request.method == "POST":
        form = kenniforms.Kennitala(request.POST)
        if form.is_valid():
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

    return render(request, "registration/kennitest.html", {'form':form})

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
    key = utils.get_key_from_oidc_provider(kid)
    payload = jwt.decode(
        id_token,
        key,
        algorithms=[alg],
        audience=constants.CLIENT_ID,
        options={"verify_at_hash": False},
    )

    return str(payload)