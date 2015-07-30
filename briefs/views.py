from django.contrib import messages
from django.core.urlresolvers import reverse
from briefs import models as b
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from gallant import models as g
from django.views.generic import ListView, DetailView, View
from briefs import forms as bf
from django.shortcuts import get_object_or_404


class BriefList(ListView):
    model = b.Brief

    def render_to_response(self, context, **response_kwargs):
        context.update({'title': 'Briefs'})
        return super(ListView, self).render_to_response(context)


class ClientBriefList(ListView):
    template_name = "briefs/client_brief_list.html"
    model = b.ClientBrief

    def render_to_response(self, context, **response_kwargs):
        context['title'] = 'Briefs'
        context['client'] = g.Client.objects.get(id=self.kwargs['type_id'])
        context.update({'template_list': b.ClientBrief.objects.filter(client=self.kwargs['type_id'])})
        return super(ClientBriefList, self).render_to_response(context)


class BriefUpdate(View):
    def get(self, request, *args, **kwargs):
        context = {}
        if self.kwargs['brief_type'] == 'client':
            self.object = get_object_or_404(b.ClientBrief, pk=kwargs['pk'])
            context['client'] = self.object.client
        else:
            self.object = get_object_or_404(b.Brief, pk=kwargs['pk'])

        form = bf.BriefForm(instance=self.object)
        questions = [bf.QuestionForm(instance=q, prefix='-question-%d' % q.index) for q in self.object.questions.all()]
        context.update({'object': self.object, 'form': form, 'title': 'Edit Brief', 'questions': questions})
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            self.object = get_object_or_404(b.Brief, pk=kwargs['pk'])
        else:
            if self.kwargs['brief_type'] == 'client':
                client = get_object_or_404(g.Client, pk=kwargs['type_id'])
                self.object = b.ClientBrief(client=client)
            else:
                self.object = None

        form = bf.BriefForm(request.POST, instance=self.object)
        questions = bf.questions_from_post(request.POST)

        if form.is_valid():
            obj = form.save()
            obj.questions.clear()
            for q in questions:
                obj.questions.add(q.save())

            messages.success(self.request, 'Brief saved.')

            if self.kwargs['brief_type'] == "client":
                return HttpResponseRedirect(reverse('brief_detail', args=['client', kwargs['type_id'], obj.id]))
        else:
            return self.render_to_response({'object': self.object, 'form': form, 'title': 'Edit Brief'})

    def render_to_response(self, context, **kwargs):
        return TemplateResponse(request=self.request, template="briefs/brief_form.html", context=context, **kwargs)


class BriefCreate(BriefUpdate):
    def get(self, request, *args, **kwargs):
        context = {}
        if self.kwargs['brief_type'] == 'client':
            client = get_object_or_404(g.Client, pk=kwargs['type_id'])
            context['client'] = client
        form = bf.BriefForm()
        context.update({'form': form, 'title': 'Create Brief'})
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
