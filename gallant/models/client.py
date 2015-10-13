from django.db import models as m
from django.db import transaction
from django.conf import settings
from djmoney.forms.widgets import CURRENCY_CHOICES
from gallant import fields as gf
from gallant_user import UserModel, UserModelManager, ContactInfo
from misc import Note


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
    email = m.EmailField()
    contact_info = m.ForeignKey(ContactInfo, null=True, blank=True)

    type = m.CharField(max_length=2, choices=ClientType.choices(), blank=True)
    size = m.CharField(max_length=2, choices=ClientSize.choices(), blank=True)
    status = m.CharField(max_length=2, choices=ClientStatus.choices())

    language = m.CharField(max_length=7, choices=settings.LANGUAGES)
    currency = m.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD',)

    notes = m.ManyToManyField(Note)

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_client', 'View client'),
        )

    objects = UserModelManager()

    def soft_delete(self, deleted_by_parent=False):
        with transaction.atomic():
            for note in self.notes.all_for(self.user, 'change'):
                note.soft_delete(deleted_by_parent=True)

            for brief in self.brief_set.all_for(self.user, 'change'):
                brief.soft_delete(deleted_by_parent=True)

            for quote in self.quote_set.all_for(self.user, 'change'):
                quote.soft_delete(deleted_by_parent=True)

            super(Client, self).soft_delete(deleted_by_parent)

