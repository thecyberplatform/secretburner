import time
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from secret.models import Secret
from uuid import uuid4
from django.contrib.auth.hashers import make_password


class HandleStoreSecretTest(APITestCase):

    def test_01_store_secret_success(self):
        # API request payload for storing a secret
        payload = {
            "secret_text": "This is a secret text.",
            "expiry_seconds": 3600,
        }

        # Reverse the correct URL for storing the secret
        url = reverse("api:secret:handle_store_secret")
        response = self.client.post(url, payload, format="json")

        # Assert that the response status is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the response contains 'secret_id' and 'burn_at'
        self.assertIn("secret_id", response.data)
        self.assertIn("burn_at", response.data)

        # Check that the secret was created in the database
        self.assertTrue(
            Secret.objects.filter(secret_id=response.data["secret_id"]).exists()
        )

    def test_02_store_secret_invalid_expiry(self):
        # API request payload with invalid expiry_seconds (less than 60)
        payload = {
            "secret_text": "This is a secret text.",
            "expiry_seconds": 30,  # Invalid expiry, below 60
        }

        # Reverse the correct URL for storing the secret
        url = reverse("api:secret:handle_store_secret")
        response = self.client.post(url, payload, format="json")

        # Assert that the response status is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that the response contains validation error for 'expiry_seconds'
        self.assertEqual(response.data["errors"][0]["field"], "expiry_seconds")
        self.assertEqual(
            response.data["errors"][0]["detail"],
            "Ensure this value is greater than or equal to 60.",
        )


