import autofixture
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TransactionTestCase, TestCase
from django import forms
from django.test.client import RequestFactory
from gallant import models as g
from gallant import fields as gf
from gallant import forms as gallant_forms
from briefs import models as b
from gallant.serializers.service import ServiceSerializer
from quotes import models as q
from autofixture import AutoFixture
import warnings


class ServiceTest(TransactionTestCase):
    def test_save_load(self):
        fixture = AutoFixture(g.Service, generate_fk=True)
        service = fixture.create(1)[0]
        new_service = g.Service.objects.get_for(service.user, 'view_service', id=service.id)

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

        self.assertEqual(len(services[9].sub_services.all_for(user, 'view_service')), 9)
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
        for s in service.sub_services.all_for(user, 'view_service'):
            self.assertEqual(s.deleted, 1)
            self.assertEqual(s.deleted_by_parent, 1)

        # Check that notes have deleted = 1 & deleted_by_parent = 1
        for n in service.notes.all_for(user, 'view_note'):
            self.assertEqual(n.deleted, 1)
            self.assertEqual(n.deleted_by_parent, 1)

    def test_service_serialize(self):
        import warnings
        from django.utils.deprecation import RemovedInDjango110Warning
        warnings.filterwarnings("ignore",category=RemovedInDjango110Warning)
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        service = autofixture.create_one(g.Service, generate_fk=True, field_values={'user': user})

        request = RequestFactory().get('/')
        request.user = user
        serializer = ServiceSerializer(service, context={'request': request})
        self.assertIsNotNone(serializer.data)


class ClientTest(TransactionTestCase):
    def test_many_to_many(self):
        fixture = AutoFixture(g.Client, generate_fk=True)
        obj = fixture.create(1)[0]

        self.assertEqual(len(obj.notes.all_for(obj.user, 'view_note')), 0)

        note_fixture = AutoFixture(g.Note, generate_fk=True, field_values={'user': obj.user})
        notes = note_fixture.create(10)
        obj.notes = notes
        obj.save()

        self.assertEqual(len(obj.notes.all_for(obj.user, 'view_note')), 10)

    def test_language_length(self):
        fixture = AutoFixture(g.Client, generate_fk=True)
        obj = fixture.create(1)[0]
        obj.language = 'zh-hans'

        warnings.filterwarnings('error')

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
        for n in client.notes.all_for(client.user, 'view_note'):
            self.assertEqual(n.deleted, 1)
            self.assertEqual(n.deleted_by_parent, 1)

        # Validate client briefs deleted field & deleted_by_parent are 1
        for brief in client.brief_set.all_for(client.user, 'view_brief'):
            self.assertEqual(brief.deleted, 1)
            self.assertEqual(brief.deleted_by_parent, 1)

        # Validate client quotes deleted field & deleted_by_parent are 1
        for quote in client.quote_set.all_for(client.user, 'view_quote'):
            self.assertEqual(quote.deleted, 1)
            self.assertEqual(quote.deleted_by_parent, 1)


class ProjectTest(TransactionTestCase):
    def test_save_load(self):
        fixture = AutoFixture(g.Project, generate_fk=True)
        project = fixture.create(1)[0]
        new_project = g.Project.objects.get_for(project.user, 'view_project', id=project.id)

        self.assertEqual(project.id, new_project.id)

    def test_project_soft_delete(self):
        # Create Project
        fixture = AutoFixture(g.Project, generate_fk=True)
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
        for note in project.notes.all_for(project.user, 'view_note'):
            self.assertEqual(note.deleted, 1)
            self.assertEqual(note.deleted_by_parent, 1)


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


class GallantUserTest(TestCase):
    def test_create_user(self):
        UserModel = get_user_model()
        u = UserModel.objects.create_user(email='foo@bar.com')
        group = Group.objects.get(name='users')

        self.assertTrue(u in group.user_set.all())
