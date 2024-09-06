from unittest.mock import patch
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from core.base.api.throttling import AnonRateThrottlePerView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache


class TestAnonRateThrottlePerView(APITestCase):

    class ExampleView1(APIView):
        throttle_classes = [AnonRateThrottlePerView]

        def get(self, request, *args, **kwargs):
            return Response({"message": "View 1 response"}, status=status.HTTP_200_OK)

    class ExampleView2(APIView):
        throttle_classes = [AnonRateThrottlePerView]

        def get(self, request, *args, **kwargs):
            return Response({"message": "View 2 response"}, status=status.HTTP_200_OK)

    def setUp(self):
        cache.clear()
        self.factory = APIRequestFactory()

    @patch("core.base.api.throttling.AnonRateThrottlePerView.get_rate")
    def test_01_throttle_per_view(self, mock):
        mock.return_value = "1/day"

        # Instantiate views
        view1 = TestAnonRateThrottlePerView.ExampleView1.as_view()
        view2 = TestAnonRateThrottlePerView.ExampleView2.as_view()

        # Create request using RequestFactory
        request1 = self.factory.get("/")
        request2 = self.factory.get("/")

        # Bind request to the view
        response1 = view1(request1)
        response2 = view2(request2)

        # Check initial responses
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

        # Second requests to check throttling
        response1_again = view1(request1)
        response2_again = view2(request2)

        self.assertEqual(response1_again.status_code, 429)
        self.assertEqual(response2_again.status_code, 429)
