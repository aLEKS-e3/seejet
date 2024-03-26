from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from airport.models import Airplane, AirplaneType
from airport.serializers.airplane_serializers import AirplaneListSerializer, AirplaneTypeSerializer
from airport.tests.samples_for_tests import sample_airplane

AIRPLANE_URL = reverse("airport:airplane-list")
AIRPLANE_TYPE_URL = reverse("airport:airplanetype-list")


class UnauthenticatedAirplaneApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_airplane_list_auth_required(self):
        response = self.client.get(AIRPLANE_URL)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_airplane_type_list_auth_required(self):
        response = self.client.get(AIRPLANE_URL)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)


class AuthenticatedAirplaneApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="ceo@oes.com",
            password="1_am_CE0_1"
        )
        self.client.force_authenticate(self.user)

        self.airplane_type = AirplaneType.objects.create(name="Cargo")
        self.airplane = sample_airplane(name="Makaka")
        self.plane = sample_airplane()

    def test_airplane_list_response(self):
        response = self.client.get(AIRPLANE_URL)
        serializer = AirplaneListSerializer(Airplane.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_airplane_type_list_response(self):
        response = self.client.get(AIRPLANE_TYPE_URL)
        serializer = AirplaneTypeSerializer(
            AirplaneType.objects.all(), many=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_airplane_is_forbidden(self):
        payload = {
            "name": "Tumba",
            "type": self.airplane_type
        }
        response = self.client.post(AIRPLANE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_airplane_type_is_forbidden(self):
        payload = {
            "name": "Boat"
        }
        response = self.client.post(AIRPLANE_TYPE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
