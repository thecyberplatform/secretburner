from rest_framework.exceptions import ValidationError

from core.base.exception_handler.exception_handler import (
    convert_to_detail_string,
    list_values_to_message,
    format_and_flatten_data,
    custom_exception_handler,
    format_error_data,
)
from rest_framework.test import APITestCase


class ExceptionHandlerTest(APITestCase):
    test_data = {
        "first": ["First message."],
        "second": {
            "second_1": {
                "second_11": {
                    "second_111": ["Second message."],
                }
            },
            "second_2": ["Third message."],
            "second_3": {
                "second_31": ["Fourth message."],
                "second_32": {
                    "second_321": ["Fifth message."],
                    "second_322": ["Sixth message."],
                },
            },
        },
    }

    def test_01_list_values_to_message(self):
        list_data = ["First message.", "Second message.", "Third message."]
        result = list_values_to_message(list_data)
        self.assertEqual(result, "First message. Second message. Third message.")

    def test_02_convert_to_detail_string_when_field_errors(self):
        data = [
            {"field": "field_name_1", "detail": "First message."},
            {"field": "field_name_2", "detail": "Second message."},
        ]
        result = convert_to_detail_string(data)
        self.assertEqual(
            result, "field_name_1: First message. field_name_2: Second message."
        )

    def test_03_convert_to_detail_string_when_empty_data(self):
        data = []
        result = convert_to_detail_string(data)
        self.assertEqual(result, "")

    def test_04_convert_to_detail_string_when_non_field_errors(self):
        data = [{"detail": "Some message."}]
        result = convert_to_detail_string(data)
        self.assertEqual(result, "Some message.")

    def test_05_flatten_data_when_no_prefix_given_and_branching_true(self):
        result = format_and_flatten_data(
            data=self.test_data, data_key="", data_branching=True
        )

        self.assertEqual(
            result,
            [
                {"field": "first", "detail": "First message."},
                {"field": "second_second_1", "detail": "Second message."},
                {"field": "second_second_2", "detail": "Third message."},
                {"field": "second_second_3_second_31", "detail": "Fourth message."},
                {
                    "field": "second_second_3_second_32_second_321",
                    "detail": "Fifth message.",
                },
                {
                    "field": "second_second_3_second_32_second_322",
                    "detail": "Sixth message.",
                },
            ],
        )

    def test_06_flatten_data_when_no_prefix_given_and_branching_false(self):
        result = format_and_flatten_data(
            data=self.test_data, data_key="", data_branching=False
        )

        self.assertEqual(
            result,
            [
                {"field": "first", "detail": "First message."},
                {"field": "second_second_1", "detail": "Second message."},
                {"field": "second_second_2", "detail": "Third message."},
                {"field": "second_second_3_second_31", "detail": "Fourth message."},
                {
                    "field": "second_second_3_second_32_second_321",
                    "detail": "Fifth message.",
                },
                {
                    "field": "second_second_3_second_32_second_322",
                    "detail": "Sixth message.",
                },
            ],
        )

    def test_07_flatten_data_when_prefix_given_and_branching_true(self):
        result = format_and_flatten_data(
            data=self.test_data, data_key="some_prefix", data_branching=True
        )

        self.assertEqual(
            result,
            [
                {"field": "some_prefix_first", "detail": "First message."},
                {"field": "some_prefix_second_second_1", "detail": "Second message."},
                {"field": "some_prefix_second_second_2", "detail": "Third message."},
                {
                    "field": "some_prefix_second_second_3_second_31",
                    "detail": "Fourth message.",
                },
                {
                    "field": "some_prefix_second_second_3_second_32_second_321",
                    "detail": "Fifth message.",
                },
                {
                    "field": "some_prefix_second_second_3_second_32_second_322",
                    "detail": "Sixth message.",
                },
            ],
        )

    def test_08_flatten_data_when_prefix_given_and_branching_false(self):
        result = format_and_flatten_data(
            data=self.test_data, data_key="some_prefix", data_branching=False
        )

        self.assertEqual(
            result,
            [
                {"field": "some_prefix", "detail": "First message."},
                {"field": "some_prefix_second_1", "detail": "Second message."},
                {"field": "some_prefix_second_2", "detail": "Third message."},
                {
                    "field": "some_prefix_second_3_second_31",
                    "detail": "Fourth message.",
                },
                {
                    "field": "some_prefix_second_3_second_32_second_321",
                    "detail": "Fifth message.",
                },
                {
                    "field": "some_prefix_second_3_second_32_second_322",
                    "detail": "Sixth message.",
                },
            ],
        )

    def test_09_flatten_data_when_list_given(self):
        test_data = ["First message.", "Second message"]

        result = format_and_flatten_data(
            data=test_data, data_key="", data_branching=False
        )

        self.assertEqual(result, [{"detail": "First message. Second message"}])

    def test_10_custom_exception_handler(self):
        exception = ValidationError(detail=self.test_data)
        result = custom_exception_handler(exception, context=None)

        formatted_data = format_and_flatten_data(self.test_data, "", True)

        self.assertEqual(
            result.data,
            {
                "detail": convert_to_detail_string(formatted_data),
                "errors": formatted_data,
                "code": "invalid",  # default code for DRF ValidationError
            },
        )

    def test_11_format_error_data(self):
        error_message = "Some message."
        code = "invalid_request"

        data, content = format_error_data(error_message, code)

        self.assertEqual(data["detail"], error_message)
        self.assertEqual(data["errors"], [{"detail": error_message}])
        self.assertEqual(data["code"], code)
        self.assertNotIn("is_processed", data)

        self.assertIsInstance(content, bytes)
