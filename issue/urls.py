from django.urls import re_path
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.generic import UpdateView

from issue.dataviews import issue_comment_send
from issue.dataviews import issue_poll
from issue.dataviews import issue_vote
from issue.dataviews import issue_showclosed
from issue.dataviews import documentcontent_render_diff
from issue.dataviews import documentcontent_retract
from issue.models import Issue
from issue.views import document_add
from issue.views import document_agreements
from issue.views import document_view
from issue.views import documentcontent_add
from issue.views import documentcontent_edit
from issue.views import issue_add_edit
from issue.views import issue_view
from issue.views import issues

urlpatterns = [

    re_path(r'^polity/(?P<polity_id>\d+)/issues/$', issues, name='issues'),
    re_path(r'^polity/(?P<polity_id>\d+)/issue/(?P<issue_id>\d+)/edit/$', issue_add_edit, name='issue_edit'),
    re_path(r'^polity/(?P<polity_id>\d+)/issue/new/(documentcontent/(?P<documentcontent_id>\d+)/)?$', issue_add_edit, name='issue_add'),
    re_path(r'^polity/(?P<polity_id>\d+)/issue/(?P<issue_id>\d+)/$', never_cache(issue_view), name='issue'),

    re_path(r'^polity/(?P<polity_id>\d+)/agreements/$', document_agreements, name="agreements"),
    re_path(r'^polity/(?P<polity_id>\d+)/document/new/$', document_add),
    re_path(r'^polity/(?P<polity_id>\d+)/document/(?P<document_id>\d+)/v(?P<version>\d+)/$', document_view, name='document_view'),
    re_path(r'^polity/(?P<polity_id>\d+)/document/(?P<document_id>\d+)/v(?P<version>\d+)/edit/$', documentcontent_edit, name='documentcontent_edit'),
    re_path(r'^polity/(?P<polity_id>\d+)/document/(?P<document_id>\d+)/new/$', documentcontent_add, name='documentcontent_add'),
    re_path(r'^polity/(?P<polity_id>\d+)/document/(?P<document_id>\d+)/$', document_view, name='document'),

    re_path(r'^api/issue/comment/send/$', never_cache(issue_comment_send)),
    re_path(r'^api/issue/poll/$', never_cache(issue_poll)),
    re_path(r'^api/issue/vote/$', never_cache(issue_vote)),
    re_path(r'^api/issue/showclosed/$', issue_showclosed),

    re_path(r'^api/documentcontent/render-diff/$', documentcontent_render_diff),
    re_path(r'^api/documentcontent/(?P<documentcontent_id>\d+)/retract/$', documentcontent_retract),
]
