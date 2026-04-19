import json

from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser

from .models import CloudDataset


class MLTests(TestCase):
    def test_predict_requires_authentication(self):
        response = self.client.get(reverse('ml:predict'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('ml:predict')}")

    def test_predict_placeholder_endpoint_for_authenticated_user(self):
        user = CustomUser.objects.create_user(username='mluser', password='StrongPass1!')
        self.client.force_login(user)
        response = self.client.get(reverse('ml:predict'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('placeholder', response.json()['message'].lower())

    def test_upload_dataset_json_success(self):
        user = CustomUser.objects.create_user(username='datasetuser', password='StrongPass1!')
        self.client.force_login(user)
        payload = {
            'records': [
                {'cpu': 1.5, 'memory': 2.0, 'cost': 10.0, 'tag': 'api', 'cloud': 'AWS'},
                {'cpu': 2.5, 'memory': 4.0, 'cost': 20.0, 'tag': 'db', 'cloud': 'Azure'},
            ]
        }
        response = self.client.post(
            reverse('ml:upload_dataset'),
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(CloudDataset.objects.count(), 2)

    def test_upload_dataset_requires_authentication(self):
        response = self.client.post(
            reverse('ml:upload_dataset'),
            data=json.dumps({'records': []}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 302)

    def test_upload_dataset_invalid_payload_fails(self):
        user = CustomUser.objects.create_user(username='datasetuser2', password='StrongPass1!')
        self.client.force_login(user)
        response = self.client.post(
            reverse('ml:upload_dataset'),
            data='{"records":"invalid"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
