from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.utils.translation import get_language
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from quotes import models as q
from quotes import forms as qf
from reportlab.pdfgen import canvas
from django.http import HttpResponse


class QuoteCreate(View):
    def get(self, request):
        self.object = None
        context = {}
        template_id = self.request.GET.get('template_id', None)
        lang = self.request.GET.get('lang', None)
        if template_id is not None:
            template = get_object_or_404(q.QuoteTemplate, pk=template_id)
            quote = template.quote
            context.update({'sections': [s.as_form_table() for s in quote.all_sections()]}) # TODO: need to bring in sections w/o ID so they don't get saved
            quote.pk = None
            if lang is not None:
                quote.language = lang
                context.update({'language': lang, 'form': qf.QuoteForm(instance=quote), 'object': quote})
        else:
            context.update({'form': qf.QuoteForm(instance=q.Quote())})

        return self.render_to_response(context)

    def post(self, request):
        self.object = None
        form = qf.QuoteForm(request.POST)
        section_forms = qf.section_forms_post(request.POST)
        valid = list([form.is_valid()] + [s.is_valid() for s in section_forms])
        if all(valid):
            return self.form_valid(form, section_forms)
        else:
            return self.render_to_response({'form': form, 'sections': section_forms})

    def form_valid(self, form, section_forms):
        self.object = qf.create_quote(form, section_forms)
        messages.success(self.request, 'Quote saved.')
        return HttpResponseRedirect(reverse('quote_detail', args=[self.object.id]))

    def render_to_response(self, context):
        context.update({'title': 'Add Quote'})
        return TemplateResponse(request=self.request,
                                template="quotes/quote_form.html",
                                context=context)


class QuoteUpdate(View):
    def get(self, request, **kwargs):
        self.object = get_object_or_404(q.Quote, pk=self.kwargs['pk'])
        form = qf.QuoteForm(instance=self.object)
        section_forms = qf.section_forms_quote(quote=self.object)
        return self.render_to_response({'object': self.object, 'form': form, 'sections': section_forms})

    def post(self, request, **kwargs):
        self.object = get_object_or_404(q.Quote, pk=self.kwargs['pk'])
        form = qf.QuoteForm(request.POST, instance=self.object)
        section_forms = qf.section_forms_post(request.POST)
        if form.is_valid():
            return self.form_valid(form, section_forms)
        else:
            return self.render_to_response({'object': self.object, 'form': form, 'sections': section_forms})

    def form_valid(self, form, section_forms):
        self.object = qf.create_quote(form, section_forms)
        messages.success(self.request, 'Quote saved.')
        return HttpResponseRedirect(reverse('quote_detail', args=[self.object.id]))

    def render_to_response(self, context):
        context.update({'title': 'Update Quote'})
        return TemplateResponse(request=self.request,
                                template="quotes/quote_form.html",
                                context=context)


class QuoteDetail(View):
    def get(self, request, **kwargs):
        quote = get_object_or_404(q.Quote, pk=self.kwargs['pk'])
        return TemplateResponse(request=self.request,
                                template="quotes/quote_detail.html",
                                context={'title': 'Quote', 'object': quote})


class QuoteList(View):
    def get(self, request):
        return TemplateResponse(request=self.request,
                                template="quotes/quote_list.html",
                                context={'title': 'Quotes',
                                         'object_list': q.Quote.objects.filter(client__isnull=False),
                                         'template_list': q.QuoteTemplate.objects.all()})


class QuoteTemplateList(View):
    def get(self, request):
        return TemplateResponse(request=self.request,
                                template="quotes/quotetemplate_list.html",
                                context={'title': 'Quote Templates',
                                         'object_list': q.QuoteTemplate.objects.all()})


class QuoteTemplateView(View):
    def get(self, request, **kwargs):
        if 'pk' in self.kwargs:
            self.object = get_object_or_404(q.QuoteTemplate, pk=self.kwargs['pk'])
            form = qf.QuoteTemplateForm(instance=self.object.quote)
            section_forms = qf.section_forms_quote(self.object.quote)
        else:
            self.object = None
            if self.kwargs['quote_id'] is not None:
                quote = get_object_or_404(q.Quote, pk=self.kwargs['quote_id'])
                form = qf.QuoteTemplateForm(instance=quote)
                section_forms = qf.section_forms_quote(quote)
            else:
                form = qf.QuoteTemplateForm()
                section_forms = [qf.SectionForm(instance=q.Section(name='intro', index=0), prefix='-section-0'),
                                 qf.SectionForm(instance=q.Section(name='margin', index=1), prefix='-section-1')]

        return self.render_to_response({'form': form, 'sections': section_forms})

    def post(self, request, **kwargs):
        section_forms = qf.section_forms_post(request.POST)
        if 'pk' in self.kwargs:
            self.object = get_object_or_404(q.QuoteTemplate, pk=self.kwargs['pk'])
            form = qf.QuoteTemplateForm(request.POST, instance=self.object.quote)
        else:
            self.object = None
            form = qf.QuoteTemplateForm(request.POST)

        if form.is_valid():
            return self.form_valid(form, section_forms)
        else:
            return self.render_to_response({'form': form, 'sections': section_forms})

    def form_valid(self, form, section_forms):
        quote = qf.create_quote(form, section_forms)
        if hasattr(self, 'object') and self.object is None:
            self.object = q.QuoteTemplate.objects.create(quote=quote)
        messages.success(self.request, 'Template saved.')
        return HttpResponseRedirect(reverse('edit_quote_template', args=[self.object.id]))

    def render_to_response(self, context):
        lang_dict = dict(settings.LANGUAGES)
        form = qf.LanguageForm()
        language_set = set([get_language()])

        if hasattr(self.object, 'quote'):
            language_set.update(self.object.quote.get_languages())
            quote = self.object.quote
            context.update({'title': 'Edit Template'})
        elif 'quote_id' in self.kwargs and self.kwargs['quote_id'] is not None:
            quote = get_object_or_404(q.Quote, pk=self.kwargs['quote_id'])
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


def quote_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="quote.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response