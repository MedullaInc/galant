from calendr.models import Task
from calendr.serializers import TaskSerializer
from django.shortcuts import render
from gallant.utils import GallantObjectPermissions
from rest_framework import generics


def calendar(request):
    return render(request, 'calendr/calendr.html', {'title': 'Calendar'})


class TaskDetailAPI(generics.RetrieveUpdateAPIView):
    model = Task
    serializer_class = TaskSerializer
    permission_classes = [
        GallantObjectPermissions
    ]

    def get_queryset(self):
        return self.model.objects.all_for(self.request.user, 'view_task')

