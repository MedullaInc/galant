from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from briefs import views

urlpatterns = [
    url(r'^$', login_required(views.BriefList.as_view()), name='briefs'),
    url(r'^answer/(?P<token>[a-f0-9]{32})$', views.BriefAnswer.as_view(), name='brief_answer'),
    url(r'^client/(?P<type_id>[0-9]+)/add/$',
        login_required(views.BriefCreate.as_view()), name='add_brief'),
    url(r'^client/(?P<type_id>[0-9]+)/$',
        login_required(views.BriefList.as_view()), name='brief_list'),
    url(r'^(?:client/(?P<type_id>[0-9]+)/)?edit/(?P<pk>[0-9]+)$',
        login_required(views.BriefUpdate.as_view()), name='edit_brief'),
    url(r'^(?:client/(?P<type_id>[0-9]+)/)?(?P<pk>[0-9]+)?$',
        login_required(views.BriefDetail.as_view()), name='brief_detail'),
    url(r'^template/$', login_required(views.BriefTemplateList.as_view()), name='brief_templates'),
    url(r'^template/add/(?P<brief_id>[0-9]+)?$', login_required(views.BriefTemplateView.as_view()), name='add_brief_template'),
    url(r'^template/edit/(?P<pk>[0-9]+)?$', login_required(views.BriefTemplateView.as_view()), name='edit_brief_template'),
]