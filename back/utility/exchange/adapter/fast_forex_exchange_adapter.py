from utility.exchange.adapter.i_exchange_adapter import IExchangeAdapter
from utility.env_loader import EnvLoader
import requests

class FastForexExchangeAdapter(IExchangeAdapter):
    """
    Implementación de adaptador para el API de FastForex
    """

    def __init__(self):
        self.api_key = EnvLoader.get("FAST_FOREX_API_KEY") # get api key
        self.fetch_url = f"https://api.fastforex.io/fetch-one?api_key={self.api_key}"
        
    def get_rate(self, from_currency: str, to_currency: str) -> float:
        url = f"{self.fetch_url}&from={from_currency}&to={to_currency}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}")

        try:
            data = response.json()
            result = data["result"][to_currency]
            return result
        except Exception as e:
            raise e