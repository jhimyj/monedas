from fastapi import APIRouter, HTTPException
from utility.exchange.exchange_manager import ExchangeManager
from utility.exchange.adapter.currency_api_exchange_adapter import CurrencyApiExchangeAdapter
from utility.exchange.adapter.frankfurter_exchange_adapter import FrankfurterExchangeAdapter

router = APIRouter()
manager = ExchangeManager()

exchangers = {
    "currency_api": CurrencyApiExchangeAdapter(),
    "frankfurter": FrankfurterExchangeAdapter()
}

# Gets transaction by its ID
@router.get("/exchange/{exchanger_name}/{from_currency}/{to_currency}")
def get_exchange_rate(exchanger_name: str, from_currency: str, to_currency: str):
    if exchanger_name not in exchangers.keys():
        raise HTTPException(status_code=402, detail="Exchanger not found")

    adapter = exchangers[exchanger_name]
    manager.set_adapter(adapter)

    try:
        rate = manager.get_exchange_rate(from_currency=from_currency, to_currency=to_currency)
        return { "rate": rate }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")