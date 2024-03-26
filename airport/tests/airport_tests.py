from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from airport.models import Airport
from airport.serializers.airport_serializers import AirportSerializer
from airport.tests.samples_for_tests import sample_airport, sample_city

AIRPORT_URL = reverse("airport:airport-list")


class UnauthenticatedAirportApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_airport_list_auth_required(self):
        response = self.client.get(AIRPORT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="ceo@oes.com",
            password="1_am_CE0_1"
        )
        self.client.force_authenticate(self.user)

        self.airport = sample_airport(name="Baobab")
        self.airport2 = sample_airport()

    def test_airport_list_response(self):
        response = self.client.get(AIRPORT_URL)
        serializer = AirportSerializer(Airport.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_airport_is_forbidden(self):
        payload = {
            "name": "OdesaMama",
            "closest_big_city": sample_city()
        }
        response = self.client.post(AIRPORT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
