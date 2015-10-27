from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserModelSerializer(serializers.ModelSerializer):
    contact_info = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'contact_info')
