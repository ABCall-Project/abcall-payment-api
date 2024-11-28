import unittest
from unittest.mock import MagicMock, patch
from uuid import uuid4
from datetime import datetime
from flaskr.infrastructure.databases.invoice_detail_postgresql_repository import InvoiceDetailPostgresqlRepository
from flaskr.infrastructure.databases.model_sqlalchemy import InvoiceDetailModelSqlAlchemy
from flaskr.domain.models import InvoiceDetail


class TestInvoiceDetailPostgresqlRepository(unittest.TestCase):

    def setUp(self):
        self.repo = InvoiceDetailPostgresqlRepository()
        self.session_mock = patch('flaskr.infrastructure.databases.postgres.db.Session').start()
        self.addCleanup(patch.stopall)

    

    def test_get_factured_issue_ids(self):
        # Mock data
        mock_issue_ids = [(uuid4(),), (uuid4(),)]
        session = self.session_mock()
        session.query().filter().distinct().all.return_value = mock_issue_ids

        result = self.repo.get_factured_issue_ids()

        self.assertEqual(len(result), 0)


    def test_get_by_invoice_details_by_id(self):
        # Mock data
        invoice_id = str(uuid4())
        mock_details = [
            InvoiceDetailModelSqlAlchemy(
                id=uuid4(),
                detail="Detail 1",
                amount=50.0,
                tax=5.0,
                total_amount=55.0,
                issue_id=uuid4(),
                chanel_plan_id=uuid4(),
                invoice_id=invoice_id,
                issue_date=datetime.utcnow()
            ),
            InvoiceDetailModelSqlAlchemy(
                id=uuid4(),
                detail="Detail 2",
                amount=70.0,
                tax=7.0,
                total_amount=77.0,
                issue_id=uuid4(),
                chanel_plan_id=uuid4(),
                invoice_id=invoice_id,
                issue_date=datetime.utcnow()
            )
        ]

        session = self.session_mock()
        session.query().filter_by().all.return_value = mock_details

        result = self.repo.get_by_invoice_details_by_id(invoice_id)

        self.assertEqual(len(result), 0)


    def test_get_total_amount_by_invoice_id(self):
        # Mock data
        invoice_id = uuid4()
        total_amount = 120.0

        session = self.session_mock()
        session.query().filter_by().scalar.return_value = total_amount

        result = self.repo.get_total_amount_by_invoice_id(invoice_id)

        self.assertEqual(0)

    def test_get_total_amount_by_invoice_id_zero(self):
        # Mock data
        invoice_id = uuid4()

        session = self.session_mock()
        session.query().filter_by().scalar.return_value = None

        result = self.repo.get_total_amount_by_invoice_id(invoice_id)

        self.assertEqual(result, 0)
