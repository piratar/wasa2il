from django.urls import re_path
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from tasks.models import Task
from tasks.views import task_main
from tasks.views import task_add_edit
from tasks.views import task_delete
from tasks.views import task_detail
from tasks.views import task_applications
from tasks.views import task_user_tasks

urlpatterns = [
    re_path(r'^polity/(?P<polity_id>\d+)/tasks/$', task_main, name='task_main'),
    re_path(r'^polity/(?P<polity_id>\d+)/tasks/(?P<task_id>\d+)/edit/$', task_add_edit, name='task_edit'),
    re_path(r'^polity/(?P<polity_id>\d+)/tasks/(?P<task_id>\d+)/delete/$', task_delete, name='task_delete'),
    re_path(r'^polity/(?P<polity_id>\d+)/tasks/new/$', task_add_edit, name='task_add'),
    re_path(r'^polity/(?P<polity_id>\d+)/tasks/(?P<task_id>\d+)/$', task_detail, name='task_detail'),
    re_path(r'^polity/(?P<polity_id>\d+)/tasks/applications/$', task_applications, name='task_applications'),

    re_path(r'^accounts/profile/(?:(?P<username>[^/]+)/tasks/)?$', task_user_tasks, name='task_user_tasks'),
]
