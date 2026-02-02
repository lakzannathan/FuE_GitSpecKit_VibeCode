from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# --- Das Datenmodell (Simpel, noch keine DB) ---
class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int

# --- In-Memory Speicher (Das ist der "State") ---
fake_product_db = [
    Product(id=1, name="Laptop", price=999.99, stock=5),
    Product(id=2, name="Maus", price=29.99, stock=100),
]

# --- Die Endpunkte ---
@app.get("/products", response_model=List[Product])
def get_products():
    return fake_product_db

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    for product in fake_product_db:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products", response_model=Product)
def create_product(product: Product):
    # Check ob ID schon existiert
    for p in fake_product_db:
        if p.id == product.id:
            raise HTTPException(status_code=400, detail="ID already exists")
    
    fake_product_db.append(product)
    return product