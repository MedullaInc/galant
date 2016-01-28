from gallant.serializers.misc import ULTextField
from rest_framework import serializers
from gallant.models import Service
from gallant.serializers.misc import MoneyField

class ServiceSerializer(serializers.ModelSerializer):
	name = ULTextField()
	description = ULTextField()
	cost = MoneyField()
	notes = serializers.CharField(read_only=True)

	class Meta:
		model = Service
		fields = ('id', 'user', 'name', 'description', 'cost', 'quantity', 'type', 'parent', 'notes')
		extra_kwargs = {
			'id': {'read_only': False, 'required': False},
		}

	def create(self, validated_data):

		validated_data.pop('id', None)
		instance = super(ServiceSerializer, self).create(validated_data)

		return instance
