from rest_framework.viewsets import ModelViewSet

from .models import Company
from .serializers import (
    CompanyDetailSerializer,
    CompanyListSerializer,
    CompanyUpdateSerializer,
)


class CompanyViewSet(ModelViewSet):
    """The viewset for the User model."""

    queryset = Company.objects.all()

    # mapping serializer into the action
    serializer_classes = {
        "list": CompanyListSerializer,
        "retrieve": CompanyDetailSerializer,
        "update": CompanyUpdateSerializer,
        "create": CompanyDetailSerializer,
    }
    default_serializer_class = CompanyListSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)
