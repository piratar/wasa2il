import json

from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView

from issue.forms import DocumentForm, DocumentContentForm, IssueForm
from issue.models import Document, DocumentContent, Issue

from polity.models import Polity
from topic.models import Topic


@login_required
def issue_add_edit(request, polity_id, issue_id=None, documentcontent_id=None):
    polity = get_object_or_404(Polity, id=polity_id)

    # Make sure that user is allowed to do this.
    if (
        polity.is_newissue_only_officers
        and request.user not in polity.officers.all()
    ):
        raise PermissionDenied()

    if issue_id:
        issue = get_object_or_404(Issue, id=issue_id, polity_id=polity_id)
        current_content = issue.documentcontent

        # We don't want to edit anything that has already been processed.
        if issue.is_processed:
            raise PermissionDenied()
    else:
        issue = Issue(polity=polity)
        if documentcontent_id:
            try:
                current_content = DocumentContent.objects.select_related(
                    'document'
                ).get(id=documentcontent_id)
            except DocumentContent.DoesNotExist:
                raise Http404
        else:
            current_content = None

    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.apply_ruleset()
            issue.documentcontent = current_content
            issue.special_process_set_by = (
                request.user if issue.special_process else None
            )
            issue.save()

            issue.topics.clear()
            for topic in request.POST.getlist('topics'):
                issue.topics.add(topic)

            return redirect(reverse('issue', args=(polity_id, issue.id)))
    else:
        # Check if we need to inherit information from previous documentcontent.
        if not issue_id and current_content:
            name = current_content.name
            selected_topics = []

            # If this is a new issue, being made from existing content, we
            # want to inherit the previously selected topics, and add a
            # version number to the name.
            if current_content.order > 1:
                name += u', %s %d' % (_(u'version'), current_content.order)
                selected_topics = current_content.previous_topics()

            form = IssueForm(
                instance=issue,
                initial={
                    'name': name,
                    'description': current_content.comments.replace(
                        "\n", "\\n"
                    ),
                    'topics': selected_topics,
                },
            )
        else:
            form = IssueForm(instance=issue)

    # Make only topics from this polity available.
    form.fields['topics'].queryset = Topic.objects.filter(polity=polity)

    ctx = {
        'polity': polity,
        'issue': issue,
        'form': form,
        'documentcontent': current_content,
        'tab': 'diff' if current_content.order > 1 else '',
    }

    return render(request, 'issue/issue_form.html', ctx)


def issue_view(request, polity_id, issue_id):
    polity = get_object_or_404(Polity, id=polity_id)
    issue = get_object_or_404(Issue, id=issue_id, polity_id=polity_id)

    ctx = {}

    if issue.documentcontent:
        documentcontent = issue.documentcontent
        if documentcontent.order > 1:
            ctx['tab'] = 'diff'
        else:
            ctx['tab'] = 'view'

        ctx['documentcontent'] = documentcontent
        if issue.is_processed:
            ctx['selected_diff_documentcontent'] = documentcontent.predecessor
        else:
            ctx[
                'selected_diff_documentcontent'
            ] = documentcontent.document.preferred_version()

    ctx['polity'] = polity
    ctx['issue'] = issue
    ctx['can_vote'] = request.user is not None and issue.can_vote(request.user)
    ctx['comments_closed'] = (
        not request.user.is_authenticated or issue.discussions_closed()
    )

    # People say crazy things on the internet. We'd like to keep the record of
    # conversations about issues well into the future but still we'd like to
    # protect users from having to answer for something they said a long time
    # ago. To try and achieve both goals, we require a logged in user to see
    # comments to older issues.
    comment_protection_timing = datetime.now() - timedelta(
        days=settings.RECENT_ISSUE_DAYS
    )
    if (
        not request.user.is_authenticated
        and issue.deadline_votes < comment_protection_timing
    ):
        ctx['comments_hidden'] = True

    return render(request, 'issue/issue_detail.html', ctx)


def issues(request, polity_id):
    polity = get_object_or_404(Polity, id=polity_id)

    issues = polity.issue_set.order_by('-created')

    ctx = {
        'polity': polity,
        'issues': issues,
    }
    return render(request, 'issue/issues.html', ctx)


@login_required
def document_add(request, polity_id):
    try:
        polity = Polity.objects.get(id=polity_id, members=request.user)
    except Polity.DoesNotExist:
        raise PermissionDenied()

    document = Document(polity=polity, user=request.user)

    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            document.polity = polity
            document.user = request.user
            document.save()
            return redirect(
                reverse('documentcontent_add', args=(polity_id, document.id))
            )
    else:
        form = DocumentForm()

    ctx = {
        'polity': polity,
        'form': form,
    }
    return render(request, 'issue/document_form.html', ctx)


