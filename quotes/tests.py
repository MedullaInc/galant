from django.test import TransactionTestCase
from quotes import models as q
from gallant import models as g
from autofixture import AutoFixture


# Create your tests here.
class SectionTest(TransactionTestCase):
    def test_save_load(self):
        fixture = AutoFixture(q.Section, generate_fk=True)
        section = fixture.create(1)[0]
        new_section = q.Section.objects.get(id=section.id)

        self.assertEqual(section.title, new_section.title)
        self.assertEqual(section.text, new_section.text)

    def test_render_html(self):
        fixture = AutoFixture(q.Section, generate_fk=True)
        section = fixture.create(1)[0]

        self.assertTrue(section.render_html().startswith("<h1>"))
        self.assertTrue("</h1><br>" in section.render_html())

    def test_sub_sections(self):
        fixture = AutoFixture(q.Section, generate_fk=True)
        sections = fixture.create(10)
        for s in sections[0:9]:
            s.parent = sections[9]
            s.save()

        self.assertEqual(len(sections[9].sub_sections.all()), 9)

    def test_safe_html(self):
        fixture = AutoFixture(q.Section, generate_fk=True)
        section = fixture.create(1)[0]
        section.text.set_text('<script>evil</script>')

        self.assertFalse("<script>" in section.render_html())


class QuoteTest(TransactionTestCase):
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

