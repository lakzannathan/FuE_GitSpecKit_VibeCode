from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool
import pytest
from src.main import app, get_session, Product

# --- Test Database Setup ---
# Use in-memory SQLite for tests to ensure isolation
sqlite_url = "sqlite://" 
engine = create_engine(
    sqlite_url, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_order_success(client: TestClient, session: Session):
    # 1. Create a product
    product = Product(name="Test Product", price=10.0, stock=10)
    session.add(product)
    session.commit()
    session.refresh(product)
    
    # 2. Order the product
    response = client.post("/orders", json={"product_id": product.id, "quantity": 2})
    data = response.json()
    
    # 3. Verify response
    assert response.status_code == 200
    assert data["product_id"] == product.id
    assert data["quantity"] == 2
    
    # 4. Verify stock reduction in DB
    session.refresh(product)
    assert product.stock == 8

def test_create_order_insufficient_stock(client: TestClient, session: Session):
    # 1. Create a product with low stock
    product = Product(name="Low Stock Product", price=10.0, stock=1)
    session.add(product)
    session.commit()
    session.refresh(product)
    
    # 2. Try to order more than available
    response = client.post("/orders", json={"product_id": product.id, "quantity": 5})
    
    # 3. Verify error response
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient stock"
    
    # 4. Verify stock remains unchanged
    session.refresh(product)
    assert product.stock == 1

def test_create_order_product_not_found(client: TestClient):
    response = client.post("/orders", json={"product_id": 999, "quantity": 1})
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"