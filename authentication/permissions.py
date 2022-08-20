from rest_framework import permissions
from rest_framework.exceptions import NotFound

# from .models import TeamMembership


class IsManagement(permissions.BasePermission):
    """Custom Permission that defines what members of the Management team
    are allowed to do"""
    # management_members = [
    #     member.employee for member in TeamMembership.objects.filter(
    #         team__name='Management'
    #     )
    # ]

    def has_permission(self, request, view):
        # if request.user in self.management_members:
        #     return True
        return False

    def has_object_permission(self, request, view, obj):
        # if request.user in self.management_members:
        #     return True
        return False


class IsSales(permissions.BasePermission):
    """Custom Permission that defines what members of the Sales team
        are allowed to do"""
    # sales_members = [
    #     member.employee for member in TeamMembership.objects.filter(
    #         team__name='Sales'
    #     )
    # ]

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class IsSupport(permissions.BasePermission):
    """Custom Permission that defines what members of the Support team
        are allowed to do"""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True
