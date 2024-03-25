from rest_framework import serializers

from airport.models import Airport, Route, Crew


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = "__all__"


class CrewImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "portrait",)


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
