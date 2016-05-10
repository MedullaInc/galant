from rest_framework import serializers
from kanban import models as k


class KanbanCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = k.KanbanCard
        fields = ('id', 'user', 'title', 'text', 'link', 'xindex', 'yindex', 'alert')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False}
        }

    def create(self, validated_data):
        if self.context.has_key('request'):
            user = self.context['request'].user
        else:
            user = self.context.get("user")

        validated_data.update({'user': user})
        return super(KanbanCardSerializer, self).create(validated_data)
