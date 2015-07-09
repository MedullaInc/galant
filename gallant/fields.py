from django.utils import translation
from django import forms
from django.core.exceptions import FieldError
from jsonfield import JSONField
from enum import Enum
import inspect


class ULTextDict(dict):
    def get_text(self, language=None):
        if language is None:
            language = translation.get_language()

        if language in self:
            return self[language]
        else:
            return ''

    def set_text(self, text, language=None):
        if language is None:
            language = translation.get_language()

        self[language] = text


def _ultext_to_python(value):
    if isinstance(value, dict):
        d = ULTextDict()
        d.update(value)
        return d
    elif isinstance(value, basestring):
        d = ULTextDict()
        d.update({translation.get_language(): value})
        return d

    if value is None:
        return value

    raise FieldError("ULTextField requires a dictionary.")


def _ultext_array_to_python(value):
    arr = []
    for v in value:
        arr.append(_ultext_to_python(v))
    return arr


class ULTextFormField(forms.fields.CharField):
    def to_python(self, value):
        return _ultext_to_python(value)


class ULTextArrayFormField(forms.fields.CharField):
    def to_python(self, value):
        return _ultext_array_to_python(value)


class ULTextField(JSONField):
    form_class = ULTextFormField

    def formfield(self, **kwargs):
        field = super(JSONField, self).formfield(**kwargs)
        field.widget = forms.Textarea(attrs={'rows': 3})
        field.help_text = ''
        return field

    def pre_init(self, value, obj):
        value = super(JSONField, self).pre_init(value, obj)
        return _ultext_to_python(value)


class ULTextArrayField(ULTextField):
    form_class = ULTextArrayFormField

    def pre_init(self, value, obj):
        value = super(JSONField, self).pre_init(value, obj)
        return _ultext_array_to_python(value)


class ULCharField(ULTextField):
    def formfield(self, **kwargs):
        field = super(ULTextField, self).formfield(**kwargs)
        field.widget = forms.TextInput()
        field.help_text = ''
        return field


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not (inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not (m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices