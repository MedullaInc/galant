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
        fields['services'] = ServiceSerializer(many=True, partial=self.partial)

        return fields

    class Meta:
        model = Project
        fields = ('id', 'user', 'name', 'status', 'notes', 'services', 'client', 'field_choices', 'link')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False, 'allow_null':True},
            'user': {'required': False},
        }

    def create(self, validated_data):
        validated_data.update({'user': self.context['request'].user})

        services_data = validated_data.pop('services', None)
        validated_data.pop('id', None)

        instance = super(ProjectSerializer, self).create(validated_data)

        if services_data:
            self._write_services(instance, services_data)

        return instance

    def update(self, instance, validated_data):
        validated_data.update({'user': self.context['request'].user})

        services_data = validated_data.pop('services', None)

        if services_data:
            self._write_services(instance, services_data)

        return super(ProjectSerializer, self).update(instance, validated_data)

    def _write_services(self, instance, services_data):
        user = instance.user
        init_services = set(instance.services.all_for(user))
        new_services = set()

        for id, service_data in enumerate(services_data):
            service_id = service_data.get('id', None)
            service_data['index'] = id
            if service_id:
                service_instance = g.Service.objects.get_for(user, 'change', pk=service_id)
                ss = ServiceSerializer(data=service_data, instance=service_instance)
                service = ss.update(service_instance, service_data)
            else:
                service_data.update({'user': user})
                ss = ServiceSerializer(data=service_data)

                service = ss.create(service_data)

            new_services.add(service)

        instance.services = new_services

        for service in (init_services - new_services):
            service.delete()
