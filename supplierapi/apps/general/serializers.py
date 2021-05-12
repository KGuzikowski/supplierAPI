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


class SubIndustrySerializer(ModelSerializer):
    """Serializer for Industry model (used in IndustrySerializer)."""

    class Meta:
        model = Industry
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name


class IndustrySerializer(ModelSerializer):
    """Serializer for Industry model."""

    sub_industries = SubIndustrySerializer(many=True, required=False)

    class Meta:
        model = Industry
        fields = ["name", "sub_industries"]
