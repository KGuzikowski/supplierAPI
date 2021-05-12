from rest_framework import serializers

from .models import User

"""Serializers below are defined for the User model."""


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer used when we want to get user details."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "profile_image",
            "description",
            "is_active",
            "confirmed",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "profile_image": {"required": False},
            "description": {"required": False},
            "is_active": {"read_only": True, "required": False},
            "confirmed": {"read_only": True, "required": False},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserListSerializer(serializers.ModelSerializer):
    """Serializer used when we want user basic data."""

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "profile_image"]


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer used when we want to update user."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "profile_image",
            "description",
        ]
        extra_kwargs = {
            "email": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "profile_image": {"required": False},
            "description": {"required": False},
        }


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change endpoint."""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
