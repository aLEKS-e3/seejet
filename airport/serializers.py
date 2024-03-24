from rest_framework import serializers

from airport.models import Country, City, Airport, Route, AirplaneType, Airplane, Crew


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
