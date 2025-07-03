from utility.exchange.adapter.i_exchange_adapter import IExchangeAdapter
from utility.env_loader import EnvLoader
import requests

class CurrencyApiExchangeAdapter(IExchangeAdapter):
    """
    Implementación de adaptador para el API de CurrencyAPI
    """
    
    def __init__(self):
        self.api_key = EnvLoader.get("CURRENCY_API_API_KEY") # get api key
        self.fetch_url = f"https://api.currencyapi.com/v3/latest?apikey={self.api_key}"
        
    def get_rate(self, from_currency: str, to_currency: str) -> float:
        url = f"{self.fetch_url}&base_currency={from_currency}&currencies={to_currency}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}")

        try:
            data = response.json()
            result = data["data"][to_currency]["value"]
            return result
        except Exception as e:
            raise e

    def get_name(self):
        return "currency_api"