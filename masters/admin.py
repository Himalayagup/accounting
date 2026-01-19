from django.contrib import admin

# Register your models here.
from .models import AccountGroup, CostCenter, Ledger, Unit, Warehouse, Item, Batch

@admin.register(AccountGroup)
class AccountGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'nature', 'organization', 'parent')
    list_filter = ('nature', 'organization')
    search_fields = ('name',)

@admin.register(CostCenter)
class CostCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'parent')
    list_filter = ('organization',)
    search_fields = ('name',)

@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'organization', 'gstin')
    list_filter = ('organization', 'group')
    search_fields = ('name', 'gstin', 'mobile')

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'organization')
    list_filter = ('organization',)

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'organization')
    list_filter = ('organization',)
    search_fields = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'organization', 'selling_price', 'current_stock')
    list_filter = ('organization', 'unit')
    search_fields = ('name', 'sku', 'barcode')

    def current_stock(self, obj):
        # Placeholder for actual stock logic if available, else just a header
        return "N/A"

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'item', 'organization', 'expiry_date')
    list_filter = ('organization', 'item')
    search_fields = ('batch_number', 'item__name')
