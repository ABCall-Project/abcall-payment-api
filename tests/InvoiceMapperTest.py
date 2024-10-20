import unittest
from datetime import datetime
from uuid import uuid4
from flaskr.infrastructure.mappers import InvoiceMapper
from flaskr.domain.models.invoice import Invoice


class TestInvoiceMapper(unittest.TestCase):
    def setUp(self):
        self.mapper = InvoiceMapper()

    def test_list_response(self):

        invoices = [
            Invoice(
                id=uuid4(),
                invoice_id="INV123",
                customer_id=uuid4(),
                plan_id=uuid4(),
                amount=100.0,
                tax=5.0,
                total_amount=105.0,
                status="PAID",
                created_at=datetime(2024, 1, 1),
                start_at=datetime(2024, 1, 1),
                generation_date=datetime(2024, 1, 1),
                end_at=datetime(2024, 2, 1),
                plan_amount=0,
                issues_amount=0
            ),
            Invoice(
                id=uuid4(),
                invoice_id="INV124",
                customer_id=uuid4(),
                plan_id=uuid4(),
                amount=200.0,
                tax=10.0,
                total_amount=210.0,
                status="PENDING",
                created_at=datetime(2024, 2, 1),
                start_at=datetime(2024, 2, 1),
                generation_date=datetime(2024, 2, 1),
                end_at=datetime(2024, 3, 1),
                plan_amount=0,
                issues_amount=0
            )
        ]


        response = self.mapper.list_response(invoices)


        self.assertEqual(len(response), 2) 


        self.assertEqual(response[0]['invoiceId'], "INV123")
        self.assertEqual(response[0]['amount'], 100.0)
        self.assertEqual(response[0]['status'], "PAID")
        self.assertEqual(response[0]['createdAt'], "2024-01-01T00:00:00")
        
        
        self.assertEqual(response[1]['invoiceId'], "INV124")
        self.assertEqual(response[1]['amount'], 200.0)
        self.assertEqual(response[1]['status'], "PENDING")
        self.assertEqual(response[1]['createdAt'], "2024-02-01T00:00:00")

