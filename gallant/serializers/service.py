from gallant.serializers.misc import ULTextField
from rest_framework import serializers
from gallant.models import Service
from gallant.serializers.misc import MoneyField


class ServiceSerializer(serializers.ModelSerializer):
    name = ULTextField()
    description = ULTextField()
    cost = MoneyField()
    notes = serializers.CharField(read_only=True)
    views = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Service
        fields = ('id', 'user', 'name', 'description', 'cost', 'quantity', 'type', 'parent', 'notes', 'views', 'index')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
        }

    def create(self, validated_data):
        validated_data.pop('id', None)
        instance = super(ServiceSerializer, self).create(validated_data)

        return instance

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
