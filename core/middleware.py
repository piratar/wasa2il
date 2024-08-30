
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import resolve
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from polity.models import Polity

from django.contrib import auth

from datetime import datetime
from datetime import timedelta

# A middleware to make certain variables available to both templates and views.
class GlobalsMiddleware(MiddlewareMixin):
    def process_request(self, request):

        global_vars = {
            'polity': None,
            'user_is_member': False,
            'user_is_officer': False,
            'user_is_wrangler': False,
            'WASA2IL_VERSION': settings.WASA2IL_VERSION,
            'WASA2IL_HASH': settings.WASA2IL_HASH,
            'CONTACT_EMAIL': settings.CONTACT_EMAIL,
            'ORGANIZATION_NEWS_URL': settings.ORGANIZATION_NEWS_URL,
            'FEATURE_AUDKENNI': settings.FEATURES["audkenni"],
        }

        try:
            match = resolve(request.path)

            if 'polity_id' in match.kwargs:
                polity_id = int(match.kwargs['polity_id'])
                global_vars['polity'] = polity = Polity.objects.prefetch_related(
                    'members',
                    'officers',
                    'wranglers'
                ).get(id=polity_id)

                if not request.user.is_anonymous:
                    global_vars['user_is_member'] = request.user in polity.members.all()
                    global_vars['user_is_officer'] = request.user in polity.officers.all()
                    # Officers are automatically wranglers.
                    if global_vars['user_is_officer']:
                        global_vars['user_is_wrangler'] = True
                    else:
                        global_vars['user_is_wrangler'] = request.user in polity.wranglers.all()
        except:
            # Basically only 404-errors and such cause errors here. Besides,
            # we'll want to move on with our lives anyway.
            pass

        request.globals = global_vars


# Middleware for automatically logging out a user once AUTO_LOGOUT_DELAY
# seconds have been reached without activity.
class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if hasattr(settings, 'AUTO_LOGOUT_DELAY'):

            now = timezone.now()

            if not request.user.is_authenticated :
                # Set the last visit to now when attempting to log in, so that
                # auto-logout feature doesn't immediately log the user out
                # when the user is already logged out but the session is still
                # active.
                if request.path_info == '/accounts/login/' and request.method == 'POST':
                    request.session['last_visit'] = now.strftime('%Y-%m-%d %H:%M:%S')

                # Can't log out if not logged in
                return

            if 'last_visit' in request.session:
                last_visit = datetime.strptime(request.session['last_visit'], '%Y-%m-%d %H:%M:%S')
                last_visit = timezone.make_aware(last_visit, timezone.get_current_timezone())
                if now - last_visit > timedelta(0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                    auth.logout(request)
                    request.auto_logged_out = True

            request.session['last_visit'] = now.strftime('%Y-%m-%d %H:%M:%S')


class VerificationMiddleware(MiddlewareMixin):
    """
    Insists on verifying using electronic ID if feature is turned on.
    """

    def process_request(self, request):

        if not settings.FEATURES['audkenni']:
            return

        # Short-hands.
        path_ok = request.path_info in [
            '/accounts/verify/',
            '/accounts/logout/',
            '/terms/',
        ]
        logged_in = request.user.is_authenticated
        verified = request.user.userprofile.verified if logged_in else False

        if logged_in and not verified and not path_ok:
            return redirect("verify")
