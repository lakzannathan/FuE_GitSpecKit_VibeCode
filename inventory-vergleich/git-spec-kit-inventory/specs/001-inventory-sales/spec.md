# Feature Specification: Inventory Persistence & Sales Logic

**Feature Branch**: `001-inventory-sales`
**Created**: 2026-01-04
**Status**: Draft
**Input**: User description: "Unser aktuelles MVP hat zwei kritische geschäftliche Schwächen, die wir beheben müssen: 1. Datenverlust... 2. Verkaufsprozess..."

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Persistent Inventory Management (Priority: P1)

As a store operator, I want all product data to be stored in a persistent database so that inventory records are preserved across server restarts.

**Why this priority**: Critical business requirement. Currently, all data is lost on restart, making the system unusable for real operations.

**Independent Test**:

1. Start the server.
2. Create a new product "Test Item" with stock 10.
3. Stop and restart the server.
4. Query the product list.
5. Verify "Test Item" still exists with stock 10.

**Acceptance Scenarios**:

1. **Given** a running server, **When** I create a product, **Then** it is saved to the SQLite database.
2. **Given** a server with existing data, **When** the process is killed and restarted, **Then** all previous data is available.

---

### User Story 2 - Order Processing with Stock Validation (Priority: P1)

As a customer, I want to place an order for a product so that I can purchase items, but only if they are actually in stock.

**Why this priority**: Core business function. Selling products is the primary purpose of the system.

**Independent Test**:

1. Create a product with stock 5.
2. Place an order for 3 units.
3. Verify order is accepted and stock becomes 2.
4. Place another order for 3 units.
5. Verify order is rejected (insufficient stock) and stock remains 2.

**Acceptance Scenarios**:

1. **Given** a product with stock 10, **When** I order 1 unit, **Then** the order is accepted and stock becomes 9.
2. **Given** a product with stock 1, **When** I order 2 units, **Then** the order is rejected with a clear error message.
3. **Given** a product with stock 0, **When** I order 1 unit, **Then** the order is rejected.

---

### Edge Cases

- **Concurrent Orders**: Two users try to buy the last item at the exact same time. Only one should succeed.
- **Database Lock**: Database is busy/locked during a write operation.
- **Invalid Quantity**: User tries to order 0 or negative quantity.

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST persist all Product and Order data to a local SQLite database using SQLModel.
- **FR-002**: System MUST provide an API to create new products with name, price, and initial stock.
- **FR-003**: System MUST provide an API to create a new order specifying product ID and quantity.
- **FR-004**: System MUST validate that `requested_quantity <= current_stock` before accepting an order.
- **FR-005**: System MUST atomically decrement the product stock when an order is successfully created.
- **FR-006**: System MUST return a 400 Bad Request (or appropriate error) if stock is insufficient.
- **FR-007**: System MUST NOT allow orders with non-positive quantities (<= 0).

### Key Entities _(include if feature involves data)_

- **Product**: Represents an item for sale. Attributes: `id`, `name`, `price`, `stock`.
- **Order**: Represents a completed sale. Attributes: `id`, `product_id`, `quantity`, `status` (optional), `created_at`.

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Data Persistence: 100% of created products are available after a forced server restart.
- **SC-002**: Oversell Protection: In a load test with 10 concurrent requests for a single item (stock=1), exactly 1 request succeeds and 9 fail.
- **SC-003**: Stock Integrity: The sum of (Current Stock + Total Sold Items) MUST always equal Initial Stock (assuming no restocks).
