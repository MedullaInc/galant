from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from briefs import models as b
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.translation import get_language
from django.views.generic import View
from briefs import forms as bf
from gallant import forms as gf
from gallant.utils import get_one_or_404, query_url
from django.utils.translation import ugettext_lazy as _
from briefs.views.brief import _update_from_query


class BriefTemplateList(View):
    def get(self, request):
        self.request.breadcrumbs([(_('Briefs'), reverse('briefs')),
                                  (_('Templates'), request.path_info)])
        return TemplateResponse(request=request,
                                template="briefs/brieftemplate_list.html",
                                context={'title': 'Brief Templates',
                                         'object_list': b.BriefTemplate.objects
                                                         .all_for(request.user)})


class BriefTemplateDetail(View):
    def get(self, request, **kwargs):
        context = {'title': 'Brief Template Detail'}
        brief = get_one_or_404(request.user, 'view_brieftemplate', b.BriefTemplate, id=kwargs['pk'])

        answers_q = brief.brief.briefanswers_set.all_for(request.user)
        if answers_q.count() > 0:
            brief_answers = answers_q.last()
            context.update({'answer_set': brief_answers,
                            'answers': brief_answers.answers
                                                    .all_for(request.user)
                                                    .order_by('question__index')})

        _update_from_query(request, context)
        context.update({'object': brief,
                        'questions': brief.brief.questions
                                          .all_for(request.user)\
                                          .order_by('index')})

        request.breadcrumbs([(_('Briefs'), reverse('briefs')), (_('Templates'), reverse('brief_templates')), (_('Template: ') + brief.brief.name, request.path_info + query_url(request))])
        return TemplateResponse(request=request,
                                template="briefs/brieftemplate_detail.html",
                                context=context)


class BriefTemplateView(View):
    def get(self, request, **kwargs):
        self.request.breadcrumbs([(_('Briefs'), reverse('briefs')),
                                  (_('Templates'), reverse('brief_templates'))])
        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'view_brieftemplate', b.BriefTemplate, pk=kwargs['pk'])
            form = bf.BriefTemplateForm(request.user, instance=self.object.brief)
            question_forms = bf.question_forms_brief(self.object.brief)
            self.request.breadcrumbs(_('Template: %s' % self.object.brief.name), reverse('brief_template_detail', args=[kwargs['pk']]))

            if not request.user.has_perm('change_brieftemplate', self.object):
                messages.warning(request, 'Warning: you don\'t have permission to change this template. '
                                 'To save it as your own, use it to create a brief, then '
                                 'create a separate template from the new brief.')

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
                        'template': self.object,
                        'object': brief,
                        'language': get_language()})
        return TemplateResponse(request=self.request,
                                template="briefs/brief_template.html",
                                context=context)


class BriefTemplateDelete(View):
    def get(self, request, **kwargs):
        brief = get_one_or_404(request.user, 'change_brieftemplate', b.BriefTemplate, id=kwargs['pk'])
        brief.soft_delete()

        return HttpResponseRedirect(reverse('brief_templates'))

