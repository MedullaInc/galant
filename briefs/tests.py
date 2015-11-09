import autofixture
from django import test
from briefs import models as b, serializers, views
from autofixture import AutoFixture
from django.core.urlresolvers import reverse
from gallant import models as g
from quotes import models as q
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate


class BriefTest(test.TransactionTestCase):
    def setUp(self):
        user = autofixture.create_one(g.GallantUser)
        client = autofixture.create_one(g.Client, generate_fk=True, field_values={'user': user})
        quote = autofixture.create_one(q.Quote, generate_fk=True, field_values={'user': user})

        # Create Brief
        brief = autofixture.create_one(b.Brief, generate_fk=True, field_values={'user': user, 'client': client})

        # Create Questions
        question = b.TextQuestion.objects.create(user=brief.user, question='What?')
        multiple_choice_question = b.MultipleChoiceQuestion.objects.create(user=brief.user, question='Huh?',
                                                                           choices=['a', 'b', 'c'], index=1)

        # Add questions to Brief
        brief.questions.add(question)
        brief.questions.add(multiple_choice_question)
        brief.quote = quote
        self.user = user
        self.brief = brief
        
    def test_save_load(self):
        fixture = AutoFixture(b.Brief, generate_fk=True)
        brief = fixture.create(1)[0]
        new_brief = b.Brief.objects.get_for(brief.user, id=brief.id)
        self.assertEqual(brief.id, new_brief.id)

    def test_brief_soft_delete(self):
        brief = self.brief
        user = self.user

        # Soft Delete Brief
        brief.soft_delete()

        # Validate Brief deleted field is 1 and deleted_by_parent is 0
        self.assertEqual(brief.deleted, 1)
        self.assertEqual(brief.deleted_by_parent, 0)

        # Validate questions deleted field is 1 and deleted_by_parent is 1
        for q in brief.questions.all_for(user):
            self.assertEqual(q.deleted, 1)
            self.assertEqual(q.deleted_by_parent, 1)

    def test_brief_serialize(self):
        factory = APIRequestFactory()
        brief = self.brief
        user = self.user

        request = factory.get(reverse('api-brief-detail', args=[brief.id]))
        request.user = user
        force_authenticate(request, user=user)
        
        serializer = serializers.BriefSerializer(brief, context={'request': request})
        self.assertIsNotNone(serializer.data)

        parser = serializers.BriefSerializer(brief, data=serializer.data, context={'request': request})
        self.assertTrue(parser.is_valid())

        self.assertEqual(parser.save(), brief)

    def test_brief_serialize_create(self):
        factory = APIRequestFactory()
        brief = self.brief
        user = self.user

        request = factory.get(reverse('api-brief-detail', args=[brief.id]))
        request.user = user
        force_authenticate(request, user=user)

        serializer = serializers.BriefSerializer(brief, context={'request': request})
        self.assertIsNotNone(serializer.data)

        parser = serializers.BriefSerializer(data=serializer.data, context={'request': request})
        self.assertTrue(parser.is_valid())

        self.assertNotEqual(parser.save(user=user).id, brief.id)

    def test_access_api_brief(self):
        factory = APIRequestFactory()
        brief = self.brief
        user = self.user

        request = factory.get(reverse('api-brief-detail', args=[brief.id]))
        request.user = user
        force_authenticate(request, user=user)

        response = views.BriefViewSet.as_view({'get': 'retrieve'})(request, pk=brief.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_api_brief(self):
        factory = APIRequestFactory()
        brief = self.brief
        user = self.user

        data = {'questions': []}

        request = factory.patch(reverse('api-brief-detail', args=[brief.id]), data=data, format='json')
        force_authenticate(request, user=user)

        class Object(object):
            def add(self, a, b):
                pass
        request._messages = Object()

        response = views.BriefViewSet.as_view({'patch': 'partial_update'})(request, pk=brief.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        brief.refresh_from_db()
        self.assertEqual(brief.questions.count(), 0)


class BriefTemplateTest(test.TransactionTestCase):
    def setUp(self):
        user = autofixture.create_one(g.GallantUser)
        client = autofixture.create_one(g.Client, generate_fk=True, field_values={'user': user})
        quote = autofixture.create_one(q.Quote, generate_fk=True, field_values={'user': user})

        # Create Brief
        brief = autofixture.create_one(b.Brief, generate_fk=True, field_values={'user': user, 'client': client})

        # Create Questions
        question = b.TextQuestion.objects.create(user=brief.user, question='What?')
        multiple_choice_question = b.MultipleChoiceQuestion.objects.create(user=brief.user, question='Huh?',
                                                                           choices=['a', 'b', 'c'], index=1)

        # Add questions to Brief
        brief.questions.add(question)
        brief.questions.add(multiple_choice_question)
        brief.quote = quote
        
        brief_template = autofixture.create_one(b.BriefTemplate, generate_fk=True,
                                                field_values={'user': user, 'brief': brief})
        self.user = user
        self.brief = brief
        self.brief_template = brief_template
        
    def test_save_load(self):
        fixture = AutoFixture(b.Brief, generate_fk=True)
        brief = fixture.create(1)[0]
        new_brief = b.Brief.objects.get_for(brief.user, id=brief.id)
        self.assertEqual(brief.id, new_brief.id)

        template_fixture = AutoFixture(b.BriefTemplate, generate_fk=True)
        template_brief = template_fixture.create(1)[0]
        new_template_brief = b.BriefTemplate.objects.all_for(template_brief.user)[0]
        self.assertEqual(template_brief.id, new_template_brief.id)

    def test_brief_template_soft_delete(self):
        user = self.user
        brief = self.brief
        brief_no_client = autofixture.create_one(b.Brief, generate_fk=True, field_values={'user': user, 'client': None})

        # Create Questions
        question = b.TextQuestion.objects.create(user=brief.user, question='What?')
        multiple_choice_question = b.MultipleChoiceQuestion.objects.create(user=brief.user, question='Huh?',
                                                                           choices=['a', 'b', 'c'], index=1)

        question_b = b.TextQuestion.objects.create(user=brief.user, question='What?')
        multiple_choice_question_b = b.MultipleChoiceQuestion.objects.create(user=brief.user, question='Huh?',
                                                                             choices=['a', 'b', 'c'], index=1)

        # Add questions to Brief
        brief.questions.add(question)
        brief.questions.add(multiple_choice_question)

        brief_no_client.questions.add(question_b)
        brief_no_client.questions.add(multiple_choice_question_b)

        # Create Template
        template = self.brief_template
        template_no_client = autofixture.create_one(b.BriefTemplate, generate_fk=True,
                                                    field_values={'user': user, 'brief': brief_no_client})

        # Soft Delete Template
        template.soft_delete()
        template_no_client.soft_delete()

        # Validate Template deleted field is 1 and deleted_by_parent is 0
        self.assertEqual(template.deleted, 1)
        self.assertEqual(template.deleted_by_parent, 0)

        # Validate Brief with Client deleted field is 0 and deleted_by_parent is 0
        self.assertEqual(template.brief.deleted, 0)
        self.assertEqual(template.brief.deleted_by_parent, 0)

        # Validate Brief without Client deleted field is 1 and deleted_by_parent is 1
        self.assertEqual(template_no_client.brief.deleted, 1)
        self.assertEqual(template_no_client.brief.deleted_by_parent, 1)

    def test_brief_template_serialize(self):
        factory = APIRequestFactory()
        brief_template = self.brief_template
        user = self.user

        request = factory.get(reverse('api_brief_template_detail', args=[brief_template.id]))
        request.user = user
        force_authenticate(request, user=user)
        
        serializer = serializers.BriefTemplateSerializer(brief_template, context={'request': request})
        self.assertIsNotNone(serializer.data)

        parser = serializers.BriefTemplateSerializer(brief_template, data=serializer.data, context={'request': request})
        self.assertTrue(parser.is_valid())

        self.assertEqual(parser.save(), brief_template)

    def test_brief_template_serialize_create(self):
        factory = APIRequestFactory()
        brief_template = self.brief_template
        user = self.user

        request = factory.get(reverse('api_brief_template_detail', args=[brief_template.id]))
        request.user = user
        force_authenticate(request, user=user)

        serializer = serializers.BriefTemplateSerializer(brief_template, context={'request': request})
        self.assertIsNotNone(serializer.data)

        parser = serializers.BriefTemplateSerializer(data=serializer.data, context={'request': request})
        self.assertTrue(parser.is_valid())

    def test_access_api_brief_template(self):
        factory = APIRequestFactory()
        brief_template = self.brief_template
        user = self.user

        request = factory.get(reverse('api_brief_template_detail', args=[brief_template.id]))
        request.user = user
        force_authenticate(request, user=user)

        response = views.BriefTemplateDetailAPI.as_view()(request, pk=brief_template.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class QuestionTest(test.TransactionTestCase):
    def setUp(self):
        user = autofixture.create_one(g.GallantUser)
        question = b.TextQuestion.objects.create(user=user, question='What?')
        multiple_choice_question = b.MultipleChoiceQuestion.objects.create(user=user, question='Huh?',
                                                                           choices=['a', 'b', 'c'], index=1)
        self.user = user
        self.question = question
        self.multiple_choice_question = multiple_choice_question
    
    def test_question_serialize(self):
        question = self.question

        serializer = serializers.QuestionSerializer(question)
        self.assertIsNotNone(serializer.data)

        parser = serializers.QuestionSerializer(question, data=serializer.data)
        self.assertTrue(parser.is_valid())

        self.assertEqual(parser.save(), question)

    def test_question_serialize_create(self):
        question = self.question

        serializer = serializers.QuestionSerializer(question)
        self.assertIsNotNone(serializer.data)

        parser = serializers.QuestionSerializer(data=serializer.data)
        self.assertTrue(parser.is_valid())
    
    def test_multiple_choice_question_serialize(self):
        multiple_choice_question = self.multiple_choice_question
        
        serializer = serializers.QuestionSerializer(multiple_choice_question)
        self.assertIsNotNone(serializer.data)

        parser = serializers.QuestionSerializer(multiple_choice_question, data=serializer.data)
        self.assertTrue(parser.is_valid())

        self.assertEqual(parser.save(), multiple_choice_question)

    def test_multiple_choice_question_serialize_create(self):
        multiple_choice_question = self.multiple_choice_question

        serializer = serializers.QuestionSerializer(multiple_choice_question)
        self.assertIsNotNone(serializer.data)

        parser = serializers.QuestionSerializer(data=serializer.data)
        self.assertTrue(parser.is_valid())

    def test_access_api_question(self):
        factory = APIRequestFactory()
        question = self.question
        user = self.user

        request = factory.get(reverse('api_question_detail', args=[question.id]))
        request.user = user
        force_authenticate(request, user=user)

        response = views.QuestionDetailAPI.as_view()(request, pk=question.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_api_question(self):
        factory = APIRequestFactory()
        question = self.question
        user = self.user

        request = factory.patch(reverse('api_question_detail', args=[question.id]), {'is_long_answer': True})
        request.user = user
        force_authenticate(request, user=user)

        response = views.QuestionDetailAPI.as_view()(request, pk=question.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
