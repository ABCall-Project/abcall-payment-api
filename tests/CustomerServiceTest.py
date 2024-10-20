import unittest
from unittest.mock import patch, MagicMock
from flaskr.application.customer_service import CustomerService
from flaskr.domain.models.customer import Customer

class TestCustomerService(unittest.TestCase):

    def setUp(self):
        self.service = CustomerService()

    @patch('flaskr.application.customer_service.requests.get')
    def test_get_customer_list_success(self, mock_get):
        # Simular una respuesta exitosa de la API con datos de clientes
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'id': 1,
                'name': 'John Doe',
                'plan_id': 101,
                'date_suscription': '2024-01-01'
            },
            {
                'id': 2,
                'name': 'Jane Smith',
                'plan_id': 102,
                'date_suscription': '2024-01-05'
            }
        ]
        mock_get.return_value = mock_response

        customers = self.service.get_customer_list()

        # Verificar que se devuelven dos objetos Customer
        self.assertEqual(len(customers), 2)
        self.assertEqual(customers[0].name, 'John Doe')
        self.assertEqual(customers[1].name, 'Jane Smith')

    @patch('flaskr.application.customer_service.requests.get')
    def test_get_customer_list_no_data(self, mock_get):
        # Simular una respuesta exitosa pero sin datos de clientes
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        customers = self.service.get_customer_list()

        # Verificar que se devuelve None cuando no hay clientes
        self.assertIsNone(customers)

    @patch('flaskr.application.customer_service.requests.get')
    def test_get_customer_list_error(self, mock_get):
        # Simular un error en la llamada a la API
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        customers = self.service.get_customer_list()

        # Verificar que se devuelve None cuando hay un error en la API
        self.assertIsNone(customers)

    @patch('flaskr.application.customer_service.requests.get')
    def test_get_customer_plan_rate_success(self, mock_get):
        # Simular una respuesta exitosa con la tasa del plan del cliente
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'basic_monthly_rate': 100.0
        }
        mock_get.return_value = mock_response

        rate = self.service.get_customer_plan_rate(1)

        # Verificar que se devuelve la tasa correcta
        self.assertEqual(rate, 100.0)

    @patch('flaskr.application.customer_service.requests.get')
    def test_get_customer_plan_rate_error(self, mock_get):
        # Simular un error en la llamada a la API
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        rate = self.service.get_customer_plan_rate(1)

        # Verificar que se devuelve None cuando hay un error en la API
        self.assertIsNone(rate)

    @patch('flaskr.application.customer_service.requests.get')
    def test_get_customer_plan_issue_fee_success(self, mock_get):
        # Simular una respuesta exitosa con la tarifa de emisión del cliente
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'issue_fee': 50.0
        }
        mock_get.return_value = mock_response

        fee = self.service.get_customer_plan_issue_fee(1)

        # Verificar que se devuelve la tarifa correcta
        self.assertEqual(fee, 50.0)

    @patch('flaskr.application.customer_service.requests.get')
    def test_get_customer_plan_issue_fee_error(self, mock_get):
        # Simular un error en la llamada a la API
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        fee = self.service.get_customer_plan_issue_fee(1)

        # Verificar que se devuelve None cuando hay un error en la API
        self.assertIsNone(fee)