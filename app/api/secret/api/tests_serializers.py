from rest_framework.test import APITestCase
from django.contrib.auth.hashers import check_password
from unittest.mock import patch
from secret.exceptions import EmailVerificationError
from secret.api.serializers import (
    BaseSerializer,
    SerializerWithEmailResponse,
    handle_passphrase,
)


class BaseSerializerTest(APITestCase):

    def test_01_is_valid_processes_fields_correctly(self):
        # Test that the fields 'sender_email', 'recipient_email', and 'verified_token' are correctly processed
        data = {
            "sender_email": "from@example.com",
            "recipient_email": "to@example.com",
            "verified_token": "some-token",
        }

        serializer = BaseSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        self.assertEqual(serializer._sender_email, "from@example.com")
        self.assertEqual(serializer._recipient_email, "to@example.com")
        self.assertEqual(serializer._verified_token, "some-token")

    def test_02_handle_passphrase(self):
        # Test that the passphrase is hashed correctly by handle_passphrase
        initial_data = {"passphrase": "my_secret_passphrase"}
        result = handle_passphrase(initial_data)

        # Ensure the passphrase was removed and passphrase_hash was added
        self.assertNotIn("passphrase", result)
        self.assertIn("passphrase_hash", result)

        # Check if the passphrase was hashed
        self.assertTrue(
            check_password("my_secret_passphrase", result["passphrase_hash"])
        )

    @patch("core.base.functions.mail.settings")
    @patch("secret.api.serializers.render_and_send_mail")
    @patch("secret.api.serializers.check_verification")
    def test_03_send_verified_email_success(
        self,
        mock_check_verification,
        mock_render_and_send_mail,
        mock_settings,
    ):
        # Test that email sending works when verification passes
        mock_settings.ALLOW_EMAIL = True
        mock_check_verification.return_value = True

        # Provide initial data that would simulate the request payload
        initial_data = {
            "sender_email": "sender@example.com",
            "recipient_email": "recipient@example.com",
        }

        serializer = BaseSerializer(data=initial_data)

        # Call is_valid to populate validated_data
        self.assertTrue(serializer.is_valid())

        # Now call send_verified_email after valid data has been processed
        serializer.send_verified_email(
            template_name="test-template",
            subject="Test Subject",
            context_from_serializer=["sender_email", "an_unknown_key"],
            additional_context={"extra_context": "extra_value"},
        )

        # Ensure email verification was called
        mock_check_verification.assert_called_once_with(
            verified_token=None,
            sender_email="sender@example.com",
            recipient_email="recipient@example.com",
        )

        # Ensure the email was sent
        mock_render_and_send_mail.assert_called_once()

    @patch("core.base.functions.mail.settings")
    @patch("core.base.functions.mail.render_and_send_mail")
    @patch(
        "secret.api.serializers.check_verification",
        side_effect=EmailVerificationError("Verification failed"),
    )
    def test_04_send_verified_email_verification_failure(
        self, mock_check_verification, mock_send_mail, mock_settings
    ):
        # Test that the email is not sent if verification fails
        mock_settings.ALLOW_EMAIL = True
        serializer = BaseSerializer()
        serializer._sender_email = "from@example.com"
        serializer._recipient_email = "to@example.com"

        serializer.send_verified_email(
            template_name="test-template",
            subject="Test Subject",
            context_from_serializer=["sender_email"],
            additional_context={"extra_context": "extra_value"},
        )

        # Check that the verification check was called and failed
        mock_check_verification.assert_called_once()

        # Ensure that email was NOT sent due to failed verification
        mock_send_mail.assert_not_called()

        # Ensure that the correct email response is set
        self.assertEqual(serializer.get_email_response(), "Verification failed")

    @patch("secret.api.serializers.check_verification")
    @patch("core.base.functions.mail.settings")
    @patch("core.base.functions.mail.render_and_send_mail")
    def test_05_invalid_characters_in_template(
        self, mock_send_mail, mock_settings, mock_check_verification
    ):
        mock_settings.ALLOW_EMAIL = True
        mock_check_verification.return_value = True
        serializer = BaseSerializer()
        serializer._sender_email = "from@example.com"
        serializer._recipient_email = "to@example.com"

        try:
            serializer.send_verified_email(
                template_name="test-template##",
                subject="Test Subject",
                context_from_serializer=["sender_email"],
                additional_context={"extra_context": "extra_value"},
            )
        except Exception as e:
            self.assertEqual(str(e), "Invalid template name")

        # Ensure that email function isn't called.
        mock_send_mail.assert_not_called()


class SerializerWithEmailResponseTest(APITestCase):

    def test_01_email_response_included_in_representation(self):
        # Test that the email response is included in the serialized output
        instance_data = {"secret_id": "some-secret-id", "burn_at": 1234567890}
        serializer = SerializerWithEmailResponse(email_response="ok")

        # Call to_representation with instance data
        result = serializer.to_representation(instance_data)

        # Ensure the email response is part of the result
        self.assertIn("email_response", result)
        self.assertEqual(result["email_response"], "ok")

    def test_02_set_and_get_email_response(self):
        # Test setting and getting email response
        serializer = SerializerWithEmailResponse()
        serializer.set_email_response("Test email response")

        self.assertEqual(serializer.get_email_response(), "Test email response")
