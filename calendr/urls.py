from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', login_required(TemplateView.as_view(template_name='calendr/calendr.html')), name='calendr'),
]