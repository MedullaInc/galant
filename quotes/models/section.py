from gallant import models as g
from gallant import fields as gf
from django.db import models as m
from gallant.models import PolyUserModelManager, UserModelManager


class Section(g.UserModel):
    name = m.CharField(max_length=256, default="section")
    index = m.IntegerField(default=0)
    title = gf.ULCharField(blank=True)
    text = gf.ULTextField(blank=True)

    def display_title(self):
        return self.name.replace('_', ' ').title()

    def get_languages(self):
        language_set = set()
        map(lambda l: language_set.add(l), self.title.keys())
        map(lambda l: language_set.add(l), self.text.keys())
        return language_set

    def __unicode__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name and \
               self.title == other.title and \
               self.text == other.text

    def __ne__(self, other):
        return not self.__eq__(other)

    class Meta:
        permissions = (
            ('view_text', 'View text'),
        )

    objects = UserModelManager()

