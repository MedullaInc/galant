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
        for key, value in self.data.items():
            if '-section-' in key or '-service-' in key:
                cleaned_data[key] = clean_str(self.data[key])

        return cleaned_data

    def quote_sections(self):
        if self.instance is None or self.instance.pk is None:
            return [q.Section(name='intro', index=0).as_form_table(),
                    q.Section(name='margin', index=1).as_form_table()]
        else:
            sections = list(self.instance.sections.all()) + list(self.instance.services.all())
            sections.sort(lambda a, b: cmp(a.index, b.index))
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

