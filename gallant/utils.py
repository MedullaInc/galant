from django.conf import settings
from django.http.response import Http404
from django.shortcuts import get_object_or_404

LANG_DICT = dict(settings.LANGUAGES)


def get_allowed_or_404(user, permission, *args, **kwargs):
    obj = get_object_or_404(*args, **kwargs)
    if user.has_perm(permission, obj):
        return obj
    else:
        raise Http404("Object not found.")
