from django.test import TestCase, RequestFactory
import json
from unittest.mock import Mock, patch
from .data import ConvertRequestEmptyStringToNull


class TestDataMiddleware(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = ConvertRequestEmptyStringToNull(self.get_response)
        self.get_response = Mock()

    def test_01_empty_string_to_null_conversion(self):
        # Create a mock request with JSON body containing empty strings
        request = self.factory.post(
            "/dummy-url",
            data=json.dumps({"name": "", "age": 25}),
            content_type="application/json",
        )

        # Modify the body to simulate a real Django body behavior
        request._body = request.body

        # Call the middleware
        self.middleware(request)

        # Check the modified body
        modified_data = json.loads(request._body.decode())
        expected_data = {"name": None, "age": 25}

        self.assertEqual(modified_data, expected_data)

    def test_02_invalid_json(self):
        # Create a mock request with invalid JSON body
        request = self.factory.post(
            "/dummy-url",
            data="{invalid_json}",
            content_type="application/json",
        )

        # Modify the body to simulate a real Django body behavior
        request._body = request.body

        with patch.object(self.middleware, "get_response") as mock_get_response:
            mock_get_response.return_value = Mock()

            # Call the middleware
            response = self.middleware(request)

            # Check that the request body is unchanged
            self.assertEqual(request._body, b"{invalid_json}")

            # Check that get_response was called
            mock_get_response.assert_called_once()
            self.assertEqual(response, mock_get_response.return_value)

    def test_03_unicode_decode_error(self):
        # Create a mock request with a body that cannot be decoded as UTF-8
        request = self.factory.post(
            "/dummy-url",
            data=b"\x80\x81\x82",  # Invalid UTF-8 byte sequence
            content_type="application/json",
        )

        # Modify the body to simulate a real Django body behavior
        request._body = request.body

        with patch.object(self.middleware, "get_response") as mock_get_response:
            mock_get_response.return_value = Mock()

            # Call the middleware
            response = self.middleware(request)

            # Check that the request body is unchanged and that get_response is called
            self.assertEqual(request._body, b"\x80\x81\x82")
            mock_get_response.assert_called_once()
            self.assertEqual(response, mock_get_response.return_value)

    @classmethod
    def get_response(cls, request):
        # Simple response simulation function
        return Mock()
