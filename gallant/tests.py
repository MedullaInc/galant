from django.test import TestCase
from gallant import models


# Create your tests here.
class ULTextTest(TestCase):
    def test_save_load(self):
        json = {'en': 'foobar', 'es': 'barra de foo'}
        obj = models.ULText.objects.create(text_dict=json)
        new_obj = models.ULText.objects.get(id=obj.id)

        self.assertEqual(new_obj.text_dict, json)

    def test_text(self):
        json = {'en': 'foobar', 'es': 'barra de foo'}
        obj = models.ULText.objects.create(text_dict=json)
        new_obj = models.ULText.objects.get(id=obj.id)

        self.assertEqual(new_obj.get_text(), 'foobar')
        self.assertEqual(new_obj.get_text('es'), 'barra de foo')