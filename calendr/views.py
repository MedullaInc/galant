from calendr.models import Task
from calendr.serializers import TaskSerializer
from django.shortcuts import render
from gallant.utils import GallantObjectPermissions, GallantViewSetPermissions
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet


def calendar(request):
    return render(request, 'calendr/calendr.html', {'title': 'Projects'})


class TasksAPI(ModelViewSet):
    model = Task
    serializer_class = TaskSerializer
    permission_classes = [
        GallantViewSetPermissions
    ]

    def get_queryset(self):
        user = self.request.GET.get('user', None)
        assignee = self.request.GET.get('assignee', None)

        qs = self.model.objects.all_for(self.request.user)

        if user:
            qs = qs.filter(user_id=user)
        if assignee:
            qs = qs.filter(assignee=assignee)

        return qs

