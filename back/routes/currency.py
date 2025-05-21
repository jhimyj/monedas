from fastapi import APIRouter, HTTPException
from dataclasses import dataclass
from utility.db_connector import DbConnector

router = APIRouter()

SUPPORTED_CURRENCIES = ["PEN", "USD"]

@dataclass
class Currency:
    id: int
    user_id: int
    amount: float
    type: str

currency_db = DbConnector("db/currency.json")

@router.get("/currency/{user_id}")
def get_user(user_id: int):
    currency = currency_db.get_one_by_attribute("id", user_id)
    if currency is None:
        raise HTTPException(status_code=404, detail="Currency not found")
    return currency

@router.post("/currency/")
def create_or_update_currency(currency: Currency):
    if currency.type not in SUPPORTED_CURRENCIES:
        raise HTTPException(status_code=400, detail=f"Currency of type {currency.type} currently not supported")
    # get current currency
    current_currency = currency_db.get_one_by_attribute("id", currency.id)
    # if doesnt already exists, insert it
    if current_currency is None:
        result = currency_db.insert_into_table(currency)
        if not result:
            raise HTTPException(status_code=500, detail="Could not insert into db")
        return currency
    # else, update it
    else:
        if current_currency["user_id"] != currency.user_id:
            raise HTTPException(status_code=400, detail="Mismatch in foreign key user_id")
        result = currency_db.update_one_by_attribute(currency, "id", currency.id)
        if not result:
            raise HTTPException(status_code=500, detail="Could not update db item")
        return currency