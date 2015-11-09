import autofixture
from calendr.views import TasksAPI
from django.utils import timezone
from calendr.models import Task
from django.core.urlresolvers import reverse
from gallant import models as g
from django.test.testcases import TransactionTestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate


class TaskTest(TransactionTestCase):
    def test_save_load(self):
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        task = Task.objects.create(user=user, assignee=user, start=timezone.now(),end=timezone.now())

        self.assertIsNotNone(task)

    def test_access_api_task(self):
        factory = APIRequestFactory()
        user = autofixture.create_one('gallant.GallantUser', generate_fk=True)
        task = autofixture.create_one('calendr.Task', generate_fk=True,
                                      field_values={'user': user})

        request = factory.get(reverse('api-task-detail', args=[task.id]))
        force_authenticate(request, user=user)

        response = TasksAPI.as_view({'get': 'retrieve'})(request, pk=task.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_api_task(self):
        factory = APIRequestFactory()
        user = autofixture.create_one('gallant.GallantUser', generate_fk=True)
        project = autofixture.create_one('gallant.Project', generate_fk=True,
                                              field_values={'user': user})
        task = autofixture.create_one('calendr.Task', generate_fk=True,
                                      field_values={'user': user, 'project': project})
        serialized_task = {"id":task.id, "start": task.start, "end": task.end,
                           "name": task.name, "daily_estimate": task.daily_estimate,
                           "user": task.user_id, "assignee": task.assignee_id,
                           "project": task.project_id}

        request = factory.post(reverse('api-task-list', args=[]), data=serialized_task, format='json')
        force_authenticate(request, user=user)

        response = TasksAPI.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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

        request = factory.patch(reverse('api-task-detail', args=[task.id]), data=data, format='json')
        force_authenticate(request, user=user)

        response = TasksAPI.as_view({'patch': 'partial_update'})(request, pk=task.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task.refresh_from_db()

        self.assertEqual(task.project_id, new_project.id)
        self.assertEqual(task.notes.count(), 0)

    def test_access_api_tasks(self):
        factory = APIRequestFactory()
        user1 = autofixture.create_one('gallant.GallantUser', generate_fk=True, field_values={'is_superuser': False})
        tasks1 = autofixture.create('calendr.Task', 10, generate_fk=True,
                                    field_values={'user': user1})
        user2 = autofixture.create_one('gallant.GallantUser', generate_fk=True, field_values={'is_superuser': False})
        tasks2 = autofixture.create('calendr.Task', 20, generate_fk=True,
                                    field_values={'user': user2})

        tasks1ids = [t.id for t in tasks1]
        tasks2ids = [t.id for t in tasks2]
        self.assertTrue(len(set(tasks1ids) & set(tasks2ids)) == 0)

        request1 = factory.get(reverse('api-task-list') + '?user=%s' % user1.id)
        force_authenticate(request1, user=user1)

        response = TasksAPI.as_view({'get': 'list'})(request1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for d in response.data:
            self.assertTrue(int(d['id']) in tasks1ids)

        request2 = factory.get(reverse('api-task-list') + '?user=%s' % user2.id)
        force_authenticate(request2, user=user2)

        response = TasksAPI.as_view({'get': 'list'})(request2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for d in response.data:
            self.assertTrue(int(d['id']) in tasks2ids)
