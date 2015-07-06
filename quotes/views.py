from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from quotes import forms


class QuoteCreate(CreateView):
    form_class = forms.QuoteForm
    template_name = "quotes/quote_form.html"

    def get_success_url(self):
        return reverse('home')

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