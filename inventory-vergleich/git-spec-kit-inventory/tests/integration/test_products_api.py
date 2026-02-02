from fastapi.testclient import TestClient

def test_create_product_api(client: TestClient):
    response = client.post(
        "/products",
        json={"name": "API Product", "price": 20.0, "stock": 10},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "API Product"
    assert data["id"] is not None

def test_list_products_api(client: TestClient):
    client.post("/products", json={"name": "P1", "price": 10, "stock": 5})
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) >= 1
