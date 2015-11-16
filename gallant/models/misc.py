from django.db import models as m
from django.utils import timezone
from djmoney.models.fields import MoneyField
from gallant_user import UserModel, UserModelManager


class UnsavedForeignKey(m.ForeignKey):
    # A ForeignKey which can point to an unsaved object
    allow_unsaved_instance_assignment = True


class Note(UserModel):
    text = m.TextField(help_text='User comment / note.')
    created = m.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s: %s' % (self.user.email, self.text)

    class Meta:
        permissions = (
            ('view_note', 'View note'),
        )

    objects = UserModelManager()


class Payment(UserModel):
    submitted_on = m.DateTimeField(default=timezone.now)
    amount = MoneyField(max_digits=16, decimal_places=2)
    note = m.ForeignKey(Note, null=True, blank=True)

    def __unicode__(self):
        return '%s: %s' % (self.submitted_on, self.amount)
