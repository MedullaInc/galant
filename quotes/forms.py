from django import forms
from django.utils import six
from quotes import models as q
from django.utils.encoding import smart_text
from django.utils.translation import get_language
from django.conf import settings


class QuoteForm(forms.ModelForm):
    class Meta():
        model = q.Quote
        fields = ['name', 'client', 'status']

    def clean(self):
        cleaned_data = super(QuoteForm, self).clean()
        section_names = [key for key, value in self.data.items() if '-section-' in key]

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


class LanguageForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES, label='', initial=get_language())


def clean_str(value):
    if isinstance(value, six.string_types) or value is None:
        return value
    return smart_text(value)

