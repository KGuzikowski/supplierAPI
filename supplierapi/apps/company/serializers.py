from rest_framework import serializers

from supplierapi.apps.user.serializers import UserListSerializer

from .models import Address, Company, Employee, Role


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model."""

    class Meta:
        model = Address
        fields = [
            "name",
            "country",
            "city",
            "post_code",
            "street",
            "house_number",
            "local_number",
        ]


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Address model."""

    class Meta:
        model = Role
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Address model."""

    roles = RoleSerializer(many=True)
    user = UserListSerializer(many=False)

    class Meta:
        model = Employee
        fields = ["user", "roles"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        final = {**ret["user"], "roles": ret["roles"]}
        return final


"""Serializers below are defined for the Company model."""


class CompanyDetailSerializer(serializers.ModelSerializer):
    """Serializer used when we want to get Company details."""

    localizations = AddressSerializer(many=True)
    roles = RoleSerializer(many=True, required=False)
    staff = EmployeeSerializer(many=True, required=False)
    owners = UserListSerializer(many=True, read_only=True)

    # for the creation process
    # a initial owner that creates company
    creator = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Company
        fields = [
            "id",
            "status",
            "name",
            "short_name",
            "description",
            "profile_image",
            "owners",
            "staff",
            "roles",
            "localizations",
            "nip",
            "active",
            "confirmed",
            # for the creation process
            "creator",
        ]
        extra_kwargs = {
            "id": {"required": False, "read_only": True},
            "status": {"required": False},
            "name": {"required": True},
            "short_name": {"required": False},
            "description": {"required": True},
            "profile_image": {"required": False},
            "owners": {"required": True},
            "nip": {"required": True},
            "active": {"read_only": True, "required": False},
            "confirmed": {"read_only": True, "required": False},
        }

    def create(self, validated_data):
        company_data = validated_data
        print(company_data)
        # user = User.objects.create(**validated_data)
        # Profile.objects.create(user=user, **profile_data)
        return None


class CompanyListSerializer(serializers.ModelSerializer):
    """Serializer used when we want Company basic data."""

    class Meta:
        model = Company
        fields = ["id", "short_name", "profile_image"]


class CompanyUpdateSerializer(serializers.ModelSerializer):
    """Serializer used when we want to update Company."""

    localizations = AddressSerializer(many=True, required=False, write_only=True)
    roles = RoleSerializer(many=True, required=False, write_only=True)
    staff = EmployeeSerializer(many=True, required=False, write_only=True)
    owners = UserListSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Company
        fields = [
            "status",
            "name",
            "short_name",
            "description",
            "profile_image",
            "owners",
            "staff",
            "roles",
            "localizations",
            "nip",
        ]
        extra_kwargs = {
            "status": {"required": False, "write_only": True},
            "name": {"required": False, "write_only": True},
            "short_name": {"required": False, "write_only": True},
            "description": {"required": False, "write_only": True},
            "profile_image": {"required": False, "write_only": True},
            "owners": {"required": False, "write_only": True},
            "nip": {"required": False, "write_only": True},
        }
