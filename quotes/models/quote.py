from uuid import uuid4

from django.db.models.signals import post_save, m2m_changed
from django.dispatch.dispatcher import receiver
from gallant import models as g
from gallant import fields as gf
from django.db import models as m
from django.db import transaction
from django.conf import settings
from gallant import utils
from gallant.enums import ClientStatus
from gallant.enums import ProjectStatus
from gallant.models import UserModelManager
from gallant.models.client import check_client_payments
from gallant.models import Project as gp
from moneyed import Money
from section import Section


class QuoteStatus(gf.ChoiceEnum):
    Draft = 0
    Not_Sent = 1
    Sent = 2
    Viewed = 3
    Superseded = 4  # by a new revision
    Accepted = 5
    Rejected = 6


class Quote(g.UserModel):
    name = m.CharField(max_length=255, default='New Quote')
    client = m.ForeignKey(g.Client, null=True)
    sections = m.ManyToManyField(Section, blank=True)
    services = m.ManyToManyField(g.Service, blank=True)

    language = m.CharField(max_length=7, null=True, choices=settings.LANGUAGES,
                           help_text='Language of quote, or null for template.')

    status = m.CharField(max_length=2, choices=QuoteStatus.choices(), default=QuoteStatus.Draft.value)
    modified = m.DateTimeField(auto_now=True)

    token = m.UUIDField(default=uuid4, editable=False, unique=True)

    parent = m.ForeignKey('self', null=True, blank=True, related_name='versions')
    projects = m.ManyToManyField(g.Project, blank=True)
    payments = m.ManyToManyField(g.Payment, blank=True)
    views = m.IntegerField(default=0)
    session_duration = m.FloatField(default=0.0)

    card = m.ForeignKey('kanban.KanbanCard', null=True)

    def get_languages(self):
        language_set = set()
        for s in list(self.all_sections()):
            if s is not None:
                language_set.update(s.get_languages())

        return language_set

    def intro(self):
        return self.sections.get_for(self.user, name='intro')

    def important_notes(self):
        return self.sections.get_for(self.user, name='important_notes')

    def all_sections(self):
        sections = list(self.sections.all_for(self.user)) + \
                   list(self.services.all_for(self.user))
        return sections

    def get_total_cost(self):
        total = Money(0, "USD")
        for service in self.services.all_for(self.user):
            total += service.get_total_cost()

        return total

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_quote', 'View quote'),
        )

    objects = UserModelManager()

    def soft_delete(self, deleted_by_parent=False):
        with transaction.atomic():
            for section in self.sections.all_for(self.user, 'change'):
                section.soft_delete(deleted_by_parent=True)

            for service in self.services.all_for(self.user, 'change'):
                service.soft_delete(deleted_by_parent=True)

            super(Quote, self).soft_delete(deleted_by_parent)


class QuoteTemplate(g.UserModel):
    quote = m.ForeignKey(Quote)

    class Meta:
        permissions = (
            ('view_quotetemplate', 'View quotetemplate'),
        )

    objects = UserModelManager()

    def soft_delete(self, deleted_by_parent=False):
        with transaction.atomic():
            if self.quote.client_id is None:
                self.quote.soft_delete(deleted_by_parent=True)

            super(QuoteTemplate, self).soft_delete(deleted_by_parent)


@receiver(post_save, sender=Quote)
def client_quoted(sender, instance, **kwargs):
    if instance.client_id:
        client = instance.client
        cstat = int(client.status)
        qstat = int(instance.status)

        if client.auto_pipeline and cstat < ClientStatus.Quoted.value and qstat >= QuoteStatus.Sent.value:
            client.status = ClientStatus.Quoted.value
            cstat = client.status
            client.card.alert = ''
            client.card.save()
            client.save()

        if cstat == ClientStatus.Quoted.value:
            if qstat == QuoteStatus.Rejected.value:
                client.card.alert = 'Quote Rejected'
                client.card.save()
            elif qstat == QuoteStatus.Accepted.value:
                client.card.alert = 'Quote Accepted'
                client.card.save()


@receiver(post_save, sender=Quote)
def quote_accepted(sender, instance, **kwargs):
    if instance.status == QuoteStatus.Accepted.value:
        # Create Project from Quote
        if len(instance.projects.all_for(instance.user)) == 0:
            project = gp.objects.create(user=instance.user, name=instance.name, status=ProjectStatus.Pending_Assignment.value)
            instance.projects.add(project)
            for service in instance.services.all_for(instance.user, 'change'):
                service.save()


@receiver(m2m_changed, sender=Quote.payments.through)
def client_payments_modified(action, instance, reverse, **kwargs):
    if 'post' in action:
        check_client_payments(instance.client)