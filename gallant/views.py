from django.contrib import messages
from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from gallant import forms
from gallant import models as g
from quotes import models as q
from gallant.utils import get_one_or_404


class ClientList(View):
    def get(self, request):
        return TemplateResponse(request=request,
                                template="gallant/client_list.html",
                                context={'title': 'Clients',
                                         'object_list': g.Client.objects.all_for(request.user, 'view_client')})


class ClientUpdate(View):
    def get(self, request, **kwargs):
        self.object = get_one_or_404(request.user, 'change_client', g.Client, pk=kwargs['pk'])
        form = forms.ClientForm(request.user, instance=self.object)
        return self.render_to_response({'object': self.object, 'form': form})

    def post(self, request, **kwargs):
        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'change_client', g.Client, pk=kwargs['pk'])
        else:
            # No perms currently needed to create
            self.object = None

        form = forms.ClientForm(request.user, request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.render_to_response({'object': self.object, 'form': form})

    def render_to_response(self, context):
        context.update({'title': 'Edit Client'})
        return TemplateResponse(request=self.request,
                                template="gallant/create_form.html",
                                context=context)

    def form_valid(self, form):
        obj = form.save(commit=True)
        text = '[Updated]\n' + form.cleaned_data['notes']
        note = g.Note.objects.create(text=text, user=self.request.user)
        obj.notes.add(note)
        obj.save()
        messages.success(self.request, 'Client saved.')
        return HttpResponseRedirect(reverse('client_detail', args=[obj.id]))


class ClientCreate(ClientUpdate):
    def get(self, request):
        self.object = None
        return self.render_to_response({'form': forms.ClientForm(request.user)})


def client_detail(request, pk):
    client = get_one_or_404(request.user, 'view_client', g.Client, pk=pk)

    if request.method == 'POST' and request.user.has_perm('change_client', client):
        form = forms.NoteForm(request.user, request.POST)
        if form.is_valid():
            note = g.Note.objects.create(text=form.cleaned_data['text'], user=request.user)
            client.notes.add(note)
            client.save()
            return HttpResponseRedirect(reverse('client_detail', args=[client.id]))
    else:
        form = forms.NoteForm(request.user)  # An unbound form

    return TemplateResponse(request=request,
                            template="gallant/client_detail.html",
                            context={'object': client, 'form': form})


class ServiceUpdate(View):
    def get(self, request, **kwargs):
        self.object = get_one_or_404(request.user, 'change_service', g.Service, pk=kwargs['pk'])
        form = forms.ServiceForm(request.user, instance=self.object)
        return self.render_to_response({'object': self.object, 'form': form})

    def post(self, request, **kwargs):
        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'change_service', g.Service, pk=kwargs['pk'])
        else:
            # No perms currently needed to create
            self.object = None

        form = forms.ServiceForm(request.user, request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.render_to_response({'object': self.object, 'form': form})

    def render_to_response(self, context):
        context.update({'title': 'Edit Service'})
        return TemplateResponse(request=self.request,
                                template="gallant/create_form.html",
                                context=context)

    def form_valid(self, form):
        obj = form.save(commit=True)
        text = '[Updated]\n' + form.cleaned_data['notes']
        note = g.Note.objects.create(text=text, user=self.request.user)
        obj.notes.add(note)
        obj.save()
        messages.success(self.request, 'Service saved.')
        return HttpResponseRedirect(reverse('service_detail', args=[obj.id]))


class ServiceCreate(ServiceUpdate):
    def get(self, request):
        form = forms.ServiceForm(request.user)
        return self.render_to_response({'form': form})


def service_detail(request, pk):
    service = get_one_or_404(request.user, 'view_service', g.Service, pk=pk)

    if request.method == 'POST' and request.user.has_perm('change_service', service):
        form = forms.NoteForm(request.user, request.POST)
        if form.is_valid():
            note = g.Note.objects.create(text=form.cleaned_data['text'], user=request.user)
            service.notes.add(note)
            service.save()
            return HttpResponseRedirect(reverse('service_detail', args=[service.id]))
    else:
        form = forms.NoteForm(request.user)

    return render(request, 'gallant/service_detail.html', {
        'object': service,
        'form': form,
    })



class ProjectUpdate(View):
    def get(self, request, **kwargs):
        self.object = get_one_or_404(request.user, 'change_project', g.Project, pk=kwargs['pk'])
        form = forms.ProjectForm(request.user, instance=self.object)
        return self.render_to_response({'object': self.object, 'form': form})

    def post(self, request, **kwargs):
        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'change_project', g.Project, pk=kwargs['pk'])
        else:
            # No perms currently needed to create
            self.object = None

        form = forms.ProjectForm(request.user, request.POST, instance=self.object)
        if form.is_valid():
            if 'quote_id' in kwargs:
                quote = get_one_or_404(request.user, 'view_quote', q.Quote, pk=kwargs['quote_id'])
                return self.form_valid(form, quote)
            else:
                return self.form_valid(form)
        else:
            return self.render_to_response({'object': self.object, 'form': form})

    def render_to_response(self, context):
        context.update({'title': 'Edit Project'})
        return TemplateResponse(request=self.request,
                                template="gallant/create_form.html",
                                context=context)

    def form_valid(self, form, quote=None):
        obj = form.save(commit=True)
        text = '[Updated]\n' + form.cleaned_data['notes']
        note = g.Note.objects.create(text=text, user=self.request.user)
        obj.notes.add(note)
        if quote:
            quote.project = obj
            quote.save()
        obj.save()
        messages.success(self.request, 'Project saved.')
        return HttpResponseRedirect(reverse('project_detail', args=[obj.id]))


class ProjectCreate(ProjectUpdate):
    def get(self, request, **kwargs):
        form = forms.ProjectForm(request.user)
        return self.render_to_response({'form': form})


def project_detail(request, pk):
    project = get_one_or_404(request.user, 'view_project', g.Project, pk=pk)

    if request.method == 'POST' and request.user.has_perm('change_project', project):
        form = forms.NoteForm(request.user, request.POST)
        if form.is_valid():
            note = g.Note.objects.create(text=form.cleaned_data['text'], user=request.user)
            project.notes.add(note)
            project.save()
            return HttpResponseRedirect(reverse('project_detail', args=[project.id]))
    else:
        form = forms.NoteForm(request.user)

    return render(request, 'gallant/project_detail.html', {
        'object': project,
        'form': form,
    })
