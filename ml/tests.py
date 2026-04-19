from django.test import TestCase
from django.urls import reverse


class MLTests(TestCase):
    def test_predict_placeholder_endpoint(self):
        response = self.client.get(reverse('ml:predict'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('placeholder', response.json()['message'].lower())
