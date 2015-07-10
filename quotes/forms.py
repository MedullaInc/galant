from django import forms
from django.utils.translation import get_language
from quotes import models as q


class QuoteForm(forms.ModelForm):
    class Meta():
        model = q.Quote
        fields = ['name', 'client', 'intro', 'language', 'status', 'margin_section']
    '''
    def __init__(self, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)
        self.initial['language'] = get_language()
        self.fields['notes'] = forms.CharField(
            widget=forms.Textarea(attrs={'rows': 5}), required=False)
    '''
