# Inventory System Constitution

<!--
SYNC IMPACT REPORT
Version: 0.0.0 -> 1.0.0
Type: MAJOR (Initial Ratification)

Modified Principles:
- Defined I. Persistence Strategy
- Defined II. Architecture & State
- Defined III. Quality Assurance
- Defined IV. Legacy Migration

Templates Status:
- .specify/templates/plan-template.md: ✅ Compatible
- .specify/templates/spec-template.md: ✅ Compatible
- .specify/templates/tasks-template.md: ⚠ Updated to include DTO tasks

Follow-up:
- None
-->

## Core Principles

### I. Persistence Strategy

**Rule:** The persistence layer MUST use `SQLModel` (SQLAlchemy + Pydantic) with a SQLite database (`database.db`).
**Rationale:** Ensures a consistent, type-safe interaction with the database.
**Constraint:** There MUST be a strict separation between API schemas (DTOs) and Database Models (Entities). Mixing Pydantic schemas and database tables in the same class is FORBIDDEN.

### II. Architecture & State

**Rule:** The application MUST be stateless. Global variables for state (e.g., in-memory lists) are FORBIDDEN.
**Mechanism:** Database sessions MUST be injected into routes using Dependency Injection (`Depends(get_session)`).
**Separation:** Database logic MUST reside in separate CRUD functions or Services. It is FORBIDDEN to place DB logic directly in Routers.

### III. Quality Assurance

**Rule:** A Test-Driven Mindset is MANDATORY. Every new feature MUST be covered by automated tests.
**Isolation:** Tests MUST NOT modify the productive database. Use mocking or a separate test database.
**Coverage:** Tests MUST explicitly cover Edge Cases (e.g., ordering more than available stock).

### IV. Legacy Migration

**Rule:** All existing "In-Memory" code MUST be fully refactored to the new `SQLModel` architecture.
**Rationale:** To ensure technical debt is eliminated and the system is consistent with the new persistence strategy.

## Governance

This constitution supersedes all other technical practices. Amendments require documentation, approval, and a clear migration plan.

**Compliance:** All PRs/reviews must verify compliance; Complexity must be justified.

**Version**: 1.0.0 | **Ratified**: 2026-01-04 | **Last Amended**: 2026-01-04
