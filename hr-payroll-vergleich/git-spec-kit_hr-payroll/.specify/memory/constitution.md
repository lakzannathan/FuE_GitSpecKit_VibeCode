<!-- Sync Impact Report
- Version change: 0.0.0 -> 1.0.0
- Added Principle: I. Data Privacy & GDPR (Critical Constraint)
- Added Principle: II. System Integrity & Performance
- Added Principle: III. Quality Assurance (Testing)
- Templates requiring updates: None (Templates are generic enough to support these constraints)
-->
# HR Payroll Legacy System Constitution

## Core Principles

### I. Data Privacy & GDPR (Critical Constraint)
**Principle of "Data Minimization"**: Sensitive Personally Identifiable Information (PII) such as IBAN, Tax IDs, or Salary totals MUST NEVER be stored in cleartext in logs.
**Audit Logging**: The audit log MUST store exclusively metadata (Who, When, What Action). It MUST NEVER store payload data.

### II. System Integrity & Performance
**Legacy Engine Inviolability**: The existing `legacy_engine.py` (Complexity Rank D) is extremely fragile. It MUST NOT be refactored, modified, or directly imported for the purpose of modification.
**Non-Blocking Operations**: The system suffers from blocking legacy code. `fastapi.BackgroundTasks` MUST be used for all database write operations to ensure responsiveness.

### III. Quality Assurance (Testing)
**Mandatory Regression Testing**: Automated regression tests MUST be created for every new feature to ensure no regressions are introduced into the critical legacy system.

## Governance

This constitution governs the development and maintenance of the HR Payroll Legacy System. Due to the critical and fragile nature of the legacy components, strict adherence to these principles is mandatory.

**Compliance Reviews**: All code changes must be reviewed specifically for:
1. Absence of PII in logs.
2. No modifications to `legacy_engine.py`.
3. Proper use of `BackgroundTasks` for DB writes.
4. Presence of regression tests.

**Version**: 1.0.0 | **Ratified**: 2026-01-27 | **Last Amended**: 2026-01-27
