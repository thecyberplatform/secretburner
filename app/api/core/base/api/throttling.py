from rest_framework.throttling import AnonRateThrottle


class AnonRateThrottlePerView(AnonRateThrottle):
    """
    A custom anonymous rate throttle that generates unique cache keys per view.

    This throttle class extends the default anonymous rate throttle to support
    per-view rate limiting based on the request's IP and the view's name. This is
    useful for applying different rate limits to different views dynamically.

    Attributes:
        scope (str): A default scope name for the throttle rate to be applied, used
                     in the Django settings to specify rate limits.
    """

    scope = "anon_per_view"

    def get_cache_key(self, request, view):
        """
        Overrides the base method to generate a cache key that includes the view's name.

        This method creates a unique cache key by combining the requester's IP address
        with the name of the view being accessed. This ensures that the rate limit
        is applied separately to each view rather than globally across all anonymous requests.

        Parameters:
            request (HttpRequest): The incoming HTTP request object.
            view (APIView): The view being accessed which handles the request.

        Returns:
            str: A string representing the unique cache key for throttling purposes.
        """
        ident = self.get_ident(
            request
        )  # Get the identifier for the request, typically the IP address.
        return f"throttle_{view.__class__.__name__}_{ident}"
