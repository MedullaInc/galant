from django.db import models as m
from django.db import transaction
from django.conf import settings
from djmoney.forms.widgets import CURRENCY_CHOICES
from gallant import fields as gf
from gallant_user import UserModel, UserModelManager, ContactInfo
from misc import Note


class ClientStatus(gf.ChoiceEnum):
    """ Determines Client's place in workflow / pipeline, set to >= User_Status for manual management.
    """
    Pre_Quote = 0
    Quoted = 1
    Project_Underway = 2
    Pending_Payment = 3
    Closed = 4
    User_Status = 10


class ClientReferral(gf.ChoiceEnum):
    Search = 0
    Paid_Advertisement = 1
    Social_Media = 2
    Client = 3
    Networking = 4
    Word_Of_Mouth = 5
    Other = 6


class Client(UserModel):
    name = m.CharField(max_length=255)
    email = m.EmailField()
    company = m.CharField(max_length=255, blank=True)
    contact_info = m.ForeignKey(ContactInfo, null=True, blank=True)

    status = m.CharField(max_length=2, choices=ClientStatus.choices())

    language = m.CharField(max_length=7, choices=settings.LANGUAGES)
    currency = m.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD',)
    last_contacted = m.DateTimeField(null=True, blank=True)

    referred_by = m.CharField(max_length=3, choices=ClientReferral.choices(), blank=True)

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

