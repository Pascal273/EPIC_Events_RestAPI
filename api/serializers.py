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


class ContractSerializer(serializers.HyperlinkedModelSerializer):
    """Contract model serializer"""

    payment_due = serializers.DateField(
        format="%Y-%m-%d",
        validators=[validate_date_not_in_past]
    )
    date_created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Contract
        fields = ['id', 'url', 'client', 'status', 'amount', 'payment_due',
                  'date_created', 'date_updated']


class EventSerializer(serializers.HyperlinkedModelSerializer):
    """Event model serializer"""

    date_created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    event_date_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        validators=[validate_date_time_not_in_past]
    )
    support_contact = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.filter(groups__name='Support'),
        required=True
    )
    contract = serializers.HyperlinkedRelatedField(
        view_name='contract-detail',
        queryset=Contract.objects.filter(status__in=['SIGNED', 'APPROVED']),
        required=True
    )

    class Meta:
        model = Event
        fields = ['id', 'url', 'support_contact', 'contract', 'event_name',
                  'date_created', 'date_updated', 'status', 'attendees',
                  'event_date_time', 'notes', 'client']
        read_only_fields = ['client', ]
