from supplierapi.utils.serializers import CustomModelSerializer

from .models import User

"""Serializers below are defined for the User model."""


class UserDetailSerializer(CustomModelSerializer):
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
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "profile_image": {"required": False},
            "description": {"required": False},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserListSerializer(CustomModelSerializer):
    """Serializer used when we want user basic data."""

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "profile_image"]


class UserUpdateSerializer(CustomModelSerializer):
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
