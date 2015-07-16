from django.core.urlresolvers import reverse
from briefs import models as b
from gallant import models as g
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from briefs import forms


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
    form_class = forms.BriefForm
    template_name = "briefs/brief_form.html"

    def get_success_url(self):
        return reverse('brief_detail', args=[self.object.id])

    def form_valid(self, form):
        return super(BriefCreate, self).form_valid(form)

    def render_to_response(self, context, **response_kwargs):
        context.update({'title': 'Edit Brief'})
        return super(CreateView, self).render_to_response(context)


class BriefUpdate(UpdateView):
    pass


class BriefDetail(DetailView):
    pass
