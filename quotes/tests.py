from django import test
from quotes import models as q
from autofixture import AutoFixture
from quotes import forms as qf
from gallant import models as g


# Create your tests here.
class SectionTest(test.TransactionTestCase):
    def test_save_load(self):
        fixture = AutoFixture(q.Section, generate_fk=True)
        section = fixture.create(1)[0]
        new_section = q.Section.objects.get(id=section.id)

        self.assertEqual(section.title, new_section.title)
        self.assertEqual(section.text, new_section.text)
        
    def test_sub_sections(self):
        fixture = AutoFixture(q.Section, generate_fk=True)
        sections = fixture.create(10)
        for s in sections[0:9]:
            s.parent = sections[9]
            s.save()

        self.assertEqual(len(sections[9].sub_sections.all()), 9)


class QuoteTest(test.TransactionTestCase):
    def test_save_load(self):
        fixture = AutoFixture(q.Quote, generate_fk=True)
        obj = fixture.create(1)[0]
        new_obj = q.Quote.objects.get(id=obj.id)

        self.assertEqual(obj.id, new_obj.id)

    def test_versions(self):
        fixture = AutoFixture(q.Quote, generate_fk=True)
        objs = fixture.create(10)
        base_quote = objs[9]
        for o in objs[0:9]:
            o.parent = base_quote
            o.save()

        self.assertEqual(len(base_quote.versions.all()), 9)


class QuoteFormTest(test.TestCase):
    data = {'status': '1', 'name': 'asdfQuote test edit', 'language': 'en', '-section-0-text': 'test intro text',
            '-section-0-title': 'modified intro title', '-section-0-name': 'intro', '-section-1-name': 'margin',
            '-section-1-title': 'test margin title', '-section-1-text': 'test margin text',}

    def setUp(self):
        client = AutoFixture(g.Client, generate_fk=True).create(1)
        self.data['client'] = client[0].id

    def test_create_quote(self):
        f = qf.QuoteForm(self.data)
        s = qf.section_forms_post(self.data)

        self.assertTrue(f.is_valid())

        obj = qf.create_quote(f, s)
        self.assertEquals(obj.id, 1)

    def test_edit_quote(self):
        f = qf.QuoteForm(self.data)
        s = qf.section_forms_post(self.data)

        self.assertTrue(f.is_valid())

        obj = qf.create_quote(f, s)
        new_obj = qf.create_quote(f, s)
        self.assertEquals(obj.id, new_obj.id)

    def test_new_section(self):
        new_data = {'-section-2-title': 'title123', '-section-2-text': 'text123', '-section-2-name': 'section_1'}
        new_data.update(self.data)

        f = qf.QuoteForm(new_data)
        s = qf.section_forms_post(new_data)

        self.assertTrue(f.is_valid())

        obj = qf.create_quote(f, s)
        obj.save()

        self.assertEquals(obj.sections.count(), 3)

    def test_new_service(self):
        new_data = {'-service-2-section_name': 'title123', '-service-2-type': '3',
                    '-service-2-description': 'title123', '-service-2-cost_0': '3',
                    '-service-2-quantity': '2', '-service-2-name': 'title123',
                    '-service-2-cost_1': 'USD'}
        new_data.update(self.data)

        f = qf.QuoteForm(new_data)
        s = qf.section_forms_post(new_data)

        self.assertTrue(f.is_valid())

        obj = qf.create_quote(f, s)
        obj.save()

        self.assertEquals(obj.services.count(), 1)

    def test_same_sections(self):
        new_data = {'-section-2-title': 'title123', '-section-2-text': 'text123', '-section-2-name': 'section_1'}
        new_data.update(self.data)

        f = qf.QuoteForm(new_data)
        s = qf.section_forms_post(new_data)

        self.assertTrue(f.is_valid())

        obj = qf.create_quote(f, s)
        obj.save()
        intro_id = obj.intro().id
        margin_id = obj.margin().id
        section_ids = [s.id for s in obj.sections.all()]

        new_data['-section-0-id'] = intro_id
        new_data['-section-1-id'] = margin_id
        new_data['-section-2-id'] = section_ids[2]
        s = qf.section_forms_post(new_data)

        new_obj = qf.create_quote(f, s)
        new_obj.save()
        new_section_ids = [s.id for s in new_obj.sections.all()]

        self.assertEquals(section_ids, new_section_ids)

    def test_same_services(self):
        new_data = {'-service-2-section_name': 'title123', '-service-2-type': '3',
                    '-service-2-description': 'title123', '-service-2-cost_0': '3',
                    '-service-2-quantity': '2', '-service-2-name': 'title123',
                    '-service-2-cost_1': 'USD', '-service-3-section_name': 'title123',
                    '-service-3-type': '3', '-service-3-description': 'title123',
                    '-service-3-cost_0': '3', '-service-3-quantity': '2',
                    '-service-3-name': 'title123', '-service-3-cost_1': 'USD'}
        new_data.update(self.data)

        f = qf.QuoteForm(new_data)
        s = qf.section_forms_post(new_data)

        self.assertTrue(f.is_valid())

        obj = qf.create_quote(f, s)
        obj.save()
        service_ids = [s.id for s in obj.services.all()]

        new_data['-service-2-id'] = service_ids[0]
        new_data['-service-3-id'] = service_ids[1]
        s = qf.section_forms_post(new_data)

        new_obj = qf.create_quote(f, s)
        new_obj.save()
        new_service_ids = [s.id for s in new_obj.services.all()]

        self.assertEquals(service_ids, new_service_ids)

    def test_modify_section(self):
        new_data = {'-section-2-title': 'title123', '-section-2-text': 'text123', '-section-2-name': 'section_1'}
        new_data.update(self.data)

        f = qf.QuoteForm(new_data)
        s = qf.section_forms_post(new_data)

        self.assertTrue(f.is_valid())

        obj = qf.create_quote(f, s)
        obj.save()
        section_ids = [s.id for s in obj.sections.all()]

        new_data['-section-2-title'] = 'new title'
        s = qf.section_forms_post(new_data)

        new_obj = qf.create_quote(f, s)
        new_obj.save()
        new_section_ids = [s.id for s in new_obj.sections.all()]

        self.assertNotEquals(section_ids, new_section_ids)
