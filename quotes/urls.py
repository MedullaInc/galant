from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from quotes import views

urlpatterns = [
    url(r'^$', login_required(views.QuoteList.as_view()), name='quotes'),
    url(r'^add/$', login_required(views.QuoteCreate.as_view()), name='add_quote'),
    url(r'^edit/(?P<pk>[0-9]+)$', login_required(views.QuoteUpdate.as_view()), name='edit_quote'),
    url(r'^(?P<pk>[0-9]+)?$', login_required(views.QuoteDetail.as_view()), name='quote_detail'),
]