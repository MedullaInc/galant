import inspect
from custom_user.models import AbstractEmailUser
from django.db import models
from django.conf import settings
from jsonfield import JSONField
from autofixture import generators, register, AutoFixture
from djmoney.models.fields import MoneyField
from enum import Enum


class GallantUser(AbstractEmailUser):
    """
    Custom Gallant user
    """
    class Meta(AbstractEmailUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class ULText(models.Model):
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


class Service(models.Model):
    """
    A service to be rendered for a client, will appear on Quotes. When associated with a project / user, it should
    be displayed as a 'deliverable' instead.
    """
    name = models.ForeignKey(ULText, related_name='name')
    description = models.ForeignKey(ULText, related_name='description')

    # currency is chosen based on client preference
    cost = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    quantity = models.IntegerField()
    type = models.CharField(max_length=2, choices=ServiceType.choices())

    parent = models.ForeignKey('self', null=True, blank=True, related_name='sub_services')

    def get_total_cost(self):
        total = self.cost
        for sub in self.sub_services.all():
            total += sub.get_total_cost()

        return total


