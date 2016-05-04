from django.db import models as m
from django.db import transaction
from djmoney.models.fields import MoneyField
from gallant import fields as gf
from gallant.enums import ServiceStatus, ServiceType
from gallant_user import UserModel, UserModelManager
from misc import Note


class Service(UserModel):
    """
    A service to be rendered for a client, will appear on Quotes. When associated with a project / user, it should
    be displayed as a 'deliverable' instead.
    """
    # name = m.ForeignKey(ULText, related_name='name')
    name = gf.ULCharField()
    description = gf.ULTextField(null=True)
    status = m.CharField(max_length=2, choices=ServiceStatus.choices(), default=ServiceStatus.Pending_Assignment.value)

    # TODO: brief = ServiceBrief()

    # currency is chosen based on client preference
    cost = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    quantity = m.IntegerField()
    type = m.CharField(max_length=2, choices=ServiceType.choices())
    index = m.IntegerField(default=0) 
    parent = m.ForeignKey('self', null=True, blank=True, related_name='sub_services')
    notes = m.ManyToManyField(Note)
    views = m.IntegerField(default=0)

    def get_total_cost(self):
        total = self.cost * self.quantity
        for sub in self.sub_services.all_for(self.user):
            total += sub.get_total_cost()

        return total

    def get_quote_template_services(self):
        return self.services.all_for(self.user)

    def get_languages(self):
        language_set = set()
        map(lambda l: language_set.add(l), self.name.keys())
        map(lambda l: language_set.add(l), self.description.keys())
        return language_set


    def __unicode__(self):
        return self.name.get_text()

    class Meta:
        permissions = (
            ('view_service', 'View service'),
        )

    objects = UserModelManager()

    def soft_delete(self, deleted_by_parent=False):
        with transaction.atomic():
            for note in self.notes.all_for(self.user, 'change'):
                note.soft_delete(deleted_by_parent=True)

            for service in self.sub_services.all_for(self.user, 'change'):
                service.soft_delete(deleted_by_parent=True)

            super(Service, self).soft_delete(deleted_by_parent)