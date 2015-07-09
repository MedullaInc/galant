from django.db import models
from django.db.models import *
from gallant import models as g
from gallant import fields as gf


class Brief(models.Model):
    """
    A questionnaire that will allow a user to know more about Client needs.
    There are three types of Briefs: [ClientBrief, ProjectBrief, ServiceBrief]
    """
    title = TextField(help_text='Brief title.')


class BriefTemplate(Brief):
    """
    A Brief Template to be reused on other clients.
    """


class ClientBrief(Brief):
    """
    A Client Brief
    """
    client = ForeignKey(g.Client)


class ProjectBrief(Brief):
    """
    A Project Brief
    """
    project = ForeignKey(g.Project)


class ServiceBrief(Brief):
    """
    A Service Brief
    """
    service = ForeignKey(g.Service)


class Question(models.Model):
    """
    A brief has Questions that need to be answered.
    """
    question = CharField(max_length=255)
    help_text = CharField(max_length=255)


class QuestionTemplate(Question):
    """
    A Question Template to be reused on BriefTemplates
    """


class OpenQuestion(Question):
    """
    Open Question
    """
    is_long_answer = BooleanField(default=False)


class MultipleChoiceQuestion(Question):
    """
    Multiple Choice Question. We can set it up so the user has to select only one option or can optionally
    select more than one.
    The choices field is a list field where the options for the question are stored.
    """
    can_select_multiple = BooleanField(default=False)
    choices = gf.ULTextArrayField()


class ImageQuestion(MultipleChoiceQuestion):
    """
    ImageQuestion is a Multiple Choice Questions that allows the user to select among images.
    """
    # TODO: First finish MultipleChoiceQuestion then continue with ImageQuestions.


class Image(models.Model):
    """
    Image for ImageQuestions.
    """
    # TODO: We should analyze the best place for Image model to be located in.


class Answer(models.Model):
    answer = CharField(max_length=1000)
    brief = ForeignKey(Brief)