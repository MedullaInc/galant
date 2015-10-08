from rest_framework import serializers
from gallant.models import Service
from .misc import MoneyField


class ServiceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    notes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    cost = MoneyField()

    class Meta:
        model = Service
        fields = ('id', 'user', 'name', 'description', 'cost', 'quantity', 'type', 'parent', 'notes')
