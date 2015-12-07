from django import template
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from gallant import models as g
import re

register = template.Library()


@register.simple_tag
def section_form_javascript():
    """Returns a javascript string to be used with gallant.js's format function
    """
    t = get_template('quotes/section_form.html')
    ret = t.render({'prefix': '{0}', 'name': '{1}', 'label': '{2}', 'extra_class': 'dynamic_section'})
    return mark_safe(re.sub(r'(.*)', r"'\1' +", ret) + "''")

@register.simple_tag
def service_form_javascript():
    """Returns a javascript string to be used with gallant.js's format function
    """
    t = get_template('quotes/service_section_form.html')
    ret = t.render({'prefix': '{0}', 'name': '{1}', 'label': '{2}', 'extra_class': 'dynamic_section',
                    'type_choices': g.ServiceType.choices()})
    return mark_safe(re.sub(r'(.*)', r"'\1' +", ret) + "''")