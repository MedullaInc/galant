from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from quotes import models as q
from django.core.urlresolvers import reverse
from quotes import forms


class QuoteCreate(CreateView):
    form_class = forms.QuoteForm
    template_name = "gallant/create_form.html"

    def get_success_url(self):
        return reverse('home')

    def render_to_response(self, context, **response_kwargs):
        context.update({'title': 'Edit Quote'})
        return super(CreateView, self).render_to_response(context)


    '''def form_valid(self, form):
        obj = form.save(commit=True)
        user = g.GallantUser.objects.get(id=self.request.user.id)
        text = '[Created]\n' + form.cleaned_data['notes']
        note = g.Note.objects.create(text=text, created_by=user)
        obj.notes.add(note)
        obj.save()
        # TODO: return HttpResponseRedirect(reverse('quote_detail', args=[obj.id]))
        return HttpResponseRedirect(reverse('home'))
    '''


class QuoteUpdate(UpdateView):
    model = q.Quote
    form_class = forms.QuoteForm
    template_name = "gallant/create_form.html"

    def get_success_url(self):
        return reverse('quote_detail', args=[self.object.id])

    def render_to_response(self, context, **response_kwargs):
        context.update({'title': 'Update Quote'})
        return super(UpdateView, self).render_to_response(context)


class QuoteDetail(DetailView):
    model = q.Quote