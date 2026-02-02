# Research: Inventory Persistence & Sales Logic

**Feature**: Inventory Persistence & Sales Logic
**Branch**: `001-inventory-sales`

## Decision 1: Transaction Management for Oversell Protection

**Context**: We need to ensure that we never sell more stock than we have. This requires checking the stock and decrementing it in an atomic operation.

**Decision**: Use **Database Transactions** with `SQLModel` (SQLAlchemy).
Specifically, we will use `session.begin()` or `with session:` blocks to ensure atomicity.
We will perform the check and update within the same transaction.
To prevent race conditions (Read-Modify-Write), we will use one of the following strategies:

1.  **Optimistic Locking**: Add a `version` column. (Overkill for this scale?)
2.  **Pessimistic Locking**: `SELECT ... FOR UPDATE`. (Standard for inventory)
3.  **Atomic Update**: `UPDATE product SET stock = stock - :qty WHERE id = :id AND stock >= :qty`.

**Selected Approach**: **Atomic Update (Option 3)**.
**Rationale**: It is the most efficient and robust way to handle inventory decrement in SQL. It avoids the need for explicit locking in application code and relies on the database's ACID properties. If the `UPDATE` affects 0 rows (because `stock < qty`), we know the transaction failed due to insufficient funds.

**Alternatives Considered**:

- _Python-side check_: `if product.stock >= qty: product.stock -= qty; session.commit()`.
  - _Rejection_: Vulnerable to race conditions. Two requests could read the same stock level, both pass the check, and both write, resulting in negative stock.
- _Pessimistic Locking (`with_for_update`)_:
  - _Rejection_: Valid, but SQLite's locking granularity is file-level anyway, so explicit row locking behavior varies. Atomic UPDATE is more portable and simpler to reason about for this specific "decrement" use case.

## Decision 2: Database Configuration

**Context**: We need a persistent database.

**Decision**: **SQLite** with `SQLModel`.
**Rationale**: Mandated by Constitution. Simple, file-based, zero config.
**Configuration**:

- `sqlite:///database.db`
- `check_same_thread=False` (Required for FastAPI multithreading)

## Decision 3: API Structure

**Context**: We need to expose Products and Orders.

**Decision**:

- `POST /products`: Create product (Admin/Operator)
- `GET /products`: List products
- `POST /orders`: Place an order (Customer)

**Rationale**: Minimal API to satisfy the requirements.
