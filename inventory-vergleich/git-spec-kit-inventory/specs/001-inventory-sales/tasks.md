---
description: "Task list for Inventory Persistence & Sales Logic"
---

# Tasks: Inventory Persistence & Sales Logic

**Input**: Design documents from `/specs/001-inventory-sales/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/, research.md

**Tests**: Automated tests are included per Constitution (TDD mindset).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: [US1] (Persistence), [US2] (Sales)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure (`src/models`, `src/schemas`, `src/services`, `src/routers`, `tests`)
- [x] T002 Install dependencies (`sqlmodel`, `fastapi`, `uvicorn`, `pytest`, `httpx`)
- [x] T003 Configure database engine and `get_session` dependency in `src/database.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T004 Create `init_db` function and lifespan handler in `src/main.py` to create tables on startup

---

## Phase 3: User Story 1 - Persistent Inventory Management (Priority: P1)

**Goal**: Store products in SQLite database instead of memory.
**Independent Test**: Restart server -> Products remain.

### Tests for User Story 1

- [x] T005 [US1] Create unit test for `ProductService` in `tests/unit/test_inventory_service.py`
- [x] T006 [US1] Create integration test for `/products` API in `tests/integration/test_products_api.py`

### Implementation for User Story 1

- [x] T007 [P] [US1] Create `Product` SQLModel entity in `src/models/product.py`
- [x] T008 [P] [US1] Create `ProductCreate`, `ProductRead` schemas in `src/schemas/product.py`
- [x] T009 [US1] Implement `ProductService` (create, list) in `src/services/inventory.py`
- [x] T010 [US1] Implement `/products` endpoints in `src/routers/products.py`
- [x] T011 [US1] Wire up `products` router in `src/main.py` and remove legacy in-memory code

**Checkpoint**: Verify persistence by restarting server (SC-001).

---

## Phase 4: User Story 2 - Order Processing with Stock Validation (Priority: P1)

**Goal**: Process orders with strict oversell protection.
**Independent Test**: Try to buy 11 items when stock is 10 -> Fail.

### Tests for User Story 2

- [x] T012 [US2] Create unit test for `SalesService` (oversell protection) in `tests/unit/test_sales_service.py`
- [x] T013 [US2] Create integration test for `/orders` API in `tests/integration/test_orders_api.py`

### Implementation for User Story 2

- [x] T014 [P] [US2] Create `Order` SQLModel entity in `src/models/order.py`
- [x] T015 [P] [US2] Create `OrderCreate`, `OrderRead` schemas in `src/schemas/order.py`
- [x] T016 [US2] Implement `SalesService` with atomic update transaction in `src/services/sales.py`
- [x] T017 [US2] Implement `/orders` endpoint in `src/routers/orders.py`
- [x] T018 [US2] Wire up `orders` router in `src/main.py`

**Checkpoint**: Verify oversell protection with concurrent requests (SC-002).

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T019 Run full test suite (`pytest`) and ensure all pass
- [x] T020 Verify `quickstart.md` instructions work manually
- [x] T021 Run `ruff check .` and fix any linting issues

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup.
- **User Stories (Phase 3+)**: Depend on Foundational.

### User Story Dependencies

- **User Story 1**: Independent.
- **User Story 2**: Depends on User Story 1 (needs Products to sell).

### Within Each User Story

- Tests -> Models/Schemas -> Services -> Routers -> Wiring.

## Implementation Strategy

### MVP First

1. Complete Setup & Foundation.
2. Implement US1 (Persistence) to fix data loss.
3. Implement US2 (Sales) to enable business value.
