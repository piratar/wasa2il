from wasa2il.forms import Wasa2ilForm
from django.forms import CharField
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

from tasks.models import Task

class TaskForm(Wasa2ilForm):
    short_description = CharField(
        widget=Textarea(attrs={'rows': 2}),
        label=_('Short description'),
        max_length=200,
        help_text=_('Clearly state the objective of the task. Maximum 200 letters.')
    )

    class Meta:
        model = Task
        exclude = (
            'polity',
            'is_done',
            'created_by',
            'modified_by',
            'created',
            'modified',
            'slug',
            'categories',
            'skills',
        )


