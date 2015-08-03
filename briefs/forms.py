import operator
from django import forms
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from briefs import models as b
from gallant import fields as gf
import re


class BriefForm(forms.ModelForm):
    class Meta:
        model = b.Brief
        fields = ['title', 'status']


class BriefTemplateForm(BriefForm):
    class Meta:
        model = b.Brief
        fields = ['name']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = b.Question
        fields = ['question', 'index']

    def __init__(self, data=None, prefix=None, *args, **kwargs):
        # see if update or create
        prefix = prefix or ''
        data = data or {}
        if prefix + '-id' in data:
            question = get_object_or_404(b.Question, pk=data[prefix + '-id'])
            super(QuestionForm, self).__init__(data=data, prefix=prefix, instance=question, *args, **kwargs)
        else:
            super(QuestionForm, self).__init__(data=data, prefix=prefix, *args, **kwargs)

    def as_table(self):
        t = get_template('briefs/question_form.html')
        if not self.instance:
            self.instance = self.save(commit=False)

        context = {'prefix': self.prefix + '-', 'question': self.instance, 'extra_class': 'dynamic_section'}
        return t.render(context)


class MultiQuestionForm(forms.ModelForm):
    class Meta:
        model = b.MultipleChoiceQuestion
        fields = ['question', 'index', 'choices', 'can_select_multiple']

    def __init__(self, data=None, prefix=None, *args, **kwargs):
        # see if update or create
        prefix = prefix or ''
        data = data or {}
        if prefix + '-id' in data:
            question = get_object_or_404(b.MultipleChoiceQuestion, pk=data[prefix + '-id'])
            super(MultiQuestionForm, self).__init__(data=data, prefix=prefix, instance=question, *args, **kwargs)
        else:
            super(MultiQuestionForm, self).__init__(data=data, prefix=prefix, *args, **kwargs)

    def as_table(self):
        t = get_template('briefs/multiquestion_form.html')
        if not self.instance:
            self.instance = self.save(commit=False)

        context = {'prefix': self.prefix + '-', 'question': self.instance, 'extra_class': 'dynamic_section'}
        return t.render(context)


class BriefAnswersForm(forms.ModelForm):
    class Meta:
        model = b.BriefAnswers
        fields = []

    def answer_forms(self, data=None):
        af = []
        for q in self.instance.brief.questions.all().order_by('index'):
            if type(q) is b.Question:
                FormType = AnswerForm
            elif type(q) is b.MultipleChoiceQuestion:
                FormType = MultipleChoiceAnswerForm
            elif type(q) is b.LongAnswerQuestion:
                FormType = LongAnswerForm

            af.append(FormType(question=q, data=data))

        return af


def question_forms_post(data):
    qf = []
    for key, value in sorted(data.items(), key=operator.itemgetter(1)):
        m = re.match('(-question-\d+)-question', key)
        if m is not None:
            qf.append(QuestionForm(data, prefix=m.group(1)))
        else:
            m = re.match('(-multiquestion-\d+)-question', key)
            if m is not None:
                qf.append(MultiQuestionForm(data, prefix=m.group(1)))

    return qf


def question_forms_brief(brief, clear_pk=False):
    qf = []
    for question in brief.questions.all().order_by('index'):
        if clear_pk:
            question.pk = None
        if type(question) is b.MultipleChoiceQuestion:
            qf.append(MultiQuestionForm(instance=question, prefix='-multiquestion-%d' % question.index))
        elif type(question) is b.Question:
            qf.append(QuestionForm(instance=question, prefix='-question-%d' % question.index))

    return qf


def create_brief(form, question_forms):
    obj = form.save()
    obj.questions.clear()
    for q in question_forms:
        obj.questions.add(q.save())

    return obj


class AnswerForm(forms.Form):
    answer = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, question=None, *args, **kwargs):
        self.question = question
        super(AnswerForm, self).__init__(prefix='-answer-%d' % question.id, *args, **kwargs)

    def save(self):
        return b.TextAnswer.objects.create(answer=self.cleaned_data['answer'], question=self.question)


class LongAnswerForm(AnswerForm):
    answer = forms.CharField(label='',
                             help_text='%d charater limit' %
                                       b.TextAnswer._meta.get_field('answer').max_length,
                             widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))


class MultipleChoiceAnswerForm(forms.Form):
    answer = forms.ChoiceField(label='')

    def __init__(self, question=None, *args, **kwargs):
        self.question = question
        if type(question) is not b.MultipleChoiceQuestion:
            raise RuntimeError('Attempting to use MultipleChoiceAnswerForm with non-multiple-choice question.')

        if question.can_select_multiple:
            self.base_fields['answer'] = forms.MultipleChoiceField(label='')
            self.base_fields['answer'].widget = forms.CheckboxSelectMultiple(attrs={'class': 'form-control'},
                                                                             renderer=gf.BootstrapCheckboxFieldRenderer)
        else:
            self.base_fields['answer'].widget = forms.RadioSelect(attrs={'class': 'form-control'},
                                                                  renderer=gf.BootstrapRadioFieldRenderer)

        self.base_fields['answer'].choices = enumerate(c.get_text() for c in question.choices)
        super(MultipleChoiceAnswerForm, self).__init__(prefix='-answer-%d' % question.id, *args, **kwargs)

    def save(self):
        return b.MultipleChoiceAnswer.objects.create(choices=self.cleaned_data['answer'], question=self.question)
