from django import template
from django.template.loader import get_template
import re

register = template.Library()


@register.simple_tag
def question_form_javascript():
    """Returns a javascript string to be used with gallant.js's format function
    """
    t = get_template('briefs/question_form.html')
    ret = t.render({'prefix': '{0}', 'extra_class': 'dynamic_section'})
    return re.sub(r'(.*)', r"'\1' +", ret) + "''"


@register.simple_tag
def multiquestion_form_javascript():
    """Returns a javascript string to be used with gallant.js's format function
    """
    t = get_template('briefs/multiquestion_form.html')
    ret = t.render({'prefix': '{0}', 'extra_class': 'dynamic_section'})
    return re.sub(r'(.*)', r"'\1' +", ret) + "''"
