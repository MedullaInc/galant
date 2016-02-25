from django.conf import settings
from django.utils.translation import get_language
from rest_framework import serializers
from briefs.models import BriefTemplate
from briefs import models as b
from .brief import BriefSerializer


class BriefTemplateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    brief = BriefSerializer()
    languages = serializers.SerializerMethodField()

    class Meta:
        model = BriefTemplate
        fields = ('id', 'user', 'brief', 'languages')

    def get_languages(self, template):
        lang_dict = dict(settings.LANGUAGES)
        language_set = set(template.brief.get_languages())
        if len(language_set) == 0:
            language_set.update(get_language())
        return [{'code': c, 'name': lang_dict[c]} for c in language_set if c in lang_dict]

    def create(self, validated_data):
        user = self.context['request'].user
        brief_data = validated_data.pop('brief')
        validated_data.update({'user': user})
        brief_data.update({'user': user})

        brief = BriefSerializer(context=self.context).create(brief_data)
        validated_data.update({'brief': brief})
        instance = super(BriefTemplateSerializer, self).create(validated_data)

        return instance

    def update(self, instance, validated_data):
        user = self.context['request'].user
        brief_data = validated_data.pop('brief')
        validated_data.update({'user': user})

        brief_id = brief_data.get('id', None)
        if brief_id:
            brief_instance = b.Brief.objects.get_for(user, 'change', pk=brief_id)
            bs = BriefSerializer(data=brief_data, instance=brief_instance, context=self.context)
            self.instance.brief = bs.update(brief_instance, brief_data)

        return super(BriefTemplateSerializer, self).update(self.instance, validated_data)
