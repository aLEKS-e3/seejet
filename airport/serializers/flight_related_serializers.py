from rest_framework import serializers

from airport.models import Crew, Flight
from airport.serializers.airplane_related_serializers import AirplaneListSerializer
from airport.serializers.airport_related_serializers import RouteListSerializer


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
    crew = serializers.StringRelatedField(many=True, read_only=True)


class FlightDetailSerializer(FlightSerializer):
    route = RouteListSerializer(read_only=True)
    airplane = AirplaneListSerializer(read_only=True)
    crew = serializers.SlugRelatedField(
        slug_field="full_name", read_only=True, many=True
    )