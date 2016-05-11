from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models as m
from django.db.models.signals import pre_save
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
def update_service_card(sender, instance, **kwargs):
    service = instance
    card = service.card

    try:
        quote = service.quote_set.all_for(service.user)[0]
        quote_name = quote.name
        title = service.name.get_text(quote.language)
    except IndexError:
        quote_name = ''
        title = ''

    if card is None:
        service.card = KanbanCard.objects.create(user=service.user,
                                                 title=title,
                                                 text=quote_name,
                                                 xindex=int(service.status or 0))
    else:
        card.title = title
        card.text = quote_name
        card.xindex = int(service.status or 0)
        card.save()


@receiver(pre_save, sender=g.Client)
def update_client_card(sender, instance, **kwargs):
    client = instance
    card = client.card

    if card is None:
        client.card = KanbanCard.objects.create(user=client.user,
                                                title=client.name,
                                                text=client.company,
                                                xindex=int(client.status or 0),
                                                link=reverse('client_detail', args=[client.id]))
    else:
        card.title = client.name
        card.text = client.company
        card.xindex = int(client.status or 0)
        card.link = reverse('client_detail', args=[client.id])
        card.save()


@receiver(pre_save, sender=q.Quote)
def update_quote_card(sender, instance, **kwargs):
    quote = instance
    card = quote.card
    try:
        client_name = quote.client.name
    except AttributeError:
        client_name = ''

    if card is None:
        quote.card = KanbanCard.objects.create(user=quote.user,
                                                title=quote.name,
                                                text=client_name,
                                                xindex=int(quote.status or 0),
                                                link=reverse('quote_detail', args=[quote.id]))
    else:
        card.title = quote.name
        card.text = client_name
        card.xindex = int(quote.status or 0)
        card.link = reverse('quote_detail', args=[quote.id])
        card.save()


@receiver(pre_save, sender=c.Task)
def update_task_card(sender, instance, **kwargs):
    task = instance
    card = task.card
    try:
        project_name = task.project.name
    except AttributeError:
        project = ''

    if card is None:
        task.card = KanbanCard.objects.create(user=task.user,
                                                title=task.name,
                                                text=project_name,
                                                xindex=int(task.status or 0))
    else:
        card.title = task.name
        card.text = project_name
        card.xindex = int(task.status or 0)
        card.save()
