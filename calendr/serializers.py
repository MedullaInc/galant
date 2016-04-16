from rest_framework import serializers
from calendr.models import Task
from gallant import models as g


class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()

    def get_project_name(self, task):
        return task.project.name

    def get_fields(self, *args, **kwargs):
        fields = super(TaskSerializer, self).get_fields(*args, **kwargs)
        fields['project'] = serializers.PrimaryKeyRelatedField(
            queryset=g.Project.objects.all_for(self.context['request'].user))
        fields['services'] = serializers.PrimaryKeyRelatedField(
            required=False, many=True,
            queryset=g.Service.objects.all_for(self.context['request'].user))
        fields['notes'] = serializers.PrimaryKeyRelatedField(
            required=False, many=True,
            queryset=g.Note.objects.all_for(self.context['request'].user))

        return fields

    class Meta:
        model = Task
        fields = ('id', 'user', 'name', 'start', 'end', 'daily_estimate',
                  'project', 'services', 'assignee', 'notes', 'project_name')
