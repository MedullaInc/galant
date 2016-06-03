from django.core.urlresolvers import reverse
from django.db.models.query import Prefetch
from gallant.serializers.service import ServiceSerializer
from gallant.utils import get_field_choices
from rest_framework import serializers
from gallant.models import Project
from gallant import models as g
from quotes import models as q


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    link = serializers.SerializerMethodField()
    field_choices = serializers.SerializerMethodField()

    def get_link(self, project):
        return reverse('project_detail', args=[project.id])

    def get_field_choices(self, project):
        return get_field_choices(type(project))

    def get_fields(self, *args, **kwargs):
        fields = super(ProjectSerializer, self).get_fields(*args, **kwargs)
        fields['notes'] = serializers.PrimaryKeyRelatedField(
            many=True, queryset=g.Note.objects.all_for(self.context['request'].user))
        fields['quotes'] = serializers.PrimaryKeyRelatedField(
            many=True, source='quote_set', queryset=q.Quote.objects.all_for(self.context['request'].user))
        fields['services'] = serializers.PrimaryKeyRelatedField(
            many=True, queryset=g.Service.objects.all_for(self.context['request'].user))

        return fields

    class Meta:
        model = Project
        fields = ('id', 'user', 'name', 'status', 'notes', 'services', 'client', 'field_choices', 'link')

    def create(self, validated_data):
        validated_data.update({'user': self.context['request'].user})

        return super(ProjectSerializer, self).create(validated_data)
