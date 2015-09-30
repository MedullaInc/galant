from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http.response import Http404, HttpResponse
from django.utils.safestring import mark_safe
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from gallant import forms
from gallant.utils import get_site_from_host
from django.utils.translation import ugettext_lazy as _


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
            messages.success(request, 'Request sent.')
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'gallant/base_form.html', {
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

        return render(request, 'gallant/base_form.html', {
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
        if not request.user.is_superuser:
            messages.error(request, 'You don\'t have permission to access that view.')
            return HttpResponseRedirect(reverse('home'))

        return render(request, 'gallant/base_form.html', {
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
            return render(request, 'gallant/base_form.html', {
                'form': forms.EmailForm(),
            })