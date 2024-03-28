from rest_framework import serializers

from airport.models import Airport


class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city",)


class AirportListSerializer(AirportSerializer):
    closest_big_city = serializers.SlugRelatedField(
        slug_field="name", read_only=True
    )
