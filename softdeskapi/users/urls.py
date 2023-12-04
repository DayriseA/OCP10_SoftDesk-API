"""URL configuration for users app."""
from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet

router = routers.SimpleRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("api/", include(router.urls)),
]
