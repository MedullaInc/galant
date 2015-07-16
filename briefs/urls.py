from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from briefs import views

urlpatterns = [
    url(r'^$', login_required(views.BriefList.as_view()), name='briefs'),
    url(r'^client/(?P<pk>[0-9]+)$', login_required(views.ClientBriefList.as_view()), name='client_briefs'),
    url(r'^(?P<brief_type>client|service|project)/(?P<pk>[0-9]+)/add/$', login_required(views.BriefCreate.as_view()), name='add_brief'),
    url(r'^edit/(?P<pk>[0-9]+)$', login_required(views.BriefUpdate.as_view()), name='edit_brief'),
    url(r'^(?P<brief_type>client|service|project)/(?P<pk>[0-9]+)?$', login_required(views.BriefDetail.as_view()), name='brief_detail'),
]