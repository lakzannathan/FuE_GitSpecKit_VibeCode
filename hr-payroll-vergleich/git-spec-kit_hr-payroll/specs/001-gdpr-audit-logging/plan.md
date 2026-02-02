# Implementation Plan: GDPR Audit Logging

**Branch**: `001-gdpr-audit-logging` | **Date**: 2026-01-27 | **Spec**: [specs/001-gdpr-audit-logging/spec.md](spec.md)
**Input**: Feature specification from `/specs/001-gdpr-audit-logging/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a GDPR-compliant audit logging system for the HR Payroll application. The system will log read access (`VIEW_DETAILS`) and payroll calculations (`CALC_PAYROLL`) to a new `AuditLog` database table. To ensure system integrity and performance, logging will be performed asynchronously using `fastapi.BackgroundTasks`. The implementation will strictly adhere to data minimization principles, ensuring no PII (IBAN, Salary) is stored in the logs.

## Technical Context

**Language/Version**: Python 3.x (inferred from existing code)
**Primary Dependencies**: FastAPI, SQLModel, SQLAlchemy (inferred from `src/main.py`, `src/database.py`)
**Storage**: SQLite (inferred from `src/database.py`)
**Testing**: pytest (Standard for Python/FastAPI, implied by "Automated regression tests" requirement)
**Target Platform**: Local execution / Server (Standard FastAPI deployment)
**Project Type**: Single project (API)
**Performance Goals**: Non-blocking logging (async execution required)
**Constraints**: 
- No modification of `legacy_engine.py`
- No PII in logs
- Use `BackgroundTasks` for DB writes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Data Privacy & GDPR**: Plan explicitly excludes PII from logs and mandates metadata-only logging.
- [x] **II. System Integrity & Performance**: Plan mandates `BackgroundTasks` for logging to avoid blocking the legacy system. `legacy_engine.py` is untouched.
- [x] **III. Quality Assurance**: Regression tests will be part of the implementation tasks (implied by standard workflow, will be explicit in tasks).

## Project Structure

### Documentation (this feature)

```text
specs/001-gdpr-audit-logging/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── models.py            # Update: Add AuditLog model
├── database.py          # No change expected, maybe migration support if needed
├── main.py              # Update: Register new model if needed
├── routers/
│   └── hr.py            # Update: Inject BackgroundTasks and logging logic
└── legacy_engine.py     # UNTOUCHED

tests/
├── integration/         # New: Test logging integration
└── unit/                # New: Test PII stripping logic
```

**Structure Decision**: Single project structure maintained. `AuditLog` model added to `src/models.py`. Logging logic integrated directly into `src/routers/hr.py` using `BackgroundTasks` to keep it simple and close to the usage point, avoiding over-engineering with a separate service for now unless complexity grows.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | | |
