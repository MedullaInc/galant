from django.core.urlresolvers import reverse
from django.db.models.query import Prefetch
from django.utils import timezone
from moneyed.classes import Money
from rest_framework import serializers
from gallant import models as g


class ClientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    contact_info = serializers.PrimaryKeyRelatedField(read_only=True)
    money_owed = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
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

    def get_status(self, client):
        status = [client.get_status_display()]
        current_time = timezone.now()
        for q in client.quote_set.all_for(self.context['request'].user)\
                .prefetch_related(Prefetch('payments', to_attr='payments_arr')):
            for p in q.payments_arr:
                if p.due < current_time and p.paid_on is None:
                    if 'Overdue' not in status:
                        status.append('Overdue')
                    break

        return status

    def get_link(self, client):
        return reverse('client_detail', args=[client.id])

    def get_fields(self, *args, **kwargs):
        fields = super(ClientSerializer, self).get_fields(*args, **kwargs)
        fields['notes'] = serializers.PrimaryKeyRelatedField(
            many=True, queryset=g.Note.objects.all_for(self.context['request'].user))

        return fields

    class Meta:
        model = g.Client
        fields = ('id', 'user', 'name', 'email', 'company', 'contact_info',
                  'link', 'status', 'language', 'currency', 'notes', 'money_owed',
                  'last_contacted', 'referred_by')
