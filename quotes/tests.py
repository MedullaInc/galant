import autofixture
from django import test
from django.core.urlresolvers import reverse
from quotes import models as q, serializers, views
from autofixture import AutoFixture
from quotes import forms as qf
from gallant import models as g
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

        data = {'projects': [],'services':{}}

        request = factory.patch(reverse('api-quote-detail', args=[quote.id]), data=data, format='json')
        force_authenticate(request, user=user)

        response = views.QuoteViewSet.as_view({'patch': 'partial_update'})(request, pk=quote.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        quote.refresh_from_db()
        self.assertEqual(quote.projects.count(), 0)


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
                                                field_values={'quote': quote, 'user': user, 'client':user})

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
        quote_template = self.quote_template

        serializer = serializers.QuoteTemplateSerializer(quote_template)
        self.assertIsNotNone(serializer.data)

        parser = serializers.QuoteTemplateSerializer(quote_template, data=serializer.data)
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


### DEPRECATED TEST FORMS ARE NO LONGER USED #########
######################################################
"""
class QuoteFormTest(test.TestCase):
    def setUp(self):
        client = AutoFixture(g.Client, generate_fk=True).create(1)
        self.request = type('obj', (object,), {
            'POST': {'status': '1', 'name': 'asdfQuote test edit', 'language': 'en',
                     '-section-0-text': 'test intro text',
                     '-section-0-title': 'modified intro title', '-section-0-name': 'intro', '-section-0-index': '0',
                     '-section-1-name': 'important_notes', '-section-1-title': 'test important notes title',
                     '-section-1-text': 'test important notes text', '-section-1-index': '1', 'client': client[0].id},
            'user': client[0].user,
        })

    def test_create_quote(self):
        f = qf.QuoteForm(self.request.user, self.request.POST)
        s = qf.section_forms_request(self.request)

        self.assertTrue(f.is_valid())

        obj = qf.create_quote(f, s)
        self.assertEquals(obj.id, 1)

    def test_edit_quote(self):
        f = qf.QuoteForm(self.request.user, self.request.POST)
        s = qf.section_forms_request(self.request)

        self.assertTrue(f.is_valid())

        obj = qf.create_quote(f, s)
        new_obj = qf.create_quote(f, s)
        self.assertEquals(obj.id, new_obj.id)

    def test_new_section(self):
        new_data = {'-section-2-title': 'title123', '-section-2-text': 'text123',
                    '-section-2-name': 'section_1', '-section-2-index': '2'}
        self.request.POST.update(new_data)

        f = qf.QuoteForm(self.request.user, self.request.POST)
        s = qf.section_forms_request(self.request)

        self.assertTrue(f.is_valid())

        obj = qf.create_quote(f, s)
        obj.save()

        self.assertEquals(obj.sections.count(), 3)

    def test_new_service(self):
        new_data = {'-service-2-section_name': 'title123', '-service-2-type': '3',
                    '-service-2-description': 'title123', '-service-2-cost_0': '3',
                    '-service-2-quantity': '2', '-service-2-name': 'title123',
                    '-service-2-cost_1': 'USD', '-service-2-index': '2'}
        self.request.POST.update(new_data)

        f = qf.QuoteForm(self.request.user, self.request.POST)
        s = qf.section_forms_request(self.request)

        self.assertTrue(f.is_valid())

        obj = qf.create_quote(f, s)
        obj.save()

        self.assertEquals(obj.services.count(), 1)

    def test_same_sections(self):
        new_data = {'-section-2-title': 'title123', '-section-2-text': 'text123',
                    '-section-2-name': 'section_1', '-section-2-index': '2'}
        self.request.POST.update(new_data)

        f = qf.QuoteForm(self.request.user, self.request.POST)
        s = qf.section_forms_request(self.request)
        for sf in s:
            if not sf.is_valid():
                for field in sf:
                    print '%s: %s' % (field.name, field.errors)

        self.assertTrue(f.is_valid())

        obj = qf.create_quote(f, s)
        obj.save()
        intro_id = obj.intro().id
        important_notes_id = obj.important_notes().id
        section_ids = [s.id for s in obj.sections.all_for(self.request.user)]

        new_data['-section-0-id'] = intro_id
        new_data['-section-1-id'] = important_notes_id
        new_data['-section-2-id'] = section_ids[2]
        self.request.POST.update(new_data)
        s = qf.section_forms_request(self.request)

        new_obj = qf.create_quote(f, s)
        new_obj.save()
        new_section_ids = [s.id for s in new_obj.sections.all_for(self.request.user)]

        self.assertEquals(section_ids, new_section_ids)

    def test_same_services(self):
        new_data = {'-service-2-section_name': 'title123', '-service-2-type': '3',
                    '-service-2-description': 'title123', '-service-2-cost_0': '3',
                    '-service-2-quantity': '2', '-service-2-name': 'title123',
                    '-service-2-index': '2', '-service-2-cost_1': 'USD',
                    '-service-3-section_name': 'title123', '-service-3-type': '3',
                    '-service-3-description': 'title123',
                    '-service-3-cost_0': '3', '-service-3-quantity': '2',
                    '-service-3-name': 'title123', '-service-3-cost_1': 'USD',
                    '-service-3-index': '3'}
        self.request.POST.update(new_data)

        f = qf.QuoteForm(self.request.user, self.request.POST)
        s = qf.section_forms_request(self.request)

        self.assertTrue(f.is_valid())

        obj = qf.create_quote(f, s)
        obj.save()
        service_ids = [s.id for s in obj.services.all_for(self.request.user)]

        new_data['-service-2-id'] = service_ids[0]
        new_data['-service-3-id'] = service_ids[1]
        self.request.POST.update(new_data)
        s = qf.section_forms_request(self.request)

        new_obj = qf.create_quote(f, s)
        new_obj.save()
        new_service_ids = [s.id for s in new_obj.services.all_for(self.request.user)]

        self.assertEquals(service_ids, new_service_ids)

    def test_modify_section(self):
        new_data = {'-section-2-title': 'title123', '-section-2-text': 'text123',
                    '-section-2-name': 'section_1', '-section-2-index': '2'}
        self.request.POST.update(new_data)

        f = qf.QuoteForm(self.request.user, self.request.POST)
        s = qf.section_forms_request(self.request)

        self.assertTrue(f.is_valid())

        obj = qf.create_quote(f, s)
        obj.save()
        section_ids = [s.id for s in obj.sections.all_for(self.request.user)]

        new_data['-section-2-title'] = 'new title'
        self.request.POST.update(new_data)
        s = qf.section_forms_request(self.request)

        new_obj = qf.create_quote(f, s)
        new_obj.save()
        new_section_ids = [s.id for s in new_obj.sections.all_for(self.request.user)]

        self.assertNotEquals(section_ids, new_section_ids)
"""
