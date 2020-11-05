from rest_framework import serializers


class CustomModelSerializer(serializers.ModelSerializer):
    """Custom serializer that maps pk to id."""

    id = serializers.CharField(source="pk", required=False, read_only=True)
