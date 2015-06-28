from django.test import TestCase
from gallant.models import *
from autofixture import AutoFixture


# Create your tests here.
class ULTextTest(TestCase):
    def test_save_load(self):
        json = {'en': 'foobar', 'es': 'barra de foo'}
        obj = ULText.objects.create(text_dict=json)
        new_obj = ULText.objects.get(id=obj.id)

        self.assertEqual(new_obj.text_dict, json)

    def test_text(self):
        json = {'en': 'foobar', 'es': 'barra de foo'}
        obj = ULText.objects.create(text_dict=json)
        new_obj = ULText.objects.get(id=obj.id)

        self.assertEqual(new_obj.get_text(), 'foobar')
        self.assertEqual(new_obj.get_text('es'), 'barra de foo')


class ServiceTest(TestCase):
    def test_save_load(self):
        fixture = AutoFixture(Service, generate_fk=True)
        service = fixture.create(1)[0]
        new_service = Service.objects.get(id=service.id)

        self.assertEqual(service.id, new_service.id)

    def test_sub_services(self):
        fixture = AutoFixture(Service, generate_fk=True)
        services = fixture.create(10)
        parent = services[9]
        total_cost = parent.cost
        for s in services[0:9]:
            s.parent = parent
            total_cost += s.get_total_cost()
            s.save()

        self.assertEqual(len(services[9].sub_services.all()), 9)
        self.assertEqual(total_cost, parent.get_total_cost())