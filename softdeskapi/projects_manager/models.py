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
    """Issue model."""

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
