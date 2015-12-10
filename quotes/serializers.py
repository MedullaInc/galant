from gallant.serializers.misc import ULTextField
from rest_framework import serializers
from quotes.models import Quote, QuoteTemplate
from gallant import models as g
from quotes import models as q
from gallant import serializers as s
from django.http import HttpResponse


class TextSectionSerializer(serializers.ModelSerializer):
    title = ULTextField()
    text = ULTextField()
    name = ULTextField()
    class Meta:
        model = q.TextSection
        fields = ('title','text','name','index') 


class SectionSerializer(serializers.ModelSerializer):
    textsection = TextSectionSerializer(read_only=True)
    class Meta:
        model = q.Section
        fields = ('textsection',) 


class ServiceSectionSerializer(serializers.ModelSerializer):
    service = s.ServiceSerializer(read_only=False)

    class Meta:
        model = q.ServiceSection
        fields = ('id','service')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
        }

    def update(self, instance, validated_data, user):

        self._write_services(user, self.instance, validated_data.pop('service'))

        return super(ServiceSectionSerializer, self).update(instance, validated_data)

    def create(self, validated_data, user):

        user = user
        services_data = validated_data.pop('service')
        validated_data.update({'user': user})
    
        instance = super(ServiceSectionSerializer, self).create(validated_data)

        self._write_services(user, instance, services_data)
        
        return instance


    def _write_services(self, user, instance, service_data):
        init_services = set(instance.service.objects.all_for(user))
        new_services = set()


        service_id = service_data.get('id', None)
        if service_id:
            service_instance = g.Service.objects.get_for(user, 'change', pk=service_id)
            ss = s.ServiceSerializer(data=service_data, instance=service_instance)
            service = ss.update(service_instance, service_data)
        else:
            service_data.update({'user': self.context['request'].user})
            qs = s.ServiceSerializer(data=service_data)
            question = qs.create(service_data)

            new_services.add(question)

        instance.new_services = new_services
        #for service in (init_services - new_services):
        #    service.delete()


class QuoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    def get_fields(self, *args, **kwargs):
        fields = super(QuoteSerializer, self).get_fields(*args, **kwargs)
        user = self.context['request'].user

        def model_queryset(m): return m.objects.all_for(user)

        fields['client'] = serializers.PrimaryKeyRelatedField(queryset=model_queryset(g.Client))
        fields['sections'] = SectionSerializer(many=True, read_only=True)
        fields['service_sections'] = ServiceSectionSerializer(many=True)
        fields['projects'] = serializers.PrimaryKeyRelatedField(many=True, queryset=model_queryset(g.Project))

        return fields

    def update(self, instance, validated_data):
        service_sections_data = validated_data.pop('service_sections')
        self._write_service_sections(self.context['request'].user, self.instance, service_sections_data)
        return super(QuoteSerializer, self).update(self.instance, validated_data)

    def create(self, validated_data):
        user = self.context['request'].user

        validated_data.update({'user': user})

        instance = super(QuoteSerializer, self).create(validated_data)
        service_sections_data = validated_data.pop('service_sections')
        self._write_service_sections(user, instance, service_sections_data)
        return instance

    class Meta:
        model = Quote
        fields = ('id', 'user', 'name', 'client', 'sections', 'service_sections', 'language', 'status',
                  'modified', 'token', 'parent', 'projects')

    def _write_service_sections(self, user, instance, service_sections_data):
        init_service_sections = set(instance.service_sections.all_for(user))
        new_service_sections = set()

        for service_section_data in service_sections_data:
            service_section_id = service_section_data.get('id', None)
            if service_section_id:
                service_section_instance = q.ServiceSection.objects.get_for(user, 'change', pk=service_section_id)
                ss = ServiceSectionSerializer(data=service_section_data, instance=service_section_instance)
                service_section = ss.update(service_section_instance, service_section_data, user)
            else:
                service_section_data.update({'user': self.context['request'].user})
                ss = ServiceSectionSerializer(data=service_section_data)
                service_section = ss.create(service_section_data, user)

            new_service_sections.add(service_section)

        instance.service_sections = new_service_sections

        #for service_section in (init_service_sections - new_service_sections):
        #    service_section.delete()

class QuoteTemplateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    quote = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = QuoteTemplate
        fields = ('id', 'user', 'quote')
