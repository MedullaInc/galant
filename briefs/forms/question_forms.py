import operator
from django.template.loader import get_template
from django import forms
from briefs import models as b
from gallant import forms as gf
from gallant import fields as gfields
from gallant.utils import get_one_or_404
import re


class BriefAnswersForm(gf.UserModelForm):
    class Meta:
        model = b.BriefAnswers
        fields = []

    def answer_forms(self, data=None):
        af = []
        for q in self.instance.brief.questions\
                     .all_for(self.instance.brief.user)\
                     .order_by('index'):
            if type(q) is b.TextQuestion:
                if q.is_long_answer:
                    FormType = LongAnswerForm
                else:
                    FormType = AnswerForm
            elif type(q) is b.MultipleChoiceQuestion:
                FormType = MultipleChoiceAnswerForm

            af.append(FormType(self.instance.brief.user, q, data))

        return af

    def save(self):
        # for saving from a POST from non-logged-in client, we assign the object's user to be
        # the same as the relevant brief.
        self.user = self.instance.brief.user
        return super(BriefAnswersForm, self).save()


class AnswerForm(forms.Form):
    answer = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, user, question=None, *args, **kwargs):
        self.question = question
        self.user = user
        super(AnswerForm, self).__init__(prefix='-answer-%d' % question.id, *args, **kwargs)

    def save(self):
        return b.TextAnswer.objects.create(user=self.user, answer=self.cleaned_data['answer'],
                                           question=self.question)


class LongAnswerForm(AnswerForm):
    answer = forms.CharField(label='',
                             help_text='%d charater limit' %
                                       b.TextAnswer._meta.get_field('answer').max_length,
                             widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))


class MultipleChoiceAnswerForm(forms.Form):
    answer = forms.ChoiceField(label='')

    def __init__(self, user, question=None, *args, **kwargs):
        self.question = question
        self.user = user
        if type(question) is not b.MultipleChoiceQuestion:
            raise RuntimeError('Attempting to use MultipleChoiceAnswerForm with non-multiple-choice question.')

        if question.can_select_multiple:
            self.base_fields['answer'] = forms.MultipleChoiceField(label='')
            self.base_fields['answer'].widget = forms.CheckboxSelectMultiple(attrs={'class': 'form-control'},
                                                                             renderer=gfields.BootstrapCheckboxFieldRenderer)
        else:
            self.base_fields['answer'] = forms.ChoiceField(label='')
            self.base_fields['answer'].widget = forms.RadioSelect(attrs={'class': 'form-control'},
                                                                  renderer=gfields.BootstrapRadioFieldRenderer)

        self.base_fields['answer'].choices = enumerate(c.get_text() for c in question.choices)
        super(MultipleChoiceAnswerForm, self).__init__(prefix='-answer-%d' % question.id, *args, **kwargs)

    def save(self):
        return b.MultipleChoiceAnswer.objects.create(user=self.user, choices=self.cleaned_data['answer'],
                                                     question=self.question)
