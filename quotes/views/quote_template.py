from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.utils.translation import get_language
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from gallant.utils import get_one_or_404, GallantObjectPermissions, GallantViewSetPermissions
from quotes import models as q, serializers
from quotes import forms as qf
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

        request.breadcrumbs([(_('Quotes'), reverse('quotes')),
                             (_('Quote Templates'), reverse('quote_templates')),
                             (_('Quote: %s' % quote.quote.name), request.path_info)])
        return TemplateResponse(request=request,
                                template="quotes/quotetemplate_detail_ng.html",
                                context={'title': 'Quote Template', 'object': quote})


class QuoteTemplateView(View):
    def get(self, request, **kwargs):
        self.request.breadcrumbs([(_('Quotes'), reverse('quotes')),
                                  (_('Templates'), reverse('quote_templates'))])

        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'view_quotetemplate', q.QuoteTemplate, pk=kwargs['pk'])
            form = qf.QuoteTemplateForm(request.user, instance=self.object.quote)
            #section_forms = qf.section_forms_quote(self.object.quote)

            if not request.user.has_perm('change_quotetemplate', self.object):
                messages.warning(request, 'Warning: you don\'t have permission to change this template. '
                                          'To save it as your own, use it to create a quote, then '
                                          'create a separate template from the new quote.')

            self.request.breadcrumbs([(_('Quote: %s' % self.object.quote.name), reverse('quote_template_detail', args=[self.object.id])),
                                      (_('Edit Template'), request.path_info)])
        else:
            self.object = None
            self.request.breadcrumbs([(_('Add'), request.path_info)])

            if kwargs['quote_id'] is not None:
                quote = get_one_or_404(request.user, 'view_quote', q.Quote, pk=kwargs['quote_id'])
                form = qf.QuoteTemplateForm(request.user, instance=quote)
            else:
                form = qf.QuoteTemplateForm(request.user)

        return self.render_to_response({'form': form}, request)

    def post(self, request, **kwargs):
        section_forms = qf.section_forms_request(request)
        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'change_quotetemplate', q.QuoteTemplate, pk=kwargs['pk'])
            form = qf.QuoteTemplateForm(request.user, request.POST, instance=self.object.quote)
        else:
            self.object = None
            form = qf.QuoteTemplateForm(request.user, request.POST)

        valid = list([form.is_valid()] + [s.is_valid() for s in section_forms])
        if all(valid):
            return self.form_valid(form, section_forms)
        else:
            return self.render_to_response({'form': form, 'sections': section_forms}, request)

    def form_valid(self, form, section_forms):
        quote = qf.create_quote(form, section_forms)
        if hasattr(self, 'object') and self.object is None:
            self.object = q.QuoteTemplate.objects.create(user=quote.user, quote=quote)
        messages.success(self.request, 'Template saved.')
        return HttpResponseRedirect(reverse('edit_quote_template', args=[self.object.id]))

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
                        'language_form': form,
                        'object': quote,
                        'template': self.object,
                        'language': language,
                        'quote_type': 'template'})
        return TemplateResponse(request=self.request,
                                template="quotes/quotetemplate_form_ng.html",
                                context=context)


class QuoteTemplateViewSet(ModelViewSet):
    model = q.QuoteTemplate
    serializer_class = serializers.QuoteTemplateSerializer
    permission_classes = [
         GallantViewSetPermissions
     ]

    def get_queryset(self):
        return self.model.objects.all_for(self.request.user)

    def update(self, request, *args, **kwargs):
        response = super(QuoteTemplateViewSet, self).update(request, *args, **kwargs)
        if response.status_code == HTTP_200_OK or response.status_code == HTTP_201_CREATED:
            self.request._messages.add(messages.SUCCESS, 'Quote Template saved.')
            return Response({'status': 0, 'redirect': reverse('quote_detail', args=[response.data['id']])})
        else:
            return response

    def create(self, request, *args, **kwargs):
        response = super(QuoteTemplateViewSet, self).create(request, *args, **kwargs)
        if response.status_code == HTTP_201_CREATED:
            self.request._messages.add(messages.SUCCESS, 'Quote Template saved.')
            return Response({'status': 0, 'redirect': reverse('quote_detail', args=[response.data['id']])})
        else:
            return response
