from fastapi import FastAPI 
from app.routes import assets 

app = FastAPI(
    title="Market Data API"
)

app.include_router(
    assets.router 
)