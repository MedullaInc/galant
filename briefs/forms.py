from django import forms
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.utils import six
from briefs import models as b
from django.utils.encoding import smart_text
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
        fields = ['question']

    def __init__(self, data=None, prefix=None, *args, **kwargs):
        # see if update or create
        prefix = prefix or ''
        data = data or {}
        if prefix + '-id' in data:
            section = get_object_or_404(q.Section, pk=data[prefix + '-id'])
            super(QuestionForm, self).__init__(data=data, prefix=prefix, instance=section, *args, **kwargs)
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

