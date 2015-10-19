from rest_framework import serializers
from briefs.models import Brief, BriefTemplate
from gallant import models as g
from briefs import models as b
from quotes import models as q


class BriefSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def get_fields(self, *args, **kwargs):
        fields = super(BriefSerializer, self).get_fields(*args, **kwargs)
        user = self.context['request'].user

        def model_queryset(m): return m.objects.all_for(user)

        fields['client'] = serializers.PrimaryKeyRelatedField(queryset=model_queryset(g.Client))
        fields['questions'] = serializers.PrimaryKeyRelatedField(many=True, queryset=model_queryset(b.Question))
        fields['quote'] = serializers.PrimaryKeyRelatedField(queryset=model_queryset(q.Quote))

        return fields

    class Meta:
        model = Brief
        fields = ('id', 'user', 'name', 'title', 'greeting', 'status', 'token',
                  'modified', 'questions', 'language', 'client', 'quote')


class BriefTemplateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    brief = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = BriefTemplate
        fields = ('id', 'user', 'brief')
