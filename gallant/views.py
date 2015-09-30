from itertools import chain
import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Count
from django.http.response import Http404, HttpResponse
from django.utils.safestring import mark_safe
from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from gallant import forms
from gallant import models as g
from quotes import models as q
from briefs import models as b
from gallant.utils import get_one_or_404, get_site_from_host
from django.utils.translation import ugettext_lazy as _


class ClientList(View):
    def get(self, request):
        request.breadcrumbs(_('Clients'), request.path_info)
        return TemplateResponse(request=request,
                                template="gallant/client_list.html",
                                context={'title': 'Clients',
                                         'object_list': g.Client.objects.all_for(request.user, 'view_client')})


class ClientUpdate(View):
    def get(self, request, **kwargs):
        self.object = get_one_or_404(request.user, 'change_client', g.Client, pk=kwargs['pk'])
        form = forms.ClientForm(request.user, instance=self.object)
        return self.render_to_response({'object': self.object, 'form': form,
                                        'contact_form': forms.ContactInfoForm(
                                            instance=self.object.contact_info),
                                        'note_form': forms.NoteForm(request.user)})

    def post(self, request, **kwargs):
        if 'pk' in kwargs:
            self.object = get_one_or_404(request.user, 'change_client', g.Client, pk=kwargs['pk'])
        else:
            # No perms currently needed to create
            self.object = None

        form = forms.ClientForm(request.user, request.POST, instance=self.object)
        contact_form = forms.ContactInfoForm(request.POST,
                                             instance=getattr(self.object, 'contact_info', None))
        note_form = forms.NoteForm(request.user, request.POST)

        if form.is_valid() and contact_form.is_valid():
            return self.form_valid(form, contact_form, note_form)
        else:
            response = {'status': 0, 'errors': chain(form.errors.items(), contact_form.errors.items())}
            return HttpResponse(json.dumps(response), content_type='application/json')

    def render_to_response(self, context):
        context.update({'title': 'Edit Client'})

        self.request.breadcrumbs(_('Clients'), reverse('clients'))
        if self.object:
            self.request.breadcrumbs([(_(self.object.name), reverse('client_detail', args=[self.object.id])),
                                      (_('Edit'), self.request.path_info)])
        else:
            self.request.breadcrumbs(_('Add'), self.request.path_info)
        return TemplateResponse(request=self.request,
                                template="gallant/client_form.html",
                                context=context)

    def form_valid(self, form, contact_form, note_form):
        obj = form.save(commit=True)
        if note_form.is_valid():
            note = note_form.save()
        else:
            note = g.Note.objects.create(user=obj.user)
        note.text = '[Updated]\n' + note.text
        note.save()
        obj.notes.add(note)
        obj.contact_info = contact_form.save()
        obj.save()
        messages.success(self.request, 'Client saved.')
        response = {'status': 0, 'redirect': reverse('client_detail', args=[obj.id])}
        return HttpResponse(json.dumps(response), content_type='application/json')


class ClientCreate(ClientUpdate):
    def get(self, request):
        self.object = None
        request.breadcrumbs([(_('Clients'), reverse('clients')),
                             (_('Add'), request.path_info)])
        form = forms.ClientForm(request.user)
        context = {'form': form,
                   'contact_form': forms.ContactInfoForm(),
                   'note_form': forms.NoteForm(request.user),
                   'title': 'Add Client'}
        return TemplateResponse(request=self.request,
                                template="gallant/client_form.html",
                                context=context)


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

    request.breadcrumbs([(_('Clients'), reverse('clients')),
                         (_(client.name), reverse('client_detail', args=[client.id]))])

    return TemplateResponse(request=request,
                            template="gallant/client_detail.html",
                            context={'object': client, 'form': form,
                                     'template_list': b.BriefTemplate.objects
                                                       .all_for(request.user, 'view_brieftemplate'),'title': client.name })


class ClientDelete(View):
    def get(self, request, **kwargs):
        client = get_one_or_404(request.user, 'change_client', g.Client, id=kwargs['pk'])
        client.soft_delete()

        return HttpResponseRedirect(reverse('clients'))


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


class ProjectList(View):
    def get(self, request):
        projects = g.Project.objects.all_for(request.user, 'view_project')
        quotes = q.Quote.objects.all_for(request.user, 'view_quote').annotate(projects_count=Count('projects')).filter(projects_count=0, status=5)

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
            for quote in self.object.quote_set.all_for(request.user, 'view_quote'):
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
                                template="gallant/create_form.html",
                                context=context)

    def form_valid(self, form, quotes_to_link, quotes_to_unlink):
        obj = form.save(commit=True)
        text = '[Updated]\n'
        note = g.Note.objects.create(text=text, user=self.request.user)
        obj.notes.add(note)

        # Link new quotes
        for quote_id in quotes_to_link:
            quote = q.Quote.objects.get_for(self.request.user, 'change_quote', id=quote_id)
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
        if len(obj.quote_set.all_for(self.request.user, 'view_quote')) is 0:
            quote = q.Quote.objects.get_for(self.request.user, 'change_quote', id=self.kwargs['quote_id'])
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
                                template="gallant/create_form.html",
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
    for quote in project.quote_set.all_for(request.user, 'view_quote'):
        for service in quote.services.all_for(request.user, 'view_servicesection'):
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


def _send_signup_request_email(form):
    message = 'Name: %s\nEmail: %s\nCompany: %s\nAbout:\n%s\n' % (
        form.cleaned_data['name'],
        form.cleaned_data['email'],
        form.cleaned_data['company'],
        form.cleaned_data['description'],
    )
    send_mail('Signup request', message, settings.EMAIL_HOST_USER,
              ['contact@galant.co'], fail_silently=False)


def _send_feedback_email(form, path):
    user = form.request.user
    message = 'User Email: %s\nFeedback:\n%s\n\nUserAgent: %s\nURL: %s\nCookies: %s\n' % (
        user.email if user.is_authenticated() else form.cleaned_data['email'],
        form.cleaned_data['feedback'],
        form.request.META['HTTP_USER_AGENT'],
        path,
        form.request.COOKIES,
    )
    send_mail('User feedback', message, settings.EMAIL_HOST_USER,
              ['contact@galant.co'], fail_silently=False)


class SignUpRequest(View):
    @staticmethod
    def get(request):
        request.breadcrumbs([(_('Request Account'), request.path_info)])
        return render(request, 'gallant/create_form.html', {
            'form': forms.SignUpRequestForm(),
            'title': 'Request Account',
            'submit_text': 'Submit'
        })

    @staticmethod
    def post(request):
        request.breadcrumbs([(_('Request Account'), request.path_info)])
        form = forms.SignUpRequestForm(request.POST)

        if form.is_valid():
            _send_signup_request_email(form)
            messages.success(request, 'Request sent.')
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'gallant/create_form.html', {
                'form': forms.SignUpRequestForm(),
                'title': 'Request Account',
                'submit_text': 'Submit'
            })


class SubmitFeedback(View):
    @staticmethod
    def get(request):
        app_title = request.GET.get('app_title', None)
        return render(request, 'gallant/form.html', {
            'form': forms.FeedbackForm(request, app_title),
            'submit_text': 'Submit'
        })

    @staticmethod
    def post(request):
        path = request.GET.get('path', None)
        form = forms.FeedbackForm(request, None, request.POST)

        if form.is_valid():
            _send_feedback_email(form, path)
            messages.success(request, 'Feedback sent.')
            return HttpResponse('Thank you.')
        else:
            return render(request, 'gallant/create_form.html', {
                'form': forms.SignUpRequestForm(),
                'submit_text': 'Submit'
            })


def contact(request):
    site = get_site_from_host(request)
    return render(request, 'content.html', {
        'content': mark_safe('<p class="sub-main">Send feedback or questions to <a href="mailto:contact@{0}">contact@{0}</a></p>'.format(site))
    })


class Register(View):
    @staticmethod
    def get(request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        valid = default_token_generator.check_token(user, request.GET.get('token', None))

        if valid:
            return render(request, 'gallant/register_form.html', {
                'set_password_form': SetPasswordForm(user),
                'form': forms.GallantUserForm(instance=user),
                'contact_form': forms.ContactInfoForm(instance=user.contact_info or None)
            })
        else:
            raise Http404()

    @staticmethod
    def post(request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        valid = default_token_generator.check_token(user, request.GET.get('token', None))

        if valid:
            form = forms.GallantUserForm(request.POST, instance=user)
            contact_form = forms.ContactInfoForm(request.POST, instance=user.contact_info)
            set_password_form = SetPasswordForm(user, request.POST)

            if form.is_valid() and contact_form.is_valid() and set_password_form.is_valid():
                u = form.save()
                set_password_form.save()
                u.contact_info = contact_form.save()
                u.save()
                messages.success(request, 'Registration successful.')

                # Login new user after registration
                new_user = authenticate(username=u.email, password=request.POST['new_password1'])
                login(request, new_user)

                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'gallant/register_form.html', {
                    'set_password_form': set_password_form,
                    'form': form,
                    'contact_form': contact_form
                })
        else:
            raise Http404()


def _send_register_email(email, link):
    message = 'Your registration is almost complete. Click on this link to create an account: %s' % link
    send_mail('Signup request', message, settings.EMAIL_HOST_USER,
              [email], fail_silently=False)


class AccountAdd(View):
    @staticmethod
    def get(request):
        if not request.user.is_superuser:
            messages.error(request, 'You don\'t have permission to access that view.')
            return HttpResponseRedirect(reverse('home'))

        return render(request, 'gallant/create_form.html', {
            'form': forms.EmailForm(),
        })

    @staticmethod
    def post(request):
        if not request.user.is_superuser:
            messages.error(request, 'You don\'t have permission to access that view.')
            return HttpResponseRedirect(reverse('home'))

        form = forms.EmailForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            UserModel = get_user_model()
            user = UserModel.objects.create_user(email=email)
            token = default_token_generator.make_token(user)
            link = 'http://' + request.get_host() + \
                   reverse('register', args=[user.id]) + '?token=%s' % token

            _send_register_email(email, link)
            messages.success(request, 'Registration link sent.')
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'gallant/create_form.html', {
                'form': forms.EmailForm(),
            })


def _send_reset_email(email, link):
    message = 'Click this link to reset your password: %s\n\nIgnore this email if you didn\'t ask for a password reset.'  % link
    send_mail('Password reset', message, settings.EMAIL_HOST_USER,
              [email], fail_silently=False)


class PasswordReset(View):
    @staticmethod
    def get(request):
        if not request.user.is_superuser:
            messages.error(request, 'You don\'t have permission to access that view.')
            return HttpResponseRedirect(reverse('home'))

        return render(request, 'gallant/create_form.html', {
            'form': forms.EmailForm(),
        })

    @staticmethod
    def post(request):
        if not request.user.is_superuser:
            messages.error(request, 'You don\'t have permission to access that view.')
            return HttpResponseRedirect(reverse('home'))

        form = forms.EmailForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            UserModel = get_user_model()
            user = UserModel.objects.get(email=email)
            token = default_token_generator.make_token(user)
            link = 'http://' + request.get_host() + \
                   reverse('register', args=[user.id]) + '?token=%s' % token

            _send_reset_email(email, link)
            messages.success(request, 'Password reset link sent.')
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'gallant/create_form.html', {
                'form': forms.EmailForm(),
            })
