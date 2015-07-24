from django import template
from django.template.loader import get_template
import re

register = template.Library()


@register.simple_tag
def section_form_javascript():
    """Returns a javascript string to be used with gallant.js's format function
    """

    t = get_template('quotes/section.html')
    ret = t.render({'name': '{0}', 'label': '{1'})
    return re.sub(r'(.*)', r"'\1' +", ret) + "''"