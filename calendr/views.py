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
    return render(request, 'calendr/calendr_3.html', {'title': 'Calendar'})


class TasksAPI(ModelViewSet):
    model = Task
    serializer_class = TaskSerializer
    permission_classes = [
        GallantViewSetPermissions
    ]

    def get_queryset(self):
        user = self.request.GET.get('user', None)
        if user:
            return self.model.objects.all_for(self.request.user).filter(user_id=user)
        else:
            return self.model.objects.all_for(self.request.user)

