from django.urls import re_path
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_headers

from election.dataviews import election_candidacy
from election.dataviews import election_candidates_details
from election.dataviews import election_poll
from election.dataviews import election_vote
from election.dataviews import election_showclosed
from election.dataviews import election_stats_download
from election.views import election_add_edit
from election.views import election_list
from election.views import election_view


urlpatterns = [
    re_path(r'^polity/(?P<polity_id>\d+)/elections/$', never_cache(election_list), name='elections'),
    re_path(r'^polity/(?P<polity_id>\d+)/election/new/$', election_add_edit, name='election_add_edit'),
    re_path(r'^polity/(?P<polity_id>\d+)/election/(?P<election_id>\d+)/edit/$', election_add_edit, name='election_add_edit'),
    re_path(r'^polity/(?P<polity_id>\d+)/election/(?P<election_id>\d+)/candidates-details/$', never_cache(election_candidates_details), name='election_candidates_details'),
    re_path(r'^polity/(?P<polity_id>\d+)/election/(?P<election_id>\d+)/$', never_cache(election_view), name='election'),
    re_path(r'^polity/(?P<polity_id>\d+)/election/(?P<election_id>\d+)/stats-dl/(?P<filename>.+)$', election_stats_download),

    re_path(r'^api/election/poll/$', never_cache(election_poll)),
    re_path(r'^api/election/vote/$', never_cache(election_vote)),
    re_path(r'^api/election/candidacy/$', never_cache(election_candidacy)),
    re_path(r'^api/election/showclosed/$', election_showclosed),
]
