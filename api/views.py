from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .serializers import *


class ClientViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Clients to be viewed."""

    queryset = Client.objects.all().order_by('date_updated')
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
