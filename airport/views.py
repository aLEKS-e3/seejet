from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from airport.models import (
    Country,
    City,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order
)
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport import serializers


class CountryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Country.objects.all()
    serializer_class = serializers.CountrySerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class CityViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = City.objects.select_related("country")
    serializer_class = serializers.CitySerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class AirportViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Airport.objects.select_related("closest_big_city")
    serializer_class = serializers.AirportSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class RouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Route.objects.select_related()
    serializer_class = serializers.RouteSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.RouteListSerializer
        return serializers.RouteSerializer


class AirplaneTypeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = AirplaneType.objects.all()
    serializer_class = serializers.AirplaneTypeSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("type")
    serializer_class = serializers.AirplaneSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.AirplaneListSerializer
        return serializers.AirplaneSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = serializers.CrewSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related().prefetch_related("crew")
    serializer_class = serializers.FlightSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.FlightListSerializer

        if self.action == "retrieve":
            return serializers.FlightDetailSerializer

        return serializers.FlightSerializer


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
