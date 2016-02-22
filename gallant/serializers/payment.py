from django.db.models import Prefetch
from django.utils import timezone
from gallant.utils import get_one_or_404
from moneyed import Money
from rest_framework import serializers
from gallant import models as g
from gallant.serializers.misc import MoneyField


class PaymentSerializer(serializers.ModelSerializer):
    amount = MoneyField()

    class Meta:
        model = g.Payment
        fields = ('id', 'due', 'paid_on', 'amount', 'description', 'notes', 'user')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'user': {'required': False},
            'notes': {'required': False}
        }

    def get_payments_totals(self, client, quote=None):
        total_amount = Money(0.00, client.currency)
        paid_amt = Money(0.00, client.currency)
        overdue_amt = Money(0.00, client.currency)
        pending_amt = Money(0.00, client.currency)
        on_hold_amt = Money(0.00, client.currency)

        current_time = timezone.now()

        quotes = client.quote_set.all_for(self.context['request'].user).prefetch_related(
            Prefetch('payments', to_attr='payments_arr'))

        if quote is None:
            selected_quote = "All quotes"
        else:
            selected_quote = quote.name
            quotes = quotes.filter(id=quote.id)

        for q in quotes:
            for p in q.payments_arr:
                total_amount += p.amount
                if p.paid_on is not None:
                    paid_amt += p.amount
                elif p.paid_on is None and p.due is not None:
                    if p.due < current_time:
                        overdue_amt += p.amount
                    elif p.due >= current_time:
                        pending_amt += p.amount
                elif p.due is None:
                    on_hold_amt += p.amount

        return {'quote': str(selected_quote),
                'total_amount': total_amount.amount,
                'paid_amount': paid_amt.amount,
                'overdue_amount': overdue_amt.amount,
                'pending_amount': pending_amt.amount,
                'on_hold_amount': on_hold_amt.amount,
                'currency': str(total_amount.currency)
                }

    def get_payments(self, client, quote=None):
        payments_array = []

        if quote:
            for q in client.quote_set.all_for(self.context['request'].user).filter(id=quote.id):
                for p in q.payments.all_for(self.context['request'].user):
                    payments_array.append(p)
        else:
            for q in client.quote_set.all_for(self.context['request'].user):
                for p in q.payments.all_for(self.context['request'].user):
                    payments_array.append(p)

        return payments_array

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.update({'user': user})
        instance = super(PaymentSerializer, self).create(validated_data)

        # Link payment to quote
        if self.context['request'].data['project_id']:
            project = get_one_or_404(user, 'change_project', g.Project, id=self.context['request'].data['project_id'])
            quote = project.quote_set.all_for(user)[0]
            quote.payments.add(instance)
            quote.save()

        return instance

    # def update(self, instance, validated_data):
    #     validated_data.pop('payment')
    #     return super(PaymentSerializer, self).update(instance, validated_data)

    def get_fields(self, *args, **kwargs):
        fields = super(PaymentSerializer, self).get_fields(*args, **kwargs)
        fields['notes'] = serializers.PrimaryKeyRelatedField(
            many=True, queryset=g.Note.objects.all_for(self.context['request'].user))
        return fields
