from django.views.generic import View
from django.core.urlresolvers import reverse
from market_analysis import forms
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from experiments.utils import participant
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.db import SessionStore as DatabaseSession, SessionStore


class LandingPage(View):
    def get(self, request, **kwargs):
        form = forms.CustomerLeadModelForm()
        return TemplateResponse(request=request,
                                template="market_analysis/landing.html",
                                context={'form': form})


class LandingPageFlow(View):
    def get(self, request, **kwargs):
        # Enroll user in Flow experiment
        participant(request).enroll('waiting_list', ['flow'], 'flow')

        # Redirect
        return redirect(reverse('landing'))


class LandingPageTool(View):
    def get(self, request, **kwargs):
        # Enroll user in Flow experiment
        participant(request).enroll('waiting_list', ['control'], 'control')

        # Redirect
        return redirect(reverse('landing'))


class LandingPageSubmit(View):
    def get(self, request, **kwargs):
        form = forms.CustomerLeadModelForm()
        return TemplateResponse(request=request,
                                template="market_analysis/landing.html",
                                context={'form': form})

    def post(self, request, **kwargs):
        form = forms.CustomerLeadModelForm(request.POST)

        if form.is_valid():
            participant(request).goal('page_goal')
            return self.form_valid(form)
        else:
            response = form
            return TemplateResponse(request=request,
                                    template='market_analysis/landing.html',
                                    context={'response': response})

    def render_to_response(self, context):
        return TemplateResponse(request=self.request,
                                template="market_analysis/landing.html",
                                context={'form': self.form})

    def form_valid(self, form):
        obj = form.save(commit=True)
        response = {'registration': obj}
        return TemplateResponse(request=self.request,
                                template='market_analysis/goal.html',
                                context={'response': response})
