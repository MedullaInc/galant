from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http.response import Http404, HttpResponse
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from gallant import forms, serializers
from gallant.utils import get_site_from_host, GallantViewSetPermissions
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from calendr.models import Task
from rest_framework.response import Response
from django.template.loader import render_to_string


def _send_signup_request_email(form):
    message = 'Name: %s\nEmail: %s\nCompany: %s\nAbout:\n%s\n' % (
        form.cleaned_data.get('name', '-'),
        form.cleaned_data.get('email'),
        form.cleaned_data.get('company', '-'),
        form.cleaned_data.get('description', '-'),
    )
    send_mail('Signup request', message, settings.EMAIL_HOST_USER,
              ['signup@galant.com'], fail_silently=False)


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


class Home(View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('user_dashboard'))
        else:
            return TemplateResponse(request=request,
                                    template="index.html",
                                    context={'title': 'Home'})


class UserDashboard(View):
    def get(self, request):
        request.breadcrumbs([('Dashboard', request.path_info)])
        return TemplateResponse(request=request,
                                template="gallant/user_dashboard.html",
                                context={'title': 'Dashboard'})


class SignUpRequest(View):
    @staticmethod
    def get(request):
        request.breadcrumbs([(_('Request Account'), request.path_info)])
        return render(request, 'gallant/base_form.html', {
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
            messages.success(request, 'Request sent. We\'ll contact you soon!')
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'gallant/base_form.html', {
                'form': form,
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
            return render(request, 'gallant/base_form.html', {
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
                'title': 'Register',
                'set_password_form': forms.GallantSetPasswordForm(user),
                'form': forms.GallantUserForm(instance=user)
            })
        else:
            raise Http404()

    @staticmethod
    def post(request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        valid = default_token_generator.check_token(user, request.GET.get('token', None))

        if valid:
            form = forms.GallantUserForm(request.POST, instance=user)
            set_password_form = forms.GallantSetPasswordForm(user, request.POST)

            if form.is_valid() and set_password_form.is_valid():
                u = form.save()
                set_password_form.save()
                u.save()
                messages.success(request, 'Registration successful.')

                # Login new user after registration
                new_user = authenticate(username=u.email, password=request.POST['new_password1'])
                login(request, new_user)

                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'gallant/register_form.html', {
                    'title': 'Register',
                    'set_password_form': set_password_form,
                    'form': form
                })
        else:
            raise Http404()


def _send_register_email(email, link):
    message = render_to_string('gallant/beta_tester_email.txt', {'link': link})
    send_mail('Signup request', message, settings.EMAIL_HOST_USER,
              [email], fail_silently=False)


class AccountAdd(View):
    @staticmethod
    def get(request):
        if not request.user.is_superuser:  # pragma: no cover
            messages.error(request, 'You don\'t have permission to access that view.')
            return HttpResponseRedirect(reverse('home'))

        return render(request, 'gallant/base_form.html', {
            'form': forms.EmailForm(),
        })

    @staticmethod
    def post(request):
        if not request.user.is_superuser:  # pragma: no cover
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
            return render(request, 'gallant/base_form.html', {
                'form': forms.EmailForm(),
            })


def _send_reset_email(email, link):
    message = 'Click this link to reset your password: %s\n\nIgnore this email if you didn\'t ask for a password reset.'  % link
    send_mail('Password reset', message, settings.EMAIL_HOST_USER,
              [email], fail_silently=False)


class PasswordReset(View):
    @staticmethod
    def get(request):
        if not request.user.is_superuser:  # pragma: no cover
            messages.error(request, 'You don\'t have permission to access that view.')
            return HttpResponseRedirect(reverse('home'))

        return render(request, 'gallant/base_form.html', {
            'form': forms.EmailForm(),
        })

    @staticmethod
    def post(request):
        if not request.user.is_superuser:  # pragma: no cover
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
            return render(request, 'gallant/base_form.html', {
                'form': forms.EmailForm(),
            })


class UsersAPI(generics.ListAPIView):
    model = get_user_model()
    serializer_class = serializers.UserModelSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        project = self.request.GET.get('project_id', None)
        user = self.request.user

        if user.is_superuser:
            qs = self.model.objects.filter(is_active=True, pk__gte=0)
        elif user.agency_group:
            qs = self.model.objects.filter(is_active=True, pk__gte=0, agency_group=user.agency_group)
        else:
            qs = self.model.objects.filter(is_active=True, pk=user.pk)

        if project:
            assignee_ids = Task.objects.filter(project_id=project).values('assignee').distinct()
            return qs.filter(pk__in=assignee_ids)
        else:
            return qs


class UserModelViewSet(viewsets.ModelViewSet):
    permission_classes = [
        GallantViewSetPermissions
    ]

    def get_queryset(self):
        return self.model.objects.all_for(self.request.user)

    def create(self, request, *args, **kwargs):
        response = super(UserModelViewSet, self).create(request, *args, **kwargs)
        self.request._messages.add(messages.SUCCESS, '%s saved.' % self.model._meta.model_name.title())
        if response.status_code == status.HTTP_201_CREATED:
            response.data['redirect'] = reverse('%s_detail' % self.model._meta.model_name, args=[response.data['id']])
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        self.request._messages.add(messages.SUCCESS, '%s deleted.' % self.model._meta.model_name.title())
        return Response({'status': 0, 'redirect':
                         reverse('%ss' % self.model._meta.model_name)})
