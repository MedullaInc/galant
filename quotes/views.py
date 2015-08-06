from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.utils.translation import get_language
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from gallant.utils import get_one_or_404
from quotes import models as q
from quotes import forms as qf
from gallant import forms as gf
from django.utils.text import slugify
from phantom_pdf import RequestToPDF

class QuoteUpdate(View):
    def get(self, request, **kwargs):
        self.object = get_one_or_404(request.user, 'change_quote', q.Quote, pk=kwargs['pk'])
        form = qf.QuoteForm(request.user, instance=self.object)
        section_forms = qf.section_forms_quote(quote=self.object)
        return self.render_to_response({'object': self.object, 'form': form, 'sections': section_forms,
                                        'title': 'Edit Quote'})

    def post(self, request, **kwargs):
        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'change_quote', q.Quote, pk=kwargs['pk'])
        else:
            self.object = None

        form = qf.QuoteForm(request.user, request.POST, instance=self.object)
        section_forms = qf.section_forms_request(request)

        valid = list([form.is_valid()] + [s.is_valid() for s in section_forms])
        if all(valid):
            return self.form_valid(form, section_forms)
        else:
            return self.render_to_response({'object': self.object, 'form': form, 'sections': section_forms,
                                            'title': 'Edit Quote'})

    def form_valid(self, form, section_forms):
        self.object = qf.create_quote(form, section_forms)
        messages.success(self.request, 'Quote saved.')
        return HttpResponseRedirect(reverse('quote_detail', args=[self.object.id]))

    def render_to_response(self, context):
        return TemplateResponse(request=self.request,
                                template="quotes/quote_form.html",
                                context=context)


class QuoteCreate(QuoteUpdate):
    def get(self, request):
        context = {'title': 'Add Quote'}
        template_id = request.GET.get('template_id', None)
        lang = request.GET.get('lang', None)
        if template_id is not None:
            template = get_one_or_404(request.user, 'view_quotetemplate', q.QuoteTemplate, pk=template_id)
            quote = template.quote
            section_forms = qf.section_forms_quote(quote, clear_pk=True)
            context.update({'sections': section_forms})
            quote.pk = None
            if lang is not None:
                quote.language = lang
                context.update({'language': lang, 'form': qf.QuoteForm(request.user, instance=quote), 'object': quote})
        else:
            context.update({'form': qf.QuoteForm(request.user, instance=q.Quote()),
                            'sections': qf.section_forms_initial(request.user)})

        return self.render_to_response(context)


class QuoteDetail(View):
    def get(self, request, **kwargs):
        quote = get_one_or_404(request.user, 'view_quote', q.Quote, pk=kwargs['pk'])
        return TemplateResponse(request=request,
                                template="quotes/quote_detail.html",
                                context={'title': 'Quote', 'object': quote})


class QuoteList(View):
    def get(self, request):
        return TemplateResponse(request=request,
                                template="quotes/quote_list.html",
                                context={'title': 'Quotes',
                                         'object_list': q.Quote.objects
                                                         .all_for(request.user, 'view_quote')
                                                         .filter(client__isnull=False),
                                         'template_list': q.QuoteTemplate.objects
                                                           .all_for(request.user, 'view_quotetemplate')})


class QuoteTemplateList(View):
    def get(self, request):
        return TemplateResponse(request=request,
                                template="quotes/quotetemplate_list.html",
                                context={'title': 'Quote Templates',
                                         'object_list': q.QuoteTemplate.objects
                                                         .all_for(request.user, 'view_quotetemplate')})


class QuoteTemplateView(View):
    def get(self, request, **kwargs):
        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'view_quotetemplate', q.QuoteTemplate, pk=kwargs['pk'])
            form = qf.QuoteTemplateForm(request.user, instance=self.object.quote)
            section_forms = qf.section_forms_quote(self.object.quote)
        else:
            self.object = None
            if kwargs['quote_id'] is not None:
                quote = get_one_or_404(request.user, 'view_quote', q.Quote, pk=kwargs['quote_id'])
                form = qf.QuoteTemplateForm(request.user, instance=quote)
                section_forms = qf.section_forms_quote(quote)
            else:
                form = qf.QuoteTemplateForm(request.user)
                section_forms = qf.section_forms_initial(request.user)

        return self.render_to_response({'form': form, 'sections': section_forms}, request)

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
        language_set = set([get_language()])

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

        context.update({'languages': [(c, lang_dict[c]) for c in language_set if c in lang_dict],
                        'language_form': form,
                        'object': quote,
                        'language': get_language()})
        return TemplateResponse(request=self.request,
                                template="quotes/quote_template.html",
                                context=context)


class PhantomJSBin(RequestToPDF):
    def __init__(self, *args, **kwargs):
        super(PhantomJSBin, self).__init__(PHANTOMJS_BIN='/usr/local/bin/phantomjs',*args,**kwargs)


def quote_pdf(request, *args, **kwargs):
    # Get quote
    quote = q.Quote.objects.all_for(request.user, 'view_quote', pk=kwargs['pk'])

    # Render PDF
    filename = slugify(quote.client.name + "_" + quote.name)
    pjs = PhantomJSBin()
    request.path = reverse('quote_preview', args=[quote.id])
    return pjs.request_to_pdf(request, filename, format="A4", orientation="landscape")


def quote_preview(request, *args, **kwargs):
    # Get quote
    quote = q.Quote.objects.all_for(request.user, 'view_quote', pk=kwargs['pk'])

    # Render HTML
    context = {'object': quote}
    return TemplateResponse(request, template="quotes/quote_preview.html", context=context)

