from rest_framework.serializers import ModelSerializer

from .models import Country, DialingCode, Industry


class DialingCodeSerializer(ModelSerializer):
    """Serializer for DialingCode model."""

    class Meta:
        model = DialingCode
        fields = ["name"]


class CountrySerializer(ModelSerializer):
    """Serializer for Country model."""

    class Meta:
        model = Country
        fields = ["name"]


class IndustrySerializer(ModelSerializer):
    """Serializer for Industry model."""

    class Meta:
        model = Industry
        fields = ["name", "parent_industry"]
