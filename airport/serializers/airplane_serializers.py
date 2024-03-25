from rest_framework import serializers

from airport.models import AirplaneType, Airplane


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
