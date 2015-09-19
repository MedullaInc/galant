import autofixture
from django import test
from briefs import models as b
from autofixture import AutoFixture
from gallant import models as g
import warnings


class BriefTest(test.TransactionTestCase):
    def test_save_load(self):
        fixture = AutoFixture(b.Brief, generate_fk=True)
        brief = fixture.create(1)[0]
        new_brief = b.Brief.objects.get_for(brief.user, 'view_brief', id=brief.id)
        self.assertEqual(brief.id, new_brief.id)

    def test_brief_soft_delete(self):
        user = autofixture.create_one(g.GallantUser)
        client = autofixture.create_one(g.Client, generate_fk=True, field_values={'user': user})

        # Create Brief
        brief = autofixture.create_one(b.Brief, generate_fk=True, field_values={'user': user, 'client': client})

        # Create Questions
        question = b.TextQuestion.objects.create(user=brief.user, question='What?')
        multiple_choice_question = b.MultipleChoiceQuestion.objects.create(user=brief.user, question='Huh?',
                                                                           choices=['a', 'b', 'c'], index=1)

        # Add questions to Brief
        brief.questions.add(question)
        brief.questions.add(multiple_choice_question)

        # Soft Delete Brief
        brief.soft_delete()

        # Validate Brief deleted field is 1 and deleted_by_parent is 0
        self.assertEqual(brief.deleted, 1)
        self.assertEqual(brief.deleted_by_parent, 0)

        # Validate questions deleted field is 1 and deleted_by_parent is 1
        for q in brief.questions.all_for(user, 'view_question'):
            self.assertEqual(q.deleted, 1)
            self.assertEqual(q.deleted_by_parent, 1)


class BriefTemplateTest(test.TransactionTestCase):
    def test_save_load(self):
        fixture = AutoFixture(b.Brief, generate_fk=True)
        brief = fixture.create(1)[0]
        new_brief = b.Brief.objects.get_for(brief.user, 'view_brief', id=brief.id)
        self.assertEqual(brief.id, new_brief.id)

        template_fixture = AutoFixture(b.BriefTemplate, generate_fk=True)
        template_brief = template_fixture.create(1)[0]
        new_template_brief = b.BriefTemplate.objects.get_for(template_brief.user, 'view_brieftemplate')
        self.assertEqual(template_brief.id, new_template_brief.id)

    def test_brief_template_soft_delete(self):
        user = autofixture.create_one(g.GallantUser)
        client = autofixture.create_one(g.Client, generate_fk=True, field_values={'user': user})

        # Create Brief with Client & without Client
        brief = autofixture.create_one(b.Brief, generate_fk=True, field_values={'user': user, 'client': client})
        brief_no_client = autofixture.create_one(b.Brief, generate_fk=True, field_values={'user': user, 'client': None})

        # Create Questions
        question = b.TextQuestion.objects.create(user=brief.user, question='What?')
        multiple_choice_question = b.MultipleChoiceQuestion.objects.create(user=brief.user, question='Huh?',
                                                                           choices=['a', 'b', 'c'], index=1)

        question_b = b.TextQuestion.objects.create(user=brief.user, question='What?')
        multiple_choice_question_b = b.MultipleChoiceQuestion.objects.create(user=brief.user, question='Huh?',
                                                                             choices=['a', 'b', 'c'], index=1)

        # Add questions to Brief
        brief.questions.add(question)
        brief.questions.add(multiple_choice_question)

        brief_no_client.questions.add(question_b)
        brief_no_client.questions.add(multiple_choice_question_b)

        # Create Template
        template = autofixture.create_one(b.BriefTemplate, generate_fk=True,
                                          field_values={'user': user, 'brief': brief})
        template_no_client = autofixture.create_one(b.BriefTemplate, generate_fk=True,
                                                    field_values={'user': user, 'brief': brief_no_client})

        # Soft Delete Template
        template.soft_delete()
        template_no_client.soft_delete()

        # Validate Template deleted field is 1 and deleted_by_parent is 0
        self.assertEqual(template.deleted, 1)
        self.assertEqual(template.deleted_by_parent, 0)

        # Validate Brief with Client deleted field is 0 and deleted_by_parent is 0
        self.assertEqual(template.brief.deleted, 0)
        self.assertEqual(template.brief.deleted_by_parent, 0)

        # Validate Brief without Client deleted field is 1 and deleted_by_parent is 1
        self.assertEqual(template_no_client.brief.deleted, 1)
        self.assertEqual(template_no_client.brief.deleted_by_parent, 1)
