from fastapi import FastAPI
from routes.user import router as user_router
from routes.currency import router as currency_router

app = FastAPI()

app.include_router(user_router, prefix="", tags=["User"])
app.include_router(currency_router, prefix="", tags=["Currency"])