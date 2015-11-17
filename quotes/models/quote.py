from uuid import uuid4
from gallant import models as g
from gallant import fields as gf
from django.db import models as m
from django.db import transaction
from django.conf import settings
from gallant import utils
from gallant.models import UserModelManager
from moneyed import Money
from section import TextSection, ServiceSection


class QuoteStatus(gf.ChoiceEnum):
    Draft = 0
    Not_Sent = 1
    Sent = 2
    Viewed = 3
    Superseded = 4  # by a new revision
    Accepted = 5
    Rejected = 6


class Quote(g.UserModel):
    name = m.CharField(max_length=512, default='New Quote')
    client = m.ForeignKey(g.Client, null=True)
    sections = m.ManyToManyField(TextSection, blank=True, related_name='sections')
    services = m.ManyToManyField(ServiceSection, blank=True, related_name='services')

    language = m.CharField(max_length=7, null=True, choices=settings.LANGUAGES,
                           help_text='Language of quote, or null for template.')

    status = m.CharField(max_length=2, choices=QuoteStatus.choices(), default=QuoteStatus.Draft.value)
    modified = m.DateTimeField(auto_now=True)

    token = m.UUIDField(default=uuid4, editable=False, unique=True)

    parent = m.ForeignKey('self', null=True, blank=True, related_name='versions')
    projects = m.ManyToManyField(g.Project, blank=True)
    payments = m.ManyToManyField(g.Payment, blank=True)

    def get_languages(self):
        language_set = set()
        for s in list(self.sections.all_for(self.user)):
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
        sections.sort(lambda a, b: cmp(a.index, b.index))
        return sections

    def get_total_cost(self):
        total = Money(0, "USD")
        for service in self.services.all_for(self.user):
            total += service.service.get_total_cost()

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

    def language_list(self):
        return [(c, utils.LANG_DICT[c]) for c in self.quote.get_languages() if c in utils.LANG_DICT]

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
