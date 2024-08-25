from django.utils import translation


def set_language(request, language):
    translation.activate(language)
    request.session["django_language"] = language
