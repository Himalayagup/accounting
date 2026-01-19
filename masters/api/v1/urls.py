from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LedgerViewSet, AccountGroupViewSet, ItemViewSet,
    CostCenterViewSet, WarehouseViewSet, BatchViewSet
)

router = DefaultRouter()
router.register(r'ledgers', LedgerViewSet)
router.register(r'groups', AccountGroupViewSet)
router.register(r'items', ItemViewSet)
router.register(r'cost-centers', CostCenterViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'batches', BatchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
