from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from airport.models import Route, Airport
from airport.serializers.route_serializers import RouteListSerializer
from airport.tests.samples_for_tests import sample_route, sample_airport

ROUTE_URL = reverse("airport:route-list")


class UnauthenticatedRouteApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_route_list_auth_required(self):
        response = self.client.get(ROUTE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="ceo@oes.com",
            password="1_am_CE0_1"
        )
        self.client.force_authenticate(self.user)

        self.route = sample_route()

    def test_route_list_response(self):
        response = self.client.get(ROUTE_URL)
        serializer = RouteListSerializer(Route.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def tests_create_route_is_forbidden(self):
        source = sample_airport(name="Freege")
        destination = sample_airport(name="Guitar")
        payload = {
            "source": Airport.objects.get(name=source.name).id,
            "destination": Airport.objects.get(name=destination.name).id,
            "distance": 6673
        }
        response = self.client.post(ROUTE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
