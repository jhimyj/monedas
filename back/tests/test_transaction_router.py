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

@pytest.fixture
def sample_transaction():
    return Transaction(
        currency_id_from=1,
        currency_id_to=2,
        amount_from=100.0,
        amount_to=390.0
    )

def test_create_transaction_success(mock_dependencies, sample_transaction):
    # Set up mocks
    currency_from = {"id": 1, "amount": 500.0, "type": "USD", "user_id": 10}
    currency_to = {"id": 2, "amount": 200.0, "type": "PEN", "user_id": 20}

    mock_dependencies["currency_db"].get_one_by_attribute.side_effect = [currency_from, currency_to]
    mock_dependencies["transaction_db"].insert_into_table.return_value = True

    # Instanciar el router con mocks
    router = TransactionRouter(
        user_db=mock_dependencies["user_db"],
        currency_db=mock_dependencies["currency_db"],
        transaction_db=mock_dependencies["transaction_db"],
        currency_router=mock_dependencies["currency_router"]
    )

    # Ejecutar la función
    result = router.create_transaction(sample_transaction)

    # Validaciones
    assert result.amount_from == -100.0
    assert result.amount_to == 390.0

    # Verificar que insertó la transacción
    mock_dependencies["transaction_db"].insert_into_table.assert_called_once()

    # Verificar que se actualizaron las dos monedas
    update_calls = mock_dependencies["currency_router"].update_currency_by_id.call_args_list
    assert len(update_calls) == 2

    # Revisar los valores esperados de saldo
    from_call_args = update_calls[0][0]
    to_call_args = update_calls[1][0]

    from_currency = from_call_args[0]
    to_currency = to_call_args[0]

    assert isinstance(from_currency, Currency)
    assert isinstance(to_currency, Currency)

    assert from_currency.amount == 400.0  # 500 - 100
    assert to_currency.amount == 590.0    # 200 + 390
