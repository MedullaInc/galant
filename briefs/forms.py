from django import forms
from django.utils import six
from briefs import models as b
from django.utils.encoding import smart_text


class BriefForm(forms.ModelForm):
    class Meta():
        model = b.Brief
        fields = ['title', 'status']

    def __init__(self, *args, **kwargs):
        super(BriefForm, self).__init__(*args, **kwargs)
        self.fields['title'].value = self.instance.title.get_text

    def clean(self):
        cleaned_data = super(BriefForm, self).clean()
        return cleaned_data


class ClientBriefForm(BriefForm):
    class Meta():
        model = b.ClientBrief
        fields = ['title', 'status']


# class ProjectBriefForm(BriefForm):
#     class Meta():
#         model = b.ProjectBrief
#         fields = ['title', 'status']
#
#
# class ServiceBriefForm(BriefForm):
#     class Meta():
#         model = b.ServiceBrief
#         fields = ['title', 'status']


# def clean_str(value):
#     if isinstance(value, six.string_types) or value is None:
#         return value
#     return smart_text(value)

