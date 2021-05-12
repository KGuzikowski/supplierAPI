from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Country, DialingCode, Industry
from .serializers import CountrySerializer, DialingCodeSerializer, IndustrySerializer


class DialingCodeViewSet(ReadOnlyModelViewSet):
    """The viewset for the DialingCode model."""

    queryset = DialingCode.objects.all()
    serializer_class = DialingCodeSerializer


class CountryViewSet(ReadOnlyModelViewSet):
    """The viewset for the Country model."""

    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class IndustryViewSet(ReadOnlyModelViewSet):
    """The viewset for the Industry model."""

    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
