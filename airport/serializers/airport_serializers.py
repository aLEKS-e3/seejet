from rest_framework import serializers

from airport.models import Airport


class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = ("name", "closest_big_city",)
