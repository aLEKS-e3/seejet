from rest_framework import viewsets

from airport.models import Country, City
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly
from airport.serializers import CountrySerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("country")
    serializer_class = ""
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]



