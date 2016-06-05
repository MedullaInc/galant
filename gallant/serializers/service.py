from django.utils.translation import get_language
from gallant.serializers.misc import ULTextField
from rest_framework import serializers
from gallant.models import Service
from kanban.serializers import KanbanCardSerializer
from gallant.serializers.misc import MoneyField


class ServiceSerializer(serializers.ModelSerializer):
    name = ULTextField()
    description = ULTextField()
    language = serializers.SerializerMethodField()
    cost = MoneyField(required=False, allow_null=True)
    notes = serializers.CharField(read_only=True)
    views = serializers.IntegerField(required=False, allow_null=True)

    card = KanbanCardSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Service
        fields = ('id', 'user', 'name', 'description', 'cost', 'quantity', 'type', 'card',
                  'parent', 'notes', 'views', 'index', 'status', 'language', 'time')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'user': {'required': False}
        }

    def get_language(self, service):
        try:
            return service.quote_set.all_for(service.user)[0].language \
                   or get_language()
        except (IndexError, KeyError), ex:
            return get_language()

    def create(self, validated_data):
        validated_data.pop('id', None)

        return super(ServiceSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(ServiceSerializer, self).update(instance, validated_data)

    def to_representation_lang(self, instance, language):
        ret = super(ServiceSerializer, self).to_representation(instance)
        for key in ['name', 'description']:
            if language and language in ret[key]:
                ret[key] = ret[key][language]
            else:
                try:
                    ret[key] = ret[key].itervalues().next()
                except StopIteration:
                    ret[key] = ''

        return ret


# Special serializer for client update section view count without logging in
class ServiceClientSerializer(ServiceSerializer):
    class Meta:
        model = Service
        fields = ('id', 'views')
        extra_kwargs = {
            'id': {'read_only': False, 'required': True},
        }
