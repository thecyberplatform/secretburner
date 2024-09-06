import math
from django.utils import timezone


def seconds_from_now_timestamp(seconds: int):
    """
    Adds a specified number of seconds to the current time to produce a new timestamp.

    This function calculates the future time by adding a given number of seconds to the current
    time and then converts this future time into a Unix timestamp (the number of seconds since
    January 1, 1970, UTC). The result is then rounded down to the nearest whole second.

    Parameters:
        seconds (int): The number of seconds to add to the current time.

    Returns:
        int: The Unix timestamp corresponding to the future time, rounded down to the nearest whole second.
    """
    future_time = timezone.now() + timezone.timedelta(seconds=float(seconds))
    return math.floor(future_time.timestamp())
