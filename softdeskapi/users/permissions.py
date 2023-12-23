from rest_framework.permissions import BasePermission


class IsSelfOrAdmin(BasePermission):
    """Access restricted to the user himself or superusers and staff members."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True

        return obj == request.user


class IsAdmin(BasePermission):
    """Access restricted to superusers and staff members."""

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False
