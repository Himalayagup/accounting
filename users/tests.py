from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from users.models import Organization

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/v1/users/'
        self.token_url = '/api/v1/token/'
        self.org_url = '/api/v1/organizations/'

    def test_registration(self):
        payload = {
            'email': 'newuser@example.com',
            'password': 'securepassword123'
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_login_and_org_creation(self):
        # 1. Register
        user = User.objects.create_user(email='admin@example.com', password='password123')
        
        # 2. Login (Get Token)
        login_payload = {
            'email': 'admin@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.token_url, login_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data['access']
        
        # 3. Create Organization
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        org_payload = {
            'name': 'My New Company',
            'financial_year_start': '2024-04-01',
            'gstin': '07AABBC1234D1Z5'
        }
        response = self.client.post(self.org_url, org_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organization.objects.count(), 1)
        self.assertEqual(Organization.objects.first().owner, user)
