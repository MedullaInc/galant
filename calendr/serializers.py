from rest_framework import serializers
from calendr.models import Task


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    services = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    assignee = serializers.PrimaryKeyRelatedField(read_only=True)
    notes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'user', 'name', 'start', 'end', 'daily_estimate',
                  'project', 'services', 'assignee', 'notes')
