from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .serializers import *


class ClientViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Clients to be viewed."""

    queryset = Client.objects.all().order_by('date_updated')
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContractViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Contracts to be viewed."""

    queryset = Contract.objects.all().order_by('date_updated')
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Events to be viewed."""

    queryset = Event.objects.all().order_by('date_updated')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
