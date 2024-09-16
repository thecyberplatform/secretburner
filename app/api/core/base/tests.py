from django.test import TestCase
from django.urls import reverse


class HealthCheckTest(TestCase):
    def test_01_health_check(self):
        # Simulate a GET request to the health_check view
        response = self.client.get(reverse("api:health_check"))

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
