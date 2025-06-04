from dotenv import load_dotenv
import os

class EnvLoader:
    """
    Singleton para manejar variables de entorno
    """

    _instance = None
    _loaded = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if not cls._loaded:
                load_dotenv()
                cls._loaded = True
        return cls._instance
    
    @classmethod
    def get(cls, env_var: str) -> str:
        if cls._instance is None:
            cls()

        result = os.getenv(env_var)
        if result is None:
            raise Exception(f"Couldnt find env variable {env_var}")
        return result