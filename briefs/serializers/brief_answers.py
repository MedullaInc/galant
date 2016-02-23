from gallant.serializers.misc import ULTextField
from rest_framework import serializers
from briefs import models as b


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(read_only=True)
    type = serializers.CharField(read_only=False)

    class Meta:
        model = b.Answer
        fields = ('id', 'type', 'question')

    def to_representation(self, instance):
        if isinstance(instance, b.TextAnswer):
            dct = TextAnswerSerializer(instance, context=self.context).to_representation(instance)
            dct['type'] = b.TextAnswer.__name__
            return dct
        elif isinstance(instance, b.MultipleChoiceAnswer):
            dct = MultipleChoiceAnswerSerializer(instance, context=self.context).to_representation(instance)
            dct['type'] = b.MultipleChoiceAnswer.__name__
            return dct


class TextAnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(read_only=True)
    type = serializers.CharField(read_only=False, required=False)

    class Meta:
        model = b.TextAnswer
        fields = ('id', 'type', 'question', 'answer')


class MultipleChoiceAnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(read_only=True)
    type = serializers.CharField(read_only=False, required=False)

    class Meta:
        model = b.MultipleChoiceAnswer
        fields = ('id', 'type', 'question', 'choices')


class BriefAnswersSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    answers = AnswerSerializer(many=True)

    def get_fields(self, *args, **kwargs):
        fields = super(BriefAnswersSerializer, self).get_fields(*args, **kwargs)
        user = self.context['request'].user

        def model_queryset(m): return m.objects.all_for(user)

        fields['brief'] = serializers.PrimaryKeyRelatedField(queryset=model_queryset(b.Brief), allow_null=True)

        return fields

    class Meta:
        model = b.BriefAnswers
        fields = ('id', 'user', 'brief', 'answers')
