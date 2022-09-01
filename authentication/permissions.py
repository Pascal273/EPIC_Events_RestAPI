from rest_framework import permissions
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model

from api.models import Event


User = get_user_model()
management_members = User.objects.filter(groups__name='Management')
sales_members = User.objects.filter(groups__name='Sales')
support_members = User.objects.filter(groups__name='Support')


class IsManagement(permissions.BasePermission):
    """
    Custom Permission that only allows access to members of the Management team
    """

    def has_permission(self, request, view):
        if request.user in management_members:
            return True
        return False


class IsSales(permissions.BasePermission):
    """Custom Permission that defines what members of the Sales team
        are allowed to do"""

    def has_object_permission(self, request, view, obj):
        # sales_members can:
        if request.user in sales_members:
            allowed_status_options = ['OPEN', 'SIGNED']
            # on Contract's
            if type(obj).__name__ == 'Contract':
                # view Contract
                if request.method in permissions.SAFE_METHODS:
                    return True
                # open Contract's
                if obj.status in ['OPEN', 'SIGNED']:
                    # view details
                    if not request.data:
                        return True
                    # post only allow status 'OPEN' or 'SIGNED'
                    if request.method == 'POST':
                        if request.data['status'] in allowed_status_options:
                            return True
                    # update only from status to 'SIGNED'
                    if request.method in ['PUT', 'PATCH']:
                        if 'status' in request.data.keys():
                            status = request.data['status']
                            # if status is updated only allow OPEN or SIGNED
                            if status in allowed_status_options:
                                return True
                            else:
                                return False
                        return True
                return False
        return True


class IsSupport(permissions.BasePermission):
    """Custom Permission that defines what members of the Support team
        are allowed to do"""

    def has_object_permission(self, request, view, obj):
        user = request.user
        method = request.method
        # support members can:
        if user in support_members:
            # Events
            if type(obj).__name__ == 'Event':
                # view any event
                if request.method in permissions.SAFE_METHODS:
                    return True
                # on assigned Events
                if obj.support_contact.id == user.id:
                    # view any event
                    if not request.data:
                        return True
                    # update event (except: contract-field)
                    if method in ['PUT', 'PATCH']:
                        if int(request.data['contract'][-2]) == obj.contract.id:
                            return True
                return False
        return True


class IsNotAuthenticated(permissions.BasePermission):
    """
    Custom permission that returns True if the user is not authenticated.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        return True
