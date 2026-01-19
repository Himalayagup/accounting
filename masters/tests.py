from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from users.models import Organization, OrganizationUser
from masters.models import AccountGroup, Ledger, Item, Warehouse, CostCenter

User = get_user_model()

class MastersTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='master@example.com', password='password123')
        self.client.force_authenticate(user=self.user)
        
        self.org = Organization.objects.create(
            name="Master Corp",
            financial_year_start="2024-04-01",
            owner=self.user
        )
        OrganizationUser.objects.create(organization=self.org, user=self.user, role='ADMIN')
        
        # Create a base group
        self.group = AccountGroup.objects.create(organization=self.org, name="Sundry Creditors", nature="LIABILITIES")

    def test_ledger_crud(self):
        payload = {
            "name": "Supplier A",
            "group": self.group.id,
            "organization": self.org.id,
            "state_code": "07"
        }
        response = self.client.post('/api/v1/masters/ledgers/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ledger.objects.count(), 1)

    def test_warehouse_crud(self):
        payload = {
            "name": "Main Godown",
            "address": "123 Warehouse St",
            "organization": self.org.id
        }
        response = self.client.post('/api/v1/masters/warehouses/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Warehouse.objects.count(), 1)

    def test_cost_center_crud(self):
        payload = {
            "name": "Project X",
            "organization": self.org.id
        }
        response = self.client.post('/api/v1/masters/cost-centers/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CostCenter.objects.count(), 1)

    def test_item_crud(self):
        payload = {
            "name": "Service Item",
            "organization": self.org.id,
            "tax_rate": 18.00,
            "selling_price": 500.00
        }
        response = self.client.post('/api/v1/masters/items/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
