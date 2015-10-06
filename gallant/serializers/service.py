from rest_framework import serializers
from gallant.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    notes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    cost = serializers.CharField()

    class Meta:
        model = Service
        fields = ('id', 'name', 'description', 'cost', 'quantity', 'type', 'parent', 'notes')
