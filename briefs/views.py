from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from briefs import models as b
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.translation import get_language
from gallant import models as g
from django.views.generic import DetailView, View
from briefs import forms as bf
from gallant import forms as gf
from django.shortcuts import get_object_or_404
from django.db.models import Q


class BriefList(View):
    def get(self, request, **kwargs):
        context = {}
        if 'brief_type' in kwargs:
            if kwargs['brief_type'] == "client":
                client = g.Client.objects.get(pk=kwargs['type_id'])
                context.update({'brief_type_title': 'Client', 'object_list': client.clientbrief_set.all(),
                                'create_url': reverse('add_brief', args=['client', client.id]),
                                'detail_url': reverse('brief_detail', args=['client', client.id])})
        else:
            context.update({'create_url': reverse('add_brief'), 'object_list': b.Brief.objects.all(),
                            'detail_url': reverse('brief_detail')})

        return TemplateResponse(request=request,
                                template="briefs/brief_list.html",
                                context=context)


class BriefUpdate(View):
    def get(self, request, *args, **kwargs):
        context = {}
        if kwargs['brief_type'] == 'client':
            self.object = get_object_or_404(b.ClientBrief, pk=kwargs['pk'])
            context['client'] = self.object.client
        else:
            self.object = get_object_or_404(b.Brief, pk=kwargs['pk'])

        form = bf.BriefForm(instance=self.object)
        questions = bf.question_forms_brief(self.object)
        context.update({'object': self.object, 'form': form, 'title': 'Edit Brief', 'questions': questions})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            self.object = get_object_or_404(b.Brief, pk=kwargs['pk'])
        else:
            if kwargs['brief_type'] == 'client':
                client = get_object_or_404(g.Client, pk=kwargs['type_id'])
                self.object = b.ClientBrief(client=client)
            else:
                self.object = None

        form = bf.BriefForm(request.POST, instance=self.object)
        question_forms = bf.question_forms_post(request.POST)

        valid = list([form.is_valid()] + [s.is_valid() for s in question_forms])
        if all(valid):
            obj = bf.create_brief(form, question_forms)

            messages.success(self.request, 'Brief saved.')

            if kwargs['brief_type'] == "client":
                return HttpResponseRedirect(reverse('brief_detail', args=['client', kwargs['type_id'], obj.id]))
        else:
            return self.render_to_response({'object': self.object, 'form': form, 'title': 'Edit Brief'})

    def render_to_response(self, context, **kwargs):
        return TemplateResponse(request=self.request, template="briefs/brief_form.html", context=context, **kwargs)


class BriefCreate(BriefUpdate):
    def get(self, request, *args, **kwargs):
        context = {}
        template_id = request.GET.get('template_id', None)
        lang = request.GET.get('lang', None)
        if template_id is not None:
            template = get_object_or_404(b.BriefTemplate, pk=template_id)
            brief = template.brief
            question_forms = bf.question_forms_brief(brief, clear_pk=True)
            context.update({'questions': question_forms})
            brief.pk = None
            if lang is not None:
                brief.language = lang
                context.update({'language': lang, 'form': bf.BriefForm(instance=brief), 'object': brief})
        else:
            context.update({'form': bf.BriefForm()})

        if kwargs['brief_type'] == 'client':
            context['client'] = get_object_or_404(g.Client, pk=kwargs['type_id'])

        context.update({'title': 'Create Brief'})
        return self.render_to_response(context)


class BriefDetail(DetailView):
    model = b.Brief

    def render_to_response(self, context, **response_kwargs):
        if self.kwargs['brief_type'] == "client":
            client_brief = b.ClientBrief.objects.get(id=self.kwargs['pk'])
            context['object'] = client_brief
            context['client'] = client_brief.client

        context['title'] = 'Brief Detail'

        return super(BriefDetail, self).render_to_response(context)


class BriefTemplateList(View):
    def get(self, request):
        return TemplateResponse(request=request,
                                template="quotes/brieftemplate_list.html",
                                context={'title': 'Brief Templates',
                                         'object_list': b.BriefTemplate.objects.all()})


class BriefTemplateView(View):
    def get(self, request, **kwargs):
        if 'pk' in kwargs:
            self.object = get_object_or_404(b.BriefTemplate, pk=kwargs['pk'])
            form = bf.BriefTemplateForm(instance=self.object.brief)
            question_forms = bf.question_forms_brief(self.object.brief)
        else:
            self.object = None
            if kwargs['brief_id'] is not None:
                brief = get_object_or_404(b.Brief, pk=kwargs['brief_id'])
                form = bf.BriefTemplateForm(instance=brief)
                question_forms = bf.question_forms_brief(brief)
            else:
                form = bf.BriefTemplateForm()
                question_forms = []

        return self.render_to_response({'form': form, 'questions': question_forms})

    def post(self, request, **kwargs):
        question_forms = bf.question_forms_post(request.POST)
        if 'pk' in kwargs:
            self.object = get_object_or_404(b.BriefTemplate, pk=kwargs['pk'])
            form = bf.BriefTemplateForm(request.POST, instance=self.object.brief)
        else:
            self.object = None
            form = bf.BriefTemplateForm(request.POST)

        valid = list([form.is_valid()] + [s.is_valid() for s in question_forms])
        if all(valid):
            return self.form_valid(form, question_forms)
        else:
            return self.render_to_response({'form': form, 'questions': question_forms})

    def form_valid(self, form, question_forms):
        brief = bf.create_brief(form, question_forms)
        if hasattr(self, 'object') and self.object is None:
            self.object = b.BriefTemplate.objects.create(brief=brief)
        messages.success(self.request, 'Template saved.')
        return HttpResponseRedirect(reverse('edit_brief_template', args=[self.object.id]))

    def render_to_response(self, context):
        lang_dict = dict(settings.LANGUAGES)
        form = gf.LanguageForm()
        language_set = set([get_language()])

        if hasattr(self.object, 'brief'):
            language_set.update(self.object.brief.get_languages())
            brief = self.object.brief
            context.update({'title': 'Edit Template'})
        elif 'brief_id' in self.kwargs and self.kwargs['brief_id'] is not None:
            brief = get_object_or_404(b.Brief, pk=self.kwargs['brief_id'])
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
    def get(self, request, **kwargs):
        obj = get_object_or_404(b.Brief, Q(status=2) | Q(status=3), token=kwargs['token'])
        form = bf.BriefAnswersForm(instance=b.BriefAnswers(brief=obj))

        return TemplateResponse(request=self.request,
                                template="briefs/brief_answers.html",
                                context={'form': form, 'object': obj, 'answer_forms': form.answer_forms()})

    def post(self, request, **kwargs):
        obj = get_object_or_404(b.Brief, Q(status=2) | Q(status=3), token=kwargs['token'])
        form = bf.BriefAnswersForm(instance=b.BriefAnswers(brief=obj), data=request.POST)
        answers = []

        for answer in form.answer_forms(request.POST):
            answers.append(answer)

        valid = list([form.is_valid()] + [a.is_valid() for a in answers])
        if all(valid):
            brief_answers = form.save()
            for answer in answers:
                brief_answers.answers.add(answer.save())

            messages.success(request, 'Brief answered.')
            return HttpResponseRedirect(reverse('brief_detail', args=[brief_answers.brief.id]))

        return TemplateResponse(request=request,
                                template="briefs/brief_answers.html",
                                context={'form': form, 'answer_forms': answers, 'object': obj})
