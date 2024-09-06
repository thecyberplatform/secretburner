import unittest
import string
from .crypto import RandomStringGenerator


class TestCryptoFunctions(unittest.TestCase):

    def test_01_alpha_only(self):
        generator = RandomStringGenerator(
            20, include_alpha=True, include_numeric=False, include_symbols=False
        )
        result = generator.generate()
        self.assertTrue(all(char in string.ascii_letters for char in result))
        self.assertEqual(len(result), 20)

    def test_02_numeric_only(self):
        generator = RandomStringGenerator(
            20, include_alpha=False, include_numeric=True, include_symbols=False
        )
        result = generator.generate()
        self.assertTrue(all(char in string.digits for char in result))
        self.assertEqual(len(result), 20)

    def test_03_symbols_only(self):
        generator = RandomStringGenerator(
            20, include_alpha=False, include_numeric=False, include_symbols=True
        )
        result = generator.generate()
        self.assertTrue(all(char in string.punctuation for char in result))
        self.assertEqual(len(result), 20)

    def test_04_alpha_numeric(self):
        generator = RandomStringGenerator(
            20, include_alpha=True, include_numeric=True, include_symbols=False
        )
        result = generator.generate()
        self.assertTrue(
            all(char in string.ascii_letters + string.digits for char in result)
        )
        self.assertEqual(len(result), 20)

    def test_05_alpha_symbols(self):
        generator = RandomStringGenerator(
            20, include_alpha=True, include_numeric=False, include_symbols=True
        )
        result = generator.generate()
        self.assertTrue(
            all(char in string.ascii_letters + string.punctuation for char in result)
        )
        self.assertEqual(len(result), 20)

    def test_06_numeric_symbols(self):
        generator = RandomStringGenerator(
            20, include_alpha=False, include_numeric=True, include_symbols=True
        )
        result = generator.generate()
        self.assertTrue(
            all(char in string.digits + string.punctuation for char in result)
        )
        self.assertEqual(len(result), 20)

    def test_07_all_character_types(self):
        generator = RandomStringGenerator(
            20, include_alpha=True, include_numeric=True, include_symbols=True
        )
        result = generator.generate()
        self.assertTrue(
            all(
                char in string.ascii_letters + string.digits + string.punctuation
                for char in result
            )
        )
        self.assertEqual(len(result), 20)

    def test_08_empty_character_set_raises_error(self):
        with self.assertRaises(ValueError):
            RandomStringGenerator(
                20, include_alpha=False, include_numeric=False, include_symbols=False
            )
