import unittest
from unittest.mock import patch, MagicMock
from utility.exchange.adapter.frankfurter_exchange_adapter import FrankfurterExchangeAdapter

class TestFrankfurterExchangeAdapter(unittest.TestCase):

    @patch('utility.exchange.adapter.frankfurter_exchange_adapter.requests.get')
    def test_init_fetches_available_currencies(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"USD": "US Dollar", "EUR": "Euro"}
        mock_get.return_value = mock_response

        adapter = FrankfurterExchangeAdapter()
        self.assertIn("USD", adapter.available_currencies)
        self.assertIn("EUR", adapter.available_currencies)

    @patch('utility.exchange.adapter.frankfurter_exchange_adapter.requests.get')
    def test_get_rate_success(self, mock_get):
        currencies_response = MagicMock()
        currencies_response.status_code = 200
        currencies_response.json.return_value = {"USD": "US Dollar", "EUR": "Euro"}
        
        rate_response = MagicMock()
        rate_response.status_code = 200
        rate_response.json.return_value = {"rates": {"EUR": 0.92}}

        mock_get.side_effect = [currencies_response, rate_response]

        adapter = FrankfurterExchangeAdapter()
        rate = adapter.get_rate("USD", "EUR")

        self.assertEqual(rate, 0.92)
        self.assertTrue(mock_get.called)
        self.assertEqual(mock_get.call_count, 2)

    @patch('utility.exchange.adapter.frankfurter_exchange_adapter.requests.get')
    def test_get_name(self, mock_get):
        currencies_response = MagicMock()
        currencies_response.status_code = 200
        currencies_response.json.return_value = {"USD": "US Dollar"}
        mock_get.return_value = currencies_response

        adapter = FrankfurterExchangeAdapter()
        self.assertEqual(adapter.get_name(), "frankfurter")

if __name__ == '__main__':
    unittest.main()
