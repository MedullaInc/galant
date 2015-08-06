from uuid import uuid4
from django.conf import settings
from django.db import models as m
from gallant import models as g
from gallant.models import PolyUserModelManager, UserModelManager
from quotes import models as q
from gallant import fields as gf
from jsonfield.fields import JSONField
from gallant import utils


class Question(g.PolyUserModel):
    """
    A brief has Questions that need to be answered.
    """
    question = gf.ULCharField()
    help_text = gf.ULCharField()
    index = m.IntegerField(default=0)

    class Meta:
        permissions = (
            ('view_question', 'View question'),
        )

    objects = PolyUserModelManager()


class TextQuestion(Question):
    """
    Long Answer Question
    """
    is_long_answer = m.BooleanField(default=False)

    class Meta:
        permissions = (
            ('view_textquestion', 'View textquestion'),
        )

    objects = PolyUserModelManager()


class MultipleChoiceQuestion(Question):
    """
    Multiple Choice Question. We can set it up so the user has to select only one option or can optionally
    select more than one.
    The choices field is a list field where the options for the question are stored.
    """
    can_select_multiple = m.BooleanField(default=False)
    choices = gf.ULTextArrayField()

    class Meta:
        permissions = (
            ('view_multiplechoicequestion', 'View multiplechoicequestion'),
        )

    objects = PolyUserModelManager()


class ImageQuestion(MultipleChoiceQuestion):
    """
    ImageQuestion is a Multiple Choice Questions that allows the user to select among images.
    """
    # TODO: First finish MultipleChoiceQuestion then continue with ImageQuestions.

    class Meta:
        permissions = (
            ('view_imagequestion', 'View imagequestion'),
        )

    objects = PolyUserModelManager()


class Image(g.UserModel):
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


class Brief(g.UserModel):
    """
    A questionnaire that will allow a user to know more about Client needs.
    """
    name = m.CharField(max_length=512, default='New Brief')
    title = gf.ULCharField(max_length=255, help_text='Brief title.')
    status = m.CharField(max_length=2, choices=BriefStatus.choices(), default=BriefStatus.Draft.value)
    token = m.UUIDField(default=uuid4, editable=False, unique=True)

    modified = m.DateTimeField(auto_now=True)

    questions = m.ManyToManyField(Question)
    language = m.CharField(max_length=7, null=True, choices=settings.LANGUAGES,
                           help_text='Language of brief, or null for template.')

    client = m.ForeignKey(g.Client, null=True)
    quote = m.ForeignKey(q.Quote, null=True)

    def get_languages(self):
        language_set = set()
        language_set.update(self.title.keys())
        for q in list(self.questions.all()):
            if q is not None:
                language_set.update(q.question.keys())

        return language_set

    class Meta:
        permissions = (
            ('view_brief', 'View brief'),
        )

    objects = UserModelManager()


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


class Answer(g.PolyUserModel):
    question = m.ForeignKey(Question)

    class Meta:
        permissions = (
            ('view_answer', 'View answer'),
        )

    objects = PolyUserModelManager()


class TextAnswer(Answer):
    answer = m.CharField(max_length=3000)

    class Meta:
        permissions = (
            ('view_textanswer', 'View textanswer'),
        )

    objects = PolyUserModelManager()


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

    class Meta:
        permissions = (
            ('view_multiplechoiceanswer', 'View multiplechoiceanswer'),
        )

    objects = PolyUserModelManager()


class BriefAnswers(g.UserModel):
    brief = m.ForeignKey(Brief)
    answers = m.ManyToManyField(Answer)

    created = m.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ('view_briefanswers', 'View briefanswers'),
        )

    objects = UserModelManager()