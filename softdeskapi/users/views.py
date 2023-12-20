from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsSelfOrAdmin
from users.serializers import UserSerializer, UserListSerializer


class UserViewSet(ModelViewSet):
    def get_queryset(self):
        """
        Superusers and staff members can see all users. Other users can see only active
        users.
        """
        user = self.request.user
        User = get_user_model()
        if user.is_superuser or user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(is_active=True)

    def get_serializer_class(self):
        """Return a different serializer for list and detail views."""
        if self.action == "list":
            return UserListSerializer
        return UserSerializer

    def get_permissions(self):
        """
        Any authenticated user can see the list of users. Only superusers, staff and
        the user himself can see the details of a user.
        """
        if self.action == "retrieve":
            self.permission_classes = [IsSelfOrAdmin]
        return super().get_permissions()
