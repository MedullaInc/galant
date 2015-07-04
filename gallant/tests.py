from django.test import TransactionTestCase
from gallant import models as g
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