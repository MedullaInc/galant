from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from quotes import views

urlpatterns = [
    url(r'^$', login_required(TemplateView.as_view(template_name='quotes/index.html')), name='quotes'),
    url(r'^add/$', login_required(views.QuoteCreate.as_view()), name='add_quote'),
]