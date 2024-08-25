from django.urls import include
from django.urls import re_path
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls import handler500
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import static

from registration.backends.default.views import RegistrationView

from core import views as core_views

from django.contrib import admin

urlpatterns = [
    # Uncomment the admin/doc line below to enable admin documentation:
    re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^admintools/$', core_views.view_admintools, name='admin_tools'),
    re_path(r'^admintools/push/$', core_views.view_admintools_push, name='admin_tools_push'),
    # Enabling i18n language changes per
    # https://docs.djangoproject.com/en/1.4/topics/i18n/translation/#the-set-language-redirect-view
    re_path(r'^i18n/', include('django.conf.urls.i18n')),

    re_path(r'^', include('election.urls')),
    re_path(r'^', include('issue.urls')),
    re_path(r'^', include('core.urls')),
    re_path(r'^', include('polity.urls')),
    re_path(r'^', include('topic.urls')),
    re_path(r'^', include('emailconfirmation.urls')),

    re_path(r'^accounts/profile/(?:(?P<username>[^/]+)/)?$', core_views.profile, name='profile'),
    re_path(r'^accounts/settings/', core_views.view_settings, name='account_settings'),
    re_path(r'^accounts/personal-data/fetch/', core_views.personal_data_fetch, name='personal_data_fetch'),
    re_path(r'^accounts/personal-data/', core_views.personal_data, name='personal_data'),

    re_path(r'^accounts/sso/', core_views.sso),
    re_path(r'^accounts/register/$', core_views.Wasa2ilRegistrationView.as_view(), name='registration_register'),
    re_path(
        r'^accounts/activate/(?P<activation_key>\w+)/$',
        core_views.Wasa2ilActivationView.as_view(),
        name='registration_activate'
    ),
    re_path(
        r'^accounts/password/reset/$',
        auth_views.PasswordResetView.as_view(
            email_template_name='registration/password_reset_email.txt',
            html_email_template_name='registration/password_reset_email.html'
        ),
        name='auth_password_reset'
    ),
    re_path(r'^accounts/reset-password/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # SAML-related URLs.
    re_path(r'^accounts/verify/', core_views.verify),
    re_path(r'^accounts/login-or-saml-redirect/', core_views.login_or_saml_redirect, name='login_or_saml_redirect'),

    re_path(r'^accounts/', include('registration.backends.default.urls')),

    re_path(r'^help/$', TemplateView.as_view(template_name='help/is/index.html')),
    re_path(r'^help/(?P<page>.*)/$', core_views.help),

    re_path(r'^static/(?P<path>.*)$', static.serve,  {'document_root': settings.STATIC_ROOT}),
]

if settings.FEATURES['tasks']:
    urlpatterns.append(re_path(r'^', include('tasks.urls')))


handler500 = 'core.views.error500'

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^uploads/(?P<path>.*)$', static.serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
