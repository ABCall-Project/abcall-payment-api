from typing import List
import json
from ...domain.models import Invoice

class InvoiceMapper:
    def list_response(self, invoices: List[Invoice]):
        invoices_dict = [self._to_dict(invoice) for invoice in invoices]
        return json.loads(json.dumps(invoices_dict))

    def _to_dict(self, invoice:Invoice):
        return {
            'id': str(invoice.id),
            'invoiceId': str(invoice.invoice_id),
            'customerId': str(invoice.customer_id),
            'planId': str(invoice.plan_id) if str(invoice.plan_id) else None,
            'amount': float(invoice.amount),
            'tax': float(invoice.tax),
            'totalAmount': float(invoice.total_amount),
            'status': str(invoice.status),
            'createdAt': invoice.created_at.isoformat(),
            'startAt': invoice.start_at.isoformat(),
            'generationDate': invoice.generation_date.isoformat(),
            'endAt': invoice.end_at.isoformat(),
            'plan_amount':float(invoice.plan_amount),
            'issues_amount':float(invoice.issues_amount)
        }