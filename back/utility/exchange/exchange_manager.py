from utility.exchange.adapter.i_exchange_adapter import IExchangeAdapter

class ExchangeManager:
    """
    Singleton para manejar exchange adapters, usando classmethods
    """

    _instance = None
    _adapter: IExchangeAdapter = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def set_adapter(cls, adapter: IExchangeAdapter):
        if cls._instance is None:
            cls()
        cls._adapter = adapter

    @classmethod
    def get_current_adapter_name(cls) -> str:
        if cls._instance is None:
            cls()
        if cls._adapter is None:
            return ""
        return cls._adapter.get_name()

    @classmethod
    def get_exchange_rate(cls, from_currency: str, to_currency: str) -> float:
        if cls._instance is None:
            cls()
        if cls._adapter is None:
            raise ValueError("ExchangeManager error: Adapter not set")
        return cls._adapter.get_rate(from_currency=from_currency, to_currency=to_currency)
