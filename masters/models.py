from django.db import models
from core.models import TimeStampedModel
from users.models import Organization

class AccountGroup(TimeStampedModel):
    """
    Hierarchical account groups (e.g., Assets -> Current Assets -> Bank Accounts).
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='account_groups', null=True, blank=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='subgroups')
    
    NATURE_CHOICES = (
        ('ASSETS', 'Assets'),
        ('LIABILITIES', 'Liabilities'),
        ('INCOME', 'Income'),
        ('EXPENSES', 'Expenses'),
    )
    nature = models.CharField(max_length=20, choices=NATURE_CHOICES)

    def __str__(self):
        return self.name

class CostCenter(TimeStampedModel):
    """
    For departmental or project-wise tracking.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='cost_centers')
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='sub_centers')

    def __str__(self):
        return self.name

class Ledger(TimeStampedModel):
    """
    Individual accounts with extended features for Indian Context.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='ledgers')
    name = models.CharField(max_length=255)
    group = models.ForeignKey(AccountGroup, on_delete=models.PROTECT, related_name='ledgers')
    
    # Statutory Details
    gstin = models.CharField(max_length=15, blank=True, null=True)
    pan = models.CharField(max_length=10, blank=True, null=True)
    state_code = models.CharField(max_length=2, blank=True, null=True, help_text="2-digit State Code for GST")
    
    # Contact Details
    address = models.TextField(blank=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    
    # Bank Details
    bank_account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    
    # Credit Management
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    credit_days = models.IntegerField(default=0)
    
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    opening_balance_type = models.CharField(max_length=2, choices=(('Dr', 'Debit'), ('Cr', 'Credit')), default='Dr')

    def __str__(self):
        return self.name

class Unit(TimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='units')
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class Warehouse(TimeStampedModel):
    """
    Godown/Location management.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='warehouses')
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Item(TimeStampedModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    hsn_sac = models.CharField(max_length=20, blank=True, help_text="HSN or SAC Code")
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='items', null=True, blank=True)
    
    # Tax Details
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="GST Tax Rate in %")
    
    # Pricing
    selling_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    mrp = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Inventory Settings
    min_stock_level = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    reorder_level = models.DecimalField(max_digits=15, decimal_places=3, default=0.000)
    
    # Feature Flags
    maintain_batches = models.BooleanField(default=False)
    maintain_serial_numbers = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Batch(TimeStampedModel):
    """
    For items with Expiry/Mfg Date.
    """
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='batches')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=50)
    manufacturing_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.item.name} - {self.batch_number}"
