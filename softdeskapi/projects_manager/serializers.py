from django.contrib.auth import get_user_model
from rest_framework import serializers

from projects_manager.models import Project, Issue, Comment

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for project objects.
    For educational purposes, PUT and PATCH requests handle contributors differently.
    """

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["author", "created_time"]

    def get_contributors_queryset(self):
        """Every active user can be a contributor."""
        return User.objects.filter(is_active=True)

    # I removed the validate_contributors method as already handled now with this
    contributors = serializers.PrimaryKeyRelatedField(
        queryset=get_contributors_queryset(serializers.ModelSerializer), many=True
    )

    def validate_name(self, value):
        """Check if project name is unique."""
        if Project.objects.filter(name=value).exists():
            raise serializers.ValidationError("Project name already exists")
        return value

    def validate_type(self, value):
        """Check if project type is valid."""
        if value not in [choice[0] for choice in Project.PROJECT_TYPES]:
            raise serializers.ValidationError(
                "Valid project types are: 'backend', 'frontend', 'ios', 'android'"
            )
        return value

    def create(self, validated_data):
        """
        Create and return a new project. The author is added to the contributors.
        If a list of contributors is provided, we add them to the project.
        """
        contributors = validated_data.pop("contributors", [])

        project = Project.objects.create(**validated_data)
        project.contributors.add(self.context["request"].user.id)

        # Add the contributors provided and validated to the project
        for contributor in contributors:
            project.contributors.add(contributor.id)
        return project

    def update(self, instance, validated_data):
        """
        Update and return an existing project. If a list of contributors is provided,
        we replace the existing contributors if request is PUT, or add them to the
        existing ones if request is PATCH.
        """
        contributors = validated_data.pop("contributors", [])
        # Update other simple fields with super()
        instance = super().update(instance, validated_data)

        # Check if request is PATCH or PUT
        if self.partial:
            for contributor in contributors:
                instance.contributors.add(contributor.id)
        else:
            # Replace the contributors, excepted the author, with the new list provided
            instance.contributors.clear()
            if instance.author:
                instance.contributors.add(instance.author.id)
            for contributor in contributors:
                instance.contributors.add(contributor.id)
        return instance


class IssueSerializer(serializers.ModelSerializer):
    """Serializer for issue objects."""

    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    assignees = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True), many=True
    )

    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ("project", "author", "created_time")

    def validate_assignees(self, assignees):
        """Check if assignees are contributors of the project."""
        if self.instance:
            project = self.instance.project
        else:
            project_id = self.initial_data.get("project")
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                raise serializers.ValidationError(
                    f"Project with id {project_id} does not exist."
                )
        for user in assignees:
            if user not in project.contributors.all():
                raise serializers.ValidationError(
                    f"{user.username} (id:{user.id}) is not a contributor "
                    "of this project."
                )
        return assignees

    def validate_name(self, value):
        """The name of an issue must be unique in a project."""
        if self.instance:
            project = self.instance.project
        else:
            project_id = self.initial_data.get("project")
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                raise serializers.ValidationError(
                    f"Project with id {project_id} does not exist."
                )
        if Issue.objects.filter(project=project, name=value).exists():
            raise serializers.ValidationError(
                f"An issue named '{value}' already exists in this project."
            )
        return value

    def update(self, instance, validated_data):
        """
        The project of an issue cannot be changed and is automatically set to the
        project of the instance. But if someone provides a project in the request,
        we check if it is the same of the instance to inform the user that he cannot
        change the project if he tries to.
        """
        if instance.project != validated_data["project"]:
            raise serializers.ValidationError("Project cannot be changed.")
        return super().update(instance, validated_data)

    def to_internal_value(self, data):
        """
        Add project to data from instance if it's not present in order to bypass
        automatic validation that is done before update() or validate() methods are
        called and that requires project to be present in the request data.
        """
        if "project" not in data and self.instance:
            data["project"] = self.instance.project.id
        return super().to_internal_value(data)


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comment objects."""

    issue = serializers.HyperlinkedIdentityField(view_name="issues-detail")

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("uuid", "issue", "author", "created_time")

    def update(self, instance, validated_data):
        """
        The issue of a comment cannot be changed and is automatically set to the
        issue of the instance. If someone tries to, we inform him that he cannot.
        """
        if "issue" in validated_data and instance.issue != validated_data["issue"]:
            raise serializers.ValidationError("Issue cannot be changed.")
        return super().update(instance, validated_data)
