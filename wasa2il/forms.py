from django import forms
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Button

from django.conf import settings
from django.forms.fields import DateTimeField


class Wasa2ilForm(forms.ModelForm):
    '''
    A custom form base class with functionality intended to be used with forms
    throughout Wasa2il's user interface, taking usage of Bootstrap and basic
    interface design decisions into account.
    '''

    dateTimeOptions = {
        'format': settings.DATETIME_FORMAT_DJANGO_WIDGET,
        'autoclose': True,
    }

    def __init__(self, *args, **kwargs):
        super(Wasa2ilForm, self).__init__(*args, **kwargs)

        # Make form pretty
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-6'

        # Add save/cancel buttons
        self.helper.add_input(Submit('save', _('Save')))
        self.helper.add_input(Button(
            'cancel',
            _('Cancel'),
            css_class='btn btn-default',
            onclick="var $cancel_url = $('#cancel-url').text(); if ($cancel_url) { location.href = $cancel_url } else { window.history.back(); }"
        ))

        # Automatically make selection fields prettier and easier to use.
        for fieldname in self.fields:
            field = self.fields[fieldname]
            field_type = type(field)
            if field_type is DateTimeField:
                field.widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
