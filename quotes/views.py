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
import operator


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

    saved_sections = [s.id for s in obj.sections.all()]
    obj.sections.clear()
    section_index = 0

    for key, value in sorted(form.cleaned_data.items(), key=operator.itemgetter(1)):
        if key.endswith('_title'):
            section_name = key[:-6]
            section = q.Section(name=section_name,
                                title=form.cleaned_data[section_name + '_title'],
                                text=form.cleaned_data[section_name + '_text'])

            # compare to section at same index, don't add if same
            if section_index < len(saved_sections):
                saved_section = q.Section.objects.get(id=saved_sections[section_index])
            else:
                saved_section = None

            if saved_section is None or section != saved_section:
                section.save()
            else:
                section = saved_section

            obj.sections.add(section)
            section_index += 1

    obj.save()
    return obj


class QuoteTemplateView(View):
    def get(self, request, **kwargs):
        if 'pk' in self.kwargs:
            self.object = get_object_or_404(q.QuoteTemplate, pk=self.kwargs['pk'])
            form = qf.QuoteTemplateForm(instance=self.object.quote)
        else:
            self.object = None
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
