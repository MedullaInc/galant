from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from briefs import models as b, serializers
from django.http.response import JsonResponse
from django.template.response import TemplateResponse
from gallant import models as g
from gallant.views.user import UserModelViewSet
from quotes import models as q
from django.views.generic import View
from gallant.utils import get_one_or_404, query_url, get_site_from_host, get_field_choices
from django.utils.translation import ugettext_lazy as _


def _update_from_query(request, context):
    initial = {}
    quote_id = request.GET.get('quote_id', None)
    project_id = request.GET.get('project_id', None)
    client_id = request.GET.get('client_id', None)

    if quote_id:
        quote = get_one_or_404(request.user, 'view_quote', q.Quote, pk=quote_id)
        initial = {'client': quote.client_id, 'quote': quote.id}
        context.update({'quote': quote, 'client': quote.client})
        request.breadcrumbs([(_('Quotes'), reverse('quotes')),
                             (_('Quote: %s') + quote.name, reverse('quote_detail', args=[quote.id]))])
    elif project_id:
        project = get_one_or_404(request.user, 'view_project', g.Project, pk=project_id)
        quote = project.quote_set.all_for(request.user)[0]
        initial = {'client': quote.client_id, 'quote': quote.id or None}
        context.update({'project': project, 'quote': quote, 'client': quote.client})
        request.breadcrumbs([(_('Projects'), reverse('projects')),
                             (_('Project:') + project.name, reverse('project_detail', args=[project.id]))])
    elif client_id:
        client = get_one_or_404(request.user, 'view_client', g.Client, pk=client_id)
        initial = {'client': client.id}
        context.update({'client': client})
        request.breadcrumbs([(_('Clients'), reverse('clients')),
                             (client.name, reverse('client_detail', args=[client.id]))])
        request.breadcrumbs(_('Briefs'), reverse('briefs') + query_url(request))
    else:
        request.breadcrumbs()

    return initial


class BriefList(View):
    def get(self, request, **kwargs):
        context = {'template_list': b.BriefTemplate.objects.all_for(request.user)}

        self.request.breadcrumbs([(_('Briefs'), reverse('briefs'))])

        _update_from_query(request, context)

        if 'client' in context:
            briefs = context['client'].brief_set.all_for(request.user)
            context.update({'object_list': briefs, 'title': 'Briefs'})
        else:
            context.update({'object_list': b.Brief.objects
                           .all_for(request.user)
                           .filter(client__isnull=False), 'title': 'Briefs'})

        return TemplateResponse(request=request,
                                template="briefs/brief_list.html",
                                context=context)


def _send_brief_email(email, from_name, link, site):
    message = '%s has sent you a %s questionnaire.\n\n Click this link to answer:\n %s' % \
              (from_name, site, link)
    send_mail('Client Questionnaire', message,
              '%s via %s <%s>' % (from_name, site, settings.EMAIL_HOST_USER),
              [email], fail_silently=False)


def brief_fields_json(request):
    return JsonResponse(get_field_choices(b.Brief), safe=False)


class BriefDetail(View):
    def get(self, request, **kwargs):
        context = {'title': 'Brief Detail'}
        _update_from_query(request, context)

        if 'pk' in kwargs:
            brief = get_one_or_404(request.user, 'view_brief', b.Brief, id=kwargs['pk'])

            answers_q = brief.briefanswers_set.all_for(request.user)
            if answers_q.count() > 0:
                brief_answers = answers_q.last()
                context.update({'answer_set': brief_answers,
                                'answers': brief_answers.answers
                               .all_for(request.user)
                               .order_by('question__index')})

            context.update({'object': brief,
                            'questions': brief.questions
                           .all_for(request.user) \
                           .order_by('index')})
            request.breadcrumbs(_('Brief: ') + brief.name, request.path_info + query_url(request))
        else:
            template_id = request.GET.get('template_id', None)
            if template_id:
                context.update({'template_id': template_id})
            request.breadcrumbs(_('Add'), request.path_info + query_url(request))


        return TemplateResponse(request=request,
                                template="briefs/brief_detail_ng.html",
                                context=context)

    def post(self, request, **kwargs):
        brief = get_one_or_404(request.user, 'change_brief', b.Brief, id=kwargs['pk'])
        brief.status = b.BriefStatus.Sent.value
        brief.save()

        _send_brief_email(brief.client.email, request.user.name,
                          (request.build_absolute_uri(
                              reverse('brief_answer', args=[brief.token.hex]))),
                          get_site_from_host(request))
        messages.success(request, 'Brief link sent to %s.' % brief.client.email)
        return self.get(request, **kwargs)


class BriefViewSet(UserModelViewSet):
    model = b.Brief
    serializer_class = serializers.BriefSerializer
