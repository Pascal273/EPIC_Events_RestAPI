from rest_framework import serializers
from django.contrib.auth import get_user_model

from authentication.serializers import NestedEmployeeSerializer
from authentication.models import Employee, TeamMembership

from api.models import *


User = get_user_model()


class ClientSerializer(serializers.ModelSerializer):
    sales_contact = serializers.HyperlinkedRelatedField(
        view_name='employees-detail',
        queryset=Employee.objects.filter(
            user__in=[
                member.employee for member in TeamMembership.objects.filter(
                    team__name='Sales'
                )]
        )
    )

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'mobile', 'company_name', 'date_created', 'date_updated',
                  'sales_contact', 'existing']
        read_only_fields = ['existing', ]


class ContractSerializer(serializers.ModelSerializer):
    client = serializers.HyperlinkedRelatedField(
        view_name='existing_clients-detail', queryset=Client.objects.all())

    def create(self, validated_data):
        """Modified create method to convert the related client as 'existing'
        once a contract is created."""

        # update client to 'existing' if contract status allows it
        if validated_data['status'] not in ['CLOSED', 'CANCELLED', 'EXPIRED']:
            client = Client.objects.get(id=validated_data['client'].id)
            client.existing = True
            client.save()

        contract = Contract.objects.create(**validated_data)
        return contract

    class Meta:
        model = Contract
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    support_contact = serializers.HyperlinkedRelatedField(
        view_name='employees-detail',
        queryset=Employee.objects.filter(user__in=[
            member.employee for member in TeamMembership.objects.filter(
                team__name='Support'
            )
        ])
    )
    contract = serializers.HyperlinkedRelatedField(
        view_name='contracts-detail',
        queryset=Contract.objects.all().exclude(
            contract__in=[
                event.contract.id for event in Event.objects.all()
            ]
        )
    )

    def create(self, validated_data):
        """Modifies create method to add the client from the associated
        contract automatically"""

        contract = Contract.objects.get(id=validated_data['contract'].id)
        client = contract.client
        validated_data['client'] = client

        event = Event.objects.create(**validated_data)
        return event

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['client', ]
