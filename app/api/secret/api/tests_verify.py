from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from secret.models import Verification
from django.contrib.auth.hashers import check_password, make_password
from uuid import uuid4


class HandleRequestVerificationTest(APITestCase):

    @patch("secret.api.serializers.settings")
    @patch("core.base.functions.crypto.RandomStringGenerator.generate")
    @patch("secret.api.serializers.send_mail")
    @patch("secret.api.serializers.build_email_templates")
    def test_01_request_verification_success(
        self,
        mock_build_email_templates,
        mock_send_mail,
        mock_random_string,
        mock_settings,
    ):
        # Mock the random code generator
        mock_settings.ALLOW_EMAIL = True
        mock_random_string.return_value = "123456"
        mock_build_email_templates.return_value = (
            "<html>Email</html>",
            "Plain text email",
        )

        # API request payload for requesting email verification
        payload = {"to_email": "recipient@example.com"}

        # Send POST request to request verification
        url = reverse("api:verify:handle_request_verification")
        response = self.client.post(url, payload, format="json")

        # Assert response status is 201 CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ensure that a Verification object was created
        verification = Verification.objects.get()
        self.assertTrue(
            check_password("recipient@example.com", verification.email_hash)
        )
        self.assertEqual(verification.code, "123456")

        # Ensure the email was sent
        mock_send_mail.assert_called_once()

    def test_02_request_verification_no_email(self):
        # API request payload without email
        payload = {}

        # Send POST request to request verification without email
        url = reverse("api:verify:handle_request_verification")
        response = self.client.post(url, payload, format="json")

        # Assert response status is 400 BAD REQUEST due to missing email
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert the correct error message is returned
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "no email address to verify.")


class HandleVerifyRequestTest(APITestCase):

    def setUp(self):
        # Create a Verification instance in the database
        self.verification = Verification.objects.create(
            verify_id=str(uuid4()),
            code="123456",
            email_hash=make_password("recipient@example.com"),
        )

    @patch("core.base.functions.crypto.RandomStringGenerator.generate")
    def test_01_verify_request_success(self, mock_random_string):
        # Mock the random token generator
        mock_random_string.return_value = "randomly_generated_token"

        # API request payload for verifying the email
        payload = {"verify_id": self.verification.verify_id, "code": "123456"}

        # Send POST request to verify the email
        url = reverse("api:verify:handle_retrieve_secret")
        response = self.client.post(url, payload, format="json")

        # Assert response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure that the verification token was updated
        self.verification.refresh_from_db()
        self.assertEqual(self.verification.verified_token, "randomly_generated_token")

        # Ensure the response contains the verified token and 'ok' is True
        self.assertIn("verified_token", response.data)
        self.assertTrue(response.data["ok"])

    def test_02_verify_request_incorrect_code(self):
        # API request payload with incorrect verification code
        payload = {"verify_id": self.verification.verify_id, "code": "wrongcode"}

        # Send POST request with the wrong code
        url = reverse("api:verify:handle_retrieve_secret")
        response = self.client.post(url, payload, format="json")

        # Assert response status is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert the correct error message is returned
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "verification failed")

    def test_03_verify_request_non_existent_verification(self):
        # API request payload with non-existent verify_id
        payload = {
            "verify_id": str(uuid4()),  # Non-existent verify_id
            "code": "123456",
        }

        # Send POST request with non-existent verification ID
        url = reverse("api:verify:handle_retrieve_secret")
        response = self.client.post(url, payload, format="json")

        # Assert response status is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert the correct error message is returned
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "verification failed")
