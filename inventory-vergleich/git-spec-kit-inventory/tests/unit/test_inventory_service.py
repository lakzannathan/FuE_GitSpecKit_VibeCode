from sqlmodel import Session
from src.services.inventory import ProductService
from src.schemas.product import ProductCreate

def test_create_product(session: Session):
    service = ProductService(session)
    product_in = ProductCreate(name="Test Product", price=10.0, stock=5)
    product = service.create_product(product_in)
    
    assert product.id is not None
    assert product.name == "Test Product"
    assert product.price == 10.0
    assert product.stock == 5

def test_list_products(session: Session):
    service = ProductService(session)
    service.create_product(ProductCreate(name="P1", price=1.0, stock=1))
    service.create_product(ProductCreate(name="P2", price=2.0, stock=2))
    
    products = service.list_products()
    assert len(products) == 2
