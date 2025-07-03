import unittest
from unittest.mock import MagicMock
from routes.transaction import TransactionRouter, Transaction
from routes.currency import Currency
from utility.db_connector import DbConnector

class DummyCurrencyRouter:
    def update_currency_by_id(self, currency, id):
        pass

    def get_currencies_from_user(self, user_id):
        return [{"id": 1}, {"id": 2}]

class TestTransactionRouter(unittest.TestCase):

    def setUp(self):
        # Mocks
        self.user_db = MagicMock(spec=DbConnector)
        self.currency_db = MagicMock(spec=DbConnector)
        self.transaction_db = MagicMock(spec=DbConnector)
        self.currency_router = DummyCurrencyRouter()

        self.router = TransactionRouter(
            self.user_db,
            self.currency_db,
            self.transaction_db,
            self.currency_router
        )

    def test_create_transaction_valid(self):
        transaction = Transaction(currency_id_from=1, currency_id_to=2, amount_from=100, amount_to=90)

        # Mock currency existence
        self.currency_db.get_one_by_attribute.side_effect = [
            {"id": 1, "amount": 200, "user_id": 1, "type": "USD"},
            {"id": 2, "amount": 50, "user_id": 1, "type": "EUR"}
        ]

        # Mock insert success
        self.transaction_db.insert_into_table.return_value = True

        result = self.router.create_transaction(transaction)

        self.assertEqual(result.amount_from, -100)
        self.currency_db.get_one_by_attribute.assert_any_call(attribute_name="id", attribute_value=1)
        self.currency_db.get_one_by_attribute.assert_any_call(attribute_name="id", attribute_value=2)
        self.transaction_db.insert_into_table.assert_called_once()

    def test_create_transaction_invalid_amount(self):
        transaction = Transaction(currency_id_from=1, currency_id_to=2, amount_from=0, amount_to=90)
        with self.assertRaises(Exception):
            self.router.create_transaction(transaction)

    def test_create_transaction_currency_not_found(self):
        transaction = Transaction(currency_id_from=1, currency_id_to=2, amount_from=100, amount_to=90)
        self.currency_db.get_one_by_attribute.return_value = None

        with self.assertRaises(Exception):
            self.router.create_transaction(transaction)

    def test_create_transaction_insufficient_funds(self):
        transaction = Transaction(currency_id_from=1, currency_id_to=2, amount_from=100, amount_to=90)
        self.currency_db.get_one_by_attribute.side_effect = [
            {"id": 1, "amount": 50, "user_id": 1, "type": "USD"},  # No hay fondos
            {"id": 2, "amount": 50, "user_id": 1, "type": "EUR"}
        ]

        with self.assertRaises(Exception):
            self.router.create_transaction(transaction)

if __name__ == '__main__':
    unittest.main()
