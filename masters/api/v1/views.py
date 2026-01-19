from rest_framework import viewsets, permissions, filters
from masters.models import Ledger, AccountGroup, Item, Unit, CostCenter, Warehouse, Batch
from .serializers import (
    LedgerSerializer, AccountGroupSerializer, ItemSerializer,
    CostCenterSerializer, WarehouseSerializer, BatchSerializer
)

class BaseOrgViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        # Filter by user's organization(s)
        # Assuming user has one active org or we filter by all orgs they belong to
        # For simplicity, we'll filter by organizations the user is a member of
        return self.model.objects.filter(organization__members__user=self.request.user).distinct()

    def perform_create(self, serializer):
        # Auto-assign organization (taking the first one for now, or from context)
        org_id = self.request.data.get('organization')
        if org_id:
            serializer.save() 
        else:
            # Fallback: Use the first org the user owns/is part of
            if not self.request.user.is_authenticated:
                 raise serializers.ValidationError("Authentication required.")

            # Try memberships first
            membership = self.request.user.memberships.first()
            if membership:
                serializer.save(organization=membership.organization)
                return

            # Try owned organizations
            org = self.request.user.owned_organizations.first()
            if org:
                serializer.save(organization=org)
                return
            
            raise serializers.ValidationError("User does not belong to any organization.")

class LedgerViewSet(BaseOrgViewSet):
    model = Ledger
    queryset = Ledger.objects.none() # Overridden by get_queryset
    serializer_class = LedgerSerializer
    search_fields = ['name', 'mobile', 'email']

class ItemViewSet(BaseOrgViewSet):
    model = Item
    queryset = Item.objects.none()
    serializer_class = ItemSerializer
    search_fields = ['name', 'sku', 'barcode']

class AccountGroupViewSet(BaseOrgViewSet):
    model = AccountGroup
    queryset = AccountGroup.objects.none()
    serializer_class = AccountGroupSerializer

class CostCenterViewSet(BaseOrgViewSet):
    model = CostCenter
    queryset = CostCenter.objects.none()
    serializer_class = CostCenterSerializer

class WarehouseViewSet(BaseOrgViewSet):
    model = Warehouse
    queryset = Warehouse.objects.none()
    serializer_class = WarehouseSerializer

class BatchViewSet(BaseOrgViewSet):
    model = Batch
    queryset = Batch.objects.none()
    serializer_class = BatchSerializer
