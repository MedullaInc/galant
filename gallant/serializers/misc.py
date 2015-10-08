from rest_framework import serializers
from moneyed import Money


class MoneyField(serializers.Field):
    def to_representation(self, obj):
        return '%d %s' % (obj.amount, obj.currency)

    def to_internal_value(self, data):
        val = data.split(' ')
        return Money(val[0], val[1])
