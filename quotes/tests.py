from datetime import timedelta
import autofixture
from django import test
from django.core.urlresolvers import reverse
from django.utils import timezone
from moneyed import Money
from quotes import models as q, serializers, views
from gallant.serializers import payment
from autofixture import AutoFixture
from quotes import forms as qf
from gallant import models as g
from quotes.views import QuotePaymentsAPI
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate


class QuoteTest(test.TransactionTestCase):
    def setUp(self):
        self.user = autofixture.create_one(g.GallantUser)
        client = autofixture.create_one(g.Client, generate_fk=True, field_values={'user': self.user})
        self.quote = autofixture.create_one(q.Quote, generate_fk=True,
                                            field_values={'sections': [], 'language': 'en',
                                                          'user': self.user, 'client': client,
                                                          'services': []})

    def test_save_load(self):
        fixture = AutoFixture(q.Quote, generate_fk=True)
        obj = fixture.create(1)[0]
        new_obj = q.Quote.objects.get_for(obj.user, id=obj.id)

        self.assertEqual(obj.id, new_obj.id)

    def test_versions(self):
        user = autofixture.create_one(g.GallantUser)
        fixture = AutoFixture(q.Quote, generate_fk=True, field_values={'user': user})
        objs = fixture.create(10)
        base_quote = objs[9]
        for o in objs[0:9]:
            o.parent = base_quote
            o.save()

        self.assertEqual(len(base_quote.versions.all_for(user)), 9)

    def test_quote_soft_delete(self):
        # Create Quote
        quote = self.quote
        user = self.user

        # Add sections to Quote
        intro = q.Section.objects.create(user=user, name='intro', index=0)
        important_notes = q.Section.objects.create(user=user, name='important_notes', index=1)
        quote.sections.add(intro)
        quote.sections.add(important_notes)

        # Add services to Quote
        fixture = AutoFixture(g.Service, generate_fk=True, field_values={'quote': quote})
        fixture.create(2)

        # Soft Delete Quote
        quote.soft_delete()

        # Validate Quote deleted field is 1 and deleted_by_parent is 0
        self.assertEqual(quote.deleted, 1)
        self.assertEqual(quote.deleted_by_parent, 0)

        # Validate Quote Sections deleted & deleted_by_parent fields are 1
        for section in quote.sections.all_for(user):
            self.assertEqual(section.deleted, 1)
            self.assertEqual(section.deleted_by_parent, 1)

        # Validate Quote Services deleted & deleted_by_parent fields are 1
        for service in quote.services.all_for(user):
            self.assertEqual(service.deleted, 1)
            self.assertEqual(service.deleted_by_parent, 1)

    def test_quote_serialize(self):
        factory = APIRequestFactory()
        quote = self.quote
        user = self.user

        quote.projects.add(autofixture.create_one(g.Project, generate_fk=True, field_values={'user': user}))

        request = factory.get(reverse('api-quote-detail', args=[quote.id]))
        request.user = user
        force_authenticate(request, user=user)

        serializer = serializers.QuoteSerializer(quote, context={'request': request})
        self.assertIsNotNone(serializer.data)

        parser = serializers.QuoteSerializer(quote, data=serializer.data, context={'request': request})
        self.assertTrue(parser.is_valid())

        self.assertEqual(parser.save(), quote)

    def test_quote_serialize_create(self):
        factory = APIRequestFactory()
        quote = self.quote
        user = self.user

        request = factory.get(reverse('api-quote-detail', args=[quote.id]))
        request.user = user
        force_authenticate(request, user=user)

        serializer = serializers.QuoteSerializer(quote, context={'request': request})
        self.assertIsNotNone(serializer.data)

        parser = serializers.QuoteSerializer(data=serializer.data, context={'request': request})
        self.assertTrue(parser.is_valid())

        self.assertNotEqual(parser.save(user=user).id, quote.id)

    def test_quote_payment_serialize_create(self):
        factory = APIRequestFactory()
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        client = autofixture.create_one(g.Client, generate_fk=True, field_values={
            'user': user, 'currency': 'USD'})
        quote = autofixture.create_one(q.Quote, generate_fk=True, field_values={
            'user': user, 'client': client, 'services': []})
        service = autofixture.create_one(g.Service, generate_fk=True, field_values={
            'user': user, 'quantity': 1})
        service.cost = Money(500, 'USD')
        service.save()
        quote.services.add(service)

        project = autofixture.create_one('gallant.Project', generate_fk=True,
                                         field_values={'user': user})

        project.quote_set.add(quote)

        p = autofixture.create_one(g.Payment, generate_fk=True,
                                         field_values={'user': user, 'due': timezone.now() + timedelta(days=1),
                                                       'paid_on': None})

        serialized_payment = {"project_id": project.id, "quote_id": quote.id, "amount": {"currency": "USD", "amount": 100.0},
                              "description": p.description,
                              "due": p.due, "paid_on": p.paid_on, "notes": []}

        request = factory.post('/en/quote/api/payment', data=serialized_payment, format='json')

        force_authenticate(request, user=user)

        response = QuotePaymentsAPI.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_access_api_quote(self):
        factory = APIRequestFactory()
        quote = self.quote
        user = self.user

        request = factory.get(reverse('api-quote-detail', args=[quote.id]))
        request.user = user
        force_authenticate(request, user=user)

        response = views.QuoteViewSet.as_view({'get': 'retrieve'})(request, pk=quote.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_api_quote(self):
        factory = APIRequestFactory()
        quote = self.quote
        user = self.user

        quote.projects.add(autofixture.create_one('gallant.Project', generate_fk=True,
                                                  field_values={'user': user}))

        data = {'projects': [], 'services': [], 'sections': []}

        request = factory.patch(reverse('api-quote-detail', args=[quote.id]), data=data, format='json')

        class Object(object):
            def add(self, a, b):
                pass

        request._messages = Object()

        force_authenticate(request, user=user)

        response = views.QuoteViewSet.as_view({'patch': 'partial_update'})(request, pk=quote.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        quote.refresh_from_db()
        self.assertEqual(quote.projects.count(), 0)

    def test_access_api_quote_client(self):
        quote = self.quote
        request = APIRequestFactory().get("")
        quote_detail = views.QuoteClientDetail.as_view({'get': 'retrieve'})
        response = quote_detail(request, token=quote.token)
        self.assertEqual(response.status_code, 200)

    def test_update_api_quote_client(self):
        quote = self.quote
        s1 = q.Section.objects.create(user=self.user, name='intro', title='intro', index='0')
        s2 = q.Section.objects.create(user=self.user, name='notes', title='notes', index='1')
        quote.sections.add(s1)
        quote.sections.add(s2)

        request = APIRequestFactory().patch("", data={
            'token': quote.token,
            'name': 'bogus name',
            'views': 2,
            'sections': [{'id': s1.id, 'views': 3}],
            'services': [{}]
        }, format='json')

        quote_detail = views.QuoteClientUpdate.as_view({'patch': 'partial_update'})
        quote_detail(request, token=quote.token)
        quote.refresh_from_db()
        s1.refresh_from_db()
        self.assertEqual(quote.views, 2)
        self.assertEqual(len(quote.sections.all_for(quote.user)), 2)
        self.assertEqual(s1.views, 3)


class QuoteTemplateTest(test.TestCase):
    def setUp(self):
        user = autofixture.create_one(g.GallantUser)
        client = autofixture.create_one(g.Client, generate_fk=True, field_values={'user': user})

        quote = autofixture.create_one(q.Quote, generate_fk=True,
                                       field_values={'sections': [], 'language': 'en', 'user': user, 'client': client})
        i = q.Section.objects.create(user=quote.user, name='intro', index=0)
        m = q.Section.objects.create(user=quote.user, name='important_notes', index=1)
        quote.sections.add(i)
        quote.sections.add(m)
        quote_template = autofixture.create_one(q.QuoteTemplate, generate_fk=True,
                                                field_values={'quote': quote, 'user': user, 'client': user})

        self.user = user
        self.quote = quote
        self.quote_template = quote_template

    def test_save_load(self):
        quote = self.quote
        new_quote = q.Quote.objects.get_for(quote.user, id=quote.id)

        self.assertEqual(quote.id, new_quote.id)

    def test_quote_template_soft_delete(self):
        user = self.user
        quote_template = self.quote_template
        # Create Quote with no Client
        quote_no_client = autofixture.create_one(q.Quote, generate_fk=True,
                                                 field_values={'sections': [], 'language': 'en', 'user': user,
                                                               'client': None})
        i = q.Section.objects.create(user=quote_no_client.user, name='intro', index=0)
        m = q.Section.objects.create(user=quote_no_client.user, name='important_notes', index=1)
        quote_no_client.sections.add(i)
        quote_no_client.sections.add(m)

        # Create Quote Templates
        quote_template_b = autofixture.create_one(q.QuoteTemplate, generate_fk=True,
                                                  field_values={'quote': quote_no_client, 'user': user})

        # Soft Delete Quote Templates
        quote_template.soft_delete()
        quote_template_b.soft_delete()

        # Validate Quote Templates deleted field is 1 and deleted_by_parent is 0
        self.assertEqual(quote_template.deleted, 1)
        self.assertEqual(quote_template.deleted_by_parent, 0)
        self.assertEqual(quote_template_b.deleted, 1)
        self.assertEqual(quote_template_b.deleted_by_parent, 0)

        # Validate Quote with Client was not deleted
        self.assertEqual(quote_template.quote.deleted, 0)
        self.assertEqual(quote_template.quote.deleted_by_parent, 0)

        # Validate Quote without Client was deleted
        self.assertEqual(quote_template_b.quote.deleted, 1)
        self.assertEqual(quote_template_b.quote.deleted_by_parent, 1)

    def test_quote_template_serialize(self):
        factory = APIRequestFactory()
        quote_template = self.quote_template
        user = self.user
        quote_template.user = user

        request = factory.get(reverse('api-quote-template-detail', args=[quote_template.id]))
        request.user = self.user
        force_authenticate(request, user=user)

        serializer = serializers.QuoteTemplateSerializer(quote_template, context={'request': request})

        self.assertIsNotNone(serializer.data)

        parser = serializers.QuoteTemplateSerializer(quote_template, data=serializer.data, context={'request': request})
        self.assertTrue(parser.is_valid())

    def test_access_api_quote_template(self):
        factory = APIRequestFactory()
        quote_template = self.quote_template
        user = self.user

        request = factory.get(reverse('api-quote-template-detail', args=[quote_template.id]))
        request.user = user
        force_authenticate(request, user=user)

        response = views.QuoteTemplateViewSet.as_view({'get': 'retrieve'})(request, pk=quote_template.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
