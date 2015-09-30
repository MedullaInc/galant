from django.contrib import messages
from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from gallant import forms
from gallant import models as g
from gallant.utils import get_one_or_404
from django.utils.translation import ugettext_lazy as _


class ServiceUpdate(View):
    def get(self, request, **kwargs):
        self.object = get_one_or_404(request.user, 'change_service', g.Service, pk=kwargs['pk'])
        form = forms.ServiceOnlyForm(request.user, instance=self.object)
        return self.render_to_response({'object': self.object, 'form': form})

    def post(self, request, **kwargs):
        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'change_service', g.Service, pk=kwargs['pk'])
        else:
            # No perms currently needed to create
            self.object = None

        form = forms.ServiceOnlyForm(request.user, request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.render_to_response({'object': self.object, 'form': form})

    def render_to_response(self, context):
        context.update({'title': 'Edit Service'})

        project = get_one_or_404(self.request.user, 'view_project', g.Project, pk=self.kwargs['project_id'])

        self.request.breadcrumbs([(_('Projects'), reverse('projects')),
                                  (_('Project: %s' % project), reverse('project_detail', args=[self.kwargs['project_id']])),
                                  (_('Service: %s' % self.object.name.get_text()),reverse('service_detail', args=[self.kwargs['project_id'], self.kwargs['pk']])),
                                  (_('Edit'), reverse('edit_service', args=[self.kwargs['project_id'], self.kwargs['pk']]))
                                  ])

        return TemplateResponse(request=self.request,
                                template="gallant/service_form.html",
                                context=context)

    def form_valid(self, form):
        obj = form.save(commit=True)
        text = '[Updated]\n'
        note = g.Note.objects.create(text=text, user=self.request.user)
        obj.notes.add(note)
        obj.save()

        messages.success(self.request, 'Service saved.')
        return HttpResponseRedirect(reverse('service_detail', args=[self.kwargs['project_id'], obj.id]))


class ServiceCreate(ServiceUpdate):
    def get(self, request, *args, **kwargs):
        form = forms.ServiceOnlyForm(request.user)
        return self.render_to_response({'form': form})

    def render_to_response(self, context):
        context.update({'title': 'Edit Service'})

        project = get_one_or_404(self.request.user, 'view_project', g.Project, pk=self.kwargs['project_id'])

        self.request.breadcrumbs([(_('Projects'), reverse('projects')),
                                  (_('Project: %s' % project),
                                   reverse('project_detail', args=[self.kwargs['project_id']])),
                                  (_('Add Service'), reverse('add_service', args=[self.kwargs['project_id']]))
                                  ])

        return TemplateResponse(request=self.request,
                                template="gallant/service_form.html",
                                context=context)


def service_detail(request, *args, **kwargs):
    service = get_one_or_404(request.user, 'view_service', g.Service, pk=kwargs['pk'])
    project = get_one_or_404(request.user, 'view_project', g.Project, pk=kwargs['project_id'])

    request.breadcrumbs([(_('Projects'), reverse('projects')),
                         (_('Project: %s' % project), reverse('project_detail', args=[kwargs['project_id']])),
                         (_('Service: %s' % service.name.get_text()), reverse('service_detail', args=[kwargs['project_id'], kwargs['pk']]))
                         ])

    if request.method == 'POST' and request.user.has_perm('change_service', service):
        form = forms.NoteForm(request.user, request.POST)
        if form.is_valid():
            note = g.Note.objects.create(text=form.cleaned_data['text'], user=request.user)
            service.notes.add(note)
            service.save()
            return HttpResponseRedirect(reverse('service_detail', args=[kwargs['project_id'], service.id]))
    else:
        form = forms.NoteForm(request.user)

    return render(request, 'gallant/service_detail.html', {
        'title': 'Project Service',
        'object': service,
        'project': project,
        'form': form,
    })

