from rest_framework import serializers
from django.contrib.auth import get_user_model

from api.models import Client, Contract, Event
from .validators import *


User = get_user_model()


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    """Client model serializer"""

    date_created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    sales_contact = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.filter(groups__name='Sales'),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Client
        fields = ['id', 'url', 'first_name', 'last_name', 'email', 'phone',
                  'mobile', 'company_name', 'date_created', 'date_updated',
                  'sales_contact', 'existing']
        read_only_fields = ['existing', ]


class ContractSerializer(serializers.ModelSerializer):
    """Contract model serializer"""

    payment_due = serializers.DateField(
        format="%Y-%m-%d",
        validators=[validate_date_not_in_past]
    )
    date_created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    client_url = serializers.HyperlinkedRelatedField(
        view_name='client-detail',
        source='client',
        read_only=True
    )

    class Meta:
        model = Contract
        fields = ['id', 'url', 'client', 'client_url', 'status', 'amount',
                  'payment_due', 'date_created', 'date_updated']


class EventSerializer(serializers.ModelSerializer):
    """Event model serializer"""

    date_created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    event_date = serializers.DateField(
        format="%Y-%m-%d",
        validators=[validate_date_not_in_past]
    )
    client_url = serializers.HyperlinkedRelatedField(
        view_name='client-detail',
        source='client',
        read_only=True
    )
    support_contact_url = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
        source='support_contact'
    )
    contract_url = serializers.HyperlinkedRelatedField(
        view_name='contract-detail',
        read_only=True,
        source='contract'
    )

    class Meta:
        model = Event
        fields = ['id', 'client', 'client_url', 'url', 'support_contact',
                  'support_contact_url', 'contract', 'contract_url',
                  'event_name', 'date_created', 'date_updated', 'status',
                  'attendees', 'event_date', 'notes']
        read_only_fields = ['client', 'support_contact_url', 'contract_url']
