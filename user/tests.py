from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class UserApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="boss@business.com",
            password="JPM0rgan_"
        )

    def test_create_user_with_email(self):
        payload = {
            "email": "messi@leo.com",
            "password": "F00tba11_"
        }
        response = self.client.post(reverse("user:create"), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_short_password(self):
        payload = {
            "email": "messi@leo.com",
            "password": "F00"
        }
        response = self.client.post(reverse("user:create"), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse("user:manage"),
            {
                "email": "bigboss@business.com",
                "password": "JPM0r9an_"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
