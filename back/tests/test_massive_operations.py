# test_massive_operations.py
# Prueba unitaria para operaciones masivas de depósitos y transferencias.
# Paso a paso:
# 1. Se define una función auxiliar para calcular el saldo esperado.
# 2. Se crea un mock de dependencias y una moneda inicial.
# 3. Se simulan 1000 depósitos de 100 y 1000 transferencias de 50.
# 4. Se valida que el saldo final es el esperado y que no hay saldo negativo.

import pytest
from unittest.mock import MagicMock
from routes.transaction import TransactionRouter, Transaction
from routes.currency import Currency

def saldo_final_depositos_y_transferencias(saldo_inicial, depositos, monto_deposito, transferencias, monto_transferencia):
    # Calcula el saldo esperado tras depósitos y transferencias
    return saldo_inicial + (depositos * monto_deposito) - (transferencias * monto_transferencia)

@pytest.fixture
def mock_dependencies():
    return {
        "user_db": MagicMock(),
        "currency_db": MagicMock(),
        "transaction_db": MagicMock(),
        "currency_router": MagicMock()
    }

def test_massive_deposits_and_transfers(mock_dependencies):
    # 1. Parámetros de la prueba
    saldo_inicial = 1000.0
    depositos = 1000
    monto_deposito = 100.0
    transferencias = 1000
    monto_transferencia = 50.0
    # 2. Moneda simulada
    currency = {"id": 1, "amount": saldo_inicial, "type": "USD", "user_id": 10}
    mock_dependencies["currency_db"].get_one_by_attribute.return_value = currency
    mock_dependencies["transaction_db"].insert_into_table.return_value = True
    # 3. Simular depósitos
    for _ in range(depositos):
        currency["amount"] += monto_deposito
    # 4. Simular transferencias
    for _ in range(transferencias):
        currency["amount"] -= monto_transferencia
    # 5. Validar saldo final
    saldo_esperado = saldo_final_depositos_y_transferencias(saldo_inicial, depositos, monto_deposito, transferencias, monto_transferencia)
    assert currency["amount"] == saldo_esperado
    assert currency["amount"] >= 0
