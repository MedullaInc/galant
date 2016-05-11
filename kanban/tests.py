import autofixture
from django.core.urlresolvers import reverse
from gallant import models as g
from django.test.testcases import TransactionTestCase
from kanban import serializers
from kanban.models import KanbanCard
from rest_framework.test import APIRequestFactory, force_authenticate


class KanbanCardTest(TransactionTestCase):
    def test_save_load(self):
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        card = KanbanCard.objects.create(user=user, title='hi')

        self.assertIsNotNone(card)

    def test_card_serialize_create(self):
        factory = APIRequestFactory()
        user = autofixture.create_one(g.GallantUser, generate_fk=True)
        card = autofixture.create_one('kanban.KanbanCard', generate_fk=True, field_values={'user': user})

        request = factory.get(reverse('api-card-detail', args=[card.id]))
        request.user = user
        force_authenticate(request, user=user)

        serializer = serializers.KanbanCardSerializer(card, context={'request': request})
        self.assertIsNotNone(serializer.data)
        tmp = dict(serializer.data)
        tmp.pop('id')

        parser = serializers.KanbanCardSerializer(data=tmp, context={'request': request})
        self.assertTrue(parser.is_valid())

        self.assertNotEqual(parser.save(user=user).id, card.id)
