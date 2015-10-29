from gallant.serializers.misc import ULTextField
from rest_framework import serializers
from briefs.models import Brief, BriefTemplate
from gallant.serializers import misc
from gallant import models as g
from briefs import models as b
from quotes import models as q


class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    question = ULTextField()

    class Meta:
        model = b.Question
        fields = ('id', 'user', 'question', 'help_text', 'index')

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


class TextQuestionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    question = ULTextField()

    class Meta:
        model = b.TextQuestion
        fields = ('id', 'user', 'question', 'help_text', 'index', 'is_long_answer')


class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    question = ULTextField()

    class Meta:
        model = b.MultipleChoiceQuestion
        fields = ('id', 'user', 'question', 'help_text', 'index', 'can_select_multiple', 'choices')


class BriefSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    questions = QuestionSerializer(many=True)

    def get_fields(self, *args, **kwargs):
        fields = super(BriefSerializer, self).get_fields(*args, **kwargs)
        user = self.context['request'].user

        def model_queryset(m): return m.objects.all_for(user)

        fields['client'] = serializers.PrimaryKeyRelatedField(queryset=model_queryset(g.Client))
        fields['quote'] = serializers.PrimaryKeyRelatedField(queryset=model_queryset(q.Quote))

        return fields

    class Meta:
        model = Brief
        fields = ('id', 'user', 'name', 'title', 'greeting', 'status', 'token',
                  'modified', 'questions', 'language', 'client', 'quote')


class BriefTemplateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    brief = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = BriefTemplate
        fields = ('id', 'user', 'brief')