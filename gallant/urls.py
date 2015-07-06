"""gallant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf.urls.i18n import i18n_patterns
from django.views.generic.base import TemplateView
from gallant import views

urlpatterns = i18n_patterns(
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^quote/', include('quotes.urls')),

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    # TODO: url(r'^briefs/$', login_required(briefs.views.index), name='briefs'),
    url(r'^client/add/$', login_required(views.ClientCreate.as_view()), name='add_client'),
    url(r'^client/edit/(?P<pk>[0-9]+)$', login_required(views.ClientUpdate.as_view()), name='edit_client'),
    url(r'^client/(?P<pk>[0-9]+)$', login_required(views.client_detail), name='client_detail'),
    url(r'^service/add/$', login_required(views.ServiceCreate.as_view()), name='add_service'),
    url(r'^service/edit/(?P<pk>[0-9]+)$', login_required(views.ServiceUpdate.as_view()), name='edit_service'),
    url(r'^service/(?P<pk>[0-9]+)$', login_required(views.service_detail), name='service_detail'),
)
