from itertools import chain
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import View
from django.core.urlresolvers import reverse
from market_analysis import forms
from market_analysis import models
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404


class LandingPage(View):
    def get(self, request, **kwargs):
        form = forms.CustomerLeadModelForm()
        return TemplateResponse(request=request,
                                template="landing.html",
                                context={'form': form})


class LandingPageSubmit(View):
    def get(self, request, **kwargs):
        form = forms.CustomerLeadModelForm()
        return TemplateResponse(request=request,
                                template="landing.html",
                                context={'form': form})

    def post(self, request, **kwargs):
        form = forms.CustomerLeadModelForm(request.POST)

        if form.is_valid():
            return self.form_valid(form)
        else:
            response = form
            return TemplateResponse(request=request,
                                    template='landing.html',
                                    context={'response': response})

    def render_to_response(self, context):
        return TemplateResponse(request=self.request,
                                template="landing.html",
                                context={'form': self.form})

    def form_valid(self, form):
        obj = form.save(commit=True)
        response = {'registration': obj}
        return TemplateResponse(request=self.request,
                                template='goal.html',
                                context={'response': response})
