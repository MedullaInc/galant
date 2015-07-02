from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from gallant.forms import *


class ClientCreate(CreateView):
    form_class = ClientForm
    template_name = "gallant/client_form.html"

    def form_valid(self, form):
        obj = form.save(commit=True)
        user = GallantUser.objects.get(id=self.request.user.id)
        text = '[Created]\n' + form.cleaned_data['notes']
        note = Note.objects.create(text=text, created_by=user)
        obj.notes.add(note)
        obj.save()
        return HttpResponseRedirect(reverse('client_detail', args=[obj.id]))


class ClientUpdate(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "gallant/client_form.html"

    def form_valid(self, form):
        obj = form.save(commit=True)
        user = GallantUser.objects.get(id=self.request.user.id)
        text = '[Updated]\n' + form.cleaned_data['notes']
        note = Note.objects.create(text=text, created_by=user)
        obj.notes.add(note)
        obj.save()
        return HttpResponseRedirect(reverse('client_detail', args=[obj.id]))


class ClientDetailView(DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context['note_post_url'] = reverse('add_client_note', kwargs={'client_id':self.get_object().id})
        return context


def add_client_note(request, client_id):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            client = get_object_or_404(Client, pk=client_id)
            user = GallantUser.objects.get(id=request.user.id)
            note = Note.objects.create(text=form.cleaned_data['text'], created_by=user)
            client.notes.add(note)
            client.save()
            return HttpResponseRedirect(reverse('client_detail', args=[client.id]))