from django.contrib import messages
from django.db.models import Count
from django.http.response import JsonResponse
from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from gallant import forms
from gallant import models as g
from gallant.serializers.project import ProjectSerializer
from quotes import models as q
from gallant.utils import get_one_or_404, GallantObjectPermissions, get_field_choices, GallantViewSetPermissions
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, viewsets


class ProjectList(View):
    def get(self, request):
        projects = g.Project.objects.all_for(request.user)
        quotes = q.Quote.objects.all_for(request.user).annotate(projects_count=Count('projects')).filter(
            projects_count=0, status=5)

        request.breadcrumbs(_('Projects'), request.path_info)

        return TemplateResponse(request=request,
                                template="gallant/project_list.html",
                                context={'title': 'Projects',
                                         'object_list': projects,
                                         'quote_list': quotes})


class ProjectUpdate(View):
    def get(self, request, **kwargs):
        self.object = get_one_or_404(request.user, 'change_project', g.Project, pk=kwargs['pk'])
        form = forms.ProjectOnlyForm(request.user, instance=self.object)
        return self.render_to_response({'object': self.object, 'form': form})

    def post(self, request, **kwargs):
        quotes_to_link = []
        quotes_to_unlink = []

        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'change_project', g.Project, pk=kwargs['pk'])

            # Quotes to link to project
            for quote in request.POST.getlist('available_quotes', None):
                quotes_to_link.append(int(quote))

            # Quotes to unlink to project
            for quote in self.object.quote_set.all_for(request.user):
                if request.POST.getlist('linked_quotes', None):
                    if "%s" % quote.id not in request.POST.getlist('linked_quotes'):
                        quotes_to_unlink.append(quote)
                else:
                    quotes_to_unlink.append(quote)

        else:
            # No perms currently needed to create
            self.object = None

        form = forms.ProjectOnlyForm(request.user, request.POST, instance=self.object)

        if form.is_valid():
            return self.form_valid(form, quotes_to_link, quotes_to_unlink)
        else:
            return self.render_to_response({'object': self.object, 'form': form})

    def render_to_response(self, context):
        context.update({'title': 'Edit Project'})

        self.request.breadcrumbs(_('Projects'), reverse('projects'))
        if self.object:
            self.request.breadcrumbs([(_('Project: %s' % self.object.name),
                                       reverse('project_detail', args=[self.object.id])),
                                      (_('Edit'), self.request.path_info)])
        else:
            self.request.breadcrumbs(_('Add'), self.request.path_info)
        return TemplateResponse(request=self.request,
                                template="gallant/base_form.html",
                                context=context)

    def form_valid(self, form, quotes_to_link, quotes_to_unlink):
        obj = form.save(commit=True)
        text = '[Updated]\n'
        note = g.Note.objects.create(text=text, user=self.request.user)
        obj.notes.add(note)

        # Link new quotes
        for quote_id in quotes_to_link:
            quote = q.Quote.objects.get_for(self.request.user, 'change', id=quote_id)
            quote.projects.add(obj)
            quote.save()

            text = '[Linked Quote: %s ]\n' % quote
            note = g.Note.objects.create(text=text, user=self.request.user)
            obj.notes.add(note)

        # Unlink actual quotes
        for quote in quotes_to_unlink:
            quote.projects.remove(obj)

            text = '[Unlinked Quote: %s]\n' % quote
            note = g.Note.objects.create(text=text, user=self.request.user)
            obj.notes.add(note)

        # If its a new project
        if len(obj.quote_set.all_for(self.request.user)) is 0:
            quote = q.Quote.objects.get_for(self.request.user, 'change', id=self.kwargs['quote_id'])
            quote.projects.add(obj)
            quote.save()

        obj.save()

        messages.success(self.request, 'Project saved.')
        return HttpResponseRedirect(reverse('project_detail', args=[obj.id]))


class ProjectCreate(ProjectUpdate):
    def get(self, request, **kwargs):
        form = forms.ProjectOnlyForm(request.user)
        request.breadcrumbs([(_('Projects'), reverse('projects')),
                             (_('Add'), request.path_info)])

        context = {'title': 'Add Project', 'form': form}
        return TemplateResponse(request=self.request,
                                template="gallant/base_form.html",
                                context=context)


class ProjectDelete(View):
    def get(self, request, **kwargs):
        project = get_one_or_404(request.user, 'change_project', g.Project, id=kwargs['pk'])
        project.soft_delete()

        return HttpResponseRedirect(reverse('projects'))


def project_detail(request, pk):
    project = get_one_or_404(request.user, 'view_project', g.Project, pk=pk)

    # TODO: This should be refactored!
    services = []
    for quote in project.quote_set.all_for(request.user):
        for service in quote.services.all_for(request.user):
            services.append(service)

    if request.method == 'POST' and request.user.has_perm('change_project', project):
        form = forms.NoteForm(request.user, request.POST)
        if form.is_valid():
            note = g.Note.objects.create(text=form.cleaned_data['text'], user=request.user)
            project.notes.add(note)
            project.save()
            return HttpResponseRedirect(reverse('project_detail', args=[project.id]))
    else:
        form = forms.NoteForm(request.user)

    request.breadcrumbs([(_('Projects'), reverse('projects')),
                         (_('Project: %s' % project.name), request.path_info)])
    return render(request, 'gallant/project_detail.html', {
        'object': project,
        'services': services,
        'form': form,
        'title': 'Project Detail',
    })


class ProjectDetailAPI(generics.RetrieveUpdateAPIView):
    model = g.Project
    serializer_class = ProjectSerializer
    permission_classes = [
        GallantObjectPermissions
    ]

    def get_queryset(self):
        return self.model.objects.all_for(self.request.user)


def project_fields_json(request):
    return JsonResponse(get_field_choices(g.Project), safe=False)


class ProjectsAPI(viewsets.ModelViewSet):
    model = g.Project
    serializer_class = ProjectSerializer
    permission_classes = [
        GallantViewSetPermissions
    ]

    def get_queryset(self):
        client = self.request.GET.get('client_id', None)
        if client:
            quotes = q.Quote.objects.all_for(self.request.user).filter(status=5, client_id=client)
            return self.model.objects.all_for(self.request.user).filter(user_id=self.request.user, quote__in=quotes)
        elif self.request.user.is_superuser:
            return self.model.objects.all_for(self.request.user)
        else:
            return self.model.objects.all_for(self.request.user).filter(user_id=self.request.user)