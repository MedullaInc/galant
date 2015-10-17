from gallant import serializers
from gallant import models as g
from gallant.utils import GallantObjectPermissions
from rest_framework import generics


class NoteDetailAPI(generics.RetrieveUpdateAPIView):
    model = g.Note
    serializer_class = serializers.NoteSerializer
    permission_classes = [
        GallantObjectPermissions
    ]

    def get_queryset(self):
        return self.model.objects.all_for(self.request.user)

