from fastapi import APIRouter, HTTPException
from dataclasses import dataclass
from utility.db_connector import DbConnector

router = APIRouter()

@dataclass
class Transaction:
    currency_id_from: int
    currency_id_to: int
    amount_from: float
    amount_to: float

transaction_db = DbConnector(path="db/transaction.json", key_attribute="id")

# Gets transaction by its ID
@router.get("/transaction/{transaction_id}")
def get_transaction_by_id(transaction_id: int):
    transaction = transaction_db.get_one_by_attribute(attribute_name="id", attribute_value=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

# Creates a transaction
@router.post("/transaction/")
def create_transaction(transaction: Transaction):
    if transaction.amount_from >= 0:
        raise HTTPException(status_code=400, detail="Invalid amount in transaction 'from'! Value must be negative")
    if transaction.amount_to <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount in transaction 'to'! Value must be positive")

    # lazy loading the currency db and methods
    from routes.currency import currency_db, Currency, update_currency_by_id
    
    currency_from = currency_db.get_one_by_attribute(attribute_name="id", attribute_value=transaction.currency_id_from)
    currency_to = currency_db.get_one_by_attribute(attribute_name="id", attribute_value=transaction.currency_id_to)
    
    if currency_from is None:
        raise HTTPException(status_code=404, detail=f"Currency with ID {transaction.currency_id_from} not found")
    if currency_to is None:
        raise HTTPException(status_code=404, detail=f"Currency with ID {transaction.currency_id_to} not found")

    # check if possible to reduce amount in currency from
    if currency_from["amount"] + transaction.amount_from < 0:
        raise HTTPException(status_code=400, detail=f"Currency with ID {transaction.currency_id_from} doesn't have enough funds")

    # create dataclasses with modified amounts
    currency_dataclass_from = Currency(currency_from["user_id"], currency_from["amount"] + transaction.amount_from, currency_from["type"])
    currency_dataclass_to = Currency(currency_to["user_id"], currency_to["amount"] + transaction.amount_to, currency_to["type"])
    
    result = transaction_db.insert_into_table(key_attribute="id", value=transaction)
    if not result:
        raise HTTPException(status_code=500, detail="Could not insert into db")
    
    try:
        update_currency_by_id(currency_dataclass_from, currency_from["id"])
        update_currency_by_id(currency_dataclass_to, currency_to["id"])
    except HTTPException as exception:
        raise exception
    
    return transaction

# Gets all transactions from a currency given its ID
@router.get("/transaction/currency/{currency_id}")
def get_transactions_from_currency(currency_id: int):
    transactions_from = transaction_db.get_all_by_attribute(attribute_name="currency_id_from", attribute_value=currency_id)
    transactions_to = transaction_db.get_all_by_attribute(attribute_name="currency_id_to", attribute_value=currency_id)
    result = sorted(transactions_from + transactions_to, key=lambda x: x["id"])
    return result

# Gets all transactions from a user given their ID
@router.get("/transaction/user/{user_id}")
def get_transactions_from_user(user_id: int):
    # lazy loading a currency method
    from routes.currency import get_currencies_from_user
    currencies = get_currencies_from_user(user_id)

    result = []
    for currency in currencies:
        current = get_transactions_from_currency(currency["id"])
        result = result + current
    result = sorted(result, key=lambda x: x["id"])
    return result