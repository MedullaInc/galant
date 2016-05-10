from django.conf import settings
from django.core.urlresolvers import reverse
from gallant.serializers.misc import ULTextField
from django.utils.translation import get_language
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
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = q.Section
        fields = ('title','text','name','index', 'id', 'views', 'user')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'user': {'required': False},
        }

# Special serializer for client update section view count without logging in
class SectionClientSerializer(SectionSerializer):
    class Meta:
        model = q.Section
        fields = ('id', 'views')
        extra_kwargs = {
            'id': {'read_only': False, 'required': True},
        }


class QuoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    views = serializers.IntegerField()
    session_duration = serializers.FloatField()
    client_name = serializers.SerializerMethodField(read_only=True)
    client_link = serializers.SerializerMethodField(read_only=True)
    kanban_card_description = serializers.SerializerMethodField()


    def get_client_name(self, quote):
        if quote.client:
            return quote.client.name
        else:
            return None

    def get_kanban_card_description(self, quote):
        if quote.client:
            return quote.client.name
        else:
            return None

    def get_client_link(self, quote):
        if quote.client:
            return reverse('client_detail', args=[quote.client.id])
        else:
            return None

    def get_fields(self, *args, **kwargs):
        fields = super(QuoteSerializer, self).get_fields(*args, **kwargs)

        if self.context.has_key('request'):
            user = self.context['request'].user
        else:
            user = self.context.get("user")

        def model_queryset(m): return m.objects.all_for(user)

        fields['client'] = serializers.PrimaryKeyRelatedField(queryset=model_queryset(g.Client), allow_null=True)
        fields['sections'] = SectionSerializer(many=True, partial=self.partial)
        fields['services'] = s.ServiceSerializer(many=True, partial=self.partial)
        fields['projects'] = serializers.PrimaryKeyRelatedField(many=True, queryset=model_queryset(g.Project))

        return fields

    def update(self, instance, validated_data):
        services_data = validated_data.pop('services')
        sections_data = validated_data.pop('sections')

        if self.context.has_key('request'):
            user = self.context['request'].user
        else:
            user = self.context.get("user")

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
                  'modified', 'token', 'parent', 'projects', 'views', 'session_duration', 'client_name', 'client_link', 'kanban_card_description')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False, 'allow_null':True},
            'user': {'required': False},
            'name': {'required': True},
        }

    def _write_services(self, user, instance, services_data):
        init_services = set(instance.services.all_for(user))
        new_services = set()

        for id, service_data in enumerate(services_data):
            service_id = service_data.get('id', None)
            service_data['index'] = id
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

        for id, section_data in enumerate(sections_data):
            section_id = section_data.get('id', None)
            section_data['index'] = id
            if section_id:
                section_instance = q.Section.objects.get_for(user, 'change', pk=section_id)
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


class QuoteClientSerializer(QuoteSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super(serializers.ModelSerializer, self).get_fields(*args, **kwargs)

        fields['services'] = s.ServiceClientSerializer(many=True, partial=self.partial)
        fields['sections'] = SectionClientSerializer(many=True, partial=self.partial)

        return fields

    class Meta:
        model = Quote
        fields = ('sections', 'services',
                  'views', 'session_duration')

    def update(self, instance, validated_data):
        services_data = validated_data.pop('services')
        sections_data = validated_data.pop('sections')

        self._write_services(instance.user, instance, services_data)
        self._write_sections(instance.user, instance, sections_data)

        return super(QuoteSerializer, self).update(instance, validated_data)

    def _write_sections(self, user, instance, sections_data):
        for section_data in sections_data:
            section_id = section_data.get('id', None)
            if section_id:
                section_instance = q.Section.objects.get_for(user, 'change', pk=section_id)
                ss = SectionClientSerializer(data=section_data, instance=section_instance)
                ss.update(section_instance, section_data)

    def _write_services(self, user, instance, services_data):
        for service_data in services_data:
            service_id = service_data.get('id', None)
            if service_id:
                service_instance = instance.services.get_for(user, 'change', pk=service_id)
                ss = s.ServiceClientSerializer(data=service_data, instance=service_instance)
                ss.update(service_instance, service_data)


class QuoteTemplateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    quote = QuoteSerializer()
    languages = serializers.SerializerMethodField()

    class Meta:
        model = QuoteTemplate
        fields = ('id', 'user', 'quote', 'languages')

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

    def get_languages(self, template):
        lang_dict = dict(settings.LANGUAGES)
        language_set = set(template.quote.get_languages())
        if len(language_set) == 0:
            language_set.update(get_language())
        return [{'code': c, 'name': lang_dict[c]} for c in language_set if c in lang_dict]
