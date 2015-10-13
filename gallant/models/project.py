from django.db import models as m
from django.db import transaction
from gallant import fields as gf
from gallant_user import UserModel, UserModelManager
from misc import Note


class ProjectStatus(gf.ChoiceEnum):
    On_Hold = 0
    Pending_Assignment = 1
    Active = 2
    Overdue = 3
    Completed = 4


class Project(UserModel):
    name = m.CharField(max_length=255)
    status = m.CharField(max_length=2, choices=ProjectStatus.choices(), default=ProjectStatus.Pending_Assignment.value)

    notes = m.ManyToManyField(Note)

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_project', 'View project'),
        )

    objects = UserModelManager()

    def soft_delete(self, deleted_by_parent=False):
        with transaction.atomic():
            for note in self.notes.all_for(self.user, 'change'):
                note.soft_delete(deleted_by_parent=True)

            super(Project, self).soft_delete(deleted_by_parent)
