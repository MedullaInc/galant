import json
from gallant.fields import ULTextDict, ULTextDictArray
from moneyed.classes import Money
from rest_framework import serializers
from gallant.models import Note


class MoneyField(serializers.Field):
    def to_representation(self, obj):
        return '%d %s' % (obj.amount, obj.currency)

    def to_internal_value(self, data):
        val = data.split(' ')
        return Money(val[0], val[1])


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
