from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from calendr import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'api/task', views.TasksAPI, 'api-task')

urlpatterns = [
    url(r'^$', login_required(views.calendar), name='calendr'),
]

urlpatterns += router.urls
