from fastapi.testclient import TestClient

def test_create_order_api(client: TestClient):
    # Create product
    p_resp = client.post("/products", json={"name": "P1", "price": 10, "stock": 10})
    p_id = p_resp.json()["id"]
    
    # Order
    resp = client.post("/orders", json={"product_id": p_id, "quantity": 5})
    assert resp.status_code == 201
    assert resp.json()["status"] == "completed"
    
    # Check stock
    p_resp = client.get("/products")
    product = next(p for p in p_resp.json() if p["id"] == p_id)
    assert product["stock"] == 5

def test_create_order_api_fail(client: TestClient):
    p_resp = client.post("/products", json={"name": "P1", "price": 10, "stock": 1})
    p_id = p_resp.json()["id"]
    
    resp = client.post("/orders", json={"product_id": p_id, "quantity": 2})
    assert resp.status_code == 400
