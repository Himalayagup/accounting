from rest_framework import serializers
from masters.models import Ledger, AccountGroup, Item, Unit, CostCenter, Warehouse, Batch

class AccountGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountGroup
        fields = '__all__'
        read_only_fields = ('organization',)

class LedgerSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    
    class Meta:
        model = Ledger
        fields = '__all__'
        read_only_fields = ('organization',)

class ItemSerializer(serializers.ModelSerializer):
    unit_symbol = serializers.CharField(source='unit.symbol', read_only=True)
    
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ('organization',)

class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCenter
        fields = '__all__'
        read_only_fields = ('organization',)

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'
        read_only_fields = ('organization',)

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'
        read_only_fields = ('organization',)
