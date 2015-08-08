from django import template
from django.template.loader import get_template
from gallant import models as g
import re

register = template.Library()


@register.assignment_tag(takes_context=True)
def objects_for(context, queryset, permission):
    """ Returns objects user has permission to access
    """
    return queryset.all_for(context.request.user, permission)
