from django.urls import re_path

from emailconfirmation.views import email_confirmation

urlpatterns = [
    re_path(r'^email-confirmation/(?P<key>[a-zA-Z0-9]{40})/$', email_confirmation, name='email_confirmation'),
]
