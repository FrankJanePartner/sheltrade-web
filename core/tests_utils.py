import unittest
from unittest.mock import patch, MagicMock
from core.utils import ExchangeRate

class TestExchangeRate(unittest.TestCase):
    def setUp(self):
        self.exchange = ExchangeRate()

    @patch('core.utils.Session.get')
    def test_get_price_success(self, mock_get):
        # Mock a successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {'conversion_rate': 1.23}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = self.exchange.get_price('USD', 'NGN')
        self.assertIn('conversion_rate', result)
        self.assertEqual(result['conversion_rate'], 1.23)

    @patch('core.utils.Session.get')
    def test_get_price_timeout(self, mock_get):
        # Mock a timeout exception
        mock_get.side_effect = Exception('API request timed out')

        result = self.exchange.get_price('USD', 'NGN')
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'API request timed out')

    @patch('core.utils.Session.get')
    def test_get_price_request_exception(self, mock_get):
        # Mock a generic request exception
        mock_get.side_effect = Exception('Some error')

        result = self.exchange.get_price('USD', 'NGN')
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Some error')

if __name__ == '__main__':
    unittest.main()
