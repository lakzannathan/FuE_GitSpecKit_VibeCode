---
description: "Task list for GDPR Audit Logging feature"
---

# Tasks: GDPR Audit Logging

**Input**: Design documents from `/specs/001-gdpr-audit-logging/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md, quickstart.md

**Tests**: Automated regression tests are MANDATORY per Constitution Principle III.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: US1 (Traceability), US2 (Privacy), US3 (Performance)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Verify project structure and dependencies (FastAPI, SQLModel)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T002 Create `AuditLog` model in `src/models.py` (fields: id, timestamp, employee_id, action, details)
- [ ] T003 Update database initialization to include `AuditLog` table (verify `create_db_and_tables` in `src/database.py`)
- [ ] T004 Implement `create_audit_log_entry` helper function in `src/routers/hr.py` (or `src/services/audit.py`) to handle log creation logic

**Checkpoint**: Database model exists and helper function is ready.

---

## Phase 3: User Story 1 - Seamless Traceability (Priority: P1) 🎯 MVP

**Goal**: Log every read access and payroll calculation.

**Independent Test**: Trigger API endpoints and verify `AuditLog` table contains correct entries.

### Tests for User Story 1
- [ ] T005 [P] [US1] Create integration test for `VIEW_DETAILS` logging in `tests/integration/test_audit_logging.py`
- [ ] T006 [P] [US1] Create integration test for `CALC_PAYROLL` logging in `tests/integration/test_audit_logging.py`

### Implementation for User Story 1
- [ ] T007 [US1] Inject `BackgroundTasks` into `get_employee_details` in `src/routers/hr.py`
- [ ] T008 [US1] Implement async logging for `VIEW_DETAILS` action in `get_employee_details`
- [ ] T009 [US1] Inject `BackgroundTasks` into `run_payroll` in `src/routers/hr.py`
- [ ] T010 [US1] Implement async logging for `CALC_PAYROLL` action in `run_payroll`

**Checkpoint**: API actions are logged to the database.

---

## Phase 4: User Story 2 - Sensitive Data Protection (Priority: P1)

**Goal**: Ensure NO PII (IBAN, Salary) is ever stored in logs.

**Independent Test**: Trigger actions with sensitive data, verify logs contain only generic metadata.

### Tests for User Story 2
- [ ] T011 [P] [US2] Create unit test for PII stripping logic in `tests/unit/test_pii_stripping.py`
- [ ] T012 [P] [US2] Create integration test verifying `details` field does not contain IBAN/Salary in `tests/integration/test_audit_privacy.py`

### Implementation for User Story 2
- [ ] T013 [US2] Refine `create_audit_log_entry` to strictly filter/exclude PII from `details` field
- [ ] T014 [US2] Verify `VIEW_DETAILS` log payload is metadata-only
- [ ] T015 [US2] Verify `CALC_PAYROLL` log payload is metadata-only

**Checkpoint**: Logs are verified to be GDPR compliant (no PII).

---

## Phase 5: User Story 3 - Performance Protection (Priority: P2)

**Goal**: Logging must not block the main thread (Async/BackgroundTasks).

**Independent Test**: API response time remains stable; logs appear slightly after response (async).

### Tests for User Story 3
- [ ] T016 [P] [US3] Create performance/async verification test (ensure response returns before log write completes if possible, or check response times) in `tests/performance/test_async_logging.py`

### Implementation for User Story 3
- [ ] T017 [US3] Verify `BackgroundTasks` is correctly used for all DB writes related to logging (Code Review / Static Check)
- [ ] T018 [US3] Optimize `create_audit_log_entry` for minimal overhead

**Checkpoint**: System performance is unaffected by logging.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements and final validation

- [ ] T019 Run full regression test suite (ensure no regressions in legacy features)
- [ ] T020 Run `quickstart.md` verification steps manually
- [ ] T021 Update API documentation (OpenAPI/Swagger) if needed (already updated in contracts, ensure code reflects it)

---

## Dependencies & Execution Order

### Phase Dependencies
- **Foundational (Phase 2)**: Blocks all user stories.
- **User Story 1 (P1)**: Depends on Foundational.
- **User Story 2 (P1)**: Depends on Foundational (can run parallel with US1, but logically refines US1's output).
- **User Story 3 (P2)**: Depends on US1 implementation (to verify its performance).

### Parallel Opportunities
- T005, T006, T011, T012, T016 (Tests) can be written in parallel.
- US1 and US2 implementation can theoretically overlap, but US2 refines US1's logging content.

## Implementation Strategy

### MVP First
1. Complete Foundational (Model + Helper).
2. Implement US1 (Basic Logging).
3. Validate US2 (Privacy) & US3 (Performance) on top of US1.
