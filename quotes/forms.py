from django import forms
from django.utils import six
from quotes import models as q
from django.utils.encoding import smart_text


class QuoteForm(forms.ModelForm):
    class Meta():
        model = q.Quote
        fields = ['name', 'client', 'language', 'status']

    def clean(self):
        cleaned_data = super(QuoteForm, self).clean()
        for extra_section in ['intro', 'margin_section']:
            for postfix in ['_title', '_text']:
                field = extra_section + postfix
                if field in self.data:
                    cleaned_data[field] = clean_str(self.data[field])
        return cleaned_data


def clean_str(value):
    if isinstance(value, six.string_types) or value is None:
        return value
    return smart_text(value)

