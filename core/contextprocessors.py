from django.conf import settings
from django.utils.translation import gettext as _


def globals(request):

    ctx = {
        'ORGANIZATION_NAME': settings.ORGANIZATION_NAME,
        'INSTANCE_NAME': settings.INSTANCE_NAME,
        'INSTANCE_URL': settings.INSTANCE_URL.strip('/'),
        'INSTANCE_FACEBOOK_IMAGE': settings.INSTANCE_FACEBOOK_IMAGE,
        'INSTANCE_FACEBOOK_APP_ID': settings.INSTANCE_FACEBOOK_APP_ID,
        'INSTANCE_VERSION': settings.WASA2IL_VERSION,
        'FEATURES': settings.FEATURES,
        'GCM_APP_ID': settings.GCM_APP_ID,
        'settings': settings
    }

    # Get global variables from GlobalsMiddleWare.
    ctx.update(request.globals)

    return ctx


def auto_logged_out(request):
    if hasattr(request, 'auto_logged_out') and request.auto_logged_out:
        return {
            'splash_message': _('For security reasons, you have been automatically logged out due to inactivity.')
        }

    return {}
