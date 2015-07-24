from django.core.urlresolvers import reverse
from briefs import models as b
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from gallant import models as g
from django.views.generic import ListView, CreateView, DetailView, View
from briefs import forms
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
        context['client'] = g.Client.objects.get(id=self.kwargs['pk'])
        context.update({'template_list': b.ClientBrief.objects.filter(client=self.kwargs['pk'])})
        return super(ClientBriefList, self).render_to_response(context)


class BriefCreate(CreateView):
    template_name = "briefs/brief_form.html"

    def get_form(self):
        if self.kwargs['brief_type'] == "client":
            form = super(BriefCreate, self).get_form(forms.ClientBriefForm)
            client = get_object_or_404(g.Client, pk=self.kwargs['pk'])
            form.instance.client = client
        else:
            form = super(BriefCreate, self).get_form(forms.BriefForm)

        return form

    def render_to_response(self, context, **response_kwargs):
        context['title'] = 'Edit Brief'
        context['client'] = g.Client.objects.get(id=self.kwargs['pk'])
        return super(BriefCreate, self).render_to_response(context)

    def get_success_url(self):
        return reverse('brief_detail', args=[self.kwargs['brief_type'], self.object.id])


class BriefUpdate(View):
    template_name = "briefs/brief_form.html"

    def get(self, request, *args, **kwargs):
        if self.kwargs['brief_type'] == "client":
            self.object = get_object_or_404(b.ClientBrief, pk=kwargs['pk'])
        else:
            self.object = get_object_or_404(b.Brief, pk=kwargs['pk'])

        form = forms.BriefForm(instance=self.object)
        return self.render_to_response({'object': self.object, 'form': form})

    def render_to_response(self, context, **kwargs):
        if self.kwargs['brief_type'] == "client":
            context['client'] = self.object.client

        context.update({'title': 'Update Brief'})
        return TemplateResponse(request=self.request, template="briefs/brief_form.html", context=context, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(b.Brief, pk=kwargs['pk'])
        form = forms.BriefForm(request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.render_to_response({'object': self.object, 'form': form})

    def form_valid(self, form):
        obj = form.save(commit=True)
        obj.save()

        if self.kwargs['brief_type'] == "client":
            return HttpResponseRedirect(reverse('brief_detail', args=['client',obj.id]))
        else:
            pass


class BriefDetail(DetailView):
    model = b.Brief

    def render_to_response(self, context, **response_kwargs):
        if self.kwargs['brief_type'] == "client":
            client_brief = b.ClientBrief.objects.get(id=self.kwargs['pk'])
            context['object'] = client_brief
            context['client'] = client_brief.client

        context['title'] = 'Brief Detail'

        return super(BriefDetail, self).render_to_response(context)
