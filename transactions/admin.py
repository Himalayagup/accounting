from django.contrib import admin

# Register your models here.
from .models import Voucher, VoucherDetail

class VoucherDetailInline(admin.TabularInline):
    model = VoucherDetail
    extra = 1

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('voucher_number', 'voucher_type', 'date', 'organization', 'status', 'amount')
    list_filter = ('organization', 'voucher_type', 'status', 'date')
    search_fields = ('voucher_number', 'organization__name', 'party_ledger__name')
    inlines = [VoucherDetailInline]

    def amount(self, obj):
        # Calculate total amount from details or return a stored field if added later
        # Currently Voucher doesn't have a total_amount field directly on it in the model definition shown earlier, 
        # but usually it's good to show it. For now we'll sum details.
        return sum(d.amount for d in obj.details.all())

