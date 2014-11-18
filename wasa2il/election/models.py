from datetime import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from core.models import Polity, VotingSystem
from core.base_classes import NameSlugBase


class Election(NameSlugBase):
    """
    An election is different from an issue vote; it's a vote
    on people. Users, specifically.
    """
    polity = models.ForeignKey(Polity)
    votingsystem = models.ForeignKey(
        VotingSystem, verbose_name=_('Voting system'))
    deadline_candidacy = models.DateTimeField(
        verbose_name=_('Deadline for candidacy'))
    deadline_votes = models.DateTimeField(verbose_name=_('Deadline for votes'))

    # Sometimes elections may depend on a user having been the organization's
    # member for an X amount of time. This optional field lets the vote counter
    # disregard members who are too new.
    deadline_joined_org = models.DateTimeField(
        null=True, blank=True, verbose_name=_('Membership deadline'))

    instructions = models.TextField(
        null=True, blank=True, verbose_name=_('Instructions'))

    def export_openstv_ballot(self):
        return ""

    def __unicode__(self):
        return self.name

    def is_open(self):
        return not self.is_closed()

    def is_voting(self):
        if not self.deadline_candidacy or not self.deadline_votes:
            return False

        now = datetime.now()
        if now > self.deadline_candidacy and now < self.deadline_votes:
            return True

        return False

    def is_closed(self):
        if not self.deadline_votes:
            return False

        if datetime.now() > self.deadline_votes:
            return True

        return False

    def get_candidates(self):
        ctx = {}
        ctx["count"] = self.candidate_set.count()
        ctx["users"] = [{"username": x.user.username}
                        for x in self.candidate_set.all().order_by("?")]
        return ctx

    def get_unchosen_candidates(self, user):
        if not user.is_authenticated():
            return Candidate.objects.filter(election=self)
        # votes = []
        votes = ElectionVote.objects.filter(election=self, user=user)
        votedcands = [x.candidate.id for x in votes]
        if len(votedcands) != 0:
            candidates = Candidate.objects.filter(election=self).exclude(
                id__in=votedcands)
        else:
            candidates = Candidate.objects.filter(election=self)

        return candidates

    def get_votes(self):
        ctx = {}
        ctx["count"] = self.electionvote_set.values("user").distinct().count()
        return ctx

    def get_vote(self, user):
        votes = []
        if not user.is_anonymous():
            votes = ElectionVote.objects.filter(election=self,
                                                user=user).order_by("value")
        return [x.candidate for x in votes]

    def get_ballots(self):
        ballot_box = []
        voters = self.electionvote_set.values("user").distinct().order_by('?')
        for voter in voters:
            user = User.objects.get(pk=voter["user"])
            ballot = []
            votes = user.electionvote_set.filter(election=self).order_by(
                'value')
            for vote in votes:
                ballot.append(vote.candidate.user.username)
            ballot_box.append(ballot)
        return ballot_box


class Candidate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    election = models.ForeignKey(Election)


class ElectionVote(models.Model):
    election = models.ForeignKey(Election)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    candidate = models.ForeignKey(Candidate)
    value = models.IntegerField()

    class Meta:
        unique_together = (('election', 'user', 'candidate'),
                           ('election', 'user', 'value'))

    def __unicode__(self):
        return u'In %s, user %s voted for %s for seat %d' % (
            self.election, self.user, self.candidate, self.value)
