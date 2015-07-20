from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.utils.translation import get_language
from django.conf import settings
from django.contrib import messages
from quotes import models as q
from django.core.urlresolvers import reverse
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

    def render_to_response(self, context, **response_kwargs):
        context.update({'title': 'Add Quote', 'object': q.Quote()})
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
        context.update({'title': 'Update Quote'})
        return super(UpdateView, self).render_to_response(context)


class QuoteDetail(DetailView):
    model = q.Quote


class QuoteList(ListView):
    model = q.Quote


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

        if hasattr(self.object, 'quote'):
            context.update({'object': self.object.quote})
        else:
            context.update({'object': q.Quote()})

        context.update({'title': 'Edit Template',
                        'native_language_code': get_language(),
                        'native_language': lang_dict[get_language()],
                        'language_form': form})
        return super(QuoteTemplateView, self).render_to_response(context)