from rest_framework import serializers
from calendr.models import Task
from gallant import models as g
from kanban import serializers as ks


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    project_name = serializers.SerializerMethodField()
    daily_estimate = serializers.FloatField(required=False)
    card = ks.KanbanCardSerializer(read_only=True, allow_null=True)

    def get_project_name(self, task):
        if task.project:
            return task.project.name
        else:
            return ''

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('id', None)
        validated_data.update({'user': user})

        return super(TaskSerializer, self).create(validated_data)

    def get_fields(self, *args, **kwargs):
        fields = super(TaskSerializer, self).get_fields(*args, **kwargs)
        fields['project'] = serializers.PrimaryKeyRelatedField(
            required=False,
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
        fields = ('id', 'user', 'name', 'start', 'end', 'daily_estimate', 'status',
                  'project', 'services', 'assignee', 'notes', 'project_name', 'card')

    def validate(self, data):
        start = data.get('start', None)
        end = data.get('end', None)
        if end:
            if start and start > end:
                raise serializers.ValidationError("End date can't be before start date.")
            elif start is None:
                raise serializers.ValidationError("Task can't have end date without start date.")

        return data
