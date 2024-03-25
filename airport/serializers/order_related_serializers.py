from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from airport.models import Order, Ticket
from airport.serializers.flight_related_serializers import FlightListSerializer


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
        fields = ("id", "tickets", "created_at",)

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)

            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)

            return order


class OrderDetailSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
