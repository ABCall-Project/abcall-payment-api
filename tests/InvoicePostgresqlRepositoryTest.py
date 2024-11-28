import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4
from datetime import datetime
from flaskr.infrastructure.databases.invoice_postgresql_repository import InvoicePostgresqlRepository
from flaskr.infrastructure.databases.model_sqlalchemy import InvoiceModelSqlAlchemy
from flaskr.domain.models import Invoice


class TestInvoicePostgresqlRepository(unittest.TestCase):

    def setUp(self):
        self.repo = InvoicePostgresqlRepository()
        self.session_mock = patch('flaskr.infrastructure.databases.postgres.db.Session').start()
        self.addCleanup(patch.stopall)

    def test_list_by_consumer_id(self):
        # Mock data
        customer_id = uuid4()
        mock_invoices = [
            InvoiceModelSqlAlchemy(
                id=uuid4(),
                customer_id=customer_id,
                invoice_id=uuid4(),
                amount=100.0,
                tax=10.0,
                total_amount=110.0,
                status="PAID",
                created_at=datetime.utcnow()
            )
        ]

        session = self.session_mock()
        session.query().filter_by().all.return_value = mock_invoices

        result = self.repo.list_by_consumer_id(customer_id)

        self.assertEqual(len(result), len(mock_invoices))
        self.assertEqual(result[0].customer_id, customer_id)

    def test_list(self):
        # Mock data
        mock_invoices = [
            InvoiceModelSqlAlchemy(
                id=uuid4(),
                customer_id=uuid4(),
                invoice_id=uuid4(),
                amount=100.0,
                tax=10.0,
                total_amount=110.0,
                status="PAID",
                created_at=datetime.utcnow()
            ),
            InvoiceModelSqlAlchemy(
                id=uuid4(),
                customer_id=uuid4(),
                invoice_id=uuid4(),
                amount=200.0,
                tax=20.0,
                total_amount=220.0,
                status="UNPAID",
                created_at=datetime.utcnow()
            )
        ]

        session = self.session_mock()
        session.query().all.return_value = mock_invoices

        result = self.repo.list()

        self.assertEqual(len(result), len(mock_invoices))
        self.assertEqual(result[0].amount, mock_invoices[0].amount)

    def test_invoice_by_month_year_by_customer(self):
        # Mock data
        year = 2024
        month = 1
        customer_id = uuid4()
        invoice_id = uuid4()

        session = self.session_mock()
        session.query().filter().filter().filter().first.return_value = (invoice_id,)

        result = self.repo.invoice_by_month_year_by_customer(year, month, customer_id)

        self.assertEqual(result, invoice_id)

    def test_get_invoice_by_id(self):
        # Mock data
        invoice_id = uuid4()
        mock_invoice = InvoiceModelSqlAlchemy(
            id=invoice_id,
            customer_id=uuid4(),
            invoice_id=uuid4(),
            amount=150.0,
            tax=15.0,
            total_amount=165.0,
            status="PAID",
            created_at=datetime.utcnow()
        )

        session = self.session_mock()
        session.query().filter_by().first.return_value = mock_invoice

        result = self.repo.get_invoice_by_id(invoice_id)

        self.assertEqual(result.id, mock_invoice.id)
        self.assertEqual(result.amount, mock_invoice.amount)

    def test_create_invoice(self):
        # Mock data
        invoice = Invoice(
            id=uuid4(),
            customer_id=uuid4(),
            invoice_id=uuid4(),
            amount=200.0,
            tax=20.0,
            total_amount=220.0,
            status="UNPAID",
            created_at=datetime.utcnow()
        )

        session = self.session_mock()
        session.add.return_value = None

        self.repo.create_invoice(invoice)

        session.add.assert_called_once()

    def test_update_invoice(self):
        # Mock data
        invoice = Invoice(
            id=uuid4(),
            customer_id=uuid4(),
            invoice_id=uuid4(),
            amount=250.0,
            tax=25.0,
            total_amount=275.0,
            status="PAID",
            created_at=datetime.utcnow()
        )

        session = self.session_mock()
        session.query().filter_by().update.return_value = None

        self.repo.update_invoice(invoice)

        session.query().filter_by().update.assert_called_once()

    def test_sum_total_amount_by_customer_and_status(self):
        # Mock data
        customer_id = uuid4()
        status = "PAID"
        total_amount = 500.0

        session = self.session_mock()
        session.query().filter().filter().scalar.return_value = total_amount

        result = self.repo.sum_total_amount_by_customer_and_status(customer_id, status)

        self.assertEqual(result, total_amount)

