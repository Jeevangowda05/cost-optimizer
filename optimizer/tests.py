from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser

from .models import Recommendation


class OptimizerTests(TestCase):
    def test_recommendations_requires_authentication(self):
        response = self.client.post(reverse('optimizer:recommendations'), data={'cpu': 10, 'memory': 10})
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('optimizer:recommendations')}")

    def test_recommendations_endpoint_for_authenticated_user(self):
        user = CustomUser.objects.create_user(username='optuser', password='StrongPass1!')
        self.client.force_login(user)
        response = self.client.post(
            reverse('optimizer:recommendations'),
            data={'cpu': 20, 'memory': 25, 'current_cost': 100},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload['success'])
        self.assertGreaterEqual(len(payload['recommendations']), 1)
        self.assertIn('type', payload['recommendations'][0])
        self.assertEqual(Recommendation.objects.count(), len(payload['recommendations']))

    def test_recommendations_invalid_input(self):
        user = CustomUser.objects.create_user(username='optuser2', password='StrongPass1!')
        self.client.force_login(user)
        response = self.client.post(reverse('optimizer:recommendations'), data={'cpu': 'invalid', 'memory': 25})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()['success'])
