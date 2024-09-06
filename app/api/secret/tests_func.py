from django.utils import timezone
from unittest.mock import patch

from secret.func import burn_now, check_verification

from django.test import TestCase
from django.contrib.auth.hashers import make_password
from .models import Verification
from .exceptions import EmailVerificationError


class TestBurnNow(TestCase):

    @patch("django.utils.timezone.now")
    def test_burn_now_true(self, mock_now):
        # Set a fixed time for the current time
        mock_now.return_value = timezone.datetime(2024, 1, 1, 12, 0, 0)
        timestamp = timezone.datetime(2024, 1, 1, 11, 0, 0).timestamp()
        self.assertTrue(burn_now(int(timestamp)))

    @patch("django.utils.timezone.now")
    def test_burn_now_false(self, mock_now):
        # Set a fixed time for the current time
        mock_now.return_value = timezone.datetime(2024, 1, 1, 12, 0, 0)
        timestamp = timezone.datetime(2024, 1, 1, 13, 0, 0).timestamp()
        self.assertFalse(burn_now(int(timestamp)))


class TestCheckVerification(TestCase):

    def setUp(self):
        self.valid_email = "test@example.com"
        self.valid_token = "valid-token"
        self.invalid_token = "invalid-token"
        self.valid_email_hash = make_password(self.valid_email)

        # Set up a valid verification record
        Verification.objects.create(
            verified_token=self.valid_token, email_hash=self.valid_email_hash
        )

    def test_check_verification_success(self):
        result = check_verification(self.valid_token, self.valid_email)
        self.assertTrue(result)
        # Ensure the verification record is deleted
        self.assertIsNone(
            Verification.objects.filter(verified_token=self.valid_token).first()
        )

    def test_check_verification_invalid_token(self):
        with self.assertRaises(EmailVerificationError):
            check_verification(self.invalid_token, self.valid_email)

    def test_check_verification_invalid_email(self):
        incorrect_email = "wrong@example.com"
        with self.assertRaises(EmailVerificationError):
            check_verification(self.valid_token, incorrect_email)
