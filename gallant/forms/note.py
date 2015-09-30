from django import forms
from gallant import models as g
from user import UserModelNgForm


class NoteForm(UserModelNgForm):
    class Meta:
        model = g.Note
        fields = ['text']

    def __init__(self, *args, **kwargs):
        kwargs.update(prefix='note')
        super(NoteForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = forms.Textarea(attrs={'rows': 3})
        self.fields['text'].label = 'Notes'
        self.fields['text'].help_text = ''
