import inspect
from custom_user.models import AbstractEmailUser
# TODO: from briefs.models import Brief
from django.db import models as m
from django.conf import settings
from django.utils import translation
from django import forms
from django.core.exceptions import FieldError
from jsonfield import JSONCharField, JSONField
from django.forms.utils import ValidationError
from djmoney.models.fields import MoneyField
from djmoney.forms.widgets import CURRENCY_CHOICES
from enum import Enum

class GallantUser(AbstractEmailUser):
    """
    Custom Gallant user
    """

    class Meta(AbstractEmailUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Note(m.Model):
    text = m.TextField(help_text='User comment / note.')
    created = m.DateTimeField(auto_now_add=True)
    created_by = m.ForeignKey(GallantUser)


class ULTextDict(dict):
    def get_text(self, language=None):
        if language is None:
            language = translation.get_language()

        if language in self:
            return self[language]
        else:
            return ''

    def set_text(self, text, language=None):
        if language is None:
            language = translation.get_language()

        self[language] = text


def _ultext_to_python(value):
    if isinstance(value, dict):
        d = ULTextDict()
        d.update(value)
        return d
    elif isinstance(value, basestring):
        d = ULTextDict()
        d.update({translation.get_language(): value})
        return d

    if value is None:
        return value

    raise FieldError("ULTextField requires a dictionary.")


class ULTextFormField(forms.fields.CharField):
    def to_python(self, value):
        return _ultext_to_python(value)

    def clean(self, value):

        if not value and not self.required:
            return None

        # Trap cleaning errors & bubble them up as JSON errors
        try:
            return super(ULTextFormField, self).clean(value)
        except TypeError:
            raise ValidationError("Invalid text")


class ULTextField(JSONField):
    form_class = ULTextFormField

    def formfield(self, **kwargs):
        field = super(JSONField, self).formfield(**kwargs)
        field.widget = forms.Textarea(attrs={'rows': 3})
        field.help_text = ''
        return field

    def pre_init(self, value, obj):
        value = super(JSONField, self).pre_init(value, obj)
        return _ultext_to_python(value)


class ULCharField(ULTextField):
    def formfield(self, **kwargs):
        field = super(ULTextField, self).formfield(**kwargs)
        field.widget = forms.TextInput()
        field.help_text = ''
        return field


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not (inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not (m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices


class ServiceType(ChoiceEnum):
    Branding = 0
    Design = 1
    Architecture = 2
    Advertising = 3
    Production = 4
    Illustration = 5
    Industrial_Design = 6
    Fashion_Design = 7
    Interior_Design = 8


class Service(m.Model):
    """
    A service to be rendered for a client, will appear on Quotes. When associated with a project / user, it should
    be displayed as a 'deliverable' instead.
    """
    # name = m.ForeignKey(ULText, related_name='name')
    name = ULCharField()
    description = ULTextField(null=True)
    # TODO: brief = ServiceBrief()

    # currency is chosen based on client preference
    cost = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    quantity = m.IntegerField()
    type = m.CharField(max_length=2, choices=ServiceType.choices())

    parent = m.ForeignKey('self', null=True, blank=True, related_name='sub_services')

    notes = m.ManyToManyField(Note)

    def get_total_cost(self):
        total = self.cost
        for sub in self.sub_services.all():
            total += sub.get_total_cost()

        return total


class ClientType(ChoiceEnum):
    Individual = 0
    Organization = 1


class ClientSize(ChoiceEnum):
    Micro = 0
    Small = 1
    Medium = 2
    Large = 3


class ClientStatus(ChoiceEnum):
    Approached = 0
    Quoted = 1
    Brief_Sent = 2
    Pending_Payment = 3
    Pending_Deliverables = 4
    Settled = 5
    Past_Due = 6
    Check_Notes = 7
    Blacklisted = 8


class Client(m.Model):
    name = m.CharField(max_length=255)
    type = m.CharField(max_length=2, choices=ClientType.choices())
    size = m.CharField(max_length=2, choices=ClientSize.choices())
    status = m.CharField(max_length=2, choices=ClientStatus.choices())

    language = m.CharField(max_length=7, choices=settings.LANGUAGES)
    currency = m.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')

    notes = m.ManyToManyField(Note)