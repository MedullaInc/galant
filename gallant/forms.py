from django import forms
from gallant.models import *


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "type", "size", "status", "language", "currency", "notes"]