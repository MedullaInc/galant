from datetime import datetime

from django.db import models as m
from django.db import transaction
from django.conf import settings
from django.db.models.aggregates import Sum
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils.timezone import get_current_timezone
from djmoney.forms.widgets import CURRENCY_CHOICES
from gallant.enums import ClientStatus, ClientReferral
from gallant_user import UserModel, UserModelManager, ContactInfo
from misc import Note, Payment


class Client(UserModel):
    name = m.CharField(max_length=255)
    email = m.EmailField()
    company = m.CharField(max_length=255, blank=True)
    contact_info = m.ForeignKey(ContactInfo, null=True, blank=True)

    status = m.CharField(max_length=2, choices=ClientStatus.choices())
    auto_pipeline = m.BooleanField(default=True)

    language = m.CharField(max_length=7, choices=settings.LANGUAGES)
    currency = m.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD',)
    last_contacted = m.DateTimeField(null=True, blank=True)

    referred_by = m.CharField(max_length=3, choices=ClientReferral.choices(), blank=True)

    card = m.ForeignKey('kanban.KanbanCard', null=True)

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


@receiver(post_save, sender=Payment)
def payment_saved(sender, instance, **kwargs):
    for client in Client.objects.all_for(instance.user).filter(quote__payments__in=[instance]):
        check_client_payments(client)


def check_client_payments(client):
    cstat = int(client.status)

    if client.auto_pipeline and cstat == ClientStatus.Project_Underway.value:
        client.status = ClientStatus.Pending_Payment.value
        cstat = client.status
        client.card.alert = ''
        client.card.save()
        client.save()

    if cstat == ClientStatus.Pending_Payment.value:
        set_client_payment_alert(client, client.user)

        if client.auto_pipeline:
            check_payments_and_close(client, client.user)

        client.card.save()
        client.save()


def set_client_payment_alert(client, user):
    """ Order projects for client by status importance and set alerts
    """
    val = Payment.objects.all_for(user).filter(quote__client=client,
                                               due__lte=datetime.now(get_current_timezone()),
                                               paid_on__isnull=True)\
                                       .aggregate(amount=Sum('amount'))
    overdue = val['amount']

    if overdue and overdue > 0:
        client.card.alert = '$%d %s overdue' % (overdue, client.currency)
    else:
        client.card.alert = ''


def check_payments_and_close(client, user):
    if Payment.objects.all_for(user).filter(paid_on__isnull=True, quote__client=client).count() == 0:
        client.status = ClientStatus.Closed.value
        client.card.alert = ''
