from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from gallant import forms
from gallant import models as g


class ClientList(ListView):
    model = g.Client


class ClientCreate(CreateView):
    form_class = forms.ClientForm
    template_name = "gallant/create_form.html"

    def render_to_response(self, context, **response_kwargs):
        context.update({'title': 'Add Client'})
        return super(CreateView, self).render_to_response(context)

    def form_valid(self, form):
        obj = form.save(commit=True)
        user = g.GallantUser.objects.get(id=self.request.user.id)
        text = '[Created]\n' + form.cleaned_data['notes']
        note = g.Note.objects.create(text=text, created_by=user)
        obj.notes.add(note)
        obj.save()
        return HttpResponseRedirect(reverse('client_detail', args=[obj.id]))


class ClientUpdate(UpdateView):
    model = g.Client
    form_class = forms.ClientForm
    template_name = "gallant/create_form.html"

    def render_to_response(self, context, **response_kwargs):
        context.update({'title': 'Update Client'})
        return super(UpdateView, self).render_to_response(context)

    def form_valid(self, form):
        obj = form.save(commit=True)
        user = g.GallantUser.objects.get(id=self.request.user.id)
        text = '[Updated]\n' + form.cleaned_data['notes']
        note = g.Note.objects.create(text=text, created_by=user)
        obj.notes.add(note)
        obj.save()
        return HttpResponseRedirect(reverse('client_detail', args=[obj.id]))


class ServiceUpdate(UpdateView):
    model = g.Service
    form_class = forms.ServiceForm
    template_name = "gallant/create_form.html"

    def render_to_response(self, context, **response_kwargs):
        context.update({'title': 'Update Service'})
        return super(UpdateView, self).render_to_response(context)

    def form_valid(self, form):
        obj = form.save(commit=True)
        user = g.GallantUser.objects.get(id=self.request.user.id)
        text = '[Updated]\n' + form.cleaned_data['notes']
        note = g.Note.objects.create(text=text, created_by=user)
        obj.notes.add(note)
        obj.save()
        return HttpResponseRedirect(reverse('service_detail', args=[obj.id]))


def client_detail(request, pk):
    client = get_object_or_404(g.Client, pk=pk)

    if request.method == 'POST':
        form = forms.NoteForm(request.POST)
        if form.is_valid():
            user = g.GallantUser.objects.get(id=request.user.id)
            note = g.Note.objects.create(text=form.cleaned_data['text'], created_by=user)
            client.notes.add(note)
            client.save()
            return HttpResponseRedirect(reverse('client_detail', args=[client.id]))
    else:
        form = forms.NoteForm()  # An unbound form

    return render(request, 'gallant/client_detail.html', {
        'object': client,
        'form': form,
    })


class ServiceCreate(CreateView):
    form_class = forms.ServiceForm
    template_name = "gallant/create_form.html"

    def render_to_response(self, context, **response_kwargs):
        context.update({'title': 'Add Service'})
        return super(CreateView, self).render_to_response(context)

    def form_valid(self, form):
        obj = form.save(commit=True)
        user = g.GallantUser.objects.get(id=self.request.user.id)
        text = '[Created]\n' + form.cleaned_data['notes']
        note = g.Note.objects.create(text=text, created_by=user)
        obj.notes.add(note)
        obj.save()
        return HttpResponseRedirect(reverse('service_detail', args=[obj.id]))


def service_detail(request, pk):
    service = get_object_or_404(g.Service, pk=pk)

    if request.method == 'POST':
        form = forms.NoteForm(request.POST)
        if form.is_valid():
            user = g.GallantUser.objects.get(id=request.user.id)
            note = g.Note.objects.create(text=form.cleaned_data['text'], created_by=user)
            service.notes.add(note)
            service.save()
            return HttpResponseRedirect(reverse('service_detail', args=[service.id]))
    else:
        form = forms.NoteForm()

    return render(request, 'gallant/service_detail.html', {
        'object': service,
        'form': form,
    })
