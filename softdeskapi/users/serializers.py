from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user objects."""

    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "password",
            "password_confirmation",
            "birth_date",
            "is_staff",
            "can_be_contacted",
            "can_data_be_shared",
            "is_active",
            "created_time",
        ]
        read_only_fields = ["id", "created_time"]

    def validate_birth_date(self, value):
        """Check if user is at least 15 years old."""
        if (timezone.now().date() - value).days < 15 * 365:
            raise serializers.ValidationError(
                "Users must be at least 15 years old (RGPD)"
            )
        return value

    def validate(self, data):
        """If password is to be changed, a confirmation is required."""
        if "password" in data:
            if "password_confirmation" not in data:
                raise serializers.ValidationError(
                    "password_confirmation must be provided when updating password"
                )
            elif data["password"] != data["password_confirmation"]:
                raise serializers.ValidationError(
                    "password and password_confirmation must match"
                )
        return data

    def create(self, validated_data):
        """Create and return a new user."""
        password = validated_data.pop("password")
        validated_data.pop("password_confirmation", None)
        user = get_user_model().objects.create_user(password=password, **validated_data)
        return user

    def update(self, instance, validated_data):
        """Update and return an existing user."""
        password = validated_data.pop("password", None)
        password_confirmation = validated_data.pop("password_confirmation", None)
        if password and password_confirmation:
            instance.set_password(password)
        return super().update(instance, validated_data)
