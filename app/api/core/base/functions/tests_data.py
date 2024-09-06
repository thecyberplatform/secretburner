import unittest
from .data import replace_with_null, pop_if_in, contains_invalid_characters


class TestDataFunctions(unittest.TestCase):

    def test_01_replace_with_null(self):
        # Test with a simple dictionary
        test_obj = {"a": "b", "b": "b"}
        replace_with_null(test_obj, "b")
        self.assertEqual(test_obj, {"a": None, "b": None})

        # Test with nested dictionaries and lists
        test_obj = {"x": {"y": "z", "w": ["z", "b"]}, "a": "b"}
        replace_with_null(test_obj, "z")
        self.assertEqual(test_obj, {"x": {"y": None, "w": [None, "b"]}, "a": "b"})

        # Test with nested dictionaries and lists
        test_obj = {"x": {"y": "z", "w": ["z", "b"], "b": {"y": "z"}}, "a": "b"}
        replace_with_null(test_obj, "z")
        self.assertEqual(
            test_obj, {"x": {"y": None, "w": [None, "b"], "b": {"y": None}}, "a": "b"}
        )

        test_obj = {
            "x": {"y": "z", "w": ["z", "b"], "b": {"y": "z"}},
            "a": "b",
            "d": ["z", "y"],
        }
        replace_with_null(test_obj, "z")
        self.assertEqual(
            test_obj,
            {
                "x": {"y": None, "w": [None, "b"], "b": {"y": None}},
                "a": "b",
                "d": [None, "y"],
            },
        )

        test_obj = {
            "x": ["z", ["z", "b"]],
        }
        replace_with_null(test_obj, "z")
        self.assertEqual(
            test_obj,
            {"x": [None, [None, "b"]]},
        )

        test_list = ["b", "z", {"y": "z"}]
        replace_with_null(test_list, "z")
        self.assertEqual(
            test_list,
            ["b", None, {"y": None}],
        )

    def test_02_pop_if_in(self):
        # Test key is in the dictionary
        test_obj = {"name": "John", "age": 30}
        self.assertEqual(pop_if_in(test_obj, "name"), "John")
        self.assertNotIn("name", test_obj)

        # Test key is not in the dictionary
        self.assertIsNone(pop_if_in(test_obj, "height"))

    def test_03_contains_invalid_characters(self):
        # Test string without invalid characters
        self.assertFalse(contains_invalid_characters("abc123-XYZ_"))

        # Test string with invalid characters
        self.assertTrue(contains_invalid_characters("abc*123|>XYZ"))

        # Test empty string (should not contain invalid characters)
        self.assertFalse(contains_invalid_characters(""))
