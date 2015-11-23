from analytical.templatetags.clicky import ClickyNode
from analytical.templatetags.crazy_egg import CrazyEggNode
from django import template
from gallant import models as g

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


@register.simple_tag()
def active(request, pattern):
    path = request.path
    if path == pattern:
        return 'active'
    else:
        return ''


@register.simple_tag()
def get_project_services(request, project, status=None):
    services = []

    for quote in project.quote_set.all_for(request.user):
        if status is None:
            for service in quote.service_sections.all_for(request.user):
                services.append(service)
        else:
            for service in quote.service_sections.all_for(request.user).filter(status=status):
                services.append(service)

    return services

@register.simple_tag()
def get_project_services_count(request, project, status=None):
    services = []

    for quote in project.quote_set.all_for(request.user):
        if status is None:
            for service in quote.service_sections.all_for(request.user):
                services.append(service)
        else:
            for service in quote.service_sections.all_for(request.user).filter(status=status):
                services.append(service)

    return len(services)

@register.simple_tag()
def get_client_services_count(request, client, status=None):
    projects = g.Project.objects.all_for(request.user).filter(quote__client=client)
    services = []

    for project in projects:
        for quote in project.quote_set.all_for(request.user):
            if status is None:
                for service in quote.service_sections.all_for(request.user):
                    services.append(service)
            else:
                for service in quote.service_sections.all_for(request.user).filter(status=status):
                    services.append(service)

    return len(services)
