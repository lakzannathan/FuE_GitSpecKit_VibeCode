# Implementation Plan: Inventory Persistence & Sales Logic

**Branch**: `001-inventory-sales` | **Date**: 2026-01-04 | **Spec**: [specs/001-inventory-sales/spec.md](specs/001-inventory-sales/spec.md)
**Input**: Feature specification from `/specs/001-inventory-sales/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature transitions the application from an in-memory prototype to a robust, persistent system using SQLite. It introduces a strict separation of concerns (Entities vs DTOs) and implements a sales process with strong "oversell protection" guarantees.

**Key Technical Changes:**

1.  **Persistence**: Replace global lists with `SQLModel` (SQLite).
2.  **Architecture**: Refactor `main.py` into a layered architecture (Routers -> Services -> Repositories/DB).
3.  **Business Logic**: Implement atomic order processing to ensure stock integrity.

## Technical Context

**Language/Version**: Python 3.x
**Primary Dependencies**: FastAPI, SQLModel (SQLAlchemy + Pydantic)
**Storage**: SQLite (`database.db`)
**Testing**: pytest (with `pytest-asyncio` if async, or standard `TestClient`)
**Target Platform**: Local execution (Windows/Linux)
**Project Type**: Single project (FastAPI Backend)
**Performance Goals**: N/A (Focus on correctness and data integrity)
**Constraints**: SQLite concurrency limitations (single writer)
**Scale/Scope**: Small scale, focus on architectural correctness

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

- **Persistence Layer**: Uses `SQLModel` + SQLite? **YES**
- **Separation**: DTOs (Schemas) separate from Entities (Models)? **YES** (Planned)
- **State**: No global state? **YES** (Planned removal of `fake_product_db`)
- **Testing**: TDD & Edge Cases? **YES** (Included in tasks)
- **Legacy**: Refactor existing code? **YES** (Explicit goal)

## Project Structure

### Documentation (this feature)

```text
specs/001-inventory-sales/
├── plan.md              # This file
├── research.md          # Concurrency & Transaction strategy
├── data-model.md        # Entity & Schema definitions
├── quickstart.md        # DB setup & running instructions
├── contracts/           # API Endpoint definitions
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
src/
├── database.py        # DB Engine & Session dependency
├── main.py            # App entry point & wiring
├── models/            # SQLModel Entities (DB Tables)
│   ├── product.py
│   └── order.py
├── schemas/           # Pydantic DTOs (API Request/Response)
│   ├── product.py
│   └── order.py
├── services/          # Business Logic (Transactions, Stock checks)
│   ├── inventory.py
│   └── sales.py
└── routers/           # API Endpoints (optional, can be in main.py if small)
    ├── products.py
    └── orders.py

tests/
├── conftest.py        # Test DB fixtures
├── unit/              # Service logic tests
└── integration/       # API tests (TestClient)
```

**Structure Decision**: Adopting a standard layered FastAPI architecture to satisfy the Constitution's requirement for separation of concerns and dependency injection.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --------- | ---------- | ------------------------------------ |
| None      |            |                                      |
