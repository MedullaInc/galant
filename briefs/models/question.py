from django.db import models as m
from gallant import models as g
from gallant.models import PolyUserModelManager, UserModelManager
from gallant import fields as gf
from jsonfield.fields import JSONField


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


# guardian uses django's default add / change / delete perms and doesn't play well
# with polymorphic classes, so this manual approach is necessary for subclasses
def _get_question_perms(new_perms):
    return (
        new_perms,
        ('add_question', 'Can add question'),
        ('change_question', 'Can change question'),
        ('delete_question', 'Can delete question'),
        ('view_question', 'View question'),
    )


class TextQuestion(Question):
    """
    Long Answer Question
    """
    is_long_answer = m.BooleanField(default=False)

    class Meta:
        permissions = _get_question_perms(('view_textquestion', 'View textquestion'))

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
        permissions = _get_question_perms(('view_multiplechoicequestion', 'View multiplechoicequestion'))

    objects = PolyUserModelManager()


class ImageQuestion(MultipleChoiceQuestion):
    """
    ImageQuestion is a Multiple Choice Questions that allows the user to select among images.
    """
    # TODO: First finish MultipleChoiceQuestion then continue with ImageQuestions.

    class Meta:
        permissions = _get_question_perms(('view_imagequestion', 'View imagequestion'))

    objects = PolyUserModelManager()


class Image(g.UserModel):
    """
    Image for ImageQuestions.
    """
    # TODO: We should analyze the best place for Image model to be located in.


class Answer(g.PolyUserModel):
    question = m.ForeignKey(Question)

    class Meta:
        permissions = (
            ('view_answer', 'View answer'),
        )

    objects = PolyUserModelManager()


# see _get_question_perms()
def _get_answer_perms(new_perms):
    return (
        new_perms,
        ('add_answer', 'Can add answer'),
        ('change_answer', 'Can change answer'),
        ('delete_answer', 'Can delete answer'),
        ('view_answer', 'View answer'),
    )


class TextAnswer(Answer):
    answer = m.CharField(max_length=3000)
    class Meta:
        permissions = _get_answer_perms(('view_textanswer', 'View textanswer'))

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
                return [self.question.choices[self.choices[0]]]

    class Meta:
        permissions = _get_answer_perms(('view_multiplechoiceanswer', 'View multiplechoiceanswer'))

    objects = PolyUserModelManager()

