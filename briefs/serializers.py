from django.conf import settings
from django.utils.translation import get_language
from gallant.serializers.misc import ULTextField, ULTextArrayField
from rest_framework import serializers
from briefs.models import Brief, BriefTemplate
from gallant import models as g
from briefs import models as b
from quotes import models as q


class QuestionSerializer(serializers.ModelSerializer):
    question = ULTextField()
    type = serializers.CharField(read_only=False)

    class Meta:
        model = b.Question
        fields = ('id', 'user', 'type', 'question', 'help_text', 'index')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'user': {'required': False},
            'help_text': {'required': False},
        }

    def to_internal_value(self, data):
        if 'type' not in data:
            return super(QuestionSerializer, self).to_internal_value(data)
        elif data['type'] == b.TextQuestion.__name__:
            return TextQuestionSerializer(data=data, context=self.context).to_internal_value(data)
        elif data['type'] == b.MultipleChoiceQuestion.__name__:
            return MultipleChoiceQuestionSerializer(data=data, context=self.context).to_internal_value(data)

    def to_representation(self, instance):
        if isinstance(instance, b.TextQuestion):
            dct = TextQuestionSerializer(instance, context=self.context).to_representation(instance)
            dct['type'] = b.TextQuestion.__name__
            return dct
        elif isinstance(instance, b.MultipleChoiceQuestion):
            dct = MultipleChoiceQuestionSerializer(instance, context=self.context).to_representation(instance)
            dct['type'] = b.MultipleChoiceQuestion.__name__
            return dct

    def create(self, validated_data):
        qtype = validated_data.pop('type', None)
        if qtype == b.TextQuestion.__name__:
            return TextQuestionSerializer(instance=self.instance).create(validated_data)
        if qtype == b.MultipleChoiceQuestion.__name__:
            return MultipleChoiceQuestionSerializer(instance=self.instance).create(validated_data)



class TextQuestionSerializer(serializers.ModelSerializer):
    question = ULTextField()
    type = serializers.CharField(read_only=False, required=False)

    class Meta:
        model = b.TextQuestion
        fields = ('id', 'user', 'type', 'question', 'help_text', 'index', 'is_long_answer')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'user': {'required': False},
            'help_text': {'required': False},
        }


class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    question = ULTextField()
    choices = ULTextArrayField()
    type = serializers.CharField(read_only=False, required=False)

    class Meta:
        model = b.MultipleChoiceQuestion
        fields = ('id', 'user', 'type', 'question', 'help_text', 'index', 'can_select_multiple', 'choices')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'user': {'required': False},
            'help_text': {'required': False},
        }


class BriefSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    questions = QuestionSerializer(many=True)
    title = ULTextField()
    greeting = ULTextField()

    def get_fields(self, *args, **kwargs):
        fields = super(BriefSerializer, self).get_fields(*args, **kwargs)
        user = self.context['request'].user

        def model_queryset(m): return m.objects.all_for(user)

        fields['client'] = serializers.PrimaryKeyRelatedField(queryset=model_queryset(g.Client), allow_null=True)
        fields['quote'] = serializers.PrimaryKeyRelatedField(queryset=model_queryset(q.Quote), allow_null=True)

        return fields

    def update(self, instance, validated_data):
        self._write_questions(self.context['request'].user, self.instance, validated_data.pop('questions'))

        return super(BriefSerializer, self).update(instance, validated_data)

    def create(self, validated_data):
        user = self.context['request'].user
        questions_data = validated_data.pop('questions')
        validated_data.pop('id', None)
        validated_data.update({'user': user})

        instance = super(BriefSerializer, self).create(validated_data)

        self._write_questions(user, instance, questions_data)
        return instance

    class Meta:
        model = Brief
        fields = ('id', 'user', 'name', 'title', 'greeting', 'status', 'token',
                  'modified', 'questions', 'language', 'client', 'quote')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'user': {'required': False},
        }

    def _write_questions(self, user, instance, questions_data):
        init_questions = set(instance.questions.all_for(user))
        new_questions = set()

        for question_data in questions_data:
            question_id = question_data.get('id', None)
            if question_id:
                question_instance = b.Question.objects.get_for(user, 'change', pk=question_id)
                qs = QuestionSerializer(data=question_data, instance=question_instance)
                question = qs.update(question_instance, question_data)
            else:
                question_data.update({'user': self.context['request'].user})
                qs = QuestionSerializer(data=question_data)
                question = qs.create(question_data)

            new_questions.add(question)

        instance.questions = new_questions
        for question in (init_questions - new_questions):
            question.delete()


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
