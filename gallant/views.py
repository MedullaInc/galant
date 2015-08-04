from django.contrib import messages
from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from gallant import forms
from gallant import models as g


class ClientList(View):
    def get(self, request):
        return TemplateResponse(request=request,
                                template="gallant/client_list.html",
                                context={'title': 'Clients', 'object_list': g.Client.objects.all()})


class ClientUpdate(View):
    def get(self, request, **kwargs):
        self.object = get_object_or_404(g.Client, pk=kwargs['pk'])
        form = forms.ClientForm(request.user, instance=self.object)
        return self.render_to_response({'object': self.object, 'form': form})

    def post(self, request, **kwargs):
        if 'pk' in kwargs:
            self.object = get_object_or_404(g.Client, pk=kwargs['pk'])
        else:
            self.object = None

        form = forms.ClientForm(request.user, request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.render_to_response({'object': self.object, 'form': form})

    def render_to_response(self, context):
        context.update({'title': 'Update Client'})
        return TemplateResponse(request=self.request,
                                template="gallant/create_form.html",
                                context=context)

    def form_valid(self, form):
        obj = form.save(commit=True)
        user = g.GallantUser.objects.get(id=self.request.user.id)
        text = '[Updated]\n' + form.cleaned_data['notes']
        note = g.Note.objects.create(text=text, user=user)
        obj.notes.add(note)
        obj.save()
        messages.success(self.request, 'Client saved.')
        return HttpResponseRedirect(reverse('client_detail', args=[obj.id]))


class ClientCreate(ClientUpdate):
    def get(self, request):
        self.object = None
        return self.render_to_response({'form': forms.ClientForm(request.user)})


class ServiceUpdate(View):
    def get(self, request, **kwargs):
        self.object = get_object_or_404(g.Service, pk=kwargs['pk'])
        form = forms.ServiceForm(request.user, instance=self.object)
        return self.render_to_response({'object': self.object, 'form': form})

    def post(self, request, **kwargs):
        if 'pk' in kwargs:
            self.object = get_object_or_404(g.Service, pk=kwargs['pk'])
        else:
            self.object = None

        form = forms.ServiceForm(request.user, request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.render_to_response({'object': self.object, 'form': form})

    def render_to_response(self, context):
        context.update({'title': 'Update Service'})
        return TemplateResponse(request=self.request,
                                template="gallant/create_form.html",
                                context=context)

    def form_valid(self, form):
        obj = form.save(commit=True)
        user = g.GallantUser.objects.get(id=self.request.user.id)
        text = '[Updated]\n' + form.cleaned_data['notes']
        note = g.Note.objects.create(text=text, user=user)
        obj.notes.add(note)
        obj.save()
        messages.success(self.request, 'Service saved.')
        return HttpResponseRedirect(reverse('service_detail', args=[obj.id]))


def client_detail(request, pk):
    client = get_object_or_404(g.Client, pk=pk)

    if request.method == 'POST':
        form = forms.NoteForm(request.user, request.POST)
        if form.is_valid():
            user = g.GallantUser.objects.get(id=request.user.id)
            note = g.Note.objects.create(text=form.cleaned_data['text'], user=user)
            client.notes.add(note)
            client.save()
            return HttpResponseRedirect(reverse('client_detail', args=[client.id]))
    else:
        form = forms.NoteForm(request.user)  # An unbound form

    return TemplateResponse(request=request,
                            template="gallant/client_detail.html",
                            context={'object': client, 'form': form})


class ServiceCreate(ServiceUpdate):
    def get(self, request):
        form = forms.ServiceForm(request.user)
        return self.render_to_response({'form': form})


def service_detail(request, pk):
    service = get_object_or_404(g.Service, pk=pk)

    if request.method == 'POST':
        form = forms.NoteForm(request.user, request.POST)
        if form.is_valid():
            user = g.GallantUser.objects.get(id=request.user.id)
            note = g.Note.objects.create(text=form.cleaned_data['text'], user=user)
            service.notes.add(note)
            service.save()
            return HttpResponseRedirect(reverse('service_detail', args=[service.id]))
    else:
        form = forms.NoteForm(request.user)

    return render(request, 'gallant/service_detail.html', {
        'object': service,
        'form': form,
    })
