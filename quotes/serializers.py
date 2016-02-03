from gallant.serializers.misc import ULTextField
from rest_framework import serializers
from quotes.models import Quote, QuoteTemplate
from gallant import models as g
from quotes import models as q
from gallant import serializers as s
from django.http import HttpResponse
import json

class SectionSerializer(serializers.ModelSerializer):
    title = ULTextField()
    text = ULTextField()
    views = serializers.IntegerField(required=False)

    class Meta:
        model = q.Section
        fields = ('title','text','name','index', 'id', 'views') 


class QuoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    views = serializers.IntegerField()
    session_duration = serializers.FloatField()

    def get_fields(self, *args, **kwargs):
        fields = super(QuoteSerializer, self).get_fields(*args, **kwargs)

        if self.context.has_key('request'):
            user = self.context['request'].user
        else:
            user = self.context.get("user")

        def model_queryset(m): return m.objects.all_for(user)

        fields['client'] = serializers.PrimaryKeyRelatedField(queryset=model_queryset(g.Client))
        fields['sections'] = SectionSerializer(many=True)
        fields['services'] = s.ServiceSerializer(many=True)
        fields['projects'] = serializers.PrimaryKeyRelatedField(many=True, queryset=model_queryset(g.Project))

        return fields

    def update(self, instance, validated_data):
        services_data = validated_data.pop('services')
        sections_data = validated_data.pop('sections')

        if self.context.has_key('request'):
            user = self.context['request'].user
        else:
            user = self.context.get("user")

        if self.instance is None:
            quote_instance = instance
        else:
            quote_instance = self.instance


        self._write_services(user, instance, services_data)
        self._write_sections(user, instance, sections_data)

        return super(QuoteSerializer, self).update(instance, validated_data)

    def create(self, validated_data):


        if self.context.has_key('request'):
            user = self.context['request'].user
        else:
            user = self.context.get("user")

        services_data = validated_data.pop('services')
        sections_data = validated_data.pop('sections')
        validated_data.update({'user': user})
        validated_data.pop('id', None)

        instance = super(QuoteSerializer, self).create(validated_data)

        self._write_services(user, instance, services_data)
        self._write_sections(user, instance, sections_data)
        return instance

    class Meta:
        model = Quote
        fields = ('id', 'user', 'name', 'client', 'sections', 'services', 'language', 'status',
                  'modified', 'token', 'parent', 'projects', 'views', 'session_duration')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False, 'allow_null':True},
            'user': {'required': False},
        }

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
                service_data.update({'user': user})
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
                section_data.update({'user': user})
                ss = SectionSerializer(data=section_data)
                section = ss.create(section_data)

            new_sections.add(section)

        instance.sections = new_sections

        for section in (init_sections- new_sections):
            section.delete()


class QuoteTemplateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    quote = QuoteSerializer()
    language_list = serializers.SerializerMethodField()

    class Meta:
        model = QuoteTemplate
        fields = ('id', 'user', 'quote', 'language_list')

    def create(self, validated_data):
        user = self.context['request'].user
        quote_data = validated_data.pop('quote')
        validated_data.update({'user': user})
        quote_data.update({'user': user})

        qs = QuoteSerializer(data=quote_data, context={'user': self.context['request'].user})
        quote = qs.create(quote_data);

        validated_data.update({'quote': quote})

        instance = super(QuoteTemplateSerializer, self).create(validated_data)

        return instance

    def update(self, instance, validated_data):

        user = self.context['request'].user

        quote_data = validated_data.pop('quote')
        quote_id = quote_data.get('id', None)

        quote_data.update({'user': user})

        qs = QuoteSerializer(data=quote_data, context={'user': self.context['request'].user})

        quote_instance = q.Quote.objects.get_for(user, 'change', pk=quote_id)

        quote = qs.update(quote_instance, quote_data)

        validated_data.update({'quote': quote})

        return super(QuoteTemplateSerializer, self).update(instance, validated_data)

    def get_language_list(self, obj):
        lan_list = QuoteTemplate.objects.all_for(obj.user).get(pk=obj.id).language_list()
        return lan_list