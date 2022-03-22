from rest_framework.permissions import BasePermission
from rolepermissions.checkers import has_permission


class AllowAdmin(BasePermission):
    def has_permission(self, request, view):
        return has_permission(request.user, "manage_projects")


class AllowStaff(BasePermission):
    def has_permission(self, request, view):
        return has_permission(request.user, "manage_product")

class IsOwnerOrder(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user