from django.db import models
from core.models import TimeStampedModel
from users.models import Organization
from masters.models import Ledger, Item, Warehouse, CostCenter, Batch

class Voucher(TimeStampedModel):
    VOUCHER_TYPES = (
        ('SALES', 'Sales'),
        ('PURCHASE', 'Purchase'),
        ('RECEIPT', 'Receipt'),
        ('PAYMENT', 'Payment'),
        ('CONTRA', 'Contra'),
        ('JOURNAL', 'Journal'),
        ('DEBIT_NOTE', 'Debit Note'),
        ('CREDIT_NOTE', 'Credit Note'),
        ('SALES_ORDER', 'Sales Order'),
        ('PURCHASE_ORDER', 'Purchase Order'),
    )
    
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('POSTED', 'Posted'),
        ('CANCELLED', 'Cancelled'),
    )
    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='vouchers')
    voucher_type = models.CharField(max_length=20, choices=VOUCHER_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    voucher_number = models.CharField(max_length=50)
    date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    narration = models.TextField(blank=True)
    
    # Party Details
    party_ledger = models.ForeignKey(Ledger, on_delete=models.PROTECT, related_name='vouchers_as_party', null=True, blank=True)
    shipping_address = models.TextField(blank=True)
    billing_address = models.TextField(blank=True)
    
    # Reference (e.g., PO Number for Sales)
    reference_number = models.CharField(max_length=50, blank=True)
    reference_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('organization', 'voucher_type', 'voucher_number')

    def __str__(self):
        return f"{self.voucher_type} - {self.voucher_number}"

class VoucherDetail(TimeStampedModel):
    """
    Line items for the voucher.
    """
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name='details')
    ledger = models.ForeignKey(Ledger, on_delete=models.PROTECT, related_name='voucher_details')
    
    # Inventory details
    item = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, blank=True, related_name='voucher_details')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, null=True, blank=True, related_name='voucher_details')
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, null=True, blank=True, related_name='voucher_details')
    
    quantity = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    rate = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Discounts
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Amount
    amount = models.DecimalField(max_digits=15, decimal_places=2) # Net Amount after discount
    
    # Cost Center
    cost_center = models.ForeignKey(CostCenter, on_delete=models.PROTECT, null=True, blank=True, related_name='voucher_details')
    
    # Debit/Credit
    dr_cr = models.CharField(max_length=2, choices=(('Dr', 'Debit'), ('Cr', 'Credit')))
    
    # Tax Breakdown
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    cgst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    sgst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    igst_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.voucher.voucher_number} - {self.ledger.name} - {self.amount} {self.dr_cr}"
