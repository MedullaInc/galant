from gallant.models.misc import Note
from rest_framework import serializers, relations
from gallant.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    '''parent = serializers.PrimaryKeyRelatedField(queryset=)

    def get_fields(self, *args, **kwargs):
        fields = super(ServiceSerializer, self).get_fields(*args, **kwargs)
        fields['notes'] = relations.ManyRelatedField(
            child_relation=relations.RelatedField(
                queryset=Note.objects.all_for(self.context['request'].user, 'view_note')
            )
        )
        return fields
    '''
    class Meta:
        model = Service
        fields = ('id', 'name', 'description', 'quantity', 'type')
