from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from quotes import views

urlpatterns = [
    url(r'^$', login_required(views.QuoteList.as_view()), name='quotes'),
    url(r'^add/$', login_required(views.QuoteCreate.as_view()), name='add_quote'),
    url(r'^edit/(?P<pk>[0-9]+)$', login_required(views.QuoteUpdate.as_view()), name='edit_quote'),
    url(r'^(?P<pk>[0-9]+)?$', login_required(views.QuoteDetail.as_view()), name='quote_detail'),
    url(r'^template/$', login_required(views.QuoteTemplateList.as_view()), name='quote_templates'),
    url(r'^template/add/(?P<quote_id>[0-9]+)?$', login_required(views.QuoteTemplateView.as_view()), name='add_quote_template'),
    url(r'^template/edit/(?P<pk>[0-9]+)?$', login_required(views.QuoteTemplateView.as_view()), name='edit_quote_template'),
    url(r'^preview/(?P<quote_id>[0-9]+)?$', login_required(views.quote_pdf), name='quote_preview'),
]