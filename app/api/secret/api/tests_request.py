from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from secret.models import Secret, set_burn_at
from uuid import uuid4
from freezegun import freeze_time


class HandleStoreRequestTest(APITestCase):

    def test_01_store_request_success(self):
        # API request payload
        payload = {
            "expiry_seconds": 3600,
            "from_email": "sender@example.com",
            "to_email": "recipient@example.com",
        }

        url = reverse("api:request:handle_store_request")
        response = self.client.post(url, payload, format="json")

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("request_id", response.data)
        self.assertIn("secret_id", response.data)
        self.assertIn("burn_at", response.data)

        # Check if the Secret was created in the database
        self.assertTrue(
            Secret.objects.filter(request_id=response.data["request_id"]).exists()
        )

    def test_02_store_request_invalid_expiry(self):
        # API request payload with invalid expiry_seconds
        payload = {
            "expiry_seconds": 30,  # less than min_value 60
            "from_email": "sender@example.com",
            "to_email": "recipient@example.com",
        }

        url = reverse("api:request:handle_store_request")
        response = self.client.post(url, payload, format="json")

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("expiry_seconds", response.data["detail"])
        self.assertEqual(response.data["errors"][0]["field"], "expiry_seconds")
        self.assertEqual(
            response.data["errors"][0]["detail"],
            "Ensure this value is greater than or equal to 60.",
        )


class HandleRetrieveRequestFulfilmentTest(APITestCase):

    def setUp(self):
        # Create a Secret instance in the database for testing
        self.secret = Secret.objects.create(
            request_id=str(uuid4()),
            secret_id=str(uuid4()),
            burn_at=set_burn_at(seconds=3600),
            fulfilment_id=None,
        )

        self.secret_fulfilled = Secret.objects.create(
            request_id=str(uuid4()),
            secret_id=str(uuid4()),
            burn_at=set_burn_at(seconds=3600),
            fulfilment_id=str(uuid4()),
        )

    def test_01_retrieve_fulfilment_success(self):
        payload = {"request_id": self.secret.request_id}

        url = reverse("api:request:handle_retrieve_request")
        response = self.client.post(url, payload, format="json")

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("request_id", response.data)
        self.assertIn("fulfilment_id", response.data)
        self.assertEqual(response.data["request_id"], self.secret.request_id)

    def test_02_retrieve_fulfilment_secret_not_found(self):
        payload = {"request_id": str(uuid4())}  # Non-existent request_id

        url = reverse("api:request:handle_retrieve_request")
        response = self.client.post(url, payload, format="json")

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "request not found.")

    @freeze_time("2099-09-09")
    def test_03_retrieve_fulfilment_secret_expired(self):
        payload = {"request_id": self.secret.request_id}

        url = reverse("api:request:handle_retrieve_request")
        response = self.client.post(url, payload, format="json")

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "request not found.")

    def test_04_retrieve_already_fulfilled(self):
        payload = {"request_id": self.secret_fulfilled.request_id}

        url = reverse("api:request:handle_retrieve_request")
        response = self.client.post(url, payload, format="json")

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "request not found.")


class HandleFulfilRequestTest(APITestCase):

    def setUp(self):
        # Create a Secret instance in the database for testing
        self.secret = Secret.objects.create(
            request_id=str(uuid4()),
            secret_id=str(uuid4()),
            fulfilment_id=str(uuid4()),
            secret_text=None,
        )

    def test_01_fulfil_request_success(self):
        payload = {
            "request_id": self.secret.request_id,
            "fulfilment_id": self.secret.fulfilment_id,
            "secret_text": "This is the secret text.",
        }

        url = reverse("api:request:handle_fulfil_request")
        response = self.client.post(url, payload, format="json")

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("request_id", response.data)
        self.assertIn("burn_at", response.data)

        # Check if the secret_text was updated in the database
        self.secret.refresh_from_db()
        self.assertEqual(self.secret.secret_text, payload["secret_text"])

    def test_02_fulfil_request_invalid_fulfilment_id(self):
        # Test with an invalid fulfilment_id
        payload = {
            "request_id": self.secret.request_id,
            "fulfilment_id": str(uuid4()),  # Non-existent fulfilment_id
            "secret_text": "This is the secret text.",
        }

        url = reverse("api:request:handle_fulfil_request")
        response = self.client.post(url, payload, format="json")

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "request not found or never existed")