class HandleRetrieveSecretTest(APITestCase):

    def setUp(self):
        # Create a Secret instance in the database for testing retrieval
        self.secret = Secret.objects.create(
            secret_id=str(uuid4()),
            secret_text="This is a test secret",
            expiry_seconds=3600,
            burn_at=int(time.time()) + 3600,
            passphrase_hash=make_password("test-passphrase"),
        )

        self.secret_no_passphrase = Secret.objects.create(
            secret_id=str(uuid4()),
            secret_text="This is a test secret",
            expiry_seconds=3600,
            burn_at=int(time.time()) + 3600,
        )

        self.secret_with_public_key = Secret.objects.create(
            secret_id=str(uuid4()),
            secret_text="This is a test secret",
            expiry_seconds=3600,
            burn_at=int(time.time()) + 3600,
            public_key="test-public-key",
        )

        self.secret_with_pub_and_pass = Secret.objects.create(
            secret_id=str(uuid4()),
            secret_text="This is a test secret",
            expiry_seconds=3600,
            burn_at=int(time.time()) + 3600,
            passphrase_hash=make_password("test-passphrase"),
            public_key="test-public-key",
        )

        self.secret_no_req_with_pass = Secret.objects.create(
            secret_id=str(uuid4()),
            secret_text="This is a test secret",
            expiry_seconds=3600,
            burn_at=int(time.time()) + 3600,
            passphrase_hash=make_password("test-passphrase"),
            request_id=str(uuid4()),
        )

        self.secret_request_with_public_key = Secret.objects.create(
            secret_id=str(uuid4()),
            secret_text="This is a test secret",
            expiry_seconds=3600,
            burn_at=int(time.time()) + 3600,
            public_key="test-public-key",
            request_id=str(uuid4()),
        )

    def test_01_retrieve_secret_success(self):
        # API request payload for retrieving the secret
        payload = {"secret_id": self.secret.secret_id, "passphrase": "test-passphrase"}

        # Reverse the correct URL for retrieving the secret
        url = reverse("api:secret:handle_retrieve_secret")
        response = self.client.post(url, payload, format="json")

        # Assert that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the 'secret_text' and 'burn_at'
        self.assertIn("secret_text", response.data)
        self.assertIn("burn_at", response.data)
        self.assertEqual(response.data["secret_text"], self.secret.secret_text)

        # Check if the secret was deleted after retrieval
        self.assertFalse(
            Secret.objects.filter(secret_id=self.secret.secret_id).exists()
        )

    def test_02_retrieve_secret_incorrect_passphrase(self):
        # API request payload with incorrect passphrase
        payload = {"secret_id": self.secret.secret_id, "passphrase": "wrong-passphrase"}

        # Reverse the correct URL for retrieving the secret
        url = reverse("api:secret:handle_retrieve_secret")
        response = self.client.post(url, payload, format="json")

        # Assert that the response status is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that the response contains validation error for incorrect passphrase
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "secret not found")

    def test_03_retrieve_secret_expired(self):
        # Expire the secret by setting burn_at to the past
        self.secret.burn_at = int(time.time()) - 1000
        self.secret.save()

        # API request payload for retrieving the secret
        payload = {"secret_id": self.secret.secret_id, "passphrase": "test-passphrase"}

        # Reverse the correct URL for retrieving the secret
        url = reverse("api:secret:handle_retrieve_secret")
        response = self.client.post(url, payload, format="json")

        # Assert that the response status is 400 BAD REQUEST (expired secret)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that the response contains validation error for expired secret
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "secret not found")

        # Check that the secret was deleted after expiration
        self.assertFalse(
            Secret.objects.filter(secret_id=self.secret.secret_id).exists()
        )

    def test_04_retrieve_secret_not_found(self):
        # API request payload for retrieving a non-existent secret
        payload = {
            "secret_id": str(uuid4()),  # Non-existent secret_id
            "passphrase": "test-passphrase",
        }

        # Reverse the correct URL for retrieving the secret
        url = reverse("api:secret:handle_retrieve_secret")
        response = self.client.post(url, payload, format="json")

        # Assert that the response status is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that the response contains validation error for non-existent secret
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "secret not found")

    def test_05_retrieve_secret_with_public_key(self):
        payload = {"secret_id": self.secret_with_public_key.secret_id}

        # Reverse the correct URL for retrieving the secret
        url = reverse("api:secret:handle_retrieve_secret")
        response = self.client.post(url, payload, format="json")

        # Assert that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the 'secret_text' and 'burn_at'
        self.assertIn("secret_text", response.data)
        self.assertIn("burn_at", response.data)
        self.assertIn("pki_encrypted", response.data)
        self.assertEqual(response.data["secret_text"], self.secret.secret_text)
        self.assertEqual(response.data["pki_encrypted"], True)

    def test_06_retrieve_secret_with_public_key_and_passphrase_no_request(self):
        payload = {
            "secret_id": self.secret_with_pub_and_pass.secret_id,
            "passphrase": "test-passphrase",
        }

        # Reverse the correct URL for retrieving the secret
        url = reverse("api:secret:handle_retrieve_secret")
        response = self.client.post(url, payload, format="json")

        # Assert that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the 'secret_text' and 'burn_at'
        self.assertIn("secret_text", response.data)
        self.assertIn("burn_at", response.data)
        self.assertIn("pki_encrypted", response.data)
        self.assertIn("passphrase_encrypted", response.data)
        self.assertEqual(response.data["secret_text"], self.secret.secret_text)
        self.assertEqual(response.data["pki_encrypted"], True)
        self.assertEqual(response.data["passphrase_encrypted"], False)

    def test_07_retrieve_secret_with_request_and_passphrase(self):
        payload = {
            "secret_id": self.secret_no_req_with_pass.secret_id,
            "passphrase": "test-passphrase",
        }

        # Reverse the correct URL for retrieving the secret
        url = reverse("api:secret:handle_retrieve_secret")
        response = self.client.post(url, payload, format="json")

        # Assert that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the 'secret_text' and 'burn_at'
        self.assertIn("secret_text", response.data)
        self.assertIn("burn_at", response.data)
        self.assertIn("pki_encrypted", response.data)
        self.assertIn("passphrase_encrypted", response.data)
        self.assertEqual(response.data["secret_text"], self.secret.secret_text)
        self.assertEqual(response.data["pki_encrypted"], False)
        self.assertEqual(response.data["passphrase_encrypted"], False)

    def test_08_retrieve_secret_request_with_public_key(self):
        payload = {"secret_id": self.secret_request_with_public_key.secret_id}

        # Reverse the correct URL for retrieving the secret
        url = reverse("api:secret:handle_retrieve_secret")
        response = self.client.post(url, payload, format="json")

        # Assert that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the 'secret_text' and 'burn_at'
        self.assertIn("secret_text", response.data)
        self.assertIn("burn_at", response.data)
        self.assertIn("pki_encrypted", response.data)
        self.assertEqual(response.data["secret_text"], self.secret.secret_text)
        self.assertEqual(response.data["pki_encrypted"], True)

    def test_09_retrieve_secret_check_success_without_passphrase(self):
        # API request payload for retrieving the secret
        payload = {"secret_id": self.secret_no_passphrase.secret_id}

        # Reverse the correct URL for retrieving the secret
        url = reverse("api:secret:handle_retrieve_secret_check")
        response = self.client.post(url, payload, format="json")

        # Assert that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the passphrase protected property and it's False
        self.assertIn("passphrase_protected", response.data)
        self.assertEqual(response.data["passphrase_protected"], False)

        # Check if the secret was not deleted after retrieval check
        self.assertTrue(Secret.objects.filter(secret_id=self.secret.secret_id).exists())

    def test_10_retrieve_secret_check_success_with_passphrase(self):
        # API request payload for retrieving the secret
        payload = {"secret_id": self.secret.secret_id}

        # Reverse the correct URL for retrieving the secret
        url = reverse("api:secret:handle_retrieve_secret_check")
        response = self.client.post(url, payload, format="json")

        # Assert that the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the passphrase protected property and it's True
        self.assertIn("passphrase_protected", response.data)
        self.assertEqual(response.data["passphrase_protected"], True)

        # Check if the secret was not deleted after retrieval check
        self.assertTrue(Secret.objects.filter(secret_id=self.secret.secret_id).exists())

    def test_11_retrieve_secret_check_failure(self):
        # API request payload for retrieving the secret
        payload = {"secret_id": str(uuid4())}

        # Reverse the correct URL for retrieving the secret
        url = reverse("api:secret:handle_retrieve_secret_check")
        response = self.client.post(url, payload, format="json")

        # Assert that the response status is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that the response contains validation error for non-existent secret
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "secret not found")
