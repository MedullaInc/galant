from uuid import uuid4
from django.conf import settings
from django.db import models as m
from gallant import models as g
from gallant import fields as gf
from jsonfield.fields import JSONField
from model_utils.managers import InheritanceManager


class Question(m.Model):
    """
    A brief has Questions that need to be answered.
    """
    question = gf.ULCharField()
    help_text = gf.ULCharField()
    index = m.IntegerField(default=0)

    objects = InheritanceManager()


class LongAnswerQuestion(Question):
    """
    Long Answer Question
    """


class MultipleChoiceQuestion(Question):
    """
    Multiple Choice Question. We can set it up so the user has to select only one option or can optionally
    select more than one.
    The choices field is a list field where the options for the question are stored.
    """
    can_select_multiple = m.BooleanField(default=False)
    choices = gf.ULTextArrayField()


class ImageQuestion(MultipleChoiceQuestion):
    """
    ImageQuestion is a Multiple Choice Questions that allows the user to select among images.
    """
    # TODO: First finish MultipleChoiceQuestion then continue with ImageQuestions.


class Image(m.Model):
    """
    Image for ImageQuestions.
    """
    # TODO: We should analyze the best place for Image model to be located in.


class BriefStatus(gf.ChoiceEnum):
    Draft = 0
    Not_Sent = 1
    Sent = 2
    Viewed = 3
    Answered = 4
    Rejected = 5


class Brief(m.Model):
    """
    A questionnaire that will allow a user to know more about Client needs.
    There are three types of Briefs: [ClientBrief, ProjectBrief, ServiceBrief]
    """
    name = m.CharField(max_length=512, default='New Brief')
    title = gf.ULCharField(max_length=255, help_text='Brief title.')
    status = m.CharField(max_length=2, choices=BriefStatus.choices(), default=BriefStatus.Draft.value)
    token = m.UUIDField(default=uuid4, editable=False, unique=True)

    questions = m.ManyToManyField(Question)
    language = m.CharField(max_length=7, null=True, choices=settings.LANGUAGES,
                           help_text='Language of brief, or null for template.')

    def get_languages(self):
        language_set = set()
        language_set.update(self.title.keys())
        for q in list(self.questions.all()):
            if q is not None:
                language_set.update(q.question.keys())

        return language_set


class BriefTemplate(m.Model):
    """
    A Brief Template to be reused on other clients.
    """
    brief = m.ForeignKey(Brief)


class ClientBrief(Brief):
    """
    A Client Brief
    """
    client = m.ForeignKey(g.Client)


class ProjectBrief(Brief):
    """
    A Project Brief
    """
    project = m.ForeignKey(g.Project)


class ServiceBrief(Brief):
    """
    A Service Brief
    """
    service = m.ForeignKey(g.Service)


class Answer(m.Model):
    question = m.ForeignKey(Question)


class TextAnswer(Answer):
    answer = m.CharField(max_length=3000)


class MultipleChoiceAnswer(Answer):
    # a list of choice indexes corresponding to the quesion's choice list
    choices = JSONField()

    @property
    def answer(self):
        if type(self.question) is MultipleChoiceQuestion:
            if self.question.can_select_multiple:
                return [self.question.choices[c] for c in self.choices]
            else:
                return self.question.choices[self.choices[0]]


class BriefAnswers(m.Model):
    brief = m.ForeignKey(Brief)
    answers = m.ManyToManyField(Answer)
