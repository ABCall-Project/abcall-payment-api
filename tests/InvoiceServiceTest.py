import unittest
from unittest.mock import patch, MagicMock
from flaskr.application.invoice_service import InvoiceService
from flaskr.domain.models.invoice_detail import InvoiceDetail
from flaskr.domain.models.invoice import Invoice
import uuid
from datetime import datetime, timedelta

class TestInvoiceService(unittest.TestCase):

    def setUp(self):
        self.invoice_repository_mock = MagicMock()
        self.customer_repository_mock = MagicMock()
        self.invoice_detail_repository_mock = MagicMock()
        self.invoice_service = InvoiceService(
            repository=self.invoice_repository_mock,
            customer_repository=self.customer_repository_mock,
            invoice_detail_repository=self.invoice_detail_repository_mock
        )

    # @patch('flaskr.application.invoice_service.CustomerService.get_customer_list')
    # @patch('flaskr.application.invoice_service.IssueService.get_issues_by_customer_list')
    # @patch('flaskr.application.invoice_service.requests.post')
    # def test_generate_invoices_new_invoice(self, mock_post, mock_get_issues, mock_get_customers):
    #     # Configurar el mock de los clientes
    #     mock_get_customers.return_value = [MagicMock(id=1, plan_id='plan-1', date_suscription='2024-01-01')]
    #     # Configurar el mock del issue
    #     mock_get_issues.return_value = [MagicMock(id=uuid.uuid4(), created_at='2024-01-02')]
    #     # Configurar el mock de la creación de la factura
    #     self.invoice_repository_mock.invoice_by_month_year_by_customer.return_value = None
    #     self.customer_repository_mock.get_customer_plan_rate.return_value = 100.0
    #     self.customer_repository_mock.get_customer_plan_issue_fee.return_value = 20.0
    #     mock_post.return_value = MagicMock(status_code=200, json=lambda: {})

    #     self.invoice_service.generate_invoices()

    #     # Verificar que se haya creado una nueva factura
    #     self.invoice_repository_mock.create_invoice.assert_called_once()
    #     invoice_call_args = self.invoice_repository_mock.create_invoice.call_args[0][0]
    #     self.assertEqual(invoice_call_args.amount, 100.0)

    #     # Verificar que se hayan insertado detalles en la factura
    #     self.invoice_detail_repository_mock.create_invoice_detail.assert_called_once()

    @patch('flaskr.application.invoice_service.CustomerService.get_customer_list')
    @patch('flaskr.application.invoice_service.IssueService.get_issues_by_customer_list')
    @patch('flaskr.application.invoice_service.requests.post')
    def test_generate_invoices_existing_invoice(self, mock_post, mock_get_issues, mock_get_customers):
        # Configurar el mock de los clientes
        mock_get_customers.return_value = [MagicMock(id=1, plan_id='plan-1', date_suscription='2024-01-01')]
        # Simular que ya existe una factura
        self.invoice_repository_mock.invoice_by_month_year_by_customer.return_value = uuid.uuid4()
        
        self.invoice_service.generate_invoices()

        # Verificar que no se haya creado una nueva factura
        self.invoice_repository_mock.create_invoice.assert_not_called()

    @patch('flaskr.application.invoice_service.requests.post')
    def test_send_invoice_to_document_success(self, mock_post):
        # Simular una respuesta exitosa de la API
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {})

        invoice = Invoice(
            id=uuid.uuid4(),
            customer_id=uuid.uuid4(),
            invoice_id='I202401010000',
            plan_id='plan-1',
            amount=100.0,
            tax=0,
            total_amount=100.0,
            status='Generated',
            created_at=datetime.now(),
            start_at=datetime.now(),
            generation_date=datetime.now(),
            end_at=datetime.now() + timedelta(days=30)
        )

        result = self.invoice_service._InvoiceService__send_invoice_to_document(invoice)

        self.assertTrue(result)

    @patch('flaskr.application.invoice_service.requests.post')
    def test_send_invoice_to_document_failure(self, mock_post):
        # Simular un error de API
        mock_post.return_value = MagicMock(status_code=500)

        invoice = Invoice(
            id=uuid.uuid4(),
            customer_id=uuid.uuid4(),
            invoice_id='I202401010000',
            plan_id='plan-1',
            amount=100.0,
            tax=0,
            total_amount=100.0,
            status='Generated',
            created_at=datetime.now(),
            start_at=datetime.now(),
            generation_date=datetime.now(),
            end_at=datetime.now() + timedelta(days=30)
        )

        result = self.invoice_service._InvoiceService__send_invoice_to_document(invoice)

        self.assertFalse(result)

    def test_get_total_cost_pending(self):
        customer_id = uuid.uuid4()
        self.invoice_repository_mock.sum_total_amount_by_customer_and_status.return_value = 250.0

        total_cost = self.invoice_service.get_total_cost_pending(customer_id)

        self.assertEqual(total_cost, 250.0)

    def test_list_details_invoice_by_id(self):
        invoice_id = uuid.uuid4()
        detail_mock = [MagicMock(id=uuid.uuid4(), detail='Detail 1')]
        self.invoice_detail_repository_mock.get_by_invoice_details_by_id.return_value = detail_mock

        details = self.invoice_service.list_details_invoice_by_id(invoice_id)

        self.assertEqual(details, detail_mock)
        self.invoice_detail_repository_mock.get_by_invoice_details_by_id.assert_called_with(invoice_id)
