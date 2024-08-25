from django.urls import re_path
from django.contrib.auth.decorators import login_required

from topic.dataviews import topic_showstarred
from topic.dataviews import topic_star
from topic.views import topic_add_edit
from topic.views import topic_view
from topic.views import topic_list


urlpatterns = [
    re_path(r'^polity/(?P<polity_id>\d+)/topic/new/$', topic_add_edit, name='topic_add'),
    re_path(r'^polity/(?P<polity_id>\d+)/topic/(?P<topic_id>\d+)/edit/$', topic_add_edit, name='topic_edit'),
    re_path(r'^polity/(?P<polity_id>\d+)/topic/(?P<topic_id>\d+)/$', topic_view, name='topic'),
    re_path(r'^polity/(?P<polity_id>\d+)/topics/$', topic_list, name='topics'),


    re_path(r'^api/topic/star/$', topic_star),
    re_path(r'^api/topic/showstarred/$', topic_showstarred),
]
