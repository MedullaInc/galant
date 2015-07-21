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
        section_names = [key for key, value in self.data.items() if 'section_' in key]
        for extra_section in ['intro', 'margin_section']:
            for postfix in ['_title', '_text']:
                section_names.append(extra_section + postfix)

        for s in section_names:
            if s in self.data:
                cleaned_data[s] = clean_str(self.data[s])

        return cleaned_data


class QuoteTemplateForm(forms.ModelForm):
    class Meta():
        model = q.Quote
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(QuoteTemplateForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(label='Template Name')

    def clean(self):
        cleaned_data = super(QuoteTemplateForm, self).clean()
        section_names = [key for key, value in self.data.items() if 'section_' in key]
        for extra_section in ['intro', 'margin_section']:
            for postfix in ['_title', '_text']:
                section_names.append(extra_section + postfix)

        for s in section_names:
            if s in self.data:
                cleaned_data[s] = clean_str(self.data[s])

        return cleaned_data


class LanguageForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES, label='', initial=get_language())


def clean_str(value):
    if isinstance(value, six.string_types) or value is None:
        return value
    return smart_text(value)

