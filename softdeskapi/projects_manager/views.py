from django.db.models import Q
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.viewsets import ModelViewSet

from projects_manager.models import Project, Issue, Comment
from projects_manager.permissions import AuthorOrReadOnly
from projects_manager.serializers import (
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
    ProjectListSerializer,
    IssueListSerializer,
)


class MultipleSerializerMixin:
    """Mixin to use differents serializers for different actions."""

    # For now, we only need a different serializer for list action
    list_serializer_class = None

    def get_serializer_class(self):
        """Return a different serializer for list action."""
        if self.action == "list" and self.list_serializer_class is not None:
            return self.list_serializer_class
        return super().get_serializer_class()


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectSerializer
    list_serializer_class = ProjectListSerializer
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):
        """
        Restricted to authors and contributors. Superusers and staff members can see all
        projects.
        """
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Project.objects.all()
        else:
            return (
                Project.objects.filter(Q(author=user) | Q(contributors=user))
                .distinct()
                .order_by("id")
            )

    def perform_create(self, serializer):
        """The user who made the request is set as the author of the project."""
        serializer.save(author=self.request.user)

    # update() method removed as it was only calling the super().update method

    def partial_update(self, request, *args, **kwargs):
        """Handle PATCH request."""
        return super().partial_update(request, *args, **kwargs)


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = IssueSerializer
    list_serializer_class = IssueListSerializer
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):
        """
        Restricted to authors and contributors. Superusers and staff members can see all
        issues.
        """
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Issue.objects.all()
        else:
            return (
                Issue.objects.filter(Q(author=user) | Q(project__contributors=user))
                .distinct()
                .order_by("id")
            )

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
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrReadOnly]

    def get_queryset(self):
        """
        Restricted to authors and contributors. Superusers and staff members can see all
        comments.
        """
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Comment.objects.all()
        else:
            return (
                Comment.objects.filter(
                    Q(author=user) | Q(issue__project__contributors=user)
                )
                .distinct()
                .order_by("id")
            )

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
