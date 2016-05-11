from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models as m
from django.db.models.signals import pre_save, post_save
from django.dispatch.dispatcher import receiver
from gallant import models as g
from quotes import models as q
from calendr import models as c


class KanbanCard(g.UserModel):
    title = m.CharField(max_length=255)
    text = m.CharField(max_length=255, blank=True, default='')
    link = m.CharField(max_length=255, blank=True, default='')
    xindex = m.IntegerField(blank=True, default=0)
    yindex = m.IntegerField(blank=True, default=0)
    alert = m.CharField(max_length=63, blank=True, default='')

    class Meta:
        permissions = (
            ('view_service', 'View service'),
        )

    objects = g.UserModelManager()


@receiver(pre_save, sender=g.Service)
def update_service_card_pre(sender, instance, **kwargs):
    if instance.card is None:
        instance.card = KanbanCard.objects.create(user=instance.user)


@receiver(post_save, sender=g.Service)
def update_service_card_post(sender, instance, **kwargs):
    service = instance
    card = service.card

    try:
        quote = service.quote_set.all_for(service.user)[0]
        quote_name = quote.name
        title = service.name.get_text(quote.language)
    except IndexError:
        quote_name = ''
        title = ''

    card.title = title
    card.text = quote_name
    card.xindex = int(service.status or 0)
    card.save()


@receiver(pre_save, sender=g.Client)
def update_client_card_pre(sender, instance, **kwargs):
    if instance.card is None:
        instance.card = KanbanCard.objects.create(user=instance.user)


@receiver(post_save, sender=g.Client)
def update_client_card_post(sender, instance, **kwargs):
    client = instance
    card = client.card

    card.title = client.name
    card.text = client.company
    card.xindex = int(client.status or 0)
    card.link = reverse('client_detail', args=[client.id])
    card.save()


@receiver(pre_save, sender=q.Quote)
def update_quote_card_pre(sender, instance, **kwargs):
    if instance.card is None:
        instance.card = KanbanCard.objects.create(user=instance.user)


@receiver(post_save, sender=q.Quote)
def update_quote_card_post(sender, instance, **kwargs):
    quote = instance
    card = quote.card

    try:
        client_name = quote.client.name
    except AttributeError:
        client_name = ''

    card.title = quote.name
    card.text = client_name
    card.xindex = int(quote.status or 0)
    card.link = reverse('quote_detail', args=[quote.id])
    card.save()


@receiver(pre_save, sender=c.Task)
def update_task_card_pre(sender, instance, **kwargs):
    if instance.card is None:
        instance.card = KanbanCard.objects.create(user=instance.user)


@receiver(post_save, sender=c.Task)
def update_task_card_post(sender, instance, **kwargs):
    task = instance
    card = task.card

    try:
        project_name = task.project.name
    except AttributeError:
        project = ''

    card.title = task.name
    card.text = project_name
    card.xindex = int(task.status or 0)
    card.save()
