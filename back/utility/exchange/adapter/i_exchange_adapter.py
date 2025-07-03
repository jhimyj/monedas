from abc import ABC, abstractmethod

class IExchangeAdapter(ABC):
    """
    Interfaz para implementaciones de adaptadores del API de cambio de monedas
    """

    @abstractmethod
    def get_rate(self, from_currency: str, to_currency: str) -> float:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass