from gallant.serializers.misc import ULTextField
from gallant.utils import get_field_choices
from rest_framework import serializers
from briefs.models import Brief
from gallant import models as g
from briefs import models as b
from quotes import models as q
from .question import QuestionSerializer


class BriefSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    questions = QuestionSerializer(many=True)
    title = ULTextField()
    greeting = ULTextField()
    answered = serializers.SerializerMethodField()
    field_choices = serializers.SerializerMethodField()

    def get_fields(self, *args, **kwargs):
        fields = super(BriefSerializer, self).get_fields(*args, **kwargs)
        user = self.context['request'].user

        def model_queryset(m): return m.objects.all_for(user)

        fields['client'] = serializers.PrimaryKeyRelatedField(queryset=model_queryset(g.Client), allow_null=True)
        fields['quote'] = serializers.PrimaryKeyRelatedField(queryset=model_queryset(q.Quote), allow_null=True)

        return fields

    def get_field_choices(self, brief):
        return get_field_choices(type(brief))

    def get_answered(self, brief):
        return int(brief.status) == b.BriefStatus.Answered.value

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
        fields = ('id', 'user', 'name', 'title', 'greeting', 'status', 'token', 'field_choices',
                  'modified', 'questions', 'language', 'client', 'quote', 'answered')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'user': {'required': False},
            'answered': {'required': False},
        }

    def _write_questions(self, user, instance, questions_data):
        init_questions = set(instance.questions.all_for(user))
        new_questions = set()

        for idx, question_data in enumerate(questions_data):
            question_id = question_data.get('id', None)
            question_data['index'] = idx
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
