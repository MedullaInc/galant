import datetime
from django.db.models.query import Prefetch
from django.utils import timezone
from moneyed.classes import Money
from rest_framework import serializers
from gallant import models as g


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def get_payments(self, client, quote=None):
        total_amount = Money(0.00, client.currency)
        paid_amt = Money(0.00, client.currency)
        overdue_amt = Money(0.00, client.currency)
        pending_amt = Money(0.00, client.currency)
        on_hold_amt = Money(0.00, client.currency)

        current_time = timezone.now()

        quotes = client.quote_set.all_for(self.context['request'].user).prefetch_related(Prefetch('payments', to_attr='payments_arr'))

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

    class Meta:
        model = g.Client
