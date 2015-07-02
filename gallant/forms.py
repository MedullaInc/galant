from django import forms
from django.utils.translation import get_language
from gallant import models as g


class ClientForm(forms.ModelForm):
    class Meta():
        model = g.Client
        fields = ['name', 'type', 'size', 'status', 'language', 'currency']

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.initial['language'] = get_language()
        self.fields['notes'] = forms.CharField(
            widget=forms.Textarea(attrs={'rows': 5}), required=False)

class NoteForm(forms.ModelForm):
    class Meta():
        model = g.Note
        fields = ['text']
