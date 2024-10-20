from typing import List, Optional
from uuid import UUID
from ..models.invoice_detail import InvoiceDetail

class InvoiceDetailRepository:

    
    def create_invoice_detail(self,invoice_detail: InvoiceDetail):
        raise NotImplementedError
    
