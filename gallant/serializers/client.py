from moneyed.classes import Money
from rest_framework import serializers
from gallant import models as g


class ClientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    contact_info = serializers.PrimaryKeyRelatedField(read_only=True)
    money_owed = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_money_owed(self, client):
        amt = Money(0.00, client.currency)
        for q in client.quote_set.all_for(self.context['request'].user):
            amt += q.get_total_cost()
            for p in q.payments.all_for(self.context['request'].user):
                amt -= p.amount
        return {'amount': amt.amount, 'currency': str(amt.currency)}

    def get_status(self, client):
        client.quote_set.all_for(self.context['request'].user)

    def get_fields(self, *args, **kwargs):
        fields = super(ClientSerializer, self).get_fields(*args, **kwargs)
        fields['notes'] = serializers.PrimaryKeyRelatedField(
            many=True, queryset=g.Note.objects.all_for(self.context['request'].user))

        return fields

    class Meta:
        model = g.Client
        fields = ('id', 'user', 'name', 'email', 'contact_info', 'type', 'size',
                  'status', 'language', 'currency', 'notes', 'money_owed', 'last_contacted')
