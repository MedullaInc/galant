from calendr.models import Task
from calendr.serializers import TaskSerializer
from django.shortcuts import render
from gallant.utils import GallantObjectPermissions
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


def calendar(request):
    return render(request, 'calendr/calendr_3.html', {'title': 'Calendar'})

class TaskDetailAPI(generics.RetrieveUpdateAPIView):
    model = Task
    serializer_class = TaskSerializer
    permission_classes = [
        GallantObjectPermissions
    ]

    def update(self, request, *args, **kwargs):
        task = Task.objects.get_for(self.request.user, pk=kwargs['pk'])
        serializer = self.get_serializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    def get_queryset(self):
        return self.model.objects.all_for(self.request.user)


class TaskCreateAPI(generics.ListCreateAPIView):
    model = Task
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.GET.get('user', None)
        if user:
            return self.model.objects.all_for(self.request.user).filter(user_id=user)
        else:
            return self.model.objects.all_for(self.request.user)


class TasksAPI(generics.ListAPIView):
    model = Task
    serializer_class = TaskSerializer
    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):
        user = self.request.GET.get('user', None)
        if user:
            return self.model.objects.all_for(self.request.user).filter(user_id=user)
        else:
            return self.model.objects.all_for(self.request.user)