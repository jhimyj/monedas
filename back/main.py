from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import router as user_router
from routes.currency import router as currency_router
from routes.transaction import router as transaction_router
from routes.exchange import router as exchange_router

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Ajusta según tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="", tags=["User"])
app.include_router(currency_router, prefix="", tags=["Currency"])
app.include_router(transaction_router, prefix="", tags=["Transaction"])
app.include_router(exchange_router, prefix="", tags=["Exchange"])