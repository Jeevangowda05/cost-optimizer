from django.test import TestCase
from django.urls import reverse


class OptimizerTests(TestCase):
    def test_recommendations_placeholder_endpoint(self):
        response = self.client.get(reverse('optimizer:recommendations'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('placeholder', response.json()['message'].lower())
