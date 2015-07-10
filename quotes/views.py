from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from quotes import models as q
from django.core.urlresolvers import reverse
from quotes import forms


class QuoteCreate(CreateView):
    form_class = forms.QuoteForm
    template_name = "quotes/quote_form.html"

    def get_success_url(self):
        return reverse('quote_detail', args=[self.object.id])

    def render_to_response(self, context, **response_kwargs):
        context.update({'title': 'Edit Quote'})
        return super(CreateView, self).render_to_response(context)

    def form_valid(self, form):
        obj = form.save(commit=True)
        intro = q.Section.objects.create(title=form.cleaned_data['intro_title'],
                                         text=form.cleaned_data['intro_text'])
        margin_section = q.Section.objects.create(title=form.cleaned_data['margin_section_title'],
                                                  text=form.cleaned_data['margin_section_text'])
        obj.intro = intro
        obj.margin_section = margin_section
        obj.save()
        return HttpResponseRedirect(reverse('quote_detail', args=[obj.id]))


class QuoteUpdate(UpdateView):
    model = q.Quote
    form_class = forms.QuoteForm
    template_name = "quotes/quote_form.html"

    def get_success_url(self):
        return reverse('quote_detail', args=[self.object.id])

    def render_to_response(self, context, **response_kwargs):
        context.update({'title': 'Update Quote'})
        return super(UpdateView, self).render_to_response(context)


class QuoteDetail(DetailView):
    model = q.Quote


class QuoteList(ListView):
    model = q.Quote