from analytical.templatetags.clicky import ClickyNode
from analytical.templatetags.crazy_egg import CrazyEggNode
from django import template

register = template.Library()


@register.assignment_tag(takes_context=True)
def objects_for(context, queryset, permission='view'):
    """ Returns objects user has permission to access
    """
    if queryset:
        return queryset.all_for(context.request.user, permission)
    else:
        return None


@register.simple_tag(takes_context=True)
def analytics(context):
    """ Returns analytics code
    """
    return '%s\n%s' % (ClickyNode().render(context), CrazyEggNode().render(context))


@register.simple_tag()
def custom_breadcrumb(request, breadcrumb_title):
    request.breadcrumbs((breadcrumb_title), request.path_info)
    return ''