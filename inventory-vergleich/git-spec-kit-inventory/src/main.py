from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from src.database import engine
from src.routers import products, orders

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(products.router)
app.include_router(orders.router)
