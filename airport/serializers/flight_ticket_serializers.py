from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airport.models import Flight, Ticket
from airport.serializers.airplane_serializers import AirplaneListSerializer
from airport.serializers.route_serializers import RouteListSerializer


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = "__all__"


class FlightListSerializer(serializers.ModelSerializer):
    route = serializers.StringRelatedField(read_only=True)
    airplane = serializers.StringRelatedField(read_only=True)
    crew = serializers.StringRelatedField(many=True, read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "tickets_available"
        )


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("row", "seat", "flight",)

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            ValidationError
        )
        return data


class TicketSeatsSerializer(TicketSerializer):

    class Meta:
        model = Ticket
        fields = ("row", "seat",)


class TicketListSerializer(TicketSerializer):
    flight = FlightListSerializer(read_only=True)


class FlightDetailSerializer(FlightSerializer):
    route = RouteListSerializer(read_only=True)
    airplane = AirplaneListSerializer(read_only=True)
    crew = serializers.SlugRelatedField(
        slug_field="full_name", read_only=True, many=True
    )
    taken_places = TicketSeatsSerializer(
        source="tickets", many=True, read_only=True
    )
