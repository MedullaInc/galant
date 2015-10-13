import autofixture
from calendr.models import Task
from calendr.serializers import TaskSerializer
from calendr.views import TaskDetailAPI
from django.core.urlresolvers import reverse
from gallant import models as g
from django.test.testcases import TransactionTestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate


class TaskTest(TransactionTestCase):
    def test_save_load(self):
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        task = Task.objects.create(user=user, assignee=user)

        self.assertIsNotNone(task)

    def test_access_api_task(self):
        factory = APIRequestFactory()
        user = autofixture.create_one('gallant.GallantUser', generate_fk=True)
        task = autofixture.create_one('calendr.Task', generate_fk=True,
                                      field_values={'user': user})

        request = factory.get(reverse('api_task_detail', args=[task.id]))
        force_authenticate(request, user=user)

        response = TaskDetailAPI.as_view()(request, pk=task.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_api_task(self):
        factory = APIRequestFactory()
        user = autofixture.create_one('gallant.GallantUser', generate_fk=True)
        task = autofixture.create_one('calendr.Task', generate_fk=True,
                                      field_values={'user': user})

        task.notes.add(autofixture.create_one('gallant.Note', generate_fk=True,
                                              field_values={'user': user}))
        task.notes.add(autofixture.create_one('gallant.Note', generate_fk=True,
                                              field_values={'user': user}))
        task.project = autofixture.create_one('gallant.Project', generate_fk=True,
                                              field_values={'user': user})
        
        new_project = autofixture.create_one('gallant.Project', generate_fk=True,
                                             field_values={'user': user})
        
        data = {'project': new_project.id, 'notes': []}

        request = factory.patch(reverse('api_task_detail', args=[task.id]), data=data, format='json')
        force_authenticate(request, user=user)

        response = TaskDetailAPI.as_view()(request, pk=task.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task.refresh_from_db()

        self.assertEqual(task.project_id, new_project.id)
        self.assertEqual(task.notes.count(), 0)
