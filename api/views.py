from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

# '^' Starts-with search. (example: '^first_name')
# '=' Exact matches.
# '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
# '$' Regex search.

from authentication.permissions import IsSupport, IsSales
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
    search_fields = ['first_name', 'last_name', 'email']


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
    search_fields = ['first_name', 'last_name', 'email']


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
    search_fields = ['first_name', 'last_name', 'email']


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
    search_fields = [
        'client__first_name',
        'client__last_name',
        'date_created',
        'amount'
    ]


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
    search_fields = [
        'client__first_name',
        'client__last_name',
        'event_date'
    ]
