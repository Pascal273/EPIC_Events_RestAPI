from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters, status
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
    serializer_class = ClientListSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsSupport
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ClientDetailSerializer(
            instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Destroy method with response"""
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Client has been deleted'})

    def update(self, request, *args, **kwargs):
        """Update method that allows partial updates"""
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class PotentialClientViewSet(viewsets.ModelViewSet):
    """API endpoint that allows potential Clients to be viewed."""
    queryset = Client.objects.filter(existing=False).order_by('date_updated')
    serializer_class = ClientListSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsSupport
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ClientDetailSerializer(
            instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Destroy method with response"""
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Client has been deleted'})

    def update(self, request, *args, **kwargs):
        """Update method that allows partial updates"""
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ExistingClientViewSet(viewsets.ModelViewSet):
    """API endpoint that allows existing Clients to be viewed."""
    queryset = Client.objects.filter(existing=True).order_by('date_updated')
    serializer_class = ClientListSerializer
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ClientDetailSerializer(
            instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Destroy method with response"""
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Client has been deleted'})

    def update(self, request, *args, **kwargs):
        """Update method that allows partial updates"""
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ContractViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Contracts to be viewed."""

    queryset = Contract.objects.all().order_by('date_updated')
    serializer_class = ContractListSerializer
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ContractDetailSerializer(
            instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Destroy method with response"""
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Contract has been deleted'})

    def update(self, request, *args, **kwargs):
        """Update method that allows partial updates"""
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class EventViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Events to be viewed."""

    queryset = Event.objects.all().order_by('date_updated')
    serializer_class = EventListSerializer

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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EventDetailSerializer(
            instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Destroy method with response"""
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Event has been deleted'})

    def update(self, request, *args, **kwargs):
        """
        Update method that allows partial updates and returns detailed view
        """
        kwargs['partial'] = True
        super().update(request, *args, **kwargs)
        instance = self.get_object()
        serializer = EventDetailSerializer(
            instance, context={'request': request}
        )
        return Response(serializer.data)
