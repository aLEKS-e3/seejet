from rest_framework import serializers

from airport.models import Country, City, Airport


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


class AirportListSerializer(AirportSerializer):
    closest_big_city = serializers.StringRelatedField()
