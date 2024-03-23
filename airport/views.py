from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from airport.models import Country, City, Airport
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.serializers import (
    CountrySerializer,
    CitySerializer,
    AirportSerializer
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


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related("closest_big_city__country")
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
