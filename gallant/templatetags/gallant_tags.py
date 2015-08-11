from analytical.templatetags.clicky import ClickyNode
from analytical.templatetags.crazy_egg import CrazyEggNode
from django import template

register = template.Library()


@register.assignment_tag(takes_context=True)
def objects_for(context, queryset, permission):
    """ Returns objects user has permission to access
    """
    return queryset.all_for(context.request.user, permission)


@register.simple_tag(takes_context=True)
def analytics(context):
    """ Returns analytics code
    """
    return '%s\n%s' % (ClickyNode().render(context), CrazyEggNode().render(context))
