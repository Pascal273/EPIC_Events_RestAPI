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
