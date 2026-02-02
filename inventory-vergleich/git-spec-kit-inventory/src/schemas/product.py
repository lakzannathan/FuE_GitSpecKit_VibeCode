from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(ge=0)
    stock: int = Field(ge=0)

class ProductRead(BaseModel):
    id: int
    name: str
    price: float
    stock: int
