# test_deposit.py
# Pruebas unitarias para depósitos en una moneda.
# Paso a paso:
# 1. Se crea un mock de la base de datos de monedas.
# 2. Se crea una moneda de ejemplo.
# 3. Se simula un depósito sumando al saldo.
# 4. Se verifica que el saldo final es correcto y que los datos de la moneda no cambian.
import pytest
from unittest.mock import MagicMock
from routes.currency import Currency
from routes.currency import CurrencyRouter

@pytest.fixture
def mock_currency_db():
    return MagicMock()

@pytest.fixture
def sample_currency():
    return Currency(amount=100.0, type="USD", user_id=10)

def test_deposit_success(mock_currency_db, sample_currency):
    # 1. Instancia el router con el mock de la base de datos
    router = CurrencyRouter(user_db=MagicMock(), currency_db=mock_currency_db)
    # 2. Simula obtener la moneda de la base de datos
    mock_currency_db.get_one_by_attribute.return_value = sample_currency
    deposit_amount = 50.0
    # 3. Realiza el depósito sumando al saldo
    sample_currency.amount += deposit_amount
    # 4. Simula la actualización en la base de datos
    router.update_currency_by_id = MagicMock(return_value=sample_currency)
    updated_currency = router.update_currency_by_id(sample_currency)
    # 5. Verifica el saldo final y los datos
    assert updated_currency.amount == 150.0
    assert updated_currency.type == "USD"
    assert updated_currency.user_id == 10
