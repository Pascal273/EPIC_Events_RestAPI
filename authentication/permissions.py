from rest_framework import permissions
from rest_framework.exceptions import NotFound


class IsManagement(permissions.BasePermission):

    def has_permission(self, request, view):

        return True

    def has_object_permission(self, request, view, obj):

        return True


class IsSales(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class IsSupport(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True
