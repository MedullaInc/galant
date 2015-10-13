from django.core.exceptions import ValidationError
from django import forms
from briefs import models as b
from gallant import models as g
from gallant import forms as gf


class BriefForm(gf.UserModelForm):
    class Meta:
        model = b.Brief
        fields = ['title', 'greeting', 'client', 'quote']

    def __init__(self, user, *args, **kwargs):
        super(BriefForm, self).__init__(user, *args, **kwargs)
        self.fields['quote'].widget = forms.HiddenInput()
        self.fields['quote'].required = False
        self.fields['greeting'].widget = forms.Textarea(attrs={'rows': 3})
        if 'client' in self.initial:
            self.fields['client'].widget = forms.HiddenInput()
        else:
            self.fields['client'].queryset = g.Client.objects.all_for(self.user)

    def clean_client(self):
        client = self.cleaned_data['client']
        if client is None:
            raise ValidationError('Please select a client.')
        elif self.user.has_perm('view_client', client):
            return client
        else:
            raise ValidationError('Invalid client.')


class BriefTemplateForm(gf.UserModelForm):
    class Meta:
        model = b.Brief
        fields = ['name', 'title', 'greeting']

    def __init__(self, user, *args, **kwargs):
        super(BriefTemplateForm, self).__init__(user, *args, **kwargs)
        self.fields['name'].label = 'Template Name'
        self.fields['title'].label = 'Brief Title'
        self.fields['greeting'].widget = forms.Textarea(attrs={'rows': 3})
        self.fields['title'].required = False
