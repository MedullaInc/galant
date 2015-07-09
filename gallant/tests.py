from django.test import TransactionTestCase, TestCase
from django import forms
from gallant import models as g
from gallant import fields as gf
from autofixture import AutoFixture
import warnings


class ServiceTest(TransactionTestCase):
    def test_save_load(self):
        fixture = AutoFixture(g.Service, generate_fk=True)
        service = fixture.create(1)[0]
        new_service = g.Service.objects.get(id=service.id)

        self.assertEqual(service.id, new_service.id)

    def test_sub_services(self):
        fixture = AutoFixture(g.Service, generate_fk=True)
        services = fixture.create(10)
        parent = services[9]
        total_cost = parent.cost
        for s in services[0:9]:
            s.parent = parent
            total_cost += s.get_total_cost()
            s.save()

        self.assertEqual(len(services[9].sub_services.all()), 9)
        self.assertEqual(total_cost, parent.get_total_cost())


class ClientTest(TransactionTestCase):
    def test_many_to_many(self):
        fixture = AutoFixture(g.Client, generate_fk=True)
        obj = fixture.create(1)[0]

        self.assertEqual(len(obj.notes.all()), 0)

        note_fixture = AutoFixture(g.Note, generate_fk=True)
        notes = note_fixture.create(10)
        obj.notes = notes
        obj.save()

        self.assertEqual(len(obj.notes.all()), 10)

    def test_language_length(self):
        fixture = AutoFixture(g.Client, generate_fk=True)
        obj = fixture.create(1)[0]
        obj.language = 'zh-hans'

        warnings.filterwarnings('error')

        obj.save()


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