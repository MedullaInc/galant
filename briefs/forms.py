from django import forms
from django.utils import six
from briefs import models as b
from django.utils.encoding import smart_text


class BriefForm(forms.ModelForm):
    class Meta():
        model = b.Brief
        fields = ['title']

    def clean(self):
        cleaned_data = super(BriefForm, self).clean()
        section_names = [key for key, value in self.data.items() if 'section_' in key]
        for extra_section in ['intro', 'margin_section']:
            for postfix in ['_title', '_text']:
                section_names.append(extra_section + postfix)

        for s in section_names:
            if s in self.data:
                cleaned_data[s] = clean_str(self.data[s])

        return cleaned_data


def clean_str(value):
    if isinstance(value, six.string_types) or value is None:
        return value
    return smart_text(value)

