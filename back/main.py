from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utility.db_connector import DbConnector
from routes.user import UserRouter
from routes.currency import CurrencyRouter
from routes.transaction import TransactionRouter
from routes.exchange import ExchangeRouter

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Ajusta según tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_db = DbConnector(path="db/user.json", key_attribute="id")
currency_db = DbConnector(path="db/currency.json", key_attribute="id")
transaction_db = DbConnector(path="db/transaction.json", key_attribute="id")
    
user_rt = UserRouter(user_db=user_db)
currency_rt = CurrencyRouter(user_db=user_db, currency_db=currency_db)
transaction_rt = TransactionRouter(user_db=user_db, currency_db=currency_db, transaction_db=transaction_db, currency_router=currency_rt)
exchange_rt = ExchangeRouter()

app.include_router(user_rt.router, prefix="", tags=["User"])
app.include_router(currency_rt.router, prefix="", tags=["Currency"])
app.include_router(transaction_rt.router, prefix="", tags=["Transaction"])
app.include_router(exchange_rt.router, prefix="", tags=["Exchange"])