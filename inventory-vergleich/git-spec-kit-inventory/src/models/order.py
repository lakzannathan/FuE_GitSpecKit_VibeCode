from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    quantity: int = Field(gt=0)
    status: str = Field(default="completed")
    created_at: datetime = Field(default_factory=datetime.utcnow)
