from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Users to be viewed."""

    queryset = User.objects.all().order_by('-hire_date')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeamMembershipViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Team Memberships to be viewed."""

    queryset = TeamMembership.objects.all().order_by('team')
    serializer_class = TeamMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeamViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Team Memberships to be viewed."""

    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
