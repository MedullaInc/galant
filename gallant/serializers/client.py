from django.core.urlresolvers import reverse
from django.db.models.query import Prefetch
from django.utils import timezone
from gallant.serializers.gallant_user import ContactInfoSerializer
from moneyed.classes import Money
from rest_framework import serializers
from kanban import models as k
from kanban import serializers as ks
from gallant import models as g


class ClientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    contact_info = ContactInfoSerializer(allow_null=True)
    card = ks.KanbanCardSerializer(allow_null=True)
    money_owed = serializers.SerializerMethodField()
    flags = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()

    def get_money_owed(self, client):
        amt = Money(0.00, client.currency)
        current_time = timezone.now()
        for q in client.quote_set.all_for(self.context['request'].user)\
                .prefetch_related(Prefetch('payments', to_attr='payments_arr')):
            for p in q.payments_arr:
                if (p.paid_on is None or p.paid_on > current_time) and amt.currency == p.amount.currency:
                    amt += p.amount
        return {'amount': amt.amount, 'currency': str(amt.currency)}

    def get_flags(self, client):
        flags = [client.get_status_display()]
        current_time = timezone.now()
        for q in client.quote_set.all_for(self.context['request'].user)\
                .prefetch_related(Prefetch('payments', to_attr='payments_arr')):
            for p in q.payments_arr:
                if p.due < current_time and p.paid_on is None:
                    if 'Overdue' not in flags:
                        flags.append('Overdue')
                    break

        return flags

    def get_link(self, client):
        return reverse('client_detail', args=[client.id])

    def get_fields(self, *args, **kwargs):
        fields = super(ClientSerializer, self).get_fields(*args, **kwargs)
        fields['notes'] = serializers.PrimaryKeyRelatedField(
            many=True, queryset=g.Note.objects.all_for(self.context['request'].user))

        return fields

    class Meta:
        model = g.Client
        fields = ('id', 'user', 'name', 'email', 'company', 'contact_info', 'flags',
                  'link', 'status', 'language', 'currency', 'notes', 'money_owed', 'auto_pipeline',
                  'last_contacted', 'referred_by', 'card')
        extra_kwargs = {
            'user': {'required': False},
            'alert': {'read_only': True, 'required': False},
        }

    def create(self, validated_data):
        if self.context.has_key('request'):
            user = self.context['request'].user
        else:
            user = self.context.get("user")

        validated_data.update({'user': user})
        card = validated_data.pop('card', None)
        contact_info = validated_data.pop('contact_info', None)
        instance = super(ClientSerializer, self).create(validated_data)
        if contact_info:
            contact_info.update({'user': self.context['request'].user})
            cs = ContactInfoSerializer(data=contact_info)
            c = cs.create(contact_info)
            instance.contact_info = c
            instance.save()
        if card:
            card.update({'user': self.context['request'].user})
            cs = ks.KanbanCardSerializer(data=card)
            c = cs.create(card)
            instance.card = c
            instance.save()

        return instance

    def update(self, instance, validated_data):
        if self.context.has_key('request'):
            user = self.context['request'].user
        else:
            user = self.context.get("user")

        contact_info = validated_data.pop('contact_info', None)
        card = validated_data.pop('card', None)
        instance = super(ClientSerializer, self).update(instance, validated_data)

        if contact_info and 'id' in contact_info:
            c_instance = g.ContactInfo.objects.get_for(user, 'change', pk=contact_info['id'])
            cs = ContactInfoSerializer(data=contact_info, instance=c_instance)
            cs.update(c_instance, contact_info)
        elif contact_info:
            contact_info.update({'user': self.context['request'].user})
            cs = ContactInfoSerializer(data=contact_info)
            c = cs.create(contact_info)
            instance.contact_info = c
            instance.save()

        if card and 'id' in card:
            c_instance = k.KanbanCard.objects.get_for(user, 'change', pk=card['id'])
            cs = ks.KanbanCardSerializer(data=card, instance=c_instance)
            cs.update(c_instance, card)
        elif card:
            card.update({'user': self.context['request'].user})
            cs = ks.KanbanCardSerializer(data=card)
            c = cs.create(card)
            instance.card = c
            instance.save()

        return instance
