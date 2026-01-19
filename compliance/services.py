from decimal import Decimal

class GSTService:
    @staticmethod
    def calculate_tax(amount, tax_rate, is_inter_state):
        """
        Calculates CGST/SGST or IGST based on state.
        amount: Base amount
        tax_rate: Percentage (e.g., 18.00)
        is_inter_state: Boolean
        """
        amount = Decimal(str(amount))
        tax_rate = Decimal(str(tax_rate))
        
        tax_amount = (amount * tax_rate) / 100
        
        if is_inter_state:
            return {
                'cgst': Decimal('0.00'),
                'sgst': Decimal('0.00'),
                'igst': tax_amount
            }
        else:
            half_tax = tax_amount / 2
            return {
                'cgst': half_tax,
                'sgst': half_tax,
                'igst': Decimal('0.00')
            }

    @staticmethod
    def is_inter_state(org_state_code, party_state_code):
        if not org_state_code or not party_state_code:
            return False # Default to Intra-state if unknown
        return org_state_code != party_state_code
