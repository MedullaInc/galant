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
        multiple_choice_question = b.MultipleChoiceQuestion.objects.create(user=brief.user, question='Huh?', choices=['a', 'b', 'c'], index=1)

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
