from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from briefs import models as b
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import get_language
from gallant import models as g
from quotes import models as q
from django.views.generic import View
from briefs import forms as bf
from gallant import forms as gf
from django.db.models import Q
from gallant.utils import get_one_or_404, query_url
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
        initial = {'client': project.quote.client_id, 'quote': project.quote.id or None}
        context.update({'project': project, 'quote': project.quote, 'client': project.quote.client})
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
        request.breadcrumbs(_('Briefs'), reverse('briefs'))

    return initial


class BriefList(View):
    def get(self, request, **kwargs):
        context = {'template_list': b.BriefTemplate.objects.all_for(request.user, 'view_brieftemplate')}

        _update_from_query(request, context)

        if 'client' in context:
            briefs = context['client'].brief_set.all_for(request.user, 'view_brief')
            context.update({'object_list': briefs})
        else:
            context.update({'object_list': b.Brief.objects
                                            .all_for(request.user, 'view_brief')
                                            .filter(client__isnull=False)})

        return TemplateResponse(request=request,
                                template="briefs/brief_list.html",
                                context=context)


class BriefUpdate(View):
    def get(self, request, *args, **kwargs):
        context = {}
        brief = get_one_or_404(request.user, 'change_brief', b.Brief, pk=kwargs['pk'])

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
            return self.render_to_response({'object': brief, 'form': form,
                                            'title': 'Edit Brief', 'questions': question_forms})

    def render_to_response(self, context, **kwargs):
        brief = context['object']
        self.request.breadcrumbs([(_('Brief: ') + brief.name, reverse('brief_detail', args=[brief.id])),
                                  (_('Edit'), self.request.path_info + query_url(self.request))])
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


class BriefDetail(View):
    def get(self, request, **kwargs):
        context = {'title': 'Brief Detail'}
        brief = get_one_or_404(request.user, 'view_brief', b.Brief, id=kwargs['pk'])

        answers_q = brief.briefanswers_set.all_for(request.user, 'view_briefanswers')
        if answers_q.count() > 0:
            brief_answers = answers_q.last()
            context.update({'answer_set': brief_answers,
                            'answers': brief_answers.answers.all_for(request.user, 'view_answers')\
                                                    .order_by('question__index')})

        _update_from_query(request, context)
        context.update({'object': brief, 'questions': brief.questions\
                                                           .all_for(request.user, 'view_question')\
                                                           .order_by('index')})

        request.breadcrumbs(_('Brief: ') + brief.name, request.path_info + query_url(request))
        return TemplateResponse(request=request,
                                template="briefs/brief_detail.html",
                                context=context)

    def post(self, request, **kwargs):
        brief = get_one_or_404(request.user, 'change_brief', b.Brief, id=kwargs['pk'])
        brief.status = b.BriefStatus.Sent.value
        brief.save()

        messages.warning(request, 'Email currently disabled.', 'warning client_email_link')
        return self.get(request, **kwargs)


class BriefTemplateList(View):
    def get(self, request):
        self.request.breadcrumbs([(_('Briefs'), reverse('briefs')),
                                  (_('Templates'), request.path_info)])
        return TemplateResponse(request=request,
                                template="briefs/brieftemplate_list.html",
                                context={'title': 'Brief Templates',
                                         'object_list': b.BriefTemplate.objects
                                                         .all_for(request.user, 'view_brieftemplate')})


class BriefTemplateView(View):
    def get(self, request, **kwargs):
        self.request.breadcrumbs([(_('Briefs'), reverse('briefs')),
                                  (_('Templates'), reverse('brief_templates'))])
        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'view_brieftemplate', b.BriefTemplate, pk=kwargs['pk'])
            form = bf.BriefTemplateForm(request.user, instance=self.object.brief)
            question_forms = bf.question_forms_brief(self.object.brief)

            self.request.breadcrumbs(_('Edit'), request.path_info)
        else:
            self.object = None

            self.request.breadcrumbs(_('Add'), request.path_info)

            if kwargs['brief_id'] is not None:
                brief = get_one_or_404(request.user, 'view_brief', b.Brief, pk=kwargs['brief_id'])
                form = bf.BriefTemplateForm(request.user, instance=brief)
                question_forms = bf.question_forms_brief(brief)
            else:
                form = bf.BriefTemplateForm(request.user)
                question_forms = []

        return self.render_to_response({'form': form, 'questions': question_forms}, request)

    def post(self, request, **kwargs):
        question_forms = bf.question_forms_request(request)
        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'change_brieftemplate', b.BriefTemplate, pk=kwargs['pk'])
            form = bf.BriefTemplateForm(request.user, request.POST, instance=self.object.brief)
        else:
            self.object = None
            form = bf.BriefTemplateForm(request.user, request.POST)

        valid = list([form.is_valid()] + [s.is_valid() for s in question_forms])
        if all(valid):
            return self.form_valid(form, question_forms)
        else:
            return self.render_to_response({'form': form, 'questions': question_forms}, request)

    def form_valid(self, form, question_forms):
        brief = bf.create_brief(form, question_forms)
        if hasattr(self, 'object') and self.object is None:
            self.object = b.BriefTemplate.objects.create(user=brief.user, brief=brief)
        messages.success(self.request, 'Template saved.')
        return HttpResponseRedirect(reverse('edit_brief_template', args=[self.object.id]))

    def render_to_response(self, context, request):
        lang_dict = dict(settings.LANGUAGES)
        form = gf.LanguageForm()
        language_set = set([get_language()])

        if hasattr(self.object, 'brief'):
            language_set.update(self.object.brief.get_languages())
            brief = self.object.brief
            context.update({'title': 'Edit Template'})
        elif 'brief_id' in self.kwargs and self.kwargs['brief_id'] is not None:
            brief = get_one_or_404(request.user, 'view_brief', b.Brief, pk=self.kwargs['brief_id'])
            context.update({'title': 'New Template'})
        else:
            brief = b.Brief()
            context.update({'title': 'New Template'})

        context.update({'languages': [(c, lang_dict[c]) for c in language_set if c in lang_dict],
                        'language_form': form,
                        'object': brief,
                        'language': get_language()})
        return TemplateResponse(request=self.request,
                                template="briefs/brief_template.html",
                                context=context)


class BriefAnswer(View):
    # Brief may be answered by anonymous user via token link
    def get(self, request, **kwargs):
        obj = get_object_or_404(b.Brief, Q(status=2) | Q(status=3), token=kwargs['token'])
        form = bf.BriefAnswersForm(request.user, instance=b.BriefAnswers(brief=obj))

        return TemplateResponse(request=self.request,
                                template="briefs/brief_answers.html",
                                context={'form': form, 'object': obj, 'answer_forms': form.answer_forms()})

    def post(self, request, **kwargs):
        obj = get_object_or_404(b.Brief, Q(status=2) | Q(status=3), token=kwargs['token'])
        form = bf.BriefAnswersForm(request.user, instance=b.BriefAnswers(brief=obj), data=request.POST)
        answers = []

        for answer in form.answer_forms(request.POST):
            answers.append(answer)

        valid = list([form.is_valid()] + [a.is_valid() for a in answers])
        if all(valid):
            brief_answers = form.save()
            for answer in answers:
                brief_answers.answers.add(answer.save())

            messages.success(request, 'Brief answered.')
            obj.status = b.BriefStatus.Answered.value
            obj.save()
            return HttpResponseRedirect(reverse('brief_detail', args=[brief_answers.brief.id]))

        return TemplateResponse(request=request,
                                template="briefs/brief_answers.html",
                                context={'form': form, 'answer_forms': answers, 'object': obj})
