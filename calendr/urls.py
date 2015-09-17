from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from calendr import views

urlpatterns = [
    url(r'^$', login_required(views.calendar), name='calendr'),
]