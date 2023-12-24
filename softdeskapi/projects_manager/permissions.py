from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorOrReadOnly(BasePermission):
    """
    Read-only permissions for any authenticated user. Write permissions for the author
    of the object or superusers and staff members.
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


class AuthorOrAssignee(BasePermission):
    """
    Return True if the user is the author or an assignee of the object, or if the user
    is a superuser or a staff member.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True

        is_author_or_assignee = (
            obj.author == request.user or request.user in obj.assignees.all()
        )
        return is_author_or_assignee
