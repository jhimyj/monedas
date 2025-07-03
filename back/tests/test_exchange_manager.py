import unittest
from unittest.mock import Mock
from utility.exchange.exchange_manager import ExchangeManager

class TestExchangeManager(unittest.TestCase):

    def setUp(self):
        # Creamos un mock del adapter
        self.mock_adapter = Mock()
        self.mock_adapter.get_name.return_value = "FakeAdapter"
        self.mock_adapter.get_rate.return_value = 3.5

        # Configuramos el ExchangeManager con el adapter mock
        ExchangeManager.set_adapter(self.mock_adapter)

    def test_get_exchange_rate(self):
        rate = ExchangeManager.get_exchange_rate('USD', 'EUR')
        self.assertEqual(rate, 3.5)
        self.mock_adapter.get_rate.assert_called_with(from_currency='USD', to_currency='EUR')

    def test_get_current_adapter_name(self):
        name = ExchangeManager.get_current_adapter_name()
        self.assertEqual(name, "FakeAdapter")
        self.mock_adapter.get_name.assert_called_once()

if __name__ == '__main__':
    unittest.main()
