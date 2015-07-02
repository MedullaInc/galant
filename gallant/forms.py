from django import forms
from django.utils.translation import get_language
from gallant.models import *


class ClientForm(forms.ModelForm):
    class Meta():
        model = Client
        fields = ['name', 'type', 'size', 'status', 'language', 'currency']

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.initial['language'] = get_language()
        self.fields['notes'] = forms.CharField(
            widget=forms.Textarea(attrs={'rows': 5}), required=False)

class NoteForm(forms.ModelForm):
    class Meta():
        model = Note
        fields = ['text']
