import os
import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from airport.models import Crew
from airport.serializers.crew_serializers import CrewSerializer
from airport.tests.samples_for_tests import sample_crew

CREW_URL = reverse("airport:crew-list")


def detail_url(crew_id):
    return reverse("airport:crew-detail", args=[crew_id])


class UnauthenticatedCrewApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_crew_list_auth_required(self):
        response = self.client.get(CREW_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="ceo@oes.com",
            password="1_am_CE0_1",
        )
        self.client.force_authenticate(self.user)

        self.crew = sample_crew(first_name="Petro", last_name="Gulyash")
        self.crew2 = sample_crew()

    def test_crew_list_required(self):
        response = self.client.get(CREW_URL)
        crew = Crew.objects.all()
        serializer = CrewSerializer(crew, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)


def image_upload_url(crew_id):
    return reverse("airport:crew-upload-image", args=[crew_id])


class AdminCrewApiImageUploadTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="ceo@oes.com",
            password="1_am_CE0_1",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

        self.crew = sample_crew()

    def tearDown(self):
        self.crew.portrait.delete()

    def send_request_with_image(self, url):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            portrait = Image.new("RGB", (10, 10))
            portrait.save(ntf, format="JPEG")
            ntf.seek(0)
            return self.client.post(
                url,
                {"portrait": ntf}, format="multipart"
            )

    def test_upload_image_to_crew(self):
        url = image_upload_url(self.crew.id)

        response = self.send_request_with_image(url)
        self.crew.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("portrait", response.data)
        self.assertTrue(os.path.exists(self.crew.portrait.path))

    def test_image_url_is_shown_on_crew_list(self):
        url = image_upload_url(self.crew.id)
        self.send_request_with_image(url)

        response = self.client.get(CREW_URL)

        self.assertIn("portrait", response.data[0].keys())

    def test_image_url_is_shown_on_crew_detail(self):
        url = image_upload_url(self.crew.id)
        self.send_request_with_image(url)

        response = self.client.get(detail_url(self.crew.id))

        self.assertIn("portrait", response.data)
