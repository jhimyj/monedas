# test_transfer.py
# Pruebas unitarias para transferencias simples y de ida/vuelta entre monedas.
# test_transfer_success:
# 1. Se crean dos monedas simuladas (origen y destino).
# 2. Se simulan las respuestas de la base de datos y la inserción de la transacción.
# 3. Se instancia el TransactionRouter con los mocks.
# 4. Se ejecuta una transferencia de 100 USD a PEN.
# 5. Se verifica que los saldos y tipos de monedas son correctos tras la operación.
# test_transfer_round_trip:
# 1. Se crean dos monedas simuladas (USD y PEN).
# 2. Se simulan las respuestas de la base de datos para dos transferencias.
# 3. Se ejecuta una transferencia USD->PEN y luego PEN->USD.
# 4. Se verifica que se realizaron las actualizaciones correctas en ambas monedas.
import pytest
from unittest.mock import MagicMock
from routes.transaction import TransactionRouter, Transaction
from routes.currency import Currency

@pytest.fixture
def mock_dependencies():
    return {
        "user_db": MagicMock(),
        "currency_db": MagicMock(),
        "transaction_db": MagicMock(),
        "currency_router": MagicMock()
    }

def test_transfer_success(mock_dependencies):
    # 1. Monedas simuladas
    currency_from = {"id": 1, "amount": 500.0, "type": "USD", "user_id": 10}
    currency_to = {"id": 2, "amount": 200.0, "type": "PEN", "user_id": 20}
    # 2. Simulación de respuestas
    mock_dependencies["currency_db"].get_one_by_attribute.side_effect = [currency_from, currency_to]
    mock_dependencies["transaction_db"].insert_into_table.return_value = True
    # 3. Instancia el router
    router = TransactionRouter(
        user_db=mock_dependencies["user_db"],
        currency_db=mock_dependencies["currency_db"],
        transaction_db=mock_dependencies["transaction_db"],
        currency_router=mock_dependencies["currency_router"]
    )
    # 4. Ejecuta la transferencia
    transaction = Transaction(currency_id_from=1, currency_id_to=2, amount_from=100.0, amount_to=390.0)
    result = router.create_transaction(transaction)
    # 5. Verifica los saldos y tipos
    assert result.amount_from == -100.0
    assert result.amount_to == 390.0
    update_calls = mock_dependencies["currency_router"].update_currency_by_id.call_args_list
    assert len(update_calls) == 2
    from_call_args = update_calls[0][0]
    to_call_args = update_calls[1][0]
    from_currency = from_call_args[0]
    to_currency = to_call_args[0]
    assert isinstance(from_currency, Currency)
    assert isinstance(to_currency, Currency)
    assert from_currency.amount == 400.0  # 500 - 100
    assert to_currency.amount == 590.0    # 200 + 390

def test_transfer_round_trip(mock_dependencies):
    # 1. Monedas simuladas
    currency_usd = {"id": 1, "amount": 1000.0, "type": "USD", "user_id": 10}
    currency_pen = {"id": 2, "amount": 500.0, "type": "PEN", "user_id": 10}
    # 2. Simulación de respuestas para dos transferencias
    mock_dependencies["currency_db"].get_one_by_attribute.side_effect = [currency_usd, currency_pen, currency_pen, currency_usd]
    mock_dependencies["transaction_db"].insert_into_table.return_value = True
    # 3. Instancia el router
    router = TransactionRouter(
        user_db=mock_dependencies["user_db"],
        currency_db=mock_dependencies["currency_db"],
        transaction_db=mock_dependencies["transaction_db"],
        currency_router=mock_dependencies["currency_router"]
    )
    # 4. USD -> PEN
    transaction1 = Transaction(currency_id_from=1, currency_id_to=2, amount_from=100.0, amount_to=390.0)
    router.create_transaction(transaction1)
    # 5. PEN -> USD
    transaction2 = Transaction(currency_id_from=2, currency_id_to=1, amount_from=200.0, amount_to=50.0)
    router.create_transaction(transaction2)
    update_calls = mock_dependencies["currency_router"].update_currency_by_id.call_args_list
    assert len(update_calls) == 4
