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
                        if request.data['status'] in ['OPEN', 'SIGNED']:
                            return True
                    # update only from status to 'SIGNED'
                    if request.method in ['PUT', 'PATCH']:
                        if request.data['status'] in ['OPEN', 'SIGNED']:
                            return True
                return False
        return True


class IsSupport(permissions.BasePermission):
    """Custom Permission that defines what members of the Support team
        are allowed to do"""

    def has_permission(self, request, view):
        user = request.user
        # support members can:
        if user in support_members:
            # not access Contracts
            if 'Contract' in type(view).__name__:
                return False
            # access events only if they are assigned to it
            if 'Event' in type(view).__name__:
                # override queryset with filtered by support is user
                # if Event is not finished
                not_finished = ['PROCESSING', 'UPCOMING', 'ONGOING']
                view.queryset = view.queryset.filter(
                    support_contact=user, status__in=not_finished
                )
            # access Clients if they belong to the assigned event
            if 'Client' in type(view).__name__:
                rel_events = Event.objects.filter(
                    support_contact=user
                )
                # override queryset to clients of related events
                view.queryset = view.queryset.filter(event__in=rel_events)

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        method = request.method
        # support members can:
        if user in support_members:
            # Events
            if type(obj).__name__ == 'Event':
                # on assigned Events
                if obj.support_contact.id == user.id:
                    # view event
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
