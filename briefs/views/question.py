from briefs import serializers
from gallant.utils import GallantObjectPermissions
from rest_framework import generics
from briefs import models as b


class QuestionDetailAPI(generics.RetrieveUpdateAPIView):
    model = b.Question
    serializer_class = serializers.QuestionSerializer
    permission_classes = [
        GallantObjectPermissions
    ]

    def get_queryset(self):
        return self.model.objects.all_for(self.request.user)
