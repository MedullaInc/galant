from django.core.exceptions import ValidationError
from quotes import models as q
from gallant import models as g
from gallant import forms as gf


class QuoteTemplateForm(gf.UserModelForm):
    class Meta:
        model = q.Quote
        fields = ['name']
