from django.urls import re_path
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.decorators.cache import never_cache

from polity.models import Polity
from polity.views import polity_add_edit
from polity.views import polity_apply
from polity.views import polity_list
from polity.views import polity_officers
from polity.views import polity_view


urlpatterns = [
    re_path(r'^polities/$', polity_list, name='polities'),
    re_path(r'^polity/new/$', polity_add_edit, name='polity_add'),
    re_path(r'^polity/(?P<polity_id>\d+)/edit/$', polity_add_edit, name='polity_edit'),
    re_path(r'^polity/(?P<polity_id>\d+)/officers/$', polity_officers, name='polity_officers'),
    re_path(r'^polity/(?P<polity_id>\d+)/$', never_cache(polity_view), name='polity'),
    path('polity/<int:polity_id>/apply/', polity_apply, name='polity_apply'),
]
