from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import get_language
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from gallant.utils import get_one_or_404, GallantObjectPermissions, GallantViewSetPermissions
from gallant.views.user import UserModelViewSet
from quotes import models as q, serializers
from gallant import forms as gf
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

class QuoteTemplateList(View):
    def get(self, request):
        self.request.breadcrumbs([(_('Quotes'), reverse('quotes')),
                                  (_('Templates'), request.path_info)])
        return TemplateResponse(request=request,
                                template="quotes/quotetemplate_list_ng.html",
                                context={'title': 'Quote Templates',
                                         'object_list': q.QuoteTemplate.objects
                                .all_for(request.user)})


class QuoteTemplateDetail(View):
    def get(self, request, **kwargs):
        quote = get_one_or_404(request.user, 'view_quotetemplate', q.QuoteTemplate, pk=kwargs['pk'])
        context = {'title': 'Quote Template',
                   'object': quote,
                   'is_template': True,
                   'template_id': kwargs['pk'],
                   'language_form': gf.LanguageForm()}

        request.breadcrumbs([(_('Quotes'), reverse('quotes')),
                             (_('Quote Templates'), reverse('quotetemplates')),
                             (_('Quote: %s' % quote.quote.name), request.path_info)])
        return TemplateResponse(request=request,
                                template="quotes/quotetemplate_detail_ng.html",
                                context=context)


class QuoteTemplateView(View):
    def get(self, request, **kwargs):
        self.request.breadcrumbs([(_('Quotes'), reverse('quotes')),
                                  (_('Templates'), reverse('quotetemplates'))])

        if 'pk' in kwargs:  # pragma: no cover
            self.object = get_one_or_404(request.user, 'view_quotetemplate', q.QuoteTemplate, pk=kwargs['pk'])

            if not request.user.has_perm('change_quotetemplate', self.object):
                messages.warning(request, 'Warning: you don\'t have permission to change this template. '
                                          'To save it as your own, use it to create a quote, then '
                                          'create a separate template from the new quote.')

            self.request.breadcrumbs([(_('Template: %s' % self.object.quote.name), reverse('quotetemplate_detail', args=[self.object.id])),
                                      (_('Edit Template'), request.path_info)])
        else: 
            self.object = None
            self.request.breadcrumbs([(_('Add'), request.path_info)])

        return self.render_to_response({}, request)


    def render_to_response(self, context, request):
        lang_dict = dict(settings.LANGUAGES)
        form = gf.LanguageForm()
        language_set = set()
        language = get_language()

        if hasattr(self.object, 'quote'):  # TODO: move this block out of here / remove request param
            language_set.update(self.object.quote.get_languages())
            quote = self.object.quote
            context.update({'title': 'Edit Template'})
        elif 'quote_id' in self.kwargs and self.kwargs['quote_id'] is not None:
            quote = get_one_or_404(request.user, 'view_quote', q.Quote, pk=self.kwargs['quote_id'])
            context.update({'title': 'New Template'})
        else:
            quote = q.Quote()
            context.update({'title': 'New Template'})

        if language_set:
            language = next(iter(language_set))
        else:
            language_set.add(language)
        context.update({'languages': [(c, lang_dict[c]) for c in language_set if c in lang_dict],
                        'language_form': gf.LanguageForm(),
                        'object': quote,
                        'template': self.object,
                        'is_template': True,
                        'language': language,
                        'quote_type': 'template'})
        return TemplateResponse(request=self.request,
                                template="quotes/quotetemplate_form_ng.html",
                                context=context)


class QuoteTemplateViewSet(UserModelViewSet):
    model = q.QuoteTemplate
    serializer_class = serializers.QuoteTemplateSerializer

    def get_queryset(self):
        clients_only = self.request.query_params.get('clients_only', None)
        qs = self.model.objects.all_for(self.request.user).prefetch_related('quote')
        if clients_only is not None:
            return qs.filter(quote__client__isnull=clients_only)
        else:
            return qs