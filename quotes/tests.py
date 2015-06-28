from django.test import TestCase
from quotes.models import *
from autofixture import AutoFixture


# Create your tests here.
class SectionTest(TestCase):
    def test_save_load(self):
        fixture = AutoFixture(Section, generate_fk=True)
        section = fixture.create(1)[0]
        new_section = Section.objects.get(id=section.id)

        self.assertEqual(section.title, new_section.title)
        self.assertEqual(section.text, new_section.text)

    def test_render_html(self):
        fixture = AutoFixture(Section, generate_fk=True)
        section = fixture.create(1)[0]
        new_section = Section.objects.get(id=section.id)

        self.assertTrue(section.render_html().startswith("<h1>"))
        self.assertTrue("</h1><br>" in section.render_html())

    def test_sub_sections(self):
        fixture = AutoFixture(Section, generate_fk=True)
        sections = fixture.create(10)
        for s in sections[0:9]:
            s.parent = sections[9]
            s.save()

        self.assertEqual(len(sections[9].sub_sections.all()), 9)

    def test_safe_html(self):
        fixture = AutoFixture(Section, generate_fk=True)
        section = fixture.create(1)[0]
        section.text = ULText.objects.create(text_dict={'en': '<script>evil</script>'})

        self.assertFalse("<script>" in section.render_html())
