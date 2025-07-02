from fastapi import APIRouter, HTTPException
from dataclasses import dataclass
from routes.currency import Currency, CurrencyRouter
from utility.db_connector import DbConnector

@dataclass
class Transaction:
    currency_id_from: int
    currency_id_to: int
    amount_from: float
    amount_to: float

class TransactionRouter:
    def __init__(self, user_db: DbConnector, currency_db: DbConnector, transaction_db: DbConnector, currency_router: CurrencyRouter):
        self.user_db = user_db
        self.currency_db = currency_db
        self.transaction_db = transaction_db
        self.currency_router = currency_router

        self.router = APIRouter()
        self.router.get("/transaction/{transaction_id}")(self.get_transaction_by_id)
        self.router.post("/transaction/")(self.create_transaction)
        self.router.get("/transaction/currency/{currency_id}")(self.get_transactions_from_currency)
        self.router.get("/transaction/user/{user_id}")(self.get_transactions_from_user)

    # Gets transaction by its ID
    def get_transaction_by_id(self, transaction_id: int):
        transaction = self.transaction_db.get_one_by_attribute(attribute_name="id", attribute_value=transaction_id)
        if transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction

    # Creates a transaction
    def create_transaction(self, transaction: Transaction):
        # Ambos montos deben ser positivos
        if transaction.amount_from <= 0 or transaction.amount_to <= 0:
            raise HTTPException(status_code=400, detail="Ambos montos deben ser positivos")
        # Guardar amount_from como negativo en la transacción
        transaction.amount_from = -abs(transaction.amount_from)
        
        currency_from = self.currency_db.get_one_by_attribute(attribute_name="id", attribute_value=transaction.currency_id_from)
        currency_to = self.currency_db.get_one_by_attribute(attribute_name="id", attribute_value=transaction.currency_id_to)
        
        if currency_from is None:
            raise HTTPException(status_code=404, detail=f"Currency with ID {transaction.currency_id_from} not found")
        if currency_to is None:
            raise HTTPException(status_code=404, detail=f"Currency with ID {transaction.currency_id_to} not found")

        # Validar fondos suficientes
        if currency_from["amount"] < abs(transaction.amount_from):
            raise HTTPException(status_code=400, detail=f"Currency with ID {transaction.currency_id_from} doesn't have enough funds")

        # Actualizar saldos correctamente
        nuevo_saldo_from = currency_from["amount"] + transaction.amount_from  # amount_from es negativo
        nuevo_saldo_to = currency_to["amount"] + transaction.amount_to
        currency_dataclass_from = Currency(currency_from["user_id"], nuevo_saldo_from, currency_from["type"])
        currency_dataclass_to = Currency(currency_to["user_id"], nuevo_saldo_to, currency_to["type"])
        
        result = self.transaction_db.insert_into_table(key_attribute="id", value=transaction)
        if not result:
            raise HTTPException(status_code=500, detail="Could not insert into db")
        
        try:
            self.currency_router.update_currency_by_id(currency_dataclass_from, currency_from["id"])
            self.currency_router.update_currency_by_id(currency_dataclass_to, currency_to["id"])
        except HTTPException as exception:
            raise exception
        
        return transaction

    # Gets all transactions from a currency given its ID
    def get_transactions_from_currency(self, currency_id: int):
        transactions_from = self.transaction_db.get_all_by_attribute(attribute_name="currency_id_from", attribute_value=currency_id)
        transactions_to = self.transaction_db.get_all_by_attribute(attribute_name="currency_id_to", attribute_value=currency_id)
        result = sorted(transactions_from + transactions_to, key=lambda x: x["id"])
        return result

    # Gets all transactions from a user given their ID
    def get_transactions_from_user(self, user_id: int):
        currencies = self.currency_router.get_currencies_from_user(user_id)

        result = []
        for currency in currencies:
            current = self.get_transactions_from_currency(currency["id"])
            result = result + current
        result = sorted(result, key=lambda x: x["id"])
        return result