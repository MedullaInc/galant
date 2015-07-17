from django.core.urlresolvers import reverse
from briefs import models as b
from gallant import models as g
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from briefs import forms
from django.shortcuts import get_object_or_404


class BriefList(ListView):
    def render_to_response(self, context, **response_kwargs):
        context.update({'title': 'Briefs'})
        return super(ListView, self).render_to_response(context)


class ClientBriefList(ListView):
    template_name = "briefs/client_brief_list.html"

    def render_to_response(self, context, **response_kwargs):
        context['title'] = 'Briefs'
        context['client'] = g.Client.objects.get(id=self.kwargs['pk'])
        return super(ListView, self).render_to_response(context)

    def get_queryset(self):
        try:
            briefs = b.Brief.objects.get(clientbrief=self.kwargs['pk'])
        except b.Brief.DoesNotExist:
            briefs = None
        return briefs


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


class BriefUpdate(UpdateView):
    template_name = "quotes/quote_form.html"

    def get(self, request, *args, **kwargs):

        if self.kwargs['brief_type'] == "client":
            self.model = b.ClientBrief
            self.form_class = forms.ClientBriefForm

    def get_success_url(self):
        return reverse('brief_detail', args=[self.object.id])

    def form_valid(self, form):
        form.client = self.kwargs['pk']
        form.save(commit=True)
        return super(BriefUpdate, self).form_valid(form)

    def render_to_response(self, context, **response_kwargs):
        context.update({'title': 'Update Brief'})
        return super(UpdateView, self).render_to_response(context)


class BriefDetail(DetailView):

    def get(self, request, *args, **kwargs):
        if self.kwargs['brief_type'] == "client":
            self.model = b.ClientBrief
            self.form_class = forms.ClientBriefForm
