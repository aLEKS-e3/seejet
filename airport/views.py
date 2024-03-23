from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from airport.models import Country, City, Airport
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.serializers import (
    CountrySerializer,
    CitySerializer,
    AirportSerializer,
    AirportListSerializer
)


class CountryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class CityViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = City.objects.select_related("country")
    serializer_class = CitySerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class AirportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Airport.objects.select_related("closest_big_city__country")
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return AirportListSerializer
        return AirportSerializer
