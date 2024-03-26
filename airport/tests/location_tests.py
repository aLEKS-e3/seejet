from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from airport.models import Country, City
from airport.serializers.location_serializers import CitySerializer, CountrySerializer
from airport.tests.samples_for_tests import sample_city

CITY_URL = reverse("airport:city-list")
COUNTRY_URL = reverse("airport:country-list")


class UnauthenticatedLocationApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_city_list_auth_required(self):
        response = self.client.get(CITY_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_country_list_auth_required(self):
        response = self.client.get(COUNTRY_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedLocationApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="ceo@oes.com",
            password="1_am_CE0_1"
        )
        self.client.force_authenticate(self.user)
        self.city = sample_city()
        self.country = Country.objects.create(name="Perdunlyandia")

    def test_city_list_response(self):
        response = self.client.get(CITY_URL)
        serializer = CitySerializer(City.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_country_list_response(self):
        response = self.client.get(COUNTRY_URL)
        serializer = CountrySerializer(Country.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_city_is_forbidden(self):
        payload = {
            "name": "Limpo",
            "country": self.country.id
        }
        response = self.client.post(CITY_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_country_is_forbidden(self):
        payload = {
            "name": "Magamed",
        }
        response = self.client.post(COUNTRY_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
