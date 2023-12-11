from django.contrib.auth import get_user_model
from rest_framework import serializers

from projects_manager.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for project objects."""

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "type",
            "author",
            "contributors",
            "created_time",
        ]
        read_only_fields = ["id", "author", "created_time"]

    def get_contributors_queryset(self):
        """Every active user can be a contributor."""
        return get_user_model().objects.filter(is_active=True)

    # I removed the validate_contributors method as already handled now with this
    contributors = serializers.PrimaryKeyRelatedField(
        queryset=get_contributors_queryset(serializers.ModelSerializer), many=True
    )

    def validate_name(self, value):
        """Check if project name is unique."""
        print("VALIDATE_NAME METHOD IN PROJECT SERIALIZER CALLED")  # debug
        if Project.objects.filter(name=value).exists():
            raise serializers.ValidationError("Project name already exists")
        return value

    def validate_type(self, value):
        """Check if project type is valid."""
        print("VALIDATE_TYPE METHOD IN PROJECT SERIALIZER CALLED")  # debug
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
        print("CREATE METHOD IN PROJECT SERIALIZER CALLED")  # debug
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
        print("UPDATE METHOD IN PROJECT SERIALIZER CALLED")  # debug
        contributors = validated_data.pop("contributors", [])
        # Update other simple fields with super()
        instance = super().update(instance, validated_data)

        # Check if request is PATCH or PUT
        if self.partial:
            print("PATCH REQUEST LOGIC APPLIED TO CONTRIBUTORS")  # debug
            for contributor in contributors:
                instance.contributors.add(contributor.id)
        else:
            print("PUT REQUEST LOGIC APPLIED TO CONTRIBUTORS")  # debug
            # Replace the contributors, excepted the author, with the new list provided
            instance.contributors.clear()
            if instance.author:
                instance.contributors.add(instance.author.id)
            for contributor in contributors:
                instance.contributors.add(contributor.id)
        return instance
