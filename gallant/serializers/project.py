from django.db.models.query import Prefetch
from rest_framework import serializers
from gallant.models import Project
from gallant import models as g


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    payments = serializers.SerializerMethodField()

    def get_payments(self, project):
        currency = ''
        amt = 0.00
        for q in project.quote_set.all_for(self.context['request'].user).prefetch_related(
                Prefetch('payments', to_attr='payments_arr')):
            for p in q.payments_arr:
                amt += float(p.amount.amount)

            for s in q.services.all_for(self.context['request'].user):
                currency = s.cost_currency

        return {'amount': amt, 'currency': currency}

    def get_fields(self, *args, **kwargs):
        fields = super(ProjectSerializer, self).get_fields(*args, **kwargs)
        fields['notes'] = serializers.PrimaryKeyRelatedField(
            many=True, queryset=g.Note.objects.all_for(self.context['request'].user))

        return fields

    class Meta:
        model = Project
        fields = ('id', 'user', 'name', 'status', 'notes', 'payments')
