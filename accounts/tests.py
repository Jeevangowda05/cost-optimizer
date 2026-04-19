from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class AccountsTests(TestCase):
    def test_custom_user_model_can_be_created(self):
        user = CustomUser.objects.create_user(username='tester', password='securepass123')
        self.assertEqual(user.username, 'tester')

    def test_login_page_renders(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_renders(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
