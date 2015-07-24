from django import forms
from django.utils import six
from quotes import models as q
from gallant import forms as gf
from gallant import fields as gfields
from django.utils.encoding import smart_text
from django.utils.translation import get_language
from django.conf import settings


class QuoteForm(forms.ModelForm):
    class Meta():
        model = q.Quote
        fields = ['name', 'client', 'status']

    def clean(self):
        cleaned_data = super(QuoteForm, self).clean()
        section_names = [key for key, value in self.data.items() if 'section_' in key]
        for extra_section in ['intro', 'margin']:
            for postfix in ['_title', '_text']:
                section_names.append(extra_section + postfix)

        for s in section_names:
            if s in self.data:
                cleaned_data[s] = clean_str(self.data[s])

        return cleaned_data

    def quote_sections(self):
        if self.instance is None or self.instance.pk is None:
            return [q.Section(name='intro').as_form_table(),
                    q.Section(name='margin').as_form_table()]
        else:
            return [s.as_form_table() for s in self.instance.sections.all()]


class QuoteTemplateForm(QuoteForm):
    class Meta():
        model = q.Quote
        fields = ['name']


class SectionForm(forms.ModelForm):
    class Meta():
        model = q.Section
        fields = ['name', 'index', 'title', 'text']


class ServiceSectionForm(gf.ServiceForm):
    index = forms.IntegerField()
    title = gfields.ULTextFormField()
    text = gfields.ULTextFormField()

    def as_table(self):
        super(ServiceSectionForm, self).as_table()


class LanguageForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES, label='', initial=get_language())


def clean_str(value):
    if isinstance(value, six.string_types) or value is None:
        return value
    return smart_text(value)

