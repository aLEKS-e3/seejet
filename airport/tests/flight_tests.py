from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .samples_for_tests import (
    sample_main_flight,
    sample_secondary_flight,
    sample_route,
    sample_airplane
)
from ..serializers.flight_ticket_serializers import (
    FlightListSerializer,
    FlightDetailSerializer
)
from ..views import FlightViewSet

FLIGHT_URL = reverse("airport:flight-list")


def detail_url(flight_id):
    return reverse("airport:flight-detail", args=[flight_id])


class UnauthenticatedFlightApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_flight_list_auth_required(self):
        response = self.client.get(FLIGHT_URL)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)  # TODO: check 401 after token set up


class AuthenticatedFlightApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="ceo@oes.com",
            password="1_am_CE0_1"
        )
        self.client.force_authenticate(self.user)

        self.flight = sample_main_flight()
        self.secondary_flight = sample_secondary_flight()

        self.queryset = FlightViewSet.queryset

    def test_flight_list_response(self):
        response = self.client.get(FLIGHT_URL)
        serializer = FlightListSerializer(self.queryset, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_flight_filter_by_source(self):
        response = self.client.get(FLIGHT_URL, {"from": "Airport"})

        right_serializer = FlightListSerializer(self.queryset.get(id=1))
        wrong_serializer = FlightListSerializer(self.queryset.get(id=2))

        self.assertIn(right_serializer.data, response.data)
        self.assertNotIn(wrong_serializer.data, response.data)

    def test_flight_filter_by_destination(self):
        response = self.client.get(FLIGHT_URL, {"to": "port"})

        right_serializer = FlightListSerializer(self.queryset.get(id=1))
        wrong_serializer = FlightListSerializer(self.queryset.get(id=2))

        self.assertIn(right_serializer.data, response.data)
        self.assertNotIn(wrong_serializer.data, response.data)

    def test_flight_filter_by_airplane(self):
        response = self.client.get(FLIGHT_URL, {"airplane": "boeing"})

        right_serializer = FlightListSerializer(self.queryset.get(id=1))
        wrong_serializer = FlightListSerializer(self.queryset.get(id=2))

        self.assertIn(right_serializer.data, response.data)
        self.assertNotIn(wrong_serializer.data, response.data)

    def test_flight_detail_response(self):
        response = self.client.get(detail_url(self.flight.id))

        serializer = FlightDetailSerializer(self.queryset.get(id=1))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_flight_is_forbidden(self):
        payload = {
            "route": sample_route(),
            "airplane": sample_airplane(),
            "departure_time": "2024-03-20 14:00:00",
            "arrival_time": "2024-03-21 14:00:00",
        }
        response = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
