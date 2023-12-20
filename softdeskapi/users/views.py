from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsSelfOrAdmin
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Any authenticated user can see the list of users. Only superusers, staff and
        the user himself can see the details of a user.
        """
        if self.action == "retrieve":
            self.permission_classes = [IsSelfOrAdmin]
        return super().get_permissions()
