from django import forms
from django.utils import six
from quotes import models as q
from gallant import models as g
from django.utils.encoding import smart_text
from django.utils.translation import get_language
from django.conf import settings
from django.shortcuts import get_object_or_404
import operator
import re


class QuoteForm(forms.ModelForm):
    class Meta():
        model = q.Quote
        fields = ['name', 'client', 'status']

    def clean(self):
        cleaned_data = super(QuoteForm, self).clean()
        for key, value in self.data.items():
            if '-section-' in key or '-service-' in key:
                cleaned_data[key] = clean_str(self.data[key])

        return cleaned_data

    def quote_sections(self):
        if self.instance is None or self.instance.pk is None:
            return [q.Section(name='intro', index=0).as_form_table(),
                    q.Section(name='margin', index=1).as_form_table()]
        else:
            sections = self.instance.all_sections()
            return [s.as_form_table() for s in sections]


class QuoteTemplateForm(QuoteForm):
    class Meta():
        model = q.Quote
        fields = ['name']


class LanguageForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES, label='', initial=get_language())


def clean_str(value):
    if isinstance(value, six.string_types) or value is None:
        return value
    return smart_text(value)


def create_quote(quote_form):
    obj = quote_form.save(commit=True)

    saved_sections = dict((s.index, s.id) for s in obj.sections.all())
    saved_sections.update((s.index, s.id) for s in obj.services.all())
    obj.sections.clear()
    obj.services.clear()

    for key, value in sorted(quote_form.cleaned_data.items(), key=operator.itemgetter(1)):
        m = re.match('(-section-\d+-)title', key)
        if m is not None:
            section = create_section(quote_form, m.group(1))

            obj.sections.add(section)
        else:
            m = re.match('(-service-\d+-)service_name', key)
            if m is not None:
                section = create_service(quote_form, m.group(1))

                obj.services.add(section)

    obj.save()
    return obj


def create_section(form, prefix):
    m = re.match('-section-(\d+)-', prefix)
    section_index = int(m.group(1))

    # see if update or create
    if prefix + 'id' in form.cleaned_data:
        section = get_object_or_404(q.Section, pk=form.cleaned_data[prefix + 'id'])
    else:
        section = q.Section()

    section.name = form.cleaned_data[prefix + 'name']
    section.index = section_index
    section.title = form.cleaned_data[prefix + 'title']
    section.text = form.cleaned_data[prefix + 'text']
    section.save()
    return section


def create_service(form, prefix):
    m = re.match('-service-(\d+)', prefix)
    section_index = int(m.group(1))

    # see if update or create
    if prefix + 'id' in form.cleaned_data:
        section = get_object_or_404(q.ServiceSection, pk=form.cleaned_data[prefix + 'id'])
        service = section.service
    else:
        section = q.ServiceSection()
        service = g.Service()

    service.name = form.cleaned_data[prefix + 'service_name']
    service.description = form.cleaned_data[prefix + 'description']
    # TODO: add cost dropdown or decide cost  by user preference
    service.cost = (form.cleaned_data[prefix + 'cost'], 'USD')
    service.quantity = form.cleaned_data[prefix + 'quantity']
    service.type = form.cleaned_data[prefix + 'type']
    service.save()
    section.name = form.cleaned_data[prefix + 'name']
    section.index = section_index
    section.service = service
    section.save()
    return section