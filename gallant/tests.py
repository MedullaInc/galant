from datetime import datetime
import autofixture
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.test import TransactionTestCase, TestCase
from django import forms
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from gallant import models as g
from gallant import fields as gf
from gallant import forms as gallant_forms
from briefs import models as b
from gallant import serializers
from gallant import views
from gallant.enums import ClientStatus, ProjectStatus
from gallant.fields import ULTextDictArray, _ultext_array_to_python, _ultext_to_python
from gallant.models.client import check_client_payments
from moneyed.classes import Money
from quotes import models as q
from autofixture import AutoFixture
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate


class ServiceTest(TransactionTestCase):
    fixtures = ['djmoney_rates.json']

    def test_save_load(self):
        fixture = AutoFixture(g.Service, generate_fk=True)
        service = fixture.create(1)[0]
        new_service = g.Service.objects.get_for(service.user, id=service.id)

        self.assertEqual(service.id, new_service.id)

    def test_service_form(self):
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        form = gallant_forms.ServiceForm(user=user, data={'name': 'asdf', 'description': 'aasdf', 'cost_0': '10',
                                                          'cost_1': 'USD', 'quantity': '10', 'type': '3'})

        self.assertTrue(form.is_valid())

    def test_sub_services(self):
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        fixture = AutoFixture(g.Service, generate_fk=True, field_values={'user': user})
        services = fixture.create(10)
        parent = services[9]
        total_cost = parent.cost
        for s in services[0:9]:
            s.parent = parent
            total_cost += s.get_total_cost()
            s.save()

        self.assertEqual(len(services[9].sub_services.all_for(user)), 9)
        self.assertEqual(total_cost, parent.get_total_cost())

    def test_service_soft_delete(self):
        user = autofixture.create_one(g.GallantUser, generate_fk=True)

        # Create service
        fixture = AutoFixture(g.Service, generate_fk=True, field_values={'user': user})
        service = fixture.create(1)[0]

        # Create sub_services
        fixture = AutoFixture(g.Service, generate_fk=True, field_values={'user': user, 'parent': service})
        fixture.create(2)

        # Add a couple of notes no parent service
        fixture = AutoFixture(g.Note, generate_fk=True, field_values={'text': '[Updated]', 'service': service})
        fixture.create(2)

        # Soft delete service
        service.soft_delete()

        # Check that service has deleted = 1 & deleted_by_parent = 0
        self.assertEqual(service.deleted, 1)
        self.assertEqual(service.deleted_by_parent, 0)

        # Check that subservices have deleted = 1 & deleted_by_parent = 1
        for s in service.sub_services.all_for(user):
            self.assertEqual(s.deleted, 1)
            self.assertEqual(s.deleted_by_parent, 1)

        # Check that notes have deleted = 1 & deleted_by_parent = 1
        for n in service.notes.all_for(user):
            self.assertEqual(n.deleted, 1)
            self.assertEqual(n.deleted_by_parent, 1)

    def test_service_serialize(self):
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        service = autofixture.create_one(g.Service, generate_fk=True, field_values={'user': user})
        service.notes.add(autofixture.create_one(g.Note, generate_fk=True, field_values={'user': user}))

        serializer = serializers.ServiceSerializer(service)
        self.assertIsNotNone(serializer.data)

        parser = serializers.ServiceSerializer(service, data=serializer.data)
        self.assertTrue(parser.is_valid())

        self.assertEqual(parser.save(), service)

    def test_service_serialize_create(self):
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        service = autofixture.create_one(g.Service, generate_fk=True, field_values={'user': user})

        serializer = serializers.ServiceSerializer(service)
        self.assertIsNotNone(serializer.data)

        parser = serializers.ServiceSerializer(data=serializer.data)
        self.assertTrue(parser.is_valid())

        self.assertNotEqual(parser.save(user=user).id, service.id)

    def test_service_serialize_to_rep_lang(self):
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        service = autofixture.create_one(g.Service, generate_fk=True, field_values={'user': user, 'name': {}})

        serializer = serializers.ServiceSerializer(service)
        self.assertIsNotNone(serializer.to_representation_lang(service, 'en'))


class ClientTest(TransactionTestCase):
    def test_many_to_many(self):
        fixture = AutoFixture(g.Client, generate_fk=True)
        obj = fixture.create(1)[0]

        self.assertEqual(len(obj.notes.all_for(obj.user)), 0)

        note_fixture = AutoFixture(g.Note, generate_fk=True, field_values={'user': obj.user})
        notes = note_fixture.create(10)
        obj.notes = notes
        obj.save()

        self.assertEqual(len(obj.notes.all_for(obj.user)), 10)

    def test_language_length(self):
        fixture = AutoFixture(g.Client, generate_fk=True)
        obj = fixture.create(1)[0]
        obj.language = 'zh-hans'

        obj.save()

    def test_client_soft_delete(self):
        # Create Client
        fixture = AutoFixture(g.Client, generate_fk=True)
        client = fixture.create(1)[0]

        # Create Client Notes
        fixture = AutoFixture(g.Note, generate_fk=True, field_values={'text': '[Updated]', 'client': client})
        fixture.create(2)

        # Create Client Brief
        fixture = AutoFixture(b.Brief, generate_fk=True, field_values={'user': client.user, 'client': client})
        fixture.create(1)

        # Create Quote
        fixture = AutoFixture(q.Quote, generate_fk=True, field_values={'client': client})
        fixture.create(1)

        # Soft Delete client
        client.soft_delete()

        # Validate client deleted field is 1 & deleted_by_parent is 0
        self.assertEqual(client.deleted, 1)
        self.assertEqual(client.deleted_by_parent, 0)

        # Validate client notes deleted field & deleted_by_parent are 1
        for n in client.notes.all_for(client.user):
            self.assertEqual(n.deleted, 1)
            self.assertEqual(n.deleted_by_parent, 1)

        # Validate client briefs deleted field & deleted_by_parent are 1
        for brief in client.brief_set.all_for(client.user):
            self.assertEqual(brief.deleted, 1)
            self.assertEqual(brief.deleted_by_parent, 1)

        # Validate client quotes deleted field & deleted_by_parent are 1
        for quote in client.quote_set.all_for(client.user):
            self.assertEqual(quote.deleted, 1)
            self.assertEqual(quote.deleted_by_parent, 1)

    def test_client_serialize(self):
        factory = APIRequestFactory()
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        client = autofixture.create_one(g.Client, generate_fk=True, field_values={'user': user})
        client.notes.add(autofixture.create_one(g.Note, generate_fk=True, field_values={'user': user}))

        request = factory.get(reverse('api_client_detail', args=[client.id]))
        request.user = user
        force_authenticate(request, user=user)

        serializer = serializers.ClientSerializer(client, context={'request': request})
        self.assertIsNotNone(serializer.data)

        parser = serializers.ClientSerializer(client, data=serializer.data, context={'request': request})
        self.assertTrue(parser.is_valid())

        self.assertEqual(parser.save(), client)

    def test_client_serialize_create(self):
        factory = APIRequestFactory()
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        client = autofixture.create_one(g.Client, generate_fk=True, field_values={'user': user})

        request = factory.get(reverse('api_client_detail', args=[client.id]))
        request.user = user
        force_authenticate(request, user=user)

        serializer = serializers.ClientSerializer(client, context={'request': request})
        self.assertIsNotNone(serializer.data)

        parser = serializers.ClientSerializer(data=serializer.data, context={'request': request})
        self.assertTrue(parser.is_valid())

        self.assertNotEqual(parser.save(user=user).id, client.id)

    def test_client_serialize_owed_amount(self):
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

        payment1 = autofixture.create_one(g.Payment, generate_fk=True, field_values=
        {'user': user, 'due': timezone.now(), 'paid_on': timezone.now()})
        payment2 = autofixture.create_one(g.Payment, generate_fk=True, field_values=
        {'user': user, 'due': timezone.now(), 'paid_on': None})
        payment1.amount = Money(300, 'USD')
        payment2.amount = Money(200, 'USD')
        payment1.save()
        payment2.save()
        quote.payments.add(payment1)
        quote.payments.add(payment2)

        request = factory.get(reverse('api_client_detail', args=[client.id]))
        request.user = user
        force_authenticate(request, user=user)

        serializer = serializers.ClientSerializer(client, context={'request': request})
        self.assertEqual(serializer.data['money_owed']['amount'], 200)

    def test_access_api_client(self):
        factory = APIRequestFactory()
        user = autofixture.create_one('gallant.GallantUser', generate_fk=True)
        client = autofixture.create_one('gallant.Client', generate_fk=True,
                                        field_values={'user': user})

        request = factory.get(reverse('api_client_detail', args=[client.id]))
        request.user = user
        force_authenticate(request, user=user)

        response = views.ClientDetailAPI.as_view()(request, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_api_client(self):
        factory = APIRequestFactory()
        user = autofixture.create_one('gallant.GallantUser', generate_fk=True)
        client = autofixture.create_one('gallant.Client', generate_fk=True,
                                        field_values={'user': user})

        client.notes.add(autofixture.create_one('gallant.Note', generate_fk=True,
                                                field_values={'user': user}))
        client.notes.add(autofixture.create_one('gallant.Note', generate_fk=True,
                                                field_values={'user': user}))

        data = {'notes': []}

        request = factory.patch(reverse('api_client_detail', args=[client.id]), data=data, format='json')
        force_authenticate(request, user=user)

        response = views.ClientDetailAPI.as_view()(request, pk=client.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        client.refresh_from_db()
        self.assertEqual(client.notes.count(), 0)


class NoteTest(TransactionTestCase):
    def test_note_serialize(self):
        factory = APIRequestFactory()
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        note = autofixture.create_one(g.Note, generate_fk=True, field_values={'user': user})

        request = factory.get(reverse('api_note_detail', args=[note.id]))
        request.user = user
        force_authenticate(request, user=user)

        serializer = serializers.NoteSerializer(note, context={'request': request})
        self.assertIsNotNone(serializer.data)

        parser = serializers.NoteSerializer(note, data=serializer.data, context={'request': request})
        self.assertTrue(parser.is_valid())

        self.assertEqual(parser.save(), note)

    def test_note_serialize_create(self):
        factory = APIRequestFactory()
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        note = autofixture.create_one(g.Note, generate_fk=True, field_values={'user': user})

        request = factory.get(reverse('api_note_detail', args=[note.id]))
        request.user = user
        force_authenticate(request, user=user)

        serializer = serializers.NoteSerializer(note, context={'request': request})
        self.assertIsNotNone(serializer.data)

        parser = serializers.NoteSerializer(data=serializer.data, context={'request': request})
        self.assertTrue(parser.is_valid())

        self.assertNotEqual(parser.save(user=user).id, note.id)

    def test_access_api_note(self):
        factory = APIRequestFactory()
        user = autofixture.create_one('gallant.GallantUser', generate_fk=True)
        note = autofixture.create_one('gallant.Note', generate_fk=True,
                                      field_values={'user': user})

        request = factory.get(reverse('api_note_detail', args=[note.id]))
        request.user = user
        force_authenticate(request, user=user)

        response = views.NoteDetailAPI.as_view()(request, pk=note.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_api_note(self):
        factory = APIRequestFactory()
        user = autofixture.create_one('gallant.GallantUser', generate_fk=True)
        note = autofixture.create_one('gallant.Note', generate_fk=True,
                                      field_values={'user': user})
        data = {'text': 'asdf'}

        request = factory.patch(reverse('api_note_detail', args=[note.id]), data=data, format='json')
        force_authenticate(request, user=user)

        response = views.NoteDetailAPI.as_view()(request, pk=note.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        note.refresh_from_db()
        self.assertEqual(note.text, 'asdf')


class ProjectTest(TransactionTestCase):
    def test_save_load(self):
        fixture = AutoFixture(g.Project, generate_fk=True)
        project = fixture.create(1)[0]
        new_project = g.Project.objects.get_for(project.user, id=project.id)

        self.assertEqual(project.id, new_project.id)

    def test_project_soft_delete(self):
        # Create Project
        fixture = AutoFixture(g.Project, generate_fk=True, field_values={'status': ProjectStatus.Completed.value})
        project = fixture.create(1)[0]

        # Create Project Notes
        fixture = AutoFixture(g.Note, generate_fk=True, field_values={'project', project})
        fixture.create(2)

        # Soft Delete Project
        project.soft_delete()

        # Validate project deleted field is 1 and deleted_by_parent is 0
        self.assertEqual(project.deleted, 1)
        self.assertEqual(project.deleted_by_parent, 0)

        # Validate project notes deleted and deleted_by_parent fields are 1
        for note in project.notes.all_for(project.user):
            self.assertEqual(note.deleted, 1)
            self.assertEqual(note.deleted_by_parent, 1)

    def test_project_serialize(self):
        factory = APIRequestFactory()
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        project = autofixture.create_one(g.Project, generate_fk=True, field_values={'user': user})
        project.notes.add(autofixture.create_one(g.Note, generate_fk=True, field_values={'user': user}))

        request = factory.get(reverse('api_project_detail', args=[project.id]))
        request.user = user
        force_authenticate(request, user=user)

        serializer = serializers.ProjectSerializer(project, context={'request': request})
        self.assertIsNotNone(serializer.data)

        parser = serializers.ProjectSerializer(project, data=serializer.data, context={'request': request})
        self.assertTrue(parser.is_valid())

        self.assertEqual(parser.save(), project)

    def test_project_serialize_create(self):
        factory = APIRequestFactory()
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        project = autofixture.create_one(g.Project, generate_fk=True, field_values={'user': user})

        request = factory.get(reverse('api_project_detail', args=[project.id]))
        request.user = user
        force_authenticate(request, user=user)

        serializer = serializers.ProjectSerializer(project, context={'request': request})
        self.assertIsNotNone(serializer.data)

        parser = serializers.ProjectSerializer(data=serializer.data, context={'request': request})
        self.assertTrue(parser.is_valid())

        self.assertNotEqual(parser.save(user=user).id, project.id)

    def test_access_api_project(self):
        factory = APIRequestFactory()
        user = autofixture.create_one('gallant.GallantUser', generate_fk=True)

        client = autofixture.create_one(g.Client, generate_fk=True, field_values={
            'user': user, 'currency': 'USD'})
        quote = autofixture.create_one(q.Quote, generate_fk=True, field_values={
            'user': user, 'client': client, 'services': []})
        service = autofixture.create_one(g.Service, generate_fk=True, field_values={
            'user': user, 'quantity': 1})
        service.cost = Money(500, 'USD')
        service.save()

        quote.services.add(service)

        payment = autofixture.create_one(g.Payment, generate_fk=True, field_values=
        {'user': user, 'due': timezone.now(), 'paid_on': timezone.now()})
        payment.amount = Money(100, 'USD')
        payment.save()

        quote.payments.add(payment)
        quote.save

        project = autofixture.create_one('gallant.Project', generate_fk=True,
                                         field_values={'user': user})

        project.quote_set.add(quote)
        project.save

        request = factory.get(reverse('api_project_detail', args=[project.id]))
        request.user = user
        force_authenticate(request, user=user)

        response = views.ProjectDetailAPI.as_view()(request, pk=project.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = serializers.ProjectSerializer(project, context={'request': request})
        project_payments = serializer.get_payments(project)

        self.assertEqual(project_payments['currency'], u'USD')
        self.assertEqual(project_payments['amount'], 100.0)

    def test_update_api_project(self):
        factory = APIRequestFactory()
        user = autofixture.create_one('gallant.GallantUser', generate_fk=True)
        project = autofixture.create_one('gallant.Project', generate_fk=True,
                                         field_values={'user': user})

        project.notes.add(autofixture.create_one('gallant.Note', generate_fk=True,
                                                 field_values={'user': user}))
        project.notes.add(autofixture.create_one('gallant.Note', generate_fk=True,
                                                 field_values={'user': user}))

        data = {'notes': []}

        request = factory.patch(reverse('api_project_detail', args=[project.id]), data=data, format='json')
        force_authenticate(request, user=user)

        response = views.ProjectDetailAPI.as_view()(request, pk=project.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        project.refresh_from_db()
        self.assertEqual(project.notes.count(), 0)


class PaymentTest(TransactionTestCase):
    def setUp(self):
        self.user = autofixture.create_one('gallant.GallantUser', generate_fk=True)
        self.c = autofixture.create_one(g.Client, generate_fk=True, field_values={
            'user': self.user, 'status': ClientStatus.Pending_Payment.value, 'auto_pipeline': True})
        self.quote = autofixture.create_one(q.Quote, generate_fk=True, field_values={
            'user': self.user, 'client': self.c, 'services': []})
        self.p = autofixture.create_one(g.Payment, generate_fk=True,
                                        field_values={'user': self.user, 'due': datetime.now(get_current_timezone()),
                                                      'paid_on': None})
        self.p.amount = Money(200, self.c.currency)
        self.p.save()
        self.quote.payments.add(self.p)

    def test_overdue_alert(self):
        self.assertEqual(self.c.alert, '$200 USD overdue')

    def test_close(self):
        self.p.paid_on = datetime.now(get_current_timezone())
        self.p.save()

        self.c.refresh_from_db()

        self.assertEqual(int(self.c.status), ClientStatus.Closed.value)
        self.assertEqual(self.c.alert, '')


class TestULTextForm(forms.Form):
    field = gf.ULTextFormField()


class TestULTextArrayForm(forms.Form):
    field = gf.ULTextArrayFormField()


class ULTextTest(TestCase):
    def test_ultextfield(self):
        f = TestULTextForm({'field': 'foobar'})
        self.assertTrue(f.is_valid())
        d = f.cleaned_data['field']
        self.assertEqual(d.__class__, gf.ULTextDict)
        self.assertEqual(d.get_text(), 'foobar')

        d.set_text('barra de foo', 'es')
        self.assertEqual(d.get_text('es'), 'barra de foo')

    def test_ultextarrayfield(self):
        f = TestULTextArrayForm({'field': [{"en": "choice 1", "es": "opcion 1"},
                                           {"en": "choice 2", "es": "opcion 2"}]})
        self.assertTrue(f.is_valid())
        d = f.cleaned_data['field']
        self.assertEqual(d[0].__class__, gf.ULTextDict)
        self.assertEqual(d[0].get_text(), 'choice 1')
        self.assertEqual(d[1].get_text('es'), 'opcion 2')

    def test_ultextarray_text(self):
        ulta = ULTextDictArray([{"en": "choice 1", "es": "opcion 1"},
                                {"en": "choice 2", "es": "opcion 2"}])
        ulta2 = _ultext_array_to_python('[{"en": "choice 1", "es": "opcion 1"},'
                                        '{"en": "choice 2", "es": "opcion 2"}]')
        self.assertEqual(ulta, ulta2)

    def test_ultext_string(self):
        ulta = _ultext_array_to_python('')
        self.assertEqual([], ulta)

        ulta = _ultext_array_to_python('{')
        self.assertEqual(['{'], ulta)

        ult = _ultext_to_python('{}')
        self.assertEqual({}, ult)


class GallantUserTest(TestCase):
    def test_create_user(self):
        UserModel = get_user_model()
        group, created = Group.objects.get_or_create(name='users')
        u = UserModel.objects.create_user(email='foo@bar.com')

        self.assertTrue(u in group.user_set.all())

    def test_access_api_users(self):
        factory = APIRequestFactory()
        user = autofixture.create_one('gallant.GallantUser', generate_fk=True)
        project = autofixture.create_one('gallant.Project', generate_fk=True,
                                         field_values={'user': user})

        request = factory.get(reverse('api_users') + '?project=%s' % project.id)
        request.user = user
        force_authenticate(request, user=user)

        response = views.UsersAPI.as_view()(request)
        d = response.data
        for u in d:
            if u['id'] == user.id:
                self.assertEqual(u['email'], user.email)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
