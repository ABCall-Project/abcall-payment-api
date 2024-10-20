import unittest
from unittest.mock import patch, MagicMock
from flaskr.application.issues_service import IssueService
from flaskr.domain.models.issue import Issue

class TestIssueService(unittest.TestCase):

    def setUp(self):
        self.service = IssueService()

    @patch('flaskr.application.issues_service.requests.get')
    def test_get_issues_by_customer_list_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'id': 1,
                'auth_user_id': 1001,
                'auth_user_agent_id': 2001,
                'status': 'open',
                'subject': 'Issue 1',
                'description': 'Issue description 1',
                'created_at': '2024-01-01T10:00:00',
                'closed_at': None,
                'channel_plan_id': 301
            },
            {
                'id': 2,
                'auth_user_id': 1002,
                'auth_user_agent_id': 2002,
                'status': 'closed',
                'subject': 'Issue 2',
                'description': 'Issue description 2',
                'created_at': '2024-01-02T11:00:00',
                'closed_at': '2024-01-03T12:00:00',
                'channel_plan_id': 302
            }
        ]
        mock_get.return_value = mock_response

        issues = self.service.get_issues_by_customer_list('customer-id-123', 2024, 1)

        self.assertEqual(len(issues), 2)
        self.assertEqual(issues[0].subject, 'Issue 1')
        self.assertEqual(issues[1].status, 'closed')

    @patch('flaskr.application.issues_service.requests.get')
    def test_get_issues_by_customer_list_no_data(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        issues = self.service.get_issues_by_customer_list('customer-id-123', 2024, 1)

        self.assertIsNone(issues)

    @patch('flaskr.application.issues_service.requests.get')
    def test_get_issues_by_customer_list_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        issues = self.service.get_issues_by_customer_list('customer-id-123', 2024, 1)

        self.assertIsNone(issues)

    @patch('flaskr.application.issues_service.requests.get')
    def test_get_issues_by_customer_list_exception(self, mock_get):
        mock_get.side_effect = Exception("API Error")

        issues = self.service.get_issues_by_customer_list('customer-id-123', 2024, 1)

        self.assertIsNone(issues)


