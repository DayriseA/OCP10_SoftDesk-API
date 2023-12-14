from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.viewsets import ModelViewSet

from projects_manager.models import Project, Issue, Comment
from projects_manager.permissions import AuthorOrReadOnly
from projects_manager.serializers import (
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AuthorOrReadOnly]

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
    permission_classes = [AuthorOrReadOnly]

    def create(self, request, *args, **kwargs):
        """Override create() method to only allow contributors to create issues."""
        # Check if the project exists and return an error if not
        try:
            project_id = request.data["project"]
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise ValidationError(f"Project {project_id} not found")
        if request.user not in project.contributors.all():
            raise PermissionDenied(
                "Only contributors of this project can create issues"
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """The user who made the request is set as the author of the issue."""
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrReadOnly]

    def create(self, request, *args, **kwargs):
        """Override create() method to only allow contributors to comment."""
        # Check if the issue exists and return an error if not
        try:
            issue_id = request.data["issue"]
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            raise ValidationError(f"Issue {issue_id} not found")
        if request.user not in issue.project.contributors.all():
            raise PermissionDenied(
                "Only contributors of this project can comment its issues"
            )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """The user who made the request is set as the author of the comment."""
        serializer.save(author=self.request.user)
