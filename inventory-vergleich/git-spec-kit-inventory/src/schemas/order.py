from datetime import datetime
from pydantic import BaseModel, Field

class OrderCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class OrderRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    status: str
    created_at: datetime
