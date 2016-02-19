from gallant.serializers.misc import ULTextField, ULTextArrayField
from rest_framework import serializers
from briefs import models as b


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
