from rest_framework import serializers
from django.contrib.auth import get_user_model

from api.models import Client, Contract, Event
from .validators import *


User = get_user_model()


class ClientDetailSerializer(serializers.ModelSerializer):
    """Client model serializer for detail view"""

    date_created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    sales_contact = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.filter(groups__name='Sales'),
        default=serializers.CurrentUserDefault()
    )
    sales_contact_url = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
        source='sales_contact'
    )

    class Meta:
        model = Client
        fields = ['id', 'url', 'first_name', 'last_name', 'email', 'phone',
                  'mobile', 'company_name', 'date_created', 'date_updated',
                  'sales_contact', 'sales_contact_url', 'existing']
        read_only_fields = ['existing', ]


class ClientListSerializer(serializers.ModelSerializer):
    """Client model serializer for list view"""

    sales_contact = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.filter(groups__name='Sales'),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Client
        fields = ['id', 'url', 'full_name', 'first_name', 'last_name', 'email', 'phone',
                  'mobile', 'company_name', 'sales_contact', 'existing']
        read_only_fields = ['existing', ]
        extra_kwargs = {
            'first_name': {'write_only': True},
            'last_name': {'write_only': True}
        }


class ContractDetailSerializer(serializers.ModelSerializer):
    """Contract model serializer for detail view"""

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


class ContractListSerializer(serializers.ModelSerializer):
    """Contract model serializer for list view"""

    payment_due = serializers.DateField(
        format="%Y-%m-%d",
        validators=[validate_date_not_in_past]
    )
    date_created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    client = serializers.SlugRelatedField(
        slug_field='full_name',
        queryset=Client.objects.all()
    )

    class Meta:
        model = Contract
        fields = ['id', 'url', 'client', 'status', 'amount',
                  'payment_due', 'date_created']


class EventDetailSerializer(serializers.ModelSerializer):
    """Event model serializer for detail view"""

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
    support_contact = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.filter(groups__name='Support')
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
        fields = ['id', 'url', 'event_name', 'client', 'client_url',
                  'support_contact', 'support_contact_url', 'contract',
                  'contract_url', 'date_created', 'date_updated', 'status',
                  'attendees', 'event_date', 'notes']
        read_only_fields = ['client', 'support_contact_url', 'contract_url']


class EventListSerializer(serializers.ModelSerializer):
    """Event model serializer for list view"""

    date_created = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True
    )
    event_date = serializers.DateField(
        format="%Y-%m-%d",
        validators=[validate_date_not_in_past]
    )
    client = serializers.SlugRelatedField(
        slug_field='full_name',
        read_only=True
    )
    support_contact = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.filter(groups__name='Support')
    )

    class Meta:
        model = Event
        fields = ['id', 'url', 'event_name', 'client', 'support_contact',
                  'contract', 'status', 'attendees', 'event_date',
                  'date_created', 'notes']
        read_only_fields = ['client', 'support_contact_url', 'contract_url']
        extra_kwargs = {
            'attendees': {'write_only': True},
            'notes': {'write_only': True},
        }

