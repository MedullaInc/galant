from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.utils.translation import get_language
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from quotes import models as q
from quotes import forms as qf
import operator


class QuoteCreate(CreateView):
    form_class = qf.QuoteForm
    template_name = "quotes/quote_form.html"

    def get_success_url(self):
        return reverse('quote_detail', args=[self.object.id])

    def form_valid(self, form):
        _create_quote(form)
        return super(QuoteCreate, self).form_valid(form)

    def render_to_response(self, context, **kwargs):
        template_id = self.request.GET.get('template_id', None)
        lang = self.request.GET.get('lang', None)
        if template_id is not None:
            template = get_object_or_404(q.QuoteTemplate, pk=template_id)
            quote = template.quote
            sections = quote.all_sections()
            quote.pk = None
            if lang is not None:
                quote.language = lang
        else:
            quote = q.Quote()
            sections = quote.all_sections()

        if 'form' not in context:
            context.update({'form': qf.QuoteForm(instance=quote)})

        context.update({'title': 'Add Quote', 'object': quote,
                        'language': lang, 'sections': sections})
        return super(QuoteCreate, self).render_to_response(context)


class QuoteUpdate(UpdateView):
    model = q.Quote
    form_class = qf.QuoteForm
    template_name = "quotes/quote_form.html"

    def get_success_url(self):
        return reverse('quote_detail', args=[self.object.id])

    def form_valid(self, form):
        _create_quote(form)
        return super(QuoteUpdate, self).form_valid(form)

    def render_to_response(self, context, **response_kwargs):
        context.update({'title': 'Update Quote',
                        'sections': self.object.all_sections()})
        return super(UpdateView, self).render_to_response(context)


class QuoteDetail(DetailView):
    model = q.Quote


class QuoteList(ListView):
    model = q.Quote

    def get_queryset(self):
        return self.model.objects.filter(client__isnull=False)

    def render_to_response(self, context, **response_kwargs):
        context.update({'template_list': q.QuoteTemplate.objects.all()})
        return super(QuoteList, self).render_to_response(context)


class QuoteTemplateList(ListView):
    model = q.QuoteTemplate

    def render_to_response(self, context, **response_kwargs):
        context.update({'template_list': q.QuoteTemplate.objects.all()})
        return super(QuoteTemplateList, self).render_to_response(context)


def _create_quote(form):
    obj = form.save(commit=True)
    intro = q.Section(name='intro',
                      title=form.cleaned_data['intro_title'],
                      text=form.cleaned_data['intro_text'])
    margin_section = q.Section(name='margin_section',
                               title=form.cleaned_data['margin_section_title'],
                               text=form.cleaned_data['margin_section_text'])

    saved_sections = [s.id for s in obj.sections.all()]
    obj.sections.clear()
    section_index = 0

    for key, value in sorted(form.cleaned_data.items(), key=operator.itemgetter(1)):
        if key.startswith('section_') and key.endswith('_title'):
            section_name = key[:-6]
            section = q.Section(name=section_name,
                                title=form.cleaned_data[section_name + '_title'],
                                text=form.cleaned_data[section_name + '_text'])

            # compare to section at same index, don't add if same
            if section_index < len(saved_sections):
                saved_section = q.Section.objects.get(id=saved_sections[section_index])
            else:
                saved_section = None

            if saved_section is None or section.render_html() != saved_section.render_html():
                section.save()
            else:
                section = saved_section

            obj.sections.add(section)
            section_index += 1

    if obj.intro is None or obj.intro.render_html() != intro.render_html():
        intro.save()
        obj.intro = intro

    if obj.margin_section is None or \
                    obj.margin_section.render_html() != margin_section.render_html():
        margin_section.save()
        obj.margin_section = margin_section

    return obj


class QuoteTemplateView(UpdateView):
    model = q.QuoteTemplate
    form_class = qf.QuoteTemplateForm
    template_name = "quotes/quote_template.html"

    def get_success_url(self):
        messages.success(self.request, 'Template saved.')
        return reverse('edit_quote_template', args=[self.object.id])

    def get_object(self, queryset=None):
        try:
            return super(QuoteTemplateView, self).get_object(queryset)
        except AttributeError:
            return None

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(QuoteTemplateView, self).get_form_kwargs()
        if hasattr(self, 'object') and hasattr(self.object, 'quote'):
            kwargs.update({'instance': self.object.quote})
        return kwargs

    def form_valid(self, form):
        quote = _create_quote(form)
        quote.save()
        if hasattr(self, 'object') and self.object is None:
            self.object = q.QuoteTemplate.objects.create(quote=quote)
        return HttpResponseRedirect(self.get_success_url())

    def render_to_response(self, context, **response_kwargs):
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
                        'language': get_language(),
                        'sections': quote.all_sections()})
        return super(QuoteTemplateView, self).render_to_response(context)