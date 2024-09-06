import freezegun
import json
import math

from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from django.contrib.auth.hashers import check_password

from secret.models import Secret

now = timezone.now()

DEFAULT_SECRET_TEXT = "this is a secret"
DEFAULT_PASSPHRASE = "password"


class URLS:
    store_secret = "/api/secret/"
    retrieve_secret = "/api/secret/retrieve/"

    store_request = "/api/request/"
    retrieve_fulfilment = "/api/request/fulfil/"
    fulfil_request = "/api/request/fulfil/"

    request_verification = "/api/verify/request/"
    verify = "/api/verify/"


class SecretAPITests(APITestCase):

    @freezegun.freeze_time(time_to_freeze=now)
    def test_001_store_secret_without_passphrase(self):
        response = self.client.post(
            path=URLS.store_secret,
            data={"secret_text": DEFAULT_SECRET_TEXT, "expiry_seconds": 120},
            format="json",
        )

        # Ensure it was created.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check to ensure the burn at is correctly set
        response_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(
            math.floor((now + timezone.timedelta(seconds=float(120))).timestamp()),
            response_data.get("burnAt"),
        )

    def test_002_store_secret_with_passphrase(self):
        response = self.client.post(
            path=URLS.store_secret,
            data={
                "secret_text": DEFAULT_SECRET_TEXT,
                "expiry_seconds": 120,
                "passphrase": DEFAULT_PASSPHRASE,
            },
            format="json",
        )

        # Ensure it was created.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ensure the secret has a hash
        response_data = json.loads(response.content.decode("utf-8"))

        secret = Secret.objects.filter(secret_id=response_data.get("secretId")).first()
        self.assertIsNotNone(secret)
        self.assertIsNotNone(secret.passphrase_hash)
        self.assertTrue(check_password("password", secret.passphrase_hash))

    def test_003_retrieve_secret_without_passphrase(self):
        response = self.client.post(
            path=URLS.store_secret,
            data={
                "secretText": DEFAULT_SECRET_TEXT,
                "expirySeconds": 120,
            },
            format="json",
        )

        # Ensure it was created.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ensure the secret has a hash
        response_data = json.loads(response.content.decode("utf-8"))
        secret_id = response_data.get("secretId")

        response = self.client.post(
            path=URLS.retrieve_secret, data={"secretId": secret_id}, format="json"
        )

        # Ensure it was retrieved.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the secret has a hash
        retrieve_data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(retrieve_data.get("secretText"), DEFAULT_SECRET_TEXT)

    def test_004_retrieve_secret_with_passphrase(self):
        response = self.client.post(
            path=URLS.store_secret,
            data={
                "secretText": DEFAULT_SECRET_TEXT,
                "expirySeconds": 120,
                "passphrase": DEFAULT_PASSPHRASE,
            },
            format="json",
        )

        # Ensure it was created.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ensure the secret has a hash
        response_data = json.loads(response.content.decode("utf-8"))
        secret_id = response_data.get("secretId")

        # Try without first
        response = self.client.post(
            path=URLS.retrieve_secret,
            data={
                "secretId": secret_id,
            },
            format="json",
        )

        # Ensure it was rejected.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Try with the wrong passphrase
        response = self.client.post(
            path=URLS.retrieve_secret,
            data={"secretId": secret_id, "passphrase": "wrong one"},
            format="json",
        )

        # Ensure it was rejected.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            path=URLS.retrieve_secret,
            data={"secretId": secret_id, "passphrase": DEFAULT_PASSPHRASE},
            format="json",
        )

        # Ensure it was retrieved.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the secret has a hash
        retrieve_data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(retrieve_data.get("secretText"), DEFAULT_SECRET_TEXT)


class RequestAPITests(APITestCase):

    @freezegun.freeze_time(time_to_freeze=now)
    def test_001_store_request_without_passphrase(self):
        response = self.client.post(
            path=URLS.store_request, data={"expiry_seconds": 120}, format="json"
        )

        # Ensure it was created.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = json.loads(response.content.decode("utf-8"))

        # Check to ensure the burn at is correctly set
        self.assertEqual(
            math.floor((now + timezone.timedelta(seconds=float(120))).timestamp()),
            response_data.get("burnAt"),
        )

        # Ensure we have all the data, and it's correct
        self.assertIsNotNone(response_data.get("secretId"))
        self.assertIsNotNone(response_data.get("requestId"))

        secret = Secret.objects.filter(
            request_id=response_data.get("requestId")
        ).first()
        self.assertIsNotNone(secret.request_id)
        self.assertEqual(secret.secret_id, response_data.get("secretId"))
