from django import forms
from django.utils import six
from quotes import models as q
from gallant import models as g
from django.utils.encoding import smart_text
from django.utils.translation import get_language
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
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


def create_quote(quote_form, section_forms):
    obj = quote_form.save(commit=True)
    obj.sections.clear()
    obj.services.clear()

    for s in section_forms:
        if type(s) is SectionForm:
            obj.sections.add(s.save())
        elif type(s) is ServiceSectionForm:
            obj.services.add(s.save())

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
    m = re.match('-service-(\d+)-', prefix)
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


def section_forms_post(data):
    sf = []
    for key, value in sorted(data.items(), key=operator.itemgetter(1)):
        m = re.match('(-section-\d+)-name', key)
        if m is not None:
            sf.append(SectionForm(data, prefix=m.group(1)))
        else:
            m = re.match('(-service-\d+)-name', key)
            if m is not None:
                sf.append(ServiceSectionForm(data, prefix=m.group(1)))

    return sf


def section_forms_quote(quote):
    sf = []
    for section in quote.all_sections():
        if type(section) is q.Section:
            sf.append(SectionForm(instance=section, prefix='-section-%d' % section.index))
        elif type(section) is q.ServiceSection:
            sf.append(ServiceSectionForm(instance=section, prefix='-service-%d' % section.index))

    return sf


class SectionForm(forms.ModelForm):
    class Meta():
        model = q.Section
        fields = ['name', 'title', 'text']

    def __init__(self, data=None, prefix=None, *args, **kwargs):
        # see if update or create
        prefix = prefix or ''
        data = data or {}
        if prefix + '-id' in data:
            section = get_object_or_404(q.Section, pk=data[prefix + '-id'])
            super(SectionForm, self).__init__(data=data, prefix=prefix, instance=section, *args, **kwargs)
        else:
            super(SectionForm, self).__init__(data=data, prefix=prefix, *args, **kwargs)

    def as_table(self):
        t = get_template('quotes/section_form.html')
        if self.instance:
            section = self.instance
        else:
            section = self.save(commit=False)
        context = {'prefix': self.prefix + '-', 'name': section.name, 'section': section}
        if section.name != 'margin' and section.name != 'intro':
            context.update({'extra_class': 'dynamic_section'})
        return t.render(context)

    def save(self, commit=True):
        if self.prefix:
            idx = re.match('-section-(\d+)', self.prefix).group(1) or 0
            self.instance.index = idx
        return super(SectionForm, self).save(commit)


class ServiceSectionForm(forms.ModelForm):
    class Meta():
        model = g.Service  # make sure to call with ServiceSection instance, not Service
        fields = ['name', 'description', 'cost', 'quantity', 'type']

    def __init__(self, data=None, instance=None, *args, **kwargs):
        super(ServiceSectionForm, self).__init__(data=data, instance=instance, *args, **kwargs)
        self.section = None

        # check to see if we were called with an instance param
        if instance:
            self.section = instance
            self.instance = self.section.service
        elif self.prefix + '-id' in self.data:
            self.section = get_object_or_404(q.ServiceSection, pk=self.data[self.prefix + '-id'])
            self.instance = self.section.service
        else:
            name = self.data[self.prefix + '-section_name']
            self.section = type('obj', (object,), {'name': name, 'display_title': name.replace('_', ' ').title(),
                                                   'service': self.instance})

    def as_table(self):
        t = get_template('quotes/service_section_form.html')

        return t.render({'prefix': self.prefix + '-', 'section': self.section,
                         'type_choices': g.ServiceType.choices(),
                         'extra_class': 'dynamic_section'})

    def save(self, commit=True):
        super(ServiceSectionForm, self).save(commit)
        if self.prefix:
            idx = re.match('-service-(\d+)', self.prefix).group(1) or 0
            if hasattr(self.section, 'index'):
                self.section.index = idx
            else:
                self.section = q.ServiceSection.objects.create(service=self.instance, index=idx, name=self.section.name)

        self.section.save()
        return self.section