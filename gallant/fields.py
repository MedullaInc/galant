from django.forms import widgets
from django.utils import translation
from django import forms
from jsonfield import JSONField
from enum import Enum
from django.conf import settings
from django.core.validators import RegexValidator
import inspect
import json


class ULTextDict(dict):
    def get_text(self, language=None):
        if language is None:
            language = translation.get_language()
            if language is None:
                language = settings.LANGUAGE_CODE

        if language in self:
            return self[language]
        else:
            return ''

    def set_text(self, text, language=None):
        if language is None:
            language = translation.get_language()

        self[language] = text

    def json(self):
        return json.dumps(self)

    def __unicode__(self):
        return self.json()

    def __str__(self):
        return self.json()


class ULTextDictArray(list):
    def json(self):
        return json.dumps(self)


def _ultext_to_python(value):
    d = ULTextDict()
    if isinstance(value, dict):
        d.update(value)
        return d

    try:
        d.update(json.loads(value))
    except (ValueError, TypeError):
        if value == '':
            return ''
        else:
            lang = translation.get_language()
            if lang is None:
                lang = settings.LANGUAGE_CODE
            d.update({lang: value})

    if value is None:
        return value

    return d


def _ultext_array_to_python(value):
    arr = ULTextDictArray()
    if isinstance(value, list):
        for v in value:
            arr.append(_ultext_to_python(v))
        return arr

    try:
        arr.extend(json.loads(value))
    except (ValueError, TypeError):
        return ULTextDictArray(value)
    return arr


class ULTextFormField(forms.fields.CharField):
    def to_python(self, value):
        if value in self.empty_values:
            return ULTextDict()
        else:
            return _ultext_to_python(value)

    def prepare_value(self, value):
        if isinstance(value, basestring):
            value = _ultext_to_python(value)
        if isinstance(value, ULTextDict):
            return value.get_text()
        return value


class ULTextArrayFormField(forms.fields.CharField):
    def to_python(self, value):
        if value in self.empty_values:
            return []
        else:
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
        if value in self.empty_values:
            return ULTextDict()
        else:
            return _ultext_to_python(value)


class ULTextArrayField(ULTextField):
    form_class = ULTextArrayFormField

    def pre_init(self, value, obj):
        value = super(JSONField, self).pre_init(value, obj)
        if value in self.empty_values:
            return []
        else:
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
        props.sort(key=lambda x: x[1].value)
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices


PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


ZIP_REGEX = RegexValidator(regex=r'^\d{5}(?:[-\s]\d{4})?$',
                             message="Zipcode must be entered in the format: '12345-1234' (first five digits required).")


class BootstrapRadioFieldRenderer(widgets.RadioFieldRenderer):
    def render(self):
        html = ''
        for val, text in self.choices:
            html += '''
            <div class="radio"><label>
                <input type="radio" name="%s" value="%d">%s
            </label></div>''' % (self.name, val, text)
        return html


class BootstrapCheckboxFieldRenderer(widgets.CheckboxFieldRenderer):
    def render(self):
        html = ''
        for val, text in self.choices:
            html += '''
            <div class="checkbox"><label>
                <input type="checkbox" name="%s" value="%d">%s
            </label></div>''' % (self.name, val, text)
        return html