import uuid
from django.conf import settings
from django.db import models


class Project(models.Model):
    """Project model."""

    PROJECT_TYPES = [
        ("backend", "Back-end"),
        ("frontend", "Front-end"),
        ("ios", "iOS"),
        ("android", "Android"),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=PROJECT_TYPES)
    # we don't want to delete the project automatically if the author is deleted
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="projects_created",
        null=True,
    )
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        limit_choices_to={"is_active": True},
        through="Contributor",
        related_name="contributing_projects",
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return project name."""
        return self.name


class Contributor(models.Model):
    """Custom through model for contributors."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return user and project name."""
        return f"{self.user.username} - {self.project.name}"


class Issue(models.Model):
    """
    Issue model. An issue is always linked to one (same) project. Only contributors of
    this project can be assigned to the issue.
    """

    ISSUE_TYPES = [
        ("bug", "BUG"),
        ("feature", "FEATURE"),
        ("task", "TASK"),
    ]

    PRIORITIES = [
        ("low", "LOW"),
        ("medium", "MEDIUM"),
        ("high", "HIGH"),
    ]

    STATUS = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("finished", "Finished"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=ISSUE_TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITIES)
    status = models.CharField(max_length=15, choices=STATUS)

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues"
    )

    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="issues_assigned",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="issues_created",
        null=True,
    )

    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return issue name."""
        return self.name


class Comment(models.Model):
    """Comment model. A comment is always linked to one (same) issue."""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="comments_created",
        null=True,
    )
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return comment uuid, issue name and author username."""
        comment = f"""Comment {self.uuid} from issue '{self.issue.name}',
        created by {self.author.username}"""
        return comment
