from django.db import models as m
from gallant_user import UserModel, UserModelManager


class UnsavedForeignKey(m.ForeignKey):
    # A ForeignKey which can point to an unsaved object
    allow_unsaved_instance_assignment = True


class Note(UserModel):
    text = m.TextField(help_text='User comment / note.')
    created = m.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ('view_note', 'View note'),
        )

    objects = UserModelManager()
