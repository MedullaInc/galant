import autofixture
from calendr.models import Task
from gallant import models as g
from django.test.testcases import TransactionTestCase


class TaskTest(TransactionTestCase):
    def test_save_load(self):
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        task = Task.objects.create(user=user, assignee=user)

        self.assertIsNotNone(task)
