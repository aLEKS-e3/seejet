from rest_framework import serializers

from airport.models import Crew


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = "__all__"


class CrewImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "portrait",)
