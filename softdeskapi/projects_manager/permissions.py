from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorOrReadOnly(BasePermission):
    """
    Only allow the author of an object to edit it.
    Superusers and staff members can edit any object.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:  # read-only
            return True

        # Allow write for superusers and staff members
        if request.user.is_superuser or request.user.is_staff:
            return True

        # Allow write for the author of the object
        return obj.author == request.user
