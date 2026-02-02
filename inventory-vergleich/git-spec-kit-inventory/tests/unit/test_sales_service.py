from sqlmodel import Session
from src.services.sales import SalesService
from src.schemas.order import OrderCreate
from src.schemas.product import ProductCreate
from src.services.inventory import ProductService
import pytest

def test_create_order_success(session: Session):
    # Setup product
    p_service = ProductService(session)
    product = p_service.create_product(ProductCreate(name="P1", price=10, stock=10))
    
    # Create order
    s_service = SalesService(session)
    order = s_service.create_order(OrderCreate(product_id=product.id, quantity=5))
    
    assert order.id is not None
    assert order.status == "completed"
    
    # Verify stock reduced
    session.refresh(product)
    assert product.stock == 5

def test_create_order_insufficient_stock(session: Session):
    p_service = ProductService(session)
    product = p_service.create_product(ProductCreate(name="P1", price=10, stock=1))
    
    s_service = SalesService(session)
    with pytest.raises(ValueError, match="Insufficient stock"):
        s_service.create_order(OrderCreate(product_id=product.id, quantity=2))
        
    session.refresh(product)
    assert product.stock == 1
