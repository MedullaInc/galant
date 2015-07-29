from django.conf import settings
from django.db import models as m
from gallant import models as g
from gallant import fields as gf


class Question(m.Model):
    """
    A brief has Questions that need to be answered.
    """
    question = gf.ULCharField()
    help_text = gf.ULCharField()
    index = m.IntegerField(default=0)


class QuestionTemplate(Question):
    """
    A Question Template to be reused on BriefTemplates
    """


class OpenQuestion(Question):
    """
    Open Question
    """
    is_long_answer = m.BooleanField(default=False)


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
    title = gf.ULCharField(max_length=255, help_text='Brief title.')
    status = m.CharField(max_length=2, choices=BriefStatus.choices(), default=BriefStatus.Draft.value)
    token = m.CharField(max_length=64, unique=True, null=True, help_text='For emailing URL')

    questions = m.ManyToManyField(Question)
    language = m.CharField(max_length=7, null=True, choices=settings.LANGUAGES,
                           help_text='Language of quote, or null for template.')


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
    answer = m.CharField(max_length=1000)
    brief = m.ForeignKey(Brief)
