from briefs import serializers
from gallant.utils import GallantObjectPermissions
from rest_framework import generics
from briefs import models as b
from rest_framework.permissions import IsAuthenticated


class QuestionDetailAPI(generics.RetrieveUpdateAPIView):
    model = b.Question
    serializer_class = serializers.QuestionSerializer
    permission_classes = [
        GallantObjectPermissions
    ]

    def get_queryset(self):
        return self.model.objects.all_for(self.request.user)


class QuestionsAPI(generics.ListAPIView):
    model = b.Question
    serializer_class = serializers.QuestionSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        brief_id = self.request.GET.get('brief', None)
        if brief_id:
            return self.model.objects.all_for(self.request.user).filter(brief__id=brief_id)
        else:
            return self.model.objects.all_for(self.request.user)
