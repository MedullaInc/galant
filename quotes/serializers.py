from gallant.serializers.misc import ULTextField
from rest_framework import serializers
from quotes.models import Quote, QuoteTemplate
from gallant import models as g
from quotes import models as q
from gallant import serializers as s
from django.http import HttpResponse


class SectionSerializer(serializers.ModelSerializer):
    title = ULTextField()
    text = ULTextField()
    class Meta:
        model = q.Section
        fields = ('title','text','name','index') 


class QuoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    def get_fields(self, *args, **kwargs):
        fields = super(QuoteSerializer, self).get_fields(*args, **kwargs)
        user = self.context['request'].user

        def model_queryset(m): return m.objects.all_for(user)

        fields['client'] = serializers.PrimaryKeyRelatedField(queryset=model_queryset(g.Client))
        fields['sections'] = SectionSerializer(many=True)
        fields['services'] = s.ServiceSerializer(many=True)
        fields['projects'] = serializers.PrimaryKeyRelatedField(many=True, queryset=model_queryset(g.Project))

        return fields

    def update(self, instance, validated_data):
        services_data = validated_data.pop('services')
        sections_data = validated_data.pop('sections')

        self._write_services(self.context['request'].user, self.instance, services_data)
        self._write_sections(self.context['request'].user, self.instance, sections_data)

        return super(QuoteSerializer, self).update(self.instance, validated_data)

    def create(self, validated_data):
        user = self.context['request'].user

        validated_data.update({'user': user})

        instance = super(QuoteSerializer, self).create(validated_data)
        services_data = validated_data.pop('services')
        sections_data = validated_data.pop('sections')
        self._write_services(user, instance, services_data)
        self._write_sections(user, instance, sections_data)
        return instance

    class Meta:
        model = Quote
        fields = ('id', 'user', 'name', 'client', 'sections', 'services', 'language', 'status',
                  'modified', 'token', 'parent', 'projects')

    def _write_services(self, user, instance, services_data):
        init_services = set(instance.services.all_for(user))
        new_services = set()

        for service_data in services_data:
            service_id = service_data.get('id', None)
            if service_id:
                service_instance = g.Service.objects.get_for(user, 'change', pk=service_id)
                ss = s.ServiceSerializer(data=service_data, instance=service_instance)
                service = ss.update(service_instance, service_data)
            else:
                service_data.update({'user': self.context['request'].user})
                ss = s.ServiceSerializer(data=service_data)
                service = ss.create(service_data)

            new_services.add(service)

        instance.services = new_services

        for service in (init_services - new_services):
            service.delete()

    def _write_sections(self, user, instance, sections_data):
        init_sections = set(instance.sections.all_for(user))
        new_sections = set()

        for section_data in sections_data:
            section_id = section_data.get('id', None)
            if section_id:
                section_instance = g.Text.objects.get_for(user, 'change', pk=section_data)
                ss = SectionSerializer(data=section_data, instance=section_instance)
                section = ss.update(section_instance, section_data)
            else:
                section_data.update({'user': self.context['request'].user})
                ss = SectionSerializer(data=section_data)
                section = ss.create(section_data)

            new_sections.add(section)

        instance.sections = new_sections

        for section in (init_sections- new_sections):
            section.delete()

class QuoteTemplateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    quote = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = QuoteTemplate
        fields = ('id', 'user', 'quote')
