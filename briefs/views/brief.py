from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from briefs import models as b, serializers
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from gallant import models as g
from quotes import models as q
from django.views.generic import View
from briefs import forms as bf
from gallant.utils import get_one_or_404, query_url, get_site_from_host, GallantObjectPermissions
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


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


class BriefUpdate(View):
    def get(self, request, *args, **kwargs):
        context = {}
        brief = get_one_or_404(request.user, 'change_brief', b.Brief, pk=kwargs['pk'])

        if brief.pk:
            self.request.breadcrumbs([
                (_('Clients'), reverse('clients')),
                (brief.client.name, reverse('client_detail', args=[brief.client.id])),
                (_('Briefs'), reverse('briefs') + query_url(request)),
                (_('Brief: ') + brief.name, reverse('brief_detail', args=[brief.id]) + query_url(self.request)),
                (_('Edit'), self.request.path_info + query_url(self.request))
            ])
        else:
            self.request.breadcrumbs(
                _('Add'), self.request.path_info + query_url(self.request)
            )

        form = bf.BriefForm(request.user, instance=brief)
        _update_from_query(request, context)

        questions = bf.question_forms_brief(brief)
        context.update({'object': brief, 'form': form, 'title': 'Edit Brief', 'questions': questions,
                        'client': brief.client})

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            brief = get_one_or_404(request.user, 'change_brief', b.Brief, pk=kwargs['pk'])
        else:
            brief = b.Brief()

        context = {}
        _update_from_query(request, context)

        if 'quote' in context:
            # client specified by quote takes precedence over query param
            brief.client = context['quote'].client
        elif 'project' in context:
            brief.quote = context['project'].quote
            brief.client = brief.quote.client  # likewise for project

        form = bf.BriefForm(request.user, request.POST, instance=brief)
        question_forms = bf.question_forms_request(request)

        valid = list([form.is_valid()] + [s.is_valid() for s in question_forms])
        if all(valid):
            obj = bf.create_brief(form, question_forms)

            messages.success(self.request, 'Brief saved.')

            return HttpResponseRedirect(reverse('brief_detail', args=[obj.id]))
        else:
            if brief.pk:
                self.request.breadcrumbs([
                    (_('Brief: ') + brief.name, reverse('brief_detail', args=[brief.id])),
                    (_('Edit'), self.request.path_info + query_url(self.request))
                ])
            else:
                self.request.breadcrumbs(
                    _('Add'), self.request.path_info + query_url(self.request)
                )
            return self.render_to_response({'object': brief, 'form': form,
                                            'title': 'Edit Brief', 'questions': question_forms})

    def render_to_response(self, context, **kwargs):
        brief = context['object']
        return TemplateResponse(request=self.request, template="briefs/brief_form.html", context=context, **kwargs)


class BriefCreate(BriefUpdate):
    def get(self, request, *args, **kwargs):
        context = {}
        instance = None
        template_id = request.GET.get('template_id', None)
        lang = request.GET.get('lang', None)

        initial = _update_from_query(request, context)

        if template_id is not None:
            template = get_one_or_404(request.user, 'view_brieftemplate', b.BriefTemplate, pk=template_id)
            brief = template.brief
            question_forms = bf.question_forms_brief(brief, clear_pk=True)
            context.update({'questions': question_forms})
            brief.pk = None

            instance = brief

            if lang is not None:
                brief.language = lang
                context.update({'language': lang,
                                'object': brief})

        form = bf.BriefForm(request.user, instance=instance, initial=initial)

        context.update({'title': 'Create Brief', 'form': form})
        request.breadcrumbs(_('Add'), request.path_info + query_url(request))
        return TemplateResponse(request=self.request, template="briefs/brief_form.html", context=context, **kwargs)


def _send_brief_email(email, from_name, link, site):
    message = '%s has sent you a %s questionnaire.\n\n Click this link to answer:\n %s' %\
        (from_name, site, link)
    send_mail('Client Questionnaire', message,
              '%s via %s <%s>' % (from_name, site,  settings.EMAIL_HOST_USER),
              [email], fail_silently=False)


class BriefDetail(View):
    def get(self, request, **kwargs):
        context = {'title': 'Brief Detail'}
        brief = get_one_or_404(request.user, 'view_brief', b.Brief, id=kwargs['pk'])

        answers_q = brief.briefanswers_set.all_for(request.user)
        if answers_q.count() > 0:
            brief_answers = answers_q.last()
            context.update({'answer_set': brief_answers,
                            'answers': brief_answers.answers
                                                    .all_for(request.user)
                                                    .order_by('question__index')})

        _update_from_query(request, context)
        context.update({'object': brief,
                        'questions': brief.questions
                                          .all_for(request.user)\
                                          .order_by('index')})

        request.breadcrumbs(_('Brief: ') + brief.name, request.path_info + query_url(request))
        return TemplateResponse(request=request,
                                template="briefs/brief_detail.html",
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


class BriefDelete(View):
    def get(self, request, **kwargs):
        brief = get_one_or_404(request.user, 'change_brief', b.Brief, id=kwargs['pk'])
        brief.soft_delete()

        return HttpResponseRedirect(reverse('briefs'))


class BriefDetailAPI(generics.RetrieveUpdateAPIView):
    model = b.Brief
    serializer_class = serializers.BriefSerializer
    permission_classes = [
        GallantObjectPermissions
    ]

    def get_queryset(self):
        return self.model.objects.all_for(self.request.user)

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        if response.status_code == HTTP_200_OK:
            self.request._messages.add(messages.SUCCESS, 'Brief saved')
            return Response({'status': 0, 'redirect': reverse('brief_detail', args=[response.data['id']])})
        else:
            return response
