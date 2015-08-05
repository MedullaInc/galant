from custom_user.models import AbstractEmailUser
from django.db import models as m
from django.conf import settings
from djmoney.models.fields import MoneyField
from djmoney.forms.widgets import CURRENCY_CHOICES
from gallant import fields as gf
from polymorphic import PolymorphicModel


class GallantUser(AbstractEmailUser):
    """
    Custom Gallant user
    """

    class Meta(AbstractEmailUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class UserModel(m.Model):
    user = m.ForeignKey(GallantUser)

    class Meta:
        abstract = True


class PolyUserModel(PolymorphicModel):
    user = m.ForeignKey(GallantUser)

    class Meta:
        abstract = True


class Note(UserModel):
    text = m.TextField(help_text='User comment / note.')
    created = m.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ('view_note', 'View note'),
        )


class ServiceType(gf.ChoiceEnum):
    Branding = 0
    Design = 1
    Architecture = 2
    Advertising = 3
    Production = 4
    Illustration = 5
    Industrial_Design = 6
    Fashion_Design = 7
    Interior_Design = 8


class Service(UserModel):
    """
    A service to be rendered for a client, will appear on Quotes. When associated with a project / user, it should
    be displayed as a 'deliverable' instead.
    """
    # name = m.ForeignKey(ULText, related_name='name')
    name = gf.ULCharField()
    description = gf.ULTextField(null=True)
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

    class Meta:
        permissions = (
            ('view_service', 'View service'),
        )


class ClientType(gf.ChoiceEnum):
    Individual = 0
    Organization = 1


class ClientSize(gf.ChoiceEnum):
    Micro = 0
    Small = 1
    Medium = 2
    Large = 3


class ClientStatus(gf.ChoiceEnum):
    Approached = 0
    Quoted = 1
    Brief_Sent = 2
    Pending_Payment = 3
    Pending_Deliverables = 4
    Settled = 5
    Past_Due = 6
    Check_Notes = 7
    Blacklisted = 8


class Client(UserModel):
    name = m.CharField(max_length=255)
    email = m.EmailField(blank=True)
    phone_number = m.CharField(validators=[gf.PHONE_REGEX], blank=True, max_length=15)
    address = m.TextField(blank=True)

    type = m.CharField(max_length=2, choices=ClientType.choices())
    size = m.CharField(max_length=2, choices=ClientSize.choices())
    status = m.CharField(max_length=2, choices=ClientStatus.choices())

    language = m.CharField(max_length=7, choices=settings.LANGUAGES)
    currency = m.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')

    notes = m.ManyToManyField(Note)

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_client', 'View client'),
        )


class Project(UserModel):
    name = m.CharField(max_length=255)
    # TODO: finish model according to diagrams

    class Meta:
        permissions = (
            ('view_project', 'View project'),
        )
