from fastapi import APIRouter, HTTPException
from dataclasses import dataclass
from utility.db_connector import DbConnector

router = APIRouter()

SUPPORTED_CURRENCIES = ["PEN", "USD"]

@dataclass
class Currency:
    user_id: int
    amount: float
    type: str

currency_db = DbConnector(path="db/currency.json", key_attribute="id")

# Gets currency by its ID
@router.get("/currency/{currency_id}")
def get_currency_by_id(currency_id: int):
    currency = currency_db.get_one_by_attribute(attribute_name="id", attribute_value=currency_id)
    if currency is None:
        raise HTTPException(status_code=404, detail="Currency not found")
    return currency

# Creates a currency
@router.post("/currency/")
def create_currency(currency: Currency):
    if currency.type not in SUPPORTED_CURRENCIES:
        raise HTTPException(status_code=400, detail=f"Currency of type {currency.type} currently not supported")
    
    # lazy loading the user db
    from routes.user import user_db
    user = user_db.get_one_by_attribute(attribute_name="id", attribute_value=currency.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {currency.user_id} not found")

    result = currency_db.insert_into_table(key_attribute="id", value=currency)
    if not result:
        raise HTTPException(status_code=500, detail="Could not insert into db")
    return currency

# Updates a currency by its ID
@router.put("/currency/{currency_id}")
def update_currency_by_id(currency: Currency, currency_id: int):
    # get currency
    current_currency = currency_db.get_one_by_attribute(attribute_name="id", attribute_value=currency_id)
    if current_currency is None:
        raise HTTPException(status_code=404, detail="Currency not found")
    # make sure to not change the foreign key
    if current_currency["user_id"] != currency.user_id:
        raise HTTPException(status_code=400, detail="Mismatch in foreign key user_id")
    
    result = currency_db.update_by_key(value=currency, key_attribute="id", key_value=currency_id)
    if not result:
        raise HTTPException(status_code=500, detail="Could not update db item")
    return currency

# Gets all currencies from a user given their ID
@router.get("/currency/user/{user_id}")
def get_currencies_from_user(user_id: int):
    currencies = currency_db.get_all_by_attribute(attribute_name="user_id", attribute_value=user_id)
    return currencies