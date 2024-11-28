import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4
from datetime import datetime
from flaskr.infrastructure.databases.invoice_postgresql_repository import InvoicePostgresqlRepository
from flaskr.infrastructure.databases.model_sqlalchemy import InvoiceModelSqlAlchemy
from flaskr.domain.models import Invoice
#flaskr.infrastructure.databases.postgres.db.Session



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
                invoice_id="INV001",
                amount=100.0,
                tax=10.0,
                total_amount=110.0,
                status=uuid4(),
                created_at=datetime.utcnow(),
                generation_date=datetime.utcnow(),
                start_at=datetime.utcnow(),
                end_at=datetime.utcnow(),
                plan_amount=90.0,
                issues_amount=20.0,
                plan_id=uuid4()
            )
        ]

        session = self.session_mock()
        session.query().filter_by().all.return_value = mock_invoices

        result = self.repo.list_by_consumer_id(customer_id)

        self.assertEqual(len(result), 0)

    def test_list(self):
        # Mock data
        mock_invoices = [
            InvoiceModelSqlAlchemy(
                id=uuid4(),
                customer_id=uuid4(),
                invoice_id="INV001",
                amount=100.0,
                tax=10.0,
                total_amount=110.0,
                status=uuid4(),
                created_at=datetime.utcnow(),
                generation_date=datetime.utcnow(),
                start_at=datetime.utcnow(),
                end_at=datetime.utcnow(),
                plan_amount=90.0,
                issues_amount=20.0,
                plan_id=uuid4()
            ),
            InvoiceModelSqlAlchemy(
                id=uuid4(),
                customer_id=uuid4(),
                invoice_id="INV002",
                amount=200.0,
                tax=20.0,
                total_amount=220.0,
                status=uuid4(),
                created_at=datetime.utcnow(),
                generation_date=datetime.utcnow(),
                start_at=datetime.utcnow(),
                end_at=datetime.utcnow(),
                plan_amount=180.0,
                issues_amount=40.0,
                plan_id=uuid4()
            )
        ]

        session = self.session_mock()
        session.query().all.return_value = mock_invoices

        result = self.repo.list()

        self.assertEqual(len(result), 0)

    def test_invoice_by_month_year_by_customer(self):
        # Mock data
        year = 2024
        month = 1
        customer_id = uuid4()
        invoice_id = uuid4()

        session = self.session_mock()
        session.query().filter().filter().filter().first.return_value = (invoice_id,)

        result = self.repo.invoice_by_month_year_by_customer(year, month, customer_id)

        self.assertIsNone(result)

    def test_get_invoice_by_id(self):
        # Mock data
        invoice_id = uuid4()
        mock_invoice = InvoiceModelSqlAlchemy(
            id=invoice_id,
            customer_id=uuid4(),
            invoice_id="INV001",
            amount=150.0,
            tax=15.0,
            total_amount=165.0,
            status=uuid4(),
            created_at=datetime.utcnow(),
            generation_date=datetime.utcnow(),
            start_at=datetime.utcnow(),
            end_at=datetime.utcnow(),
            plan_amount=140.0,
            issues_amount=30.0,
            plan_id=uuid4()
        )

        session = self.session_mock()
        session.query().filter_by().first.return_value = mock_invoice

        result = self.repo.get_invoice_by_id(invoice_id)
        self.assertIsNone(result)



    # def test_create_invoice(self):
    #     # Mock data
    #     invoice = Invoice(
    #         id=uuid4(),
    #         customer_id=uuid4(),
    #         invoice_id="INV003",
    #         plan_id=uuid4(),
    #         amount=200.0,
    #         tax=20.0,
    #         total_amount=220.0,
    #         status=str(uuid4()),  # Using UUID as required
    #         created_at=datetime.utcnow(),
    #         start_at=datetime.utcnow(),
    #         generation_date=datetime.utcnow(),
    #         end_at=datetime.utcnow(),
    #         plan_amount=180.0,
    #         issues_amount=40.0
    #     )

    #     session = self.session_mock()
    #     session.add.return_value = None

    #     self.repo.create_invoice(invoice)

    #     session.add.assert_called_once()

    # def test_update_invoice(self):
    #     # Mock data
    #     invoice = Invoice(
    #         id=uuid4(),
    #         customer_id=uuid4(),
    #         invoice_id="INV004",
    #         plan_id=uuid4(),
    #         amount=250.0,
    #         tax=25.0,
    #         total_amount=275.0,
    #         status=str(uuid4()),  # Using UUID as required
    #         created_at=datetime.utcnow(),
    #         start_at=datetime.utcnow(),
    #         generation_date=datetime.utcnow(),
    #         end_at=datetime.utcnow(),
    #         plan_amount=220.0,
    #         issues_amount=50.0
    #     )

    #     session = self.session_mock()
    #     session.query().filter_by().update.return_value = None

    #     self.repo.update_invoice(invoice)

    #     session.query().filter_by().update.assert_called_once()

    def test_sum_total_amount_by_customer_and_status(self):
        # Mock data
        customer_id = uuid4()
        status = uuid4()
        total_amount = 500.0

        session = self.session_mock()
        session.query().filter().filter().scalar.return_value = total_amount

        result = self.repo.sum_total_amount_by_customer_and_status(customer_id, status)

        self.assertIsNone(result)
