from rest_framework import serializers
from calendr.models import Task
from gallant import models as g


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    assignee = serializers.PrimaryKeyRelatedField(read_only=True)

    def get_fields(self, *args, **kwargs):
        fields = super(TaskSerializer, self).get_fields(*args, **kwargs)
        fields['project'] = serializers.PrimaryKeyRelatedField(
            queryset=g.Project.objects.all_for(self.context['request'].user, 'view_project'))
        fields['services'] = serializers.PrimaryKeyRelatedField(
            many=True, queryset=g.Service.objects.all_for(self.context['request'].user, 'view_service'))
        fields['notes'] = serializers.PrimaryKeyRelatedField(
            many=True, queryset=g.Note.objects.all_for(self.context['request'].user, 'view_note'))

        return fields

    class Meta:
        model = Task
        fields = ('id', 'user', 'name', 'start', 'end', 'daily_estimate',
                  'project', 'services', 'assignee', 'notes')
