from utility.exchange.adapter.i_exchange_adapter import IExchangeAdapter
import requests

class FrankfurterExchangeAdapter(IExchangeAdapter):
    """
    Implementación de adaptador para el API de Frankfurter
    """

    def __init__(self):
        # Frankfurter no necesita API key, pero tiene menos datos que CurrencyAPI
        self.fetch_url = f"https://api.frankfurter.dev/v1/latest"
        self.available_currencies = []
        self._setup_available_currencies()
        
    def get_rate(self, from_currency: str, to_currency: str) -> float:
        if from_currency not in self.available_currencies:
            raise Exception(f"Error: Currency {from_currency} not available at FrankfurterAPI")

        if to_currency not in self.available_currencies:
            raise Exception(f"Error: Currency {to_currency} not available at FrankfurterAPI")

        url = f"{self.fetch_url}?base={from_currency}&symbols={to_currency}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}")

        try:
            data = response.json()
            result = data["rates"][to_currency]
            return result
        except Exception as e:
            raise e
        
    def get_name(self):
        return "frankfurter"

    def _setup_available_currencies(self):
        currencies_url = "https://api.frankfurter.dev/v1/currencies"
        response = requests.get(currencies_url)

        if response.status_code != 200:
            raise Exception(f"Error - Couldnt fetch currencies: {response.status_code}")
        
        try:
            data = response.json()
            for key, value in data.items():
                self.available_currencies.append(key)
        except Exception as e:
            raise Exception(f"Error - Couldnt fetch currencies: {e}")