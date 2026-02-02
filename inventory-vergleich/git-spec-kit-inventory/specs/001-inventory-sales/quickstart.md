# Quickstart: Inventory System

## Prerequisites

- Python 3.10+
- pip

## Setup

1. **Install Dependencies**:

   ```bash
   pip install fastapi uvicorn sqlmodel
   ```

2. **Run the Application**:
   ```bash
   uvicorn src.main:app --reload
   ```
   The database `database.db` will be automatically created on first run.

## Usage

### Create a Product

```bash
curl -X POST "http://127.0.0.1:8000/products" -H "Content-Type: application/json" -d '{"name": "Laptop", "price": 999.99, "stock": 5}'
```

### Place an Order

```bash
curl -X POST "http://127.0.0.1:8000/orders" -H "Content-Type: application/json" -d '{"product_id": 1, "quantity": 1}'
```

### Check Stock

```bash
curl "http://127.0.0.1:8000/products"
```
