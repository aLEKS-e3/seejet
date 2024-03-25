from django.db.models import F, Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
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
from airport.serializers.location_serializers import (
    CitySerializer,
    CountrySerializer
)
from airport.serializers.airplane_serializers import (
    AirplaneListSerializer,
    AirplaneSerializer,
    AirplaneTypeSerializer
)
from airport.serializers.flight_ticket_serializers import (
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
)
from airport.serializers.airport_crew_serializers import (
    AirportSerializer,
    RouteListSerializer,
    RouteSerializer,
    CrewSerializer
)
from airport.serializers.order_serializers import (
    OrderSerializer,
    OrderDetailSerializer
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
    queryset = Airport.objects.select_related("closest_big_city")
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class RouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Route.objects.select_related()
    serializer_class = RouteSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        return self.serializer_class


class AirplaneTypeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("type")
    serializer_class = AirplaneSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        return self.serializer_class


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.select_related().prefetch_related(
        "crew"
    ).annotate(
        tickets_available=(
            F("airplane__rows") * F("airplane__seats_in_row")
            - Count("tickets")
        )
    )
    serializer_class = FlightSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return self.serializer_class

    def get_queryset(self):
        source = self.request.query_params.get("from")
        destination = self.request.query_params.get("to")
        airplane = self.request.query_params.get("airplane")

        queryset = self.queryset

        if source:
            queryset = queryset.filter(route__source__icontains=source)

        if destination:
            queryset = queryset.filter(
                route__destination__icontains=destination
            )

        if airplane:
            queryset = queryset.filter(airplane__name__icontains=airplane)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "source",
                type={"type": "list", "items": {"type": "string"}},
                description="Filter flights by source (eg. ?from=Paris)"
            ),
            OpenApiParameter(
                "destination",
                type={"type": "list", "items": {"type": "string"}},
                description="Filter flights by destination (eg. ?to=Tokyo)"
            ),
            OpenApiParameter(
                "airplane",
                type={"type": "list", "items": {"type": "string"}},
                description=(
                    "Filter flights by airplane (eg. ?airplane=Airbus)"
                )
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = OrderPagination

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
