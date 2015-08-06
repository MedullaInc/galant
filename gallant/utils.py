from django.conf import settings
from django.http.response import Http404

LANG_DICT = dict(settings.LANGUAGES)


def get_one_or_404(user, perm, klass, *args, **kwargs):
    obj = klass.objects.get(*args, **kwargs)
    if user.has_perm(perm, obj):
        return obj
    else:
        raise Http404("Object not found.")
