from django.forms import ModelForm
from market_analysis.models import CustomerLead
from django import forms


class CustomerLeadModelForm(ModelForm):
    email = forms.CharField(
        error_messages={'required': 'Email is required.', 'unique': 'Email is already on the waiting list.'})
    name = forms.CharField(error_messages={'required': 'Name is required.'})
    website = forms.URLField(error_messages={'required': 'Website URL is required.'})

    class Meta:
        model = CustomerLead
        fields = ['name', 'email', 'website']
