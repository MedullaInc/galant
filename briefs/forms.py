import operator
from django import forms
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from briefs import models as b
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
        fields = ['question', 'index', 'choices']

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
    for question in brief.questions.all().select_subclasses():
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
