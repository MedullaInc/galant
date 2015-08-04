from django import forms
from django.conf import settings
from django.utils.translation import get_language
from gallant import models as g


class UserModelForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserModelForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.user = self.user
        return super(UserModelForm, self).save(*args, **kwargs)


class ClientForm(UserModelForm):
    class Meta:
        model = g.Client
        fields = ['name', 'type', 'size', 'status', 'language', 'currency']

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.initial['language'] = get_language()
        self.fields['notes'] = forms.CharField(
            widget=forms.Textarea(attrs={'rows': 5}), required=False)


class ServiceForm(UserModelForm):
    class Meta:
        model = g.Service
        fields = ['name', 'description', 'cost', 'quantity', 'type']

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['notes'] = forms.CharField(
            widget=forms.Textarea(attrs={'rows': 5}), required=False)


class NoteForm(UserModelForm):
    class Meta:
        model = g.Note
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['text'] = forms.CharField(
            widget=forms.Textarea(attrs={'rows': 3}))


class LanguageForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES, label='', initial=get_language())