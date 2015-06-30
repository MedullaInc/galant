import inspect
from custom_user.models import AbstractEmailUser
from django.db.models import *
from django.conf import settings
from jsonfield import JSONField
from autofixture import generators, register, AutoFixture
from djmoney.models.fields import MoneyField
from djmoney.forms.widgets import CURRENCY_CHOICES
from enum import Enum


class GallantUser(AbstractEmailUser):
    """
    Custom Gallant user
    """
    class Meta(AbstractEmailUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Note(Model):
    text = TextField(help_text='User comment / note.')
    created = DateTimeField(auto_now_add=True)
    created_by = ForeignKey(GallantUser)


class ULText(Model):
    """
    User Locale Text, allows users to store translated versions of the same text and display the version that
    matches client's language preferences.
    """
    TEXT_LENGTH_MAX = 60000  # should be enough for ~2 pages in 10 languages
    text_dict = JSONField(max_length=TEXT_LENGTH_MAX,
                          help_text='JSON formatted dictionary mapping \
                          [IETF language code -> translation in that language]')

    def get_text(self, language=None):
        if language is None:
            language = settings.LANGUAGE_CODE

        if language in self.text_dict:
            return self.text_dict[language]
        else:
            return ''


class ULTextAutoFixture(AutoFixture):
    g = generators.StringGenerator()
    field_values = {
        'text_dict': {
            'en': g.get_value(),
            'es': g.get_value(),
            g.get_value(): g.get_value(),
        }
    }

register(ULText, ULTextAutoFixture)


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not(m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices


class ServiceType(ChoiceEnum):
    BRANDING = 0
    DESIGN = 1
    ARCHITECTURE = 2
    ADVERTISING = 3
    PRODUCTION = 4
    ILLUSTRATION = 5
    INDUSTRIAL_DESIGN = 6
    FASHION_DESIGN = 7
    INTERIOR_DESIGN = 8


class Service(Model):
    """
    A service to be rendered for a client, will appear on Quotes. When associated with a project / user, it should
    be displayed as a 'deliverable' instead.
    """
    name = ForeignKey(ULText, related_name='name')
    description = ForeignKey(ULText, related_name='description')

    # currency is chosen based on client preference
    cost = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    quantity = IntegerField()
    type = CharField(max_length=2, choices=ServiceType.choices())

    parent = ForeignKey('self', null=True, blank=True, related_name='sub_services')

    def get_total_cost(self):
        total = self.cost
        for sub in self.sub_services.all():
            total += sub.get_total_cost()

        return total


class ClientType(ChoiceEnum):
    INDIVIDUAL = 0
    ORGANIZATION = 1


class ClientSize(ChoiceEnum):
    MICRO = 0
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class ClientStatus(ChoiceEnum):
    APPROACHED = 0
    QUOTED = 1
    BRIEF_SENT = 2
    PENDING_PAYMENT = 3
    PENDING_DELIVERABLES = 4
    SETTLED = 5
    PAST_DUE = 6
    CHECK_NOTES = 7
    BLACKLISTED = 8


class Client(Model):
    name = CharField(max_length=255)
    type = CharField(max_length=2, choices=ClientType.choices())
    size = CharField(max_length=2, choices=ClientSize.choices())
    status = CharField(max_length=2, choices=ClientStatus.choices())

    language = CharField(max_length=7, choices=settings.LANGUAGES)
    currency = CharField(max_length=3, choices=CURRENCY_CHOICES)

    notes = ManyToManyField(Note)