from django.core.exceptions import ValidationError
from quotes import models as q
from gallant import models as g
from gallant import forms as gf


class QuoteForm(gf.UserModelForm):
    class Meta:
        model = q.Quote
        fields = ['name', 'client', 'status']

    def __init__(self, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)
        self.fields['client'].queryset = g.Client.objects.all_for(self.user)

    def clean_client(self):
        client = self.cleaned_data['client']
        if self.user.has_perm('view_client', client):
            return client
        else:
            raise ValidationError('Invalid client.')


class QuoteTemplateForm(gf.UserModelForm):
    class Meta:
        model = q.Quote
        fields = ['name']
