from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from polity.models import Polity

from topic.forms import TopicForm
from topic.models import Topic


@login_required
def topic_add_edit(request, polity_id, topic_id=None):
    try:
        polity = Polity.objects.get(id=polity_id, officers=request.user)
    except Polity.DoesNotExist:
        raise PermissionDenied()

    if topic_id:
        topic = get_object_or_404(Topic, id=topic_id, polity_id=polity_id)
    else:
        topic = Topic(polity=polity)

    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            topic = form.save()
            return redirect(reverse('topic', args=(polity_id, topic.id)))
    else:
        form = TopicForm(instance=topic)

    ctx = {
        'polity': polity,
        'topic': topic,
        'form': form,
    }
    return render(request, 'topic/topic_form.html', ctx)


def topic_view(request, polity_id, topic_id):
    polity = get_object_or_404(Polity, id=polity_id)
    topic = get_object_or_404(Topic, id=topic_id, polity_id=polity_id)

    ctx = {
        'polity': polity,
        'topic': topic,
    }
    return render(request, 'topic/topic_detail.html', ctx)

def topic_list(request, polity_id):
    polity = get_object_or_404(Polity, id=polity_id)

    ctx = {
        'polity': polity,
        'politytopics': polity.topic_set.listing_info(request.user).all(),
    }
    return render(request, 'topic/topic_list.html', ctx)
