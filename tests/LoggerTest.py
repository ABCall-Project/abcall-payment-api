import unittest
from unittest.mock import patch, call
from flaskr.utils.logger import Logger

class TestLogger(unittest.TestCase):

    def setUp(self):
        self.logger = Logger()

    @patch('flaskr.utils.logger.logging.info')
    def test_info(self, mock_logging_info):
        message = "This is an info message"
        obj = {"key": "value"}
        self.logger.info(message, obj)

        mock_logging_info.assert_called_once_with(message, {"key": "value", "environment": self.logger.environment_data["environment"], "appName": self.logger.environment_data["appName"]})

    @patch('flaskr.utils.logger.logging.debug')
    def test_debug(self, mock_logging_debug):
        message = "This is a debug message"
        obj = {"key": "value"}
        self.logger.debug(message, obj)

        mock_logging_debug.assert_called_once_with(message, {"key": "value", "environment": self.logger.environment_data["environment"], "appName": self.logger.environment_data["appName"]})

    @patch('flaskr.utils.logger.logging.error')
    def test_error(self, mock_logging_error):
        message = "This is an error message"
        obj = {"key": "value"}
        self.logger.error(message, obj)

        mock_logging_error.assert_called_once_with(message, {"key": "value", "environment": self.logger.environment_data["environment"], "appName": self.logger.environment_data["appName"]})

    @patch('flaskr.utils.logger.logging.exception')
    def test_exception(self, mock_logging_exception):
        message = "This is an exception message"
        obj = {"key": "value"}
        self.logger.exception(message, obj)

        mock_logging_exception.assert_called_once_with(message, {"key": "value", "environment": self.logger.environment_data["environment"], "appName": self.logger.environment_data["appName"]})

    @patch('flaskr.utils.logger.logging.warning')
    def test_warn(self, mock_logging_warning):
        message = "This is a warning message"
        obj = {"key": "value"}
        self.logger.warn(message, obj)

        mock_logging_warning.assert_called_once_with(message, {"key": "value", "environment": self.logger.environment_data["environment"], "appName": self.logger.environment_data["appName"]})
