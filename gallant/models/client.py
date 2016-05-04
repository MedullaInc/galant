from django.db import models as m
from django.db import transaction
from django.conf import settings
from django.db.models.signals import m2m_changed
from django.dispatch.dispatcher import receiver
from djmoney.forms.widgets import CURRENCY_CHOICES
from gallant.enums import ClientStatus, ClientReferral
from gallant_user import UserModel, UserModelManager, ContactInfo
from misc import Note


class Client(UserModel):
    name = m.CharField(max_length=255)
    email = m.EmailField()
    company = m.CharField(max_length=255, blank=True)
    contact_info = m.ForeignKey(ContactInfo, null=True, blank=True)

    status = m.CharField(max_length=2, choices=ClientStatus.choices())
    auto_pipeline = m.BooleanField(default=True)
    alert = m.CharField(max_length=63, blank=True, default='')

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


@receiver(m2m_changed, sender=Client)
def client_payments_modified(action, instance, reverse, **kwargs):
    if 'post' in action:
        cstat = int(instance.status)

        if instance.auto_pipeline and cstat == ClientStatus.Project_Underway.value:
            instance.status = ClientStatus.Pending_Payment.value
            cstat = instance.status
            instance.alert = ''
            instance.save()

        if cstat == ClientStatus.Pending_Payment.value:
            set_client_payment_alert(instance, instance.user)

            if instance.auto_pipeline:
                check_and_close(instance, instance.user)

            instance.save()
