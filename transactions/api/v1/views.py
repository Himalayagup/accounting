from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from transactions.models import Voucher
from .serializers import VoucherSerializer

class VoucherViewSet(viewsets.ModelViewSet):
    serializer_class = VoucherSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['voucher_number', 'party_ledger__name']

    def get_queryset(self):
        return Voucher.objects.filter(organization__members__user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        voucher = self.get_object()
        if voucher.status == 'CANCELLED':
            return Response({'error': 'Voucher is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Logic to reverse inventory/accounting effects would go here
        
        voucher.status = 'CANCELLED'
        voucher.save()
        return Response({'status': 'Voucher cancelled successfully'})

    @action(detail=True, methods=['get'])
    def generate_pdf(self, request, pk=None):
        voucher = self.get_object()
        # Placeholder for PDF generation
        # In real implementation, use WeasyPrint to render an HTML template to PDF
        return Response({'message': f'PDF generation for {voucher.voucher_number} not implemented yet.'})
