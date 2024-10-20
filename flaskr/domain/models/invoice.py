from uuid import UUID
from typing import Optional
from datetime import datetime

class Invoice:
    def __init__(self, id: UUID, customer_id: UUID, invoice_id: str, plan_id: Optional[UUID], amount: float, tax: float,
                 total_amount: float, status: str,
                 created_at: datetime, start_at: datetime, generation_date: datetime, end_at: datetime, plan_amount:float, issues_amount:float):
        self.id = id
        self.customer_id = customer_id
        self.invoice_id = invoice_id
        self.plan_id = plan_id
        self.amount = amount
        self.tax = tax
        self.total_amount = total_amount
        self.status = status
        self.created_at = created_at
        self.start_at = start_at
        self.generation_date = generation_date
        self.end_at = end_at
        self.plan_amount=plan_amount
        self.issues_amount=issues_amount

