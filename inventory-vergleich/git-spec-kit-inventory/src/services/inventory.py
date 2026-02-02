from typing import List
from sqlmodel import Session, select
from src.models.product import Product
from src.schemas.product import ProductCreate

class ProductService:
    def __init__(self, session: Session):
        self.session = session

    def create_product(self, product_in: ProductCreate) -> Product:
        product = Product.model_validate(product_in)
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def list_products(self) -> List[Product]:
        statement = select(Product)
        return self.session.exec(statement).all()
