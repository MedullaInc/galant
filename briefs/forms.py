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

    def clean(self):
        cleaned_data = super(BriefForm, self).clean()
        return cleaned_data


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

    def save(self, commit=True):
        if self.prefix:
            idx = re.match('-question-(\d+)', self.prefix).group(1) or 0
            self.instance.index = idx
        return super(QuestionForm, self).save(commit)


def questions_from_post(data):
    qf = []
    for key, value in sorted(data.items(), key=operator.itemgetter(1)):
        m = re.match('(-question-\d+)-question', key)
        if m is not None:
            qf.append(QuestionForm(data, prefix=m.group(1)))

    return qf
