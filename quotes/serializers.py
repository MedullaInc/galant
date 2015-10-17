from rest_framework import serializers
from quotes.models import Quote, QuoteTemplate
from gallant import models as g
from quotes import models as q


class QuoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    def get_fields(self, *args, **kwargs):
        fields = super(QuoteSerializer, self).get_fields(*args, **kwargs)
        user = self.context['request'].user

        def model_queryset(m): return m.objects.all_for(user)

        fields['client'] = serializers.PrimaryKeyRelatedField(queryset=model_queryset(g.Client))
        fields['sections'] = serializers.PrimaryKeyRelatedField(many=True, queryset=model_queryset(q.Section))
        fields['services'] = serializers.PrimaryKeyRelatedField(many=True, queryset=model_queryset(q.ServiceSection))
        fields['projects'] = serializers.PrimaryKeyRelatedField(many=True, queryset=model_queryset(g.Project))

        return fields

    class Meta:
        model = Quote
        fields = ('id', 'user', 'name', 'client', 'sections', 'services', 'language', 'status',
                  'modified', 'token', 'parent', 'projects')


class QuoteTemplateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    quote = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = QuoteTemplate
        fields = ('id', 'user', 'quote')
