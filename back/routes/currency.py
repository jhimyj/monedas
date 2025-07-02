from fastapi import APIRouter, HTTPException
from dataclasses import dataclass
from utility.db_connector import DbConnector


@dataclass
class Currency:
    user_id: int
    amount: float
    type: str

class CurrencyRouter:
    def __init__(self, user_db: DbConnector, currency_db: DbConnector):
        self.user_db = user_db
        self.currency_db = currency_db
        
        self.router = APIRouter()
        self.router.get("/currency/{currency_id}")(self.get_currency_by_id)
        self.router.post("/currency/")(self.create_currency)
        self.router.put("/currency/{currency_id}")(self.update_currency_by_id)
        self.router.get("/currency/user/{user_id}")(self.get_currencies_from_user)

    # Gets currency by its ID
    def get_currency_by_id(self, currency_id: int):
        currency = self.currency_db.get_one_by_attribute(attribute_name="id", attribute_value=currency_id)
        if currency is None:
            raise HTTPException(status_code=404, detail="Currency not found")
        return currency

    # Creates a currency
    def create_currency(self, currency: Currency):
        user = self.user_db.get_one_by_attribute(attribute_name="id", attribute_value=currency.user_id)
        if user is None:
            raise HTTPException(status_code=404, detail=f"User with ID {currency.user_id} not found")

        result = self.currency_db.insert_into_table(key_attribute="id", value=currency)
        if not result:
            raise HTTPException(status_code=500, detail="Could not insert into db")
        return currency

    # Updates a currency by its ID
    def update_currency_by_id(self, currency: Currency, currency_id: int):
        # get currency
        current_currency = self.currency_db.get_one_by_attribute(attribute_name="id", attribute_value=currency_id)
        if current_currency is None:
            raise HTTPException(status_code=404, detail="Currency not found")
        # make sure to not change the foreign key
        if current_currency["user_id"] != currency.user_id:
            raise HTTPException(status_code=400, detail="Mismatch in foreign key user_id")
        
        result = self.currency_db.update_by_key(value=currency, key_attribute="id", key_value=currency_id)
        if not result:
            raise HTTPException(status_code=500, detail="Could not update db item")
        return currency

    # Gets all currencies from a user given their ID
    def get_currencies_from_user(self, user_id: int):
        currencies = self.currency_db.get_all_by_attribute(attribute_name="user_id", attribute_value=user_id)
        return currencies