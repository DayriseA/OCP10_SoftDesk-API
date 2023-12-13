"""URL configuration for projects_manager app."""
from django.urls import path, include
from rest_framework import routers

from projects_manager.views import ProjectViewSet, IssueViewSet, CommentViewSet

router = routers.SimpleRouter()
router.register("projects", ProjectViewSet, basename="projects")
router.register("issues", IssueViewSet, basename="issues")
router.register("comments", CommentViewSet, basename="comments")


urlpatterns = [
    path("api/", include(router.urls)),
]
