from django.shortcuts import render

# Create your views here.
from gallant.utils import GallantViewSetPermissions
from gallant.views.user import UserModelViewSet
from kanban import serializers
from kanban import models as k


class KanbanCardAPI(UserModelViewSet):
    model = k.KanbanCard
    serializer_class = serializers.KanbanCardSerializer
    permission_classes = [
        GallantViewSetPermissions
    ]
