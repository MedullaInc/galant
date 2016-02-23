from django.contrib import messages
from django.core.urlresolvers import reverse
from briefs import models as b
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from gallant.views.user import UserModelViewSet
from guardian.shortcuts import remove_perm
from django.views.generic import View
from briefs import forms as bf
from briefs import serializers
from django.db.models import Q


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
        form = bf.BriefAnswersForm(obj.user, instance=b.BriefAnswers(brief=obj), data=request.POST)
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
            
            remove_perm('change_brief', obj.user, obj)
            return HttpResponseRedirect(reverse('home'))

        return TemplateResponse(request=request,
                                template="briefs/brief_answers.html",
                                context={'form': form, 'answer_forms': answers, 'object': obj})


class BriefAnswersViewSet(UserModelViewSet):
    model = b.BriefAnswers
    serializer_class = serializers.BriefAnswersSerializer

    def get_queryset(self):
        brief_id = self.request.GET.get('brief_id', None)
        if brief_id:
            return self.model.objects.filter(brief_id=brief_id)
        else:
            return self.model.objects.all()
