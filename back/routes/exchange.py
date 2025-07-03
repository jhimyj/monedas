from fastapi import APIRouter, HTTPException
from utility.exchange.exchange_manager import ExchangeManager
from utility.exchange.adapter.currency_api_exchange_adapter import CurrencyApiExchangeAdapter
from utility.exchange.adapter.frankfurter_exchange_adapter import FrankfurterExchangeAdapter

class ExchangeRouter:
    def __init__(self):
        self.manager = ExchangeManager()
        self.exchangers = {
            "currency_api": CurrencyApiExchangeAdapter(),
            "frankfurter": FrankfurterExchangeAdapter()
        }

        self.router = APIRouter()
        self.router.get("/exchange/{exchanger_name}/{from_currency}/{to_currency}")(self.get_exchange_rate)

    # Gets transaction by its ID    
    def get_exchange_rate(self, exchanger_name: str, from_currency: str, to_currency: str):
        if exchanger_name not in self.exchangers.keys():
            raise HTTPException(status_code=402, detail="Exchanger not found")

        adapter = self.exchangers[exchanger_name]
        self.manager.set_adapter(adapter)

        try:
            rate = self.manager.get_exchange_rate(from_currency=from_currency, to_currency=to_currency)
            return { "rate": rate }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {e}")