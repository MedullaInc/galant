import operator
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django import forms
from briefs import models as b
from gallant import forms as gf
from gallant import fields as gfields
import re


class BriefForm(gf.UserModelForm):
    class Meta:
        model = b.Brief
        fields = ['title']


class BriefTemplateForm(BriefForm):
    class Meta:
        model = b.Brief
        fields = ['name']


class QuestionForm(gf.UserModelForm):
    class Meta:
        model = b.TextQuestion
        fields = ['question', 'index']

    def __init__(self, user, data=None, prefix=None, *args, **kwargs):
        # see if update or create
        prefix = prefix or ''
        data = data or {}
        if prefix + '-id' in data:
            question = get_object_or_404(b.TextQuestion, pk=data[prefix + '-id'])
            super(QuestionForm, self).__init__(user, data=data, prefix=prefix, instance=question, *args, **kwargs)
        else:
            super(QuestionForm, self).__init__(user, data=data, prefix=prefix, *args, **kwargs)

    def as_table(self):
        t = get_template('briefs/question_form.html')
        if not self.instance:
            self.instance = self.save(commit=False)

        context = {'prefix': self.prefix + '-', 'question': self.instance, 'extra_class': 'dynamic_section'}
        return t.render(context)


class MultiQuestionForm(gf.UserModelForm):
    class Meta:
        model = b.MultipleChoiceQuestion
        fields = ['question', 'index', 'choices', 'can_select_multiple']

    def __init__(self, user, data=None, prefix=None, *args, **kwargs):
        # see if update or create
        prefix = prefix or ''
        data = data or {}
        if prefix + '-id' in data:
            question = get_object_or_404(b.MultipleChoiceQuestion, pk=data[prefix + '-id'])
            super(MultiQuestionForm, self).__init__(user, data=data, prefix=prefix, instance=question, *args, **kwargs)
        else:
            super(MultiQuestionForm, self).__init__(user, data=data, prefix=prefix, *args, **kwargs)

    def as_table(self):
        t = get_template('briefs/multiquestion_form.html')
        if not self.instance:
            self.instance = self.save(commit=False)

        context = {'prefix': self.prefix + '-', 'question': self.instance, 'extra_class': 'dynamic_section'}
        return t.render(context)


class BriefAnswersForm(gf.UserModelForm):
    class Meta:
        model = b.BriefAnswers
        fields = []

    def answer_forms(self, data=None):
        af = []
        for q in self.instance.brief.questions.all().order_by('index'):
            if type(q) is b.TextQuestion:
                FormType = AnswerForm
            elif type(q) is b.MultipleChoiceQuestion:
                FormType = MultipleChoiceAnswerForm
            elif type(q) is b.LongAnswerQuestion:
                FormType = LongAnswerForm

            af.append(FormType(self.instance.brief.user, q, data))

        return af

    def save(self):
        # for saving from a POST from non-logged-in client, we assign the object's user to be
        # the same as the relevant brief.
        self.user = self.instance.brief.user
        return super(BriefAnswersForm, self).save()


def question_forms_request(request):
    qf = []
    for key, value in sorted(request.POST.items(), key=operator.itemgetter(1)):
        m = re.match('(-question-\d+)-question', key)
        if m is not None:
            qf.append(QuestionForm(request.user, request.POST, prefix=m.group(1)))
        else:
            m = re.match('(-multiquestion-\d+)-question', key)
            if m is not None:
                qf.append(MultiQuestionForm(request.user, request.POST, prefix=m.group(1)))

    return qf


def question_forms_brief(brief, clear_pk=False):
    qf = []
    user = brief.user
    for question in brief.questions.all().order_by('index'):
        if clear_pk:
            question.pk = None
        if type(question) is b.MultipleChoiceQuestion:
            qf.append(MultiQuestionForm(user=user, instance=question, prefix='-multiquestion-%d' % question.index))
        elif type(question) is b.TextQuestion:
            qf.append(QuestionForm(user=user, instance=question, prefix='-question-%d' % question.index))

    return qf


def create_brief(form, question_forms):
    obj = form.save()
    obj.questions.clear()
    for q in question_forms:
        obj.questions.add(q.save())

    return obj


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
            self.base_fields['answer'].widget = forms.RadioSelect(attrs={'class': 'form-control'},
                                                                  renderer=gfields.BootstrapRadioFieldRenderer)

        self.base_fields['answer'].choices = enumerate(c.get_text() for c in question.choices)
        super(MultipleChoiceAnswerForm, self).__init__(prefix='-answer-%d' % question.id, *args, **kwargs)

    def save(self):
        return b.MultipleChoiceAnswer.objects.create(user=self.user, choices=self.cleaned_data['answer'],
                                                     question=self.question)
