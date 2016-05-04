from uuid import uuid4
from django.conf import settings
from django.db import models as m
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from gallant import models as g
from gallant.enums import ClientStatus
from gallant.models import UserModelManager
from quotes import models as q
from gallant import fields as gf
from gallant import utils
import question


class BriefStatus(gf.ChoiceEnum):
    Draft = 0
    Not_Sent = 1
    Sent = 2
    Viewed = 3
    Answered = 4
    Rejected = 5


class Brief(g.UserModel):
    """
    A questionnaire that will allow a user to know more about Client needs.
    """
    name = m.CharField(max_length=512, default='New Brief')
    title = gf.ULCharField(max_length=255, help_text='Brief title.')
    greeting = gf.ULCharField(max_length=2000, help_text='Greeting text.', blank=True)
    status = m.CharField(max_length=2, choices=BriefStatus.choices(), default=BriefStatus.Draft.value)
    token = m.UUIDField(default=uuid4, editable=False, unique=True)

    modified = m.DateTimeField(auto_now=True)

    questions = m.ManyToManyField(question.Question)
    language = m.CharField(max_length=7, null=True, choices=settings.LANGUAGES,
                           help_text='Language of brief, or null for template.')

    client = m.ForeignKey(g.Client, null=True)
    quote = m.ForeignKey(q.Quote, null=True)

    def get_languages(self):
        language_set = set()
        language_set.update(self.title.keys())
        for q in list(self.questions.all_for(self.user)):
            if q is not None:
                language_set.update(q.question.keys())

        return language_set

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_brief', 'View brief'),
        )

    objects = UserModelManager()

    def soft_delete(self, deleted_by_parent=False):
        with transaction.atomic():
            for question in self.questions.all_for(self.user, 'change'):
                question.soft_delete(deleted_by_parent=True)

            super(Brief, self).soft_delete(deleted_by_parent)


class BriefTemplate(g.UserModel):
    """
    A Brief Template to be reused on other clients.
    """
    brief = m.ForeignKey(Brief)

    def language_list(self):
        return [(c, utils.LANG_DICT[c]) for c in self.brief.get_languages() if c in utils.LANG_DICT]

    class Meta:
        permissions = (
            ('view_brieftemplate', 'View brieftemplate'),
        )

    objects = UserModelManager()

    def soft_delete(self, deleted_by_parent=False):
        with transaction.atomic():
            if self.brief.client_id is None:
                self.brief.soft_delete(deleted_by_parent=True)

            super(BriefTemplate, self).soft_delete(deleted_by_parent)


class BriefAnswers(g.UserModel):
    brief = m.ForeignKey(Brief)
    answers = m.ManyToManyField(question.Answer)

    created = m.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ('view_briefanswers', 'View briefanswers'),
        )

    objects = UserModelManager()


@receiver(post_save, sender=Brief)
def client_brief_answered(sender, instance, **kwargs):
    if instance.client_id:
        client = instance.client
        cstat = int(client.status)
        bstat = int(instance.status)

        if cstat < ClientStatus.Quoted.value and bstat >= BriefStatus.Answered.value:
            client.alert = 'Brief Answered'
            client.save()
