from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import filters

from authentication.permissions import *
from .serializers import *


class ClientViewSet(viewsets.ModelViewSet):
    """API endpoint that allows potential Clients to be viewed."""
    queryset = Client.objects.all().order_by('date_updated')
    serializer_class = ClientSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsSupport
    ]
    filter_backends = [filters.SearchFilter]


class PotentialClientViewSet(viewsets.ModelViewSet):
    """API endpoint that allows potential Clients to be viewed."""
    queryset = Client.objects.filter(existing=False).order_by('date_updated')
    serializer_class = ClientSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsSupport
    ]
    filter_backends = [filters.SearchFilter]


class ExistingClientViewSet(viewsets.ModelViewSet):
    """API endpoint that allows existing Clients to be viewed."""
    queryset = Client.objects.filter(existing=True).order_by('date_updated')
    serializer_class = ClientSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsSupport
    ]
    # post method removed: Potential clients are converted into
    # existing clients as soon as a contract is created automatically.
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options',
                         'trace']
    filter_backends = [filters.SearchFilter]


class ContractViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Contracts to be viewed."""

    queryset = Contract.objects.all().order_by('date_updated')
    serializer_class = ContractSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsSales,
        IsSupport
    ]
    filter_backends = [filters.SearchFilter]


class EventViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Events to be viewed."""

    queryset = Event.objects.all().order_by('date_updated')
    serializer_class = EventSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsSupport
    ]
    filter_backends = [filters.SearchFilter]
