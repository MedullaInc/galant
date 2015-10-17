from rest_framework import serializers
from gallant.models import Client
from gallant import models as g


class ClientSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    contact_info = serializers.PrimaryKeyRelatedField(read_only=True)

    def get_fields(self, *args, **kwargs):
        fields = super(ClientSerializer, self).get_fields(*args, **kwargs)
        fields['notes'] = serializers.PrimaryKeyRelatedField(
            many=True, queryset=g.Note.objects.all_for(self.context['request'].user))

        return fields

    class Meta:
        model = Client
        fields = ('id', 'user', 'name', 'email', 'contact_info', 'type', 'size',
                  'status', 'language', 'currency', 'notes')
