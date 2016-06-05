import json
from gallant.fields import ULTextDict, ULTextDictArray
from moneyed.classes import Money
from rest_framework import serializers
from gallant.models import Note


class MoneyField(serializers.Field):
    def to_representation(self, obj):
        return {'amount': str(obj.amount), 'currency': str(obj.currency)}

    def to_internal_value(self, data):
        json_val = json.dumps(data)
        val = json.loads(json_val)

        if not 'amount' in val:
            return None

        currency = val.get('currency', None) or self.context['request'].user.currency
        return Money(val['amount'], currency)


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