def document_view(request, polity_id, document_id, version=None):
    polity = get_object_or_404(Polity, id=polity_id)
    document = get_object_or_404(
        Document, id=document_id, polity__id=polity_id
    )

    # If version is not specified, we want the "preferred" version
    if version is not None:
        current_content = get_object_or_404(
            DocumentContent, document=document, order=version
        )
    else:
        current_content = document.preferred_version()

    issue = None
    if current_content is not None and hasattr(current_content, 'issue'):
        issue = current_content.issue

    buttons = {
        'propose_change': False,
        'put_to_vote': False,
        'edit_proposal': False,
        'retract_proposal': False,
    }
    if (
        not issue or issue.issue_state() != 'voting'
    ) and current_content is not None:

        # Check if the user should be allowed to retract the issue, which is
        # at any point in which an issue has been founded but not concluded.
        # Officers are also allowed to retract on the behalf of users.
        if issue and issue.issue_state() != 'concluded':
            buttons['retract_proposal'] = 'enabled'

        if current_content.status == 'accepted':
            if request.globals['user_is_member']:
                buttons['propose_change'] = 'enabled'
        elif current_content.status == 'proposed':
            if request.globals['user_is_officer'] and not issue:
                buttons['put_to_vote'] = (
                    'disabled' if document.has_open_issue() else 'enabled'
                )
            if current_content.user_id == request.user.id:
                buttons['edit_proposal'] = (
                    'disabled' if issue is not None else 'enabled'
                )

    ctx = {
        'polity': polity,
        'document': document,
        'current_content': current_content,
        'selected_diff_documentcontent': document.preferred_version,
        'issue': issue,
        'buttons': buttons,
        'buttons_enabled': any([b != False for b in buttons.values()]),
    }

    return render(request, 'issue/document_detail.html', ctx)


@login_required
def documentcontent_edit(request, polity_id, document_id, version):

    dc = get_object_or_404(
        DocumentContent,
        document_id=document_id,
        document__polity_id=polity_id,
        order=version,
    )

    # Editing of documentcontents should only be allowed by its author or the
    # polity's officers.
    if dc.user_id != request.user.id:
        raise PermissionDenied

    # Editing of documentcontents is only allowed before an issue has been
    # created. This is kept separate from the logic above both for reasons of
    # clarity, and because this is likely to change in the future and so
    # should remain in its own place. We may very well want to allow the user
    # to change documentcontents in the future, as long as the issue hasn't
    # reached a particular state, such as "voting" or "concluded".
    if hasattr(dc, 'issue'):
        raise PermissionDenied

    if request.method == 'POST':
        form = DocumentContentForm(request.POST, instance=dc)
        if form.is_valid():
            form.save()
            return redirect(
                reverse(
                    'document_view', args=(polity_id, document_id, version)
                )
            )
    else:
        form = DocumentContentForm(instance=dc)

    ctx = {
        'form': form,
        'polity': request.globals['polity'],
        'documentcontent': dc,
    }
    return render(request, 'issue/documentcontent_edit.html', ctx)


@login_required
def documentcontent_add(request, polity_id, document_id):

    # Only members of the polity are allowed to create proposals.
    if not request.globals['user_is_member']:
        raise PermissionDenied

    doc = Document.objects.get(id=document_id, polity_id=polity_id)

    if request.method == 'POST':
        form = DocumentContentForm(request.POST)

        form.instance.document = doc
        form.instance.user = request.user

        if form.is_valid():

            # The order of the new documentcontent shall be the count of those
            # already existing, plus one.
            form.instance.order = doc.documentcontent_set.count() + 1

            form.save()
            return redirect(
                reverse(
                    'document_view',
                    args=(polity_id, document_id, form.instance.order),
                )
            )
    else:
        form = DocumentContentForm()

        # Inherit the name and text from the previously active version if one
        # exists, otherwise from the document.
        pred = doc.preferred_version()
        if pred is not None:
            form.fields['name'].initial = pred.name
            form.fields['text'].initial = pred.text
        else:
            form.fields['name'].initial = doc.name

    ctx = {
        'form': form,
        'document': doc,
    }
    return render(request, 'issue/documentcontent_add.html', ctx)


def document_agreements(request, polity_id):
    polity = get_object_or_404(Polity, id=polity_id)

    q = request.POST.get('q') or ''
    if q:
        agreements = polity.agreements(q)
    else:
        agreements = polity.agreements()

    ctx = {
        'q': q,
        'polity': polity,
        'agreements': agreements,
    }
    return render(request, 'issue/document_list.html', ctx)
