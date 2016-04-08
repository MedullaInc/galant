from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from django.utils import timezone
from gallant.utils import get_one_or_404
from moneyed import Money
from rest_framework import serializers
from gallant import models as g
from quotes import models as q
from gallant.serializers.misc import MoneyField


class PaymentSerializer(serializers.ModelSerializer):
    amount = MoneyField()
    quote = serializers.SerializerMethodField()

    def get_quote(self, payment):
        if len(payment.quote_set.all_for(self.context['request'].user)) > 0:
            return payment.quote_set.all_for(self.context['request'].user)[0].id
        else:
            return None

    class Meta:
        model = g.Payment
        fields = ('id', 'due', 'paid_on', 'amount', 'description', 'notes', 'user', 'quote')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'user': {'required': False},
            'notes': {'required': False}
        }

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.update({'user': user})
        quote_id = self.context['request'].data.get('quote_id', None)

        # Link payment to quote
        if quote_id:
            quote = get_one_or_404(user, 'change_quote', q.Quote, id=quote_id)
            if quote.client and quote.client.currency == validated_data['amount'].currency.code:
                instance = super(PaymentSerializer, self).create(validated_data)
                quote.payments.add(instance)
            else:
                raise ValidationError('Payment currency must match quote currency.')
        else:
            instance = super(PaymentSerializer, self).create(validated_data)

        return instance

    # def update(self, instance, validated_data):
    #     validated_data.pop('payment')
    #     return super(PaymentSerializer, self).update(instance, validated_data)

    def get_fields(self, *args, **kwargs):
        fields = super(PaymentSerializer, self).get_fields(*args, **kwargs)
        fields['notes'] = serializers.PrimaryKeyRelatedField(
            many=True, queryset=g.Note.objects.all_for(self.context['request'].user))
        return fields
