from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airport.models import (
    Country,
    City,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight, Order, Ticket
)


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = "__all__"


class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = ("name", "closest_big_city",)


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ("source", "destination", "distance",)


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        slug_field="name", read_only=True
    )
    destination = serializers.SlugRelatedField(
        slug_field="name", read_only=True
    )


class AirplaneTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirplaneType
        fields = "__all__"


class AirplaneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airplane
        fields = ("name", "rows", "seats_in_row", "total_seats", "type",)


class AirplaneListSerializer(AirplaneSerializer):
    type = serializers.SlugRelatedField(slug_field="name", read_only=True)


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("first_name", "last_name", "full_name",)


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = "__all__"


class FlightListSerializer(FlightSerializer):
    route = serializers.StringRelatedField(read_only=True)
    airplane = serializers.StringRelatedField(read_only=True)
    crew = serializers.StringRelatedField(read_only=True)


class FlightDetailSerializer(FlightSerializer):
    route = RouteListSerializer(read_only=True)
    airplane = AirplaneListSerializer(read_only=True)
    crew = serializers.SlugRelatedField(
        slug_field="full_name", read_only=True, many=True
    )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("row", "seat", "flight",)


class TicketListSerializer(TicketSerializer):
    flight = FlightListSerializer(read_only=True)


class TicketSeatsSerializer(TicketSerializer):

    class Meta:
        model = Ticket
        fields = ("row", "seat",)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ("tickets", "created_at",)

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order

