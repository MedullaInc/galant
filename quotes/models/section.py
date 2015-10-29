from gallant import models as g
from gallant import fields as gf
from django.db import models as m
from gallant.models import PolyUserModelManager


class Section(g.PolyUserModel):
    name = m.CharField(max_length=256, default="section")
    index = m.IntegerField(default=0)

    parent = m.ForeignKey('self', null=True, blank=True, related_name='sub_sections')

    def display_title(self):
        return self.name.replace('_', ' ').title()

    def get_languages(self):
        language_set = set()
        map(lambda l: language_set.add(l), self.title.keys())
        map(lambda l: language_set.add(l), self.text.keys())
        return language_set

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_section', 'View section'),
        )

    objects = PolyUserModelManager()


# guardian uses django's default add / change / delete perms and doesn't play well
# with polymorphic classes, so this manual approach is necessary for subclasses
def _get_section_perms(new_perms):
    return (
        new_perms,
        ('add_section', 'Can add section'),
        ('change_section', 'Can change section'),
        ('delete_section', 'Can delete section'),
        ('view_section', 'View section'),
    )


# Text section of Quote
class TextSection(Section):
    title = gf.ULCharField(blank=True)
    text = gf.ULTextField(blank=True)

    def __eq__(self, other):
        return self.name == other.name and \
               self.title == other.title and \
               self.text == other.text

    def __ne__(self, other):
        return not self.__eq__(other)

    class Meta:
        permissions = _get_section_perms(('view_textsection', 'View textsection'))

    objects = PolyUserModelManager()


class ServiceStatus(gf.ChoiceEnum):
    On_Hold = 0
    Pending_Assignment = 1
    Active = 2
    Overdue = 3
    Completed = 4


class ServiceSection(Section):
    service = g.UnsavedForeignKey(g.Service)
    status = m.CharField(max_length=2, choices=ServiceStatus.choices(), default=ServiceStatus.Pending_Assignment.value)

    class Meta:
        permissions = _get_section_perms(('view_servicesection', 'View servicesection'))

    objects = PolyUserModelManager()
