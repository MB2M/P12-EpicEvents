from crm.models import Contract, Event
from crm.admin import ClientAdmin
from rest_framework import permissions

from crm.models import Client

class EmptyEventPermission(permissions.BasePermission):
    """[summary]
    Check if a contract already has an Event
    """

    def has_object_permission(self, request, view, obj):
        Contract.objects.filter(sales_contact=request.user.id, id=obj.id).exists()
        return super().has_permission(request, view)

class IsManager(permissions.BasePermission):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.function.name == 'manager'

class IsSales(permissions.BasePermission):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            return Client.objects.filter(sales_contact=request.user.id, id=obj.id).exists()

        if request.method == 'DELETE':
            return False

        if isinstance(obj, Event):
            obj = obj.contract

        return request.user == obj.sales_contact

class IsSupport(permissions.BasePermission):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE':
            return False

        return request.user.function.name == 'support'

class ClientPermission(permissions.BasePermission):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    # client_admin = ClientAdmin()
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        return super().has_change_permission(request,obj)