# Research: GDPR Audit Logging

**Feature**: GDPR Audit Logging
**Date**: 2026-01-27

## Decisions

### 1. Asynchronous Logging Mechanism
- **Decision**: Use `fastapi.BackgroundTasks`.
- **Rationale**: Explicitly required by the Constitution (Principle II) and the Feature Spec (FR-004) to prevent blocking the main thread, which is critical for the performance of the legacy system. It is built-in to FastAPI and simple to implement.
- **Alternatives Considered**: 
    - `Celery`: Too complex for this simple requirement, introduces infrastructure overhead (Redis/RabbitMQ).
    - `threading.Thread`: Less managed than `BackgroundTasks` within the FastAPI lifecycle.

### 2. Database Model for AuditLog
- **Decision**: Create a new `AuditLog` class in `src/models.py` inheriting from `SQLModel`.
- **Rationale**: Consistent with the existing project structure (`src/models.py` uses `SQLModel`).
- **Alternatives Considered**: 
    - Separate database: Overkill for the current scope and scale.
    - Text file logging: Harder to query for compliance audits ("trace who accessed what").

### 3. PII Stripping Strategy
- **Decision**: Implement a dedicated helper function `create_audit_log_entry` that constructs the log message. This function will strictly accept only safe metadata or explicitly sanitize inputs before writing to the `details` field.
- **Rationale**: Ensures the "Data Minimization" principle (Constitution Principle I) is enforced at the code level.
- **Alternatives Considered**: 
    - Database triggers: Harder to maintain and version control.
    - Post-processing logs: Risky, as PII would briefly exist in storage.

## Unknowns Resolved

- **Language/Version**: Confirmed Python 3.x.
- **Dependencies**: Confirmed FastAPI, SQLModel.
- **Storage**: Confirmed SQLite.
