from typing import List
from fastapi import APIRouter, Depends
from src.database import SessionDep
from src.schemas.product import ProductCreate, ProductRead
from src.services.inventory import ProductService

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", response_model=ProductRead, status_code=201)
def create_product(product_in: ProductCreate, session: SessionDep):
    service = ProductService(session)
    return service.create_product(product_in)

@router.get("", response_model=List[ProductRead])
def list_products(session: SessionDep):
    service = ProductService(session)
    return service.list_products()
