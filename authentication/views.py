from django.shortcuts import render, redirect

from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .serializers import *
from .permissions import IsNotAuthenticated, IsManagement
from .forms import SignUpForm


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Users to be viewed."""

    queryset = User.objects.all().order_by('-hire_date')
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsManagement
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']


class TeamMembershipViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Team Memberships to be viewed."""

    queryset = TeamMembership.objects.all().order_by('team')
    serializer_class = TeamMembershipSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsManagement
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user', 'team']


class TeamViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Team Memberships to be viewed."""

    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.DjangoModelPermissions,
        IsManagement
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


def signup(request):
    """The view for the sign-up page."""
    # allow only unauthenticated user to visit the signup page
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SignUpForm()
        return render(request, 'signup/signup.html', {'form': form})
