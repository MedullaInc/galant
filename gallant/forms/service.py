from django import forms
from gallant import models as g
from user import UserModelForm


class ServiceForm(UserModelForm):
    class Meta:
        model = g.Service
        fields = ['name', 'description', 'cost', 'time']

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['notes'] = forms.CharField(
            widget=forms.Textarea(attrs={'rows': 5}), required=False)


class ServiceOnlyForm(UserModelForm):
    class Meta:
        model = g.Service
        fields = ['name', 'description', 'cost', 'time']
