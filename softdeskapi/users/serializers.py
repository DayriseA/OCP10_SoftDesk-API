from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "birth_date",
            "is_staff",
            "can_be_contacted",
            "can_data_be_shared",
            "is_active",
            "created_time",
        ]
