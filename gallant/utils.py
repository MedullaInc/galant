from subprocess import check_output
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.db import models as m
from django.contrib.sites.models import Site
from rest_framework.permissions import DjangoModelPermissions

LANG_DICT = dict(settings.LANGUAGES)
SITE_CACHE = {}


def get_one_or_404(user, perm, klass, *args, **kwargs):
    obj = super(m.Manager, klass.objects).get(*args, **kwargs)
    if user.has_perm(perm, obj) and (not hasattr(obj, 'deleted') or obj.deleted is False):
        return obj

    raise Http404("Object not found.")


class GallantObjectPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['add_%(model_name)s'],
        'PUT': ['change_%(model_name)s'],
        'PATCH': ['change_%(model_name)s'],
        'DELETE': ['delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        perms = self.get_required_permissions(request.method, view.get_queryset().model)

        if view.action == 'list' or view.action == 'create':
            return request.user.is_authenticated()
        elif hasattr(view, 'get_object'):
            lookup_url_kwarg = view.lookup_url_kwarg or view.lookup_field

            if lookup_url_kwarg in view.kwargs:
                obj = view.get_object()
            else:
                return False
        else:
            return False

        return (
            request.user and
            request.user.is_authenticated() and
            request.user.has_perms(perms, obj)
        )


# Disable allauth signup for now
class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False


def get_site_from_host(request):
    host = request.get_host()
    if host not in SITE_CACHE:
        try:
            site = Site.objects.get(domain__iexact=host)
        except ObjectDoesNotExist:
            site = Site.objects.get(pk=1)
        SITE_CACHE[host] = site
    return SITE_CACHE[host]


# context processor, creates site object for access in templates
def site_processor(request):
    site = get_site_from_host(request)
    return {'site': site}


# context processor, adds DEBUG to templates
def debug_processor(request):
    return {'DEBUG': settings.DEBUG}


def url_to_pdf(url, session_key, header_url=None, footer_url=None): # pragma: no cover
    args = ['wkhtmltopdf', '--lowquality', '-T', '65mm', '-B', '32mm', '--encoding', u'utf8', '--cookie', 'sessionid', session_key,
            '--quiet', url]

    if header_url:
        args.extend(['--header-html', header_url])

    if footer_url:
        args.extend(['--footer-html', footer_url])

    args.append('-')
    return check_output(args)


def query_url(request):
    if len(request.META['QUERY_STRING']):
        return '?%s' % request.META['QUERY_STRING']
    else:
        return ''
