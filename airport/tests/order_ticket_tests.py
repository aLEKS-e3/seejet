from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase, APIClient

from airport.models import Order
from airport.serializers.order_serializers import OrderSerializer
from airport.tests.samples_for_tests import sample_main_flight

ORDER_URL = reverse("airport:order-list")


def detail_url(order_id):
    return reverse("airport:order-detail", args=[order_id])


class UnauthorizedOrderApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_order_list_auth_required(self):
        response = self.client.get(ORDER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedOrderApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="ceo@oes.com",
            password="1_am_CE0_1"
        )
        self.client.force_authenticate(self.user)

        self.order = Order.objects.create(user=self.user)

    def test_order_list_success_response(self):
        response = self.client.get(ORDER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_list_has_pagination(self):
        response = self.client.get(ORDER_URL)

        for pagination_key in ["count", "next", "previous", "results"]:
            self.assertIn(pagination_key, response.data.keys())

    def test_order_list_shows_all_orders(self):
        response = self.client.get(ORDER_URL)
        serializer = OrderSerializer(Order.objects.all(), many=True)

        self.assertEqual(response.data["results"], serializer.data)

    def test_update_order_is_forbidden(self):
        payload = {
            "created_at": "1999-05-13 10:00"
        }
        response = self.client.put(detail_url(self.order.id), payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(detail_url(self.order.id), payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_order_is_forbidden(self):
        response = self.client.delete(detail_url(self.order.id))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_ticket_success(self):
        flight = sample_main_flight()
        tickets_data = {
            "tickets":
            [
                {
                    "row": 1,
                    "seat": 1,
                    "flight": flight.id
                }
            ]
        }
        serializer = OrderSerializer(data=tickets_data)
        serializer.is_valid(raise_exception=True)

        response = self.client.post(ORDER_URL, serializer.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ticket_validation(self):
        flight = sample_main_flight()
        tickets_data = {
            "tickets":
            [
                {
                    "row": 1,
                    "seat": 1,
                    "flight": flight.id
                },
                {
                    "row": 1,
                    "seat": 1,
                    "flight": flight.id
                }
            ]
        }
        with self.assertRaises(ValidationError):
            serializer = OrderSerializer(data=tickets_data)
            serializer.is_valid(raise_exception=True)
            self.client.post(ORDER_URL, serializer.data, format="json")
