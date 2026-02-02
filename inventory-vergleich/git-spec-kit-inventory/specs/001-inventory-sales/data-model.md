# Data Model

## Entities (Database Models)

### Product

Represents an item in the inventory.

| Field   | Type    | Required | Constraints                 | Description                |
| ------- | ------- | -------- | --------------------------- | -------------------------- |
| `id`    | Integer | Yes      | Primary Key, Auto-increment | Unique identifier          |
| `name`  | String  | Yes      |                             | Product name               |
| `price` | Float   | Yes      | >= 0                        | Unit price                 |
| `stock` | Integer | Yes      | >= 0                        | Current quantity available |

### Order

Represents a customer purchase.

| Field        | Type     | Required | Constraints                 | Description                                |
| ------------ | -------- | -------- | --------------------------- | ------------------------------------------ |
| `id`         | Integer  | Yes      | Primary Key, Auto-increment | Unique identifier                          |
| `product_id` | Integer  | Yes      | Foreign Key (Product.id)    | The product purchased                      |
| `quantity`   | Integer  | Yes      | > 0                         | Number of units purchased                  |
| `status`     | String   | Yes      | Default: "completed"        | Order status (e.g., "completed", "failed") |
| `created_at` | DateTime | Yes      | Default: Now                | Timestamp of purchase                      |

## Schemas (DTOs)

### ProductCreate (Request)

| Field   | Type    | Required | Validation   |
| ------- | ------- | -------- | ------------ |
| `name`  | String  | Yes      | Min length 1 |
| `price` | Float   | Yes      | >= 0         |
| `stock` | Integer | Yes      | >= 0         |

### ProductRead (Response)

| Field   | Type    | Required |
| ------- | ------- | -------- |
| `id`    | Integer | Yes      |
| `name`  | String  | Yes      |
| `price` | Float   | Yes      |
| `stock` | Integer | Yes      |

### OrderCreate (Request)

| Field        | Type    | Required | Validation |
| ------------ | ------- | -------- | ---------- |
| `product_id` | Integer | Yes      |            |
| `quantity`   | Integer | Yes      | > 0        |

### OrderRead (Response)

| Field        | Type     | Required |
| ------------ | -------- | -------- |
| `id`         | Integer  | Yes      |
| `product_id` | Integer  | Yes      |
| `quantity`   | Integer  | Yes      |
| `status`     | String   | Yes      |
| `created_at` | DateTime | Yes      |
