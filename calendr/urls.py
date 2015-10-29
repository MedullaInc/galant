from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from calendr import views

urlpatterns = [
    url(r'^$', login_required(views.calendar), name='calendr'),
    url(r'^api/task/(?P<pk>[0-9]+)$', login_required(views.TaskDetailAPI.as_view()), name='api_task_detail'),
    url(r'^api/task/add/$', login_required(views.TaskCreateAPI.as_view()), name='api_task_create'),
    url(r'^api/tasks/', login_required(views.TasksAPI.as_view()), name='api_tasks'),
]