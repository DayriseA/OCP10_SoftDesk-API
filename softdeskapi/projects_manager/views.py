from rest_framework.viewsets import ModelViewSet

from projects_manager.models import Project, Issue
from projects_manager.serializers import ProjectSerializer, IssueSerializer


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        """The user who made the request is set as the author of the project."""
        print("PERFORM CREATE METHOD IN PROJECTVIEWSET CALLED")  # debug
        serializer.save(author=self.request.user)

    # update() method removed as it was only calling the super().update method

    def partial_update(self, request, *args, **kwargs):
        """Handle PATCH request."""
        print("PARTIAL UPDATE METHOD IN PROJECTVIEWSET CALLED")  # debug
        return super().partial_update(request, *args, **kwargs)


class IssueViewSet(ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        """The user who made the request is set as the author of the issue."""
        serializer.save(author=self.request.user)
