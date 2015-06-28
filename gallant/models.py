from custom_user.models import AbstractEmailUser
from django.db import models
from django.conf import settings
from jsonfield import JSONField
from autofixture import generators, register, AutoFixture


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