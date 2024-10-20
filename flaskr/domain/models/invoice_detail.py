from uuid import UUID
from typing import Optional
from datetime import datetime

class InvoiceDetail:
    def __init__(self, id: UUID, detail: str, invoice_id: UUID, issue_id: Optional[UUID], amount: float, tax: float,
                 total_amount: float, chanel_plan_id: UUID,issue_date:datetime=None):
        self.id = id
        self.detail=detail
        self.amount=amount
        self.tax=tax
        self.total_amount=total_amount
        self.issue_id=issue_id
        self.chanel_plan_id=chanel_plan_id
        self.invoice_id=invoice_id
        self.issue_date=issue_date

    def to_dict(self):
        return {
            'id': str(self.id),
            'detail': str(self.detail),
            'amount': str(self.amount),
            'tax': str(self.tax),
            'total_amount': str(self.total_amount),
            'issue_id': str(self.issue_id),
            'chanel_plan_id': str(self.chanel_plan_id),
            'invoice_id': str(self.invoice_id),
            'issue_date': self.issue_date.isoformat() if self.issue_date else None
        }