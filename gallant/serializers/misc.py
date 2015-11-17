import json
from gallant.fields import ULTextDict, ULTextDictArray
from moneyed.classes import Money
from rest_framework import serializers
from gallant.models import Note


class MoneyField(serializers.Field):
    def to_representation(self, obj):
        return json.dumps({'amount': str(obj.amount), 'currency': str(obj.currency)})

    def to_internal_value(self, data):
        val = json.loads(data)
        return Money(val['amount'], val['currency'])


class NoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'user', 'text', 'created')


class ULTextField(serializers.Field):
    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        return ULTextDict(data)


class ULTextArrayField(serializers.Field):
    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        return ULTextDictArray(data)
