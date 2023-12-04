from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
