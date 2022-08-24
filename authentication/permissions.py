from rest_framework import permissions
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model

from .models import TeamMembership


User = get_user_model()
management_members = User.objects.filter(groups__name='Management')
sales_members = User.objects.filter(groups__name='Sales')
support_members = User.objects.filter(groups__name='Support')


class TeamPermissions(permissions.BasePermission):

    def has_permission(self, request, view):

        return False

    def has_object_permission(self, request, view, obj):
        return False


class IsManagement(permissions.BasePermission):
    """Custom Permission that defines what members of the Management team
    are allowed to do"""

    def has_permission(self, request, view):

        return False

    def has_object_permission(self, request, view, obj):

        return False


class IsSales(permissions.BasePermission):
    """Custom Permission that defines what members of the Sales team
        are allowed to do"""

    def has_permission(self, request, view):

        return False

    def has_object_permission(self, request, view, obj):

        return False


class IsSupport(permissions.BasePermission):
    """Custom Permission that defines what members of the Support team
        are allowed to do"""

    def has_permission(self, request, view):

        return False

    def has_object_permission(self, request, view, obj):

        return False


class IsNotAuthenticated(permissions.BasePermission):
    """
    Custom permission that returns True if the user is not authenticated.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        return True
