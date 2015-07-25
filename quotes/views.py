from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.utils.translation import get_language
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from quotes import models as q
from gallant import models as g
from quotes import forms as qf
import operator, re


class QuoteCreate(View):
    def get(self, request):
        self.object = None
        return self.render_to_response({'form': qf.QuoteForm()})

    def post(self, request):
        self.object = None
        form = qf.QuoteForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.render_to_response({'form': form})

    def form_valid(self, form):
        self.object = _create_quote(form)
        return HttpResponseRedirect(reverse('quote_detail', args=[self.object.id]))

    def render_to_response(self, context):
        template_id = self.request.GET.get('template_id', None)
        lang = self.request.GET.get('lang', None)
        if template_id is not None:
            template = get_object_or_404(q.QuoteTemplate, pk=template_id)
            quote = template.quote
            quote.pk = None
            if lang is not None:
                quote.language = lang
        else:
            quote = q.Quote()

        if 'form' not in context:
            context.update({'form': qf.QuoteForm(instance=quote)})

        context.update({'title': 'Add Quote', 'object': quote,
                        'language': lang})
        return TemplateResponse(request=self.request,
                                template="quotes/quote_form.html",
                                context=context)


class QuoteUpdate(View):
    def get(self, request, **kwargs):
        self.object = get_object_or_404(q.Quote, pk=self.kwargs['pk'])
        form = qf.QuoteForm(instance=self.object)
        return self.render_to_response({'object': self.object, 'form': form})

    def post(self, request, **kwargs):
        self.object = get_object_or_404(q.Quote, pk=self.kwargs['pk'])
        form = qf.QuoteForm(request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.render_to_response({'object': self.object, 'form': form})

    def form_valid(self, form):
        self.object = _create_quote(form)
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


def _create_quote(form):
    obj = form.save(commit=True)

    saved_sections = dict((s.index, s.id) for s in obj.sections.all())
    saved_sections.update((s.index, s.id) for s in obj.services.all())
    obj.sections.clear()
    obj.services.clear()

    for key, value in sorted(form.cleaned_data.items(), key=operator.itemgetter(1)):
        m = re.match('(-section-(\d+)_([-_\w]+))_title', key)
        if m is not None:
            section_index = int(m.group(2))
            section_name = m.group(3)

            # see if update or create
            if m.group(1) + '_id' in form.cleaned_data:
                section = get_object_or_404(q.Section, pk=form.cleaned_data[m.group(1) + '_id'])
            else:
                section = q.Section()

            section.name = section_name
            section.index = section_index
            section.title = form.cleaned_data[m.group(1) + '_title']
            section.text = form.cleaned_data[m.group(1) + '_text']
            section.save()

            obj.sections.add(section)
        else:
            m = re.match('(-service-(\d+)_([-_\w]+))_name', key)
            if m is not None:
                section_index = int(m.group(2))
                section_name = m.group(3)

                service_section = q.ServiceSection()

                # see if update or create
                if m.group(1) + '_id' in form.cleaned_data:
                    section = get_object_or_404(q.ServiceSection, pk=form.cleaned_data[m.group(1) + '_id'])
                else:
                    section = q.ServiceSection()
                    service = g.Service()

                service.name = form.cleaned_data[m.group(1) + '_name'],
                service.description = form.cleaned_data[m.group(1) + '_description'],
                service.cost = form.cleaned_data[m.group(1) + '_cost'],
                service.quantity = form.cleaned_data[m.group(1) + '_quantity'],
                service.type = form.cleaned_data[m.group(1) + '_type']
                section.name = section_name
                section.index = section_index
                section.service = service

                obj.services.add(service_section)

    obj.save()
    return obj


class QuoteTemplateView(View):
    def get(self, request, **kwargs):
        if 'pk' in self.kwargs:
            self.object = get_object_or_404(q.QuoteTemplate, pk=self.kwargs['pk'])
            form = qf.QuoteTemplateForm(instance=self.object.quote)
        else:
            self.object = None
            if self.kwargs['quote_id'] is not None:
                quote = get_object_or_404(q.Quote, pk=self.kwargs['quote_id'])
                form = qf.QuoteTemplateForm(instance=quote)
            else:
                form = qf.QuoteTemplateForm()

        return self.render_to_response({'form': form})

    def post(self, request, **kwargs):
        if 'pk' in self.kwargs:
            self.object = get_object_or_404(q.QuoteTemplate, pk=self.kwargs['pk'])
            form = qf.QuoteTemplateForm(request.POST, instance=self.object.quote)
        else:
            self.object = None
            form = qf.QuoteTemplateForm(request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.render_to_response({'form': form})

    def form_valid(self, form):
        quote = _create_quote(form)
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
