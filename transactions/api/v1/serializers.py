from rest_framework import serializers
from django.db import transaction
from transactions.models import Voucher, VoucherDetail
from compliance.services import GSTService
from masters.models import Ledger

class VoucherDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherDetail
        fields = '__all__'
        read_only_fields = ('voucher', 'cgst_amount', 'sgst_amount', 'igst_amount')

class VoucherSerializer(serializers.ModelSerializer):
    details = VoucherDetailSerializer(many=True)
    
    class Meta:
        model = Voucher
        fields = '__all__'
        read_only_fields = ('organization', 'voucher_number', 'status')

    def validate(self, data):
        # Validate Credit/Debit Note references
        if data.get('voucher_type') in ['DEBIT_NOTE', 'CREDIT_NOTE']:
            if not data.get('reference_number'):
                raise serializers.ValidationError("Reference Number (Original Invoice) is required for Credit/Debit Notes.")
        return data

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        
        # Auto-assign organization from context
        user = self.context['request'].user
        organization = user.memberships.first().organization
        validated_data['organization'] = organization
        
        # Generate Voucher Number (Simple logic for now)
        # In prod, this should be a robust sequence generator
        last_voucher = Voucher.objects.filter(organization=organization).order_by('-id').first()
        next_id = last_voucher.id + 1 if last_voucher else 1
        validated_data['voucher_number'] = f"VCH-{next_id:04d}"
        
        with transaction.atomic():
            voucher = Voucher.objects.create(**validated_data)
            
            # Process Details & Calculate Tax
            org_state = organization.gstin[0:2] if organization.gstin else None
            party_ledger = validated_data.get('party_ledger')
            party_state = party_ledger.state_code if party_ledger else None
            
            is_inter_state = GSTService.is_inter_state(org_state, party_state)
            
            for detail_data in details_data:
                # Calculate Tax
                amount = detail_data.get('amount', 0)
                tax_rate = detail_data.get('tax_rate', 0)
                
                tax_breakdown = GSTService.calculate_tax(amount, tax_rate, is_inter_state)
                
                VoucherDetail.objects.create(
                    voucher=voucher,
                    cgst_amount=tax_breakdown['cgst'],
                    sgst_amount=tax_breakdown['sgst'],
                    igst_amount=tax_breakdown['igst'],
                    **detail_data
                )
        
        return voucher
