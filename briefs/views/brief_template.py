from django.core.urlresolvers import reverse
from briefs import models as b, serializers
from django.template.response import TemplateResponse
from django.utils.translation import get_language
from django.views.generic import View
from gallant import forms as gf
from gallant.utils import get_one_or_404, query_url
from django.utils.translation import ugettext_lazy as _
from briefs.views.brief import _update_from_query
from gallant.views.user import UserModelViewSet


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
        context = {'title': 'Brief Template Detail',
                   'is_template': True,
                   'language': get_language(),
                   'language_form': gf.LanguageForm()}

        _update_from_query(request, context)

        request.breadcrumbs([(_('Briefs'), reverse('briefs')),
                             (_('Templates'), reverse('brieftemplates'))])

        if 'pk' in kwargs:
            brief_template = get_one_or_404(request.user, 'view_brieftemplate',
                                            b.BriefTemplate, id=kwargs['pk'])
            context.update({'template_id': kwargs['pk']})

            request.breadcrumbs([(_('Template: ') + brief_template.brief.name,
                                  request.path_info + query_url(request))])
        else:
            brief_id = request.GET.get('brief_id', None)
            if brief_id:
                brief = get_one_or_404(request.user, 'view_brief', b.Brief, id=brief_id)
                context.update({'object': brief})
            request.breadcrumbs([(_('Add'), request.path_info + query_url(request))])

        return TemplateResponse(request=request,
                                template="briefs/brief_detail_ng.html",
                                context=context)


class BriefTemplateViewSet(UserModelViewSet):
    model = b.BriefTemplate
    serializer_class = serializers.BriefTemplateSerializer
