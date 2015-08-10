from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.http.response import Http404
from django.db import models as m

LANG_DICT = dict(settings.LANGUAGES)


def get_one_or_404(user, perm, klass, *args, **kwargs):
    obj = super(m.Manager, klass.objects).get(*args, **kwargs)
    if user.has_perm(perm, obj):
        return obj

    raise Http404("Object not found.")


# Disable allauth signup for now
class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False