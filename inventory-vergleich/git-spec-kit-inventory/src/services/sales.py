from sqlmodel import Session, select
from src.models.order import Order
from src.models.product import Product
from src.schemas.order import OrderCreate

class SalesService:
    def __init__(self, session: Session):
        self.session = session

    def create_order(self, order_in: OrderCreate) -> Order:
        # Atomic update: decrement stock only if sufficient
        # UPDATE product SET stock = stock - :qty WHERE id = :id AND stock >= :qty
        statement = (
            select(Product)
            .where(Product.id == order_in.product_id)
            .with_for_update()
        )
        product = self.session.exec(statement).one_or_none()
        
        if not product:
            raise ValueError("Product not found")
            
        if product.stock < order_in.quantity:
            raise ValueError("Insufficient stock")
            
        product.stock -= order_in.quantity
        self.session.add(product)
        
        order = Order(
            product_id=order_in.product_id,
            quantity=order_in.quantity,
            status="completed"
        )
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        return order
