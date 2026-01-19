from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from users.models import Organization, OrganizationUser
from masters.models import AccountGroup, Ledger, Item, Unit
from transactions.models import Voucher

User = get_user_model()

class AccountingIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # 1. Setup User & Auth
        self.user = User.objects.create_user(email='test@example.com', password='password123')
        self.client.force_authenticate(user=self.user)
        
        # 2. Setup Organization (Delhi - Code 07)
        self.org = Organization.objects.create(
            name="Test Corp",
            gstin="07AAAAA0000A1Z5",
            financial_year_start="2024-04-01",
            owner=self.user
        )
        OrganizationUser.objects.create(organization=self.org, user=self.user, role='ADMIN')
        
        # 3. Setup Masters
        # Group
        self.group = AccountGroup.objects.create(
            organization=self.org,
            name="Sundry Debtors",
            nature="ASSETS"
        )
        
        # Unit
        self.unit = Unit.objects.create(organization=self.org, name="Numbers", symbol="Nos")
        
        # Item (18% Tax)
        self.item = Item.objects.create(
            organization=self.org,
            name="Test Product",
            tax_rate=18.00,
            unit=self.unit,
            selling_price=100.00
        )

    def test_intra_state_transaction(self):
        """
        Test Sales to a local party (Delhi to Delhi) -> Should have CGST + SGST
        """
        # Create Local Ledger (Delhi)
        local_party = Ledger.objects.create(
            organization=self.org,
            name="Local Customer",
            group=self.group,
            state_code="07" # Same as Org
        )
        
        payload = {
            "voucher_type": "SALES",
            "date": "2024-04-01",
            "party_ledger": local_party.id,
            "details": [
                {
                    "ledger": local_party.id, # In real accounting, this would be Sales Account, but using party for simplicity here
                    "item": self.item.id,
                    "quantity": 10,
                    "rate": 100.00,
                    "amount": 1000.00,
                    "tax_rate": 18.00,
                    "dr_cr": "Cr"
                }
            ]
        }
        
        response = self.client.post('/api/v1/transactions/vouchers/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        voucher_id = response.data['id']
        voucher = Voucher.objects.get(id=voucher_id)
        detail = voucher.details.first()
        
        # Verify Tax: 18% of 1000 = 180. Intra-state means 90 CGST, 90 SGST.
        self.assertEqual(detail.cgst_amount, 90.00)
        self.assertEqual(detail.sgst_amount, 90.00)
        self.assertEqual(detail.igst_amount, 0.00)

    def test_inter_state_transaction(self):
        """
        Test Sales to an out-of-state party (Delhi to Mumbai) -> Should have IGST
        """
        # Create Inter-state Ledger (Maharashtra - 27)
        inter_party = Ledger.objects.create(
            organization=self.org,
            name="Mumbai Customer",
            group=self.group,
            state_code="27" # Different from Org (07)
        )
        
        payload = {
            "voucher_type": "SALES",
            "date": "2024-04-01",
            "party_ledger": inter_party.id,
            "details": [
                {
                    "ledger": inter_party.id,
                    "item": self.item.id,
                    "quantity": 10,
                    "rate": 100.00,
                    "amount": 1000.00,
                    "tax_rate": 18.00,
                    "dr_cr": "Cr"
                }
            ]
        }
        
        response = self.client.post('/api/v1/transactions/vouchers/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        voucher_id = response.data['id']
        voucher = Voucher.objects.get(id=voucher_id)
        detail = voucher.details.first()
        
        # Verify Tax: 18% of 1000 = 180. Inter-state means 180 IGST.
        self.assertEqual(detail.cgst_amount, 0.00)
        self.assertEqual(detail.sgst_amount, 0.00)
        self.assertEqual(detail.igst_amount, 180.00)

    def test_voucher_cancellation(self):
        """
        Test cancelling a voucher
        """
        # Create a dummy voucher first
        voucher = Voucher.objects.create(
            organization=self.org,
            voucher_type="SALES",
            voucher_number="TEST-001",
            date="2024-04-01",
            status="POSTED"
        )
        
        url = f'/api/v1/transactions/vouchers/{voucher.id}/cancel/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        voucher.refresh_from_db()
        self.assertEqual(voucher.status, 'CANCELLED')
