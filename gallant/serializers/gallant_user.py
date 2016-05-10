from django.contrib.auth import get_user_model
from gallant.models.gallant_user import ContactInfo
from rest_framework import serializers


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'phone_number', 'address', 'address_2', 'city', 'state', 'zip', 'country')


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ('id', 'user', 'phone_number', 'address', 'address_2', 'city', 'state', 'zip', 'country')
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'user': {'required': False},
        }
