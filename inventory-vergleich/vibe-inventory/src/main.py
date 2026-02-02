from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
from contextlib import asynccontextmanager

# --- Database Setup ---
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# --- Models ---
class ProductBase(SQLModel):
    name: str
    price: float
    stock: int

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ProductCreate(ProductBase):
    pass

class OrderCreate(SQLModel):
    product_id: int
    quantity: int

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    quantity: int
    status: str = "completed"

# --- App Lifecycle ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    # Seed initial data if empty to match original behavior
    with Session(engine) as session:
        statement = select(Product)
        results = session.exec(statement).first()
        if not results:
            session.add(Product(name="Laptop", price=999.99, stock=5))
            session.add(Product(name="Maus", price=29.99, stock=100))
            session.commit()
    yield

app = FastAPI(lifespan=lifespan)

# --- Endpoints ---
@app.get("/products", response_model=List[Product])
def get_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products", response_model=Product)
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.post("/orders", response_model=Order)
def create_order(order_request: OrderCreate, session: Session = Depends(get_session)):
    # 1. Produkt laden
    product = session.get(Product, order_request.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # 2. Stock prüfen
    if product.stock < order_request.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    # 3. Stock reduzieren
    product.stock -= order_request.quantity
    session.add(product)
    
    # 4. Order speichern
    order = Order(product_id=order_request.product_id, quantity=order_request.quantity)
    session.add(order)
    
    session.commit()
    session.refresh(order)
    return order