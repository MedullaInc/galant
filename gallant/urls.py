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
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf.urls.i18n import i18n_patterns
from django.views.generic.base import TemplateView
import gallant
from gallant import views
import allauth.urls
import experiments.urls

urlpatterns = i18n_patterns(
    # Experiments
    url(r'^landing', TemplateView.as_view(template_name='landing.html'),
        name='experiment_landing'),
    url(r'^goal', TemplateView.as_view(template_name='goal.html'), name='experiment_goal'),

    url(r'^accounts/', include(allauth.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^quote/', include('quotes.urls')),
    url(r'^briefs/', include('briefs.urls')),
    url(r'^calendar/', include('calendr.urls')),

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^signup/', gallant.views.SignUpRequest.as_view(), name='signup'),
    url(r'^contact/', gallant.views.contact, name='contact'),

    url(r'^clients/$', login_required(gallant.views.ClientList.as_view()), name='clients'),
    url(r'^client/add/$', login_required(gallant.views.ClientCreate.as_view()), name='add_client'),
    url(r'^client/edit/(?P<pk>[0-9]+)$', login_required(gallant.views.ClientUpdate.as_view()), name='edit_client'),
    url(r'^client/delete/(?P<pk>[0-9]+)$', login_required(gallant.views.ClientDelete.as_view()), name='delete_client'),
    url(r'^client/(?P<pk>[0-9]+)?$', login_required(gallant.views.client_detail), name='client_detail'),
    url(r'^client/(?P<pk>[0-9]+)/work/$', login_required(gallant.views.client_work_detail), name='client_work_detail'),
    url(r'^client/(?P<pk>[0-9]+)/money/$', login_required(gallant.views.client_money_detail),
        name='client_money_detail'),

    url(r'^projects/$', login_required(gallant.views.ProjectList.as_view()), name='projects'),
    url(r'^project/add/quote/(?P<quote_id>[0-9]+)?$', login_required(gallant.views.ProjectCreate.as_view()),
        name='add_project'),
    url(r'^project/edit/(?P<pk>[0-9]+)$', login_required(gallant.views.ProjectUpdate.as_view()), name='edit_project'),
    url(r'^project/delete/(?P<pk>[0-9]+)$', login_required(gallant.views.ProjectDelete.as_view()),
        name='delete_project'),
    url(r'^project/(?P<pk>[0-9]+)?$', login_required(gallant.views.project_detail), name='project_detail'),

    url(r'^project/(?P<project_id>[0-9]+)/service/add/$', login_required(gallant.views.ServiceCreate.as_view()),
        name='add_service'),
    url(r'^project/(?P<project_id>[0-9]+)/service/edit/(?P<pk>[0-9]+)$',
        login_required(gallant.views.ServiceUpdate.as_view()), name='edit_service'),
    url(r'^project/(?P<project_id>[0-9]+)/service/(?P<pk>[0-9]+)$', login_required(gallant.views.service_detail),
        name='service_detail'),

    url(r'^api/service/(?P<pk>[0-9]+)$', login_required(gallant.views.ServiceDetailAPI.as_view()),
        name='api_service_detail'),
    url(r'^api/project/(?P<pk>[0-9]+)$', login_required(gallant.views.ProjectDetailAPI.as_view()),
        name='api_project_detail'),
    url(r'^api/client/(?P<pk>[0-9]+)$', login_required(gallant.views.ClientDetailAPI.as_view()),
        name='api_client_detail'),
    url(r'^api/note/(?P<pk>[0-9]+)$', login_required(gallant.views.NoteDetailAPI.as_view()), name='api_note_detail'),
    url(r'^api/users/?$', login_required(gallant.views.UsersAPI.as_view()), name='api_users'),
    url(r'^api/projects/?$', login_required(gallant.views.ProjectsAPI.as_view()), name='api_projects'),

    url(r'^register/(?P<pk>[0-9]+)', gallant.views.Register.as_view(), name='register'),
    url(r'^account/add/', login_required(gallant.views.AccountAdd.as_view()), name='add_account'),
    url(r'^account/reset/', login_required(gallant.views.PasswordReset.as_view()), name='reset_password'),
    url(r'^feedback/', gallant.views.SubmitFeedback.as_view(), name='feedback'),
)

urlpatterns += patterns('',
    url(r'^experiments/', include(experiments.urls)),
)