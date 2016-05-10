from __future__ import unicode_literals
from django.db import models as m
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from gallant import models as g


class KanbanCard(g.UserModel):
    title = m.CharField(max_length=255)
    text = m.CharField(max_length=255, blank=True, default='')
    link = m.CharField(max_length=255, blank=True, default='')
    xindex = m.IntegerField(blank=True, default=0)
    yindex = m.IntegerField(blank=True, default=0)
    alert = m.CharField(max_length=63, blank=True, default='')


@receiver(pre_save, sender=g.Service)
def update_service_card(sender, instance, **kwargs):
    service = instance

    try:
        quote = service.quote_set.all_for(service.user)[0]
        quote_name = quote.name
        title = service.name.get_text(quote.language)
    except IndexError:
        quote_name = ''
        title = ''

    if service.card is None:
        service.card = KanbanCard.objects.create(user=service.user,
                                                 title=title,
                                                 text=quote_name,
                                                 xindex=int(service.status or 0))
    else:
        service.card.title = service.name
        service.card.text = quote_name
        service.card.xindex = int(service.status or 0)
        service.card.save()


@receiver(pre_save, sender=g.Client)
def update_client_card(sender, instance, **kwargs):
    client = instance

    if client.card is None:
        client.card = KanbanCard.objects.create(user=client.user,
                                                title=client.name,
                                                text=client.company,
                                                xindex=int(client.status or 0))
    else:
        client.card.title = client.name
        client.card.text = client.company
        client.card.xindex = int(client.status or 0)
        client.card.save()
