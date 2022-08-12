from rest_framework import serializers

from api.models import *
from authentication.models import User


class ClientSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(source='id', read_only=True)
    # sales_contact = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault())

    class Meta:
        model = Client
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    contract_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Contract
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
