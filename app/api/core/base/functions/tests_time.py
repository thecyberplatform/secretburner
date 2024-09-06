import unittest
import math
from django.utils import timezone
from freezegun import freeze_time
from .time import seconds_from_now_timestamp


class TestTimeFunctions(unittest.TestCase):

    @freeze_time("2021-01-01 12:00:00")
    def test_01_seconds_from_now_timestamp(self):
        # Calculate what we expect to see after adding 10 seconds to the frozen time
        expected_time = timezone.now() + timezone.timedelta(seconds=10)
        expected_timestamp = math.floor(expected_time.timestamp())

        # Run the function with 10 seconds added
        result_timestamp = seconds_from_now_timestamp(10)

        # Assert the expected and result timestamps are the same
        self.assertEqual(result_timestamp, expected_timestamp)
