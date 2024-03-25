from django.db import transaction
from rest_framework import serializers

from airport.models import Order, Ticket
from airport.serializers.flight_ticket_serializers import (
    TicketListSerializer,
    TicketSerializer
)


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
