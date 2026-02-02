---
description: "Task list for API Rate Limiting feature"
---

# Tasks: API Rate Limiting

**Input**: Design documents from `/specs/001-api-rate-limiting/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: MANDATORY per Constitution Principle III.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure (new files) per implementation plan
- [x] T002 [P] Install/Verify dependencies (FastAPI, Uvicorn) in requirement.txt
- [x] T003 [P] Configure pytest in pyproject.toml or pytest.ini (if not exists)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create RateLimitEntry data model in src/rate_limiter.py
- [x] T005 Implement global in-memory store in src/rate_limiter.py
- [x] T006 [P] Create test fixtures (client, mock time) in tests/conftest.py
- [x] T007 Define custom RateLimitExceeded exception in src/rate_limiter.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Free User Rate Limiting (Priority: P1) 🎯 MVP

**Goal**: Limit users without API key to 5 requests/minute.

**Independent Test**: Send 6 requests without header, verify 6th is 429.

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T008 [P] [US1] Create unit test for Free User limit logic in tests/test_rate_limiter.py
- [x] T009 [P] [US1] Create integration test for /analyze endpoint (Free User) in tests/test_rate_limiter.py

### Implementation for User Story 1

- [x] T010 [US1] Implement `check_rate_limit` function for Free Users in src/rate_limiter.py
- [x] T011 [US1] Create dependency `get_rate_limiter` in src/dependencies.py
- [x] T012 [US1] Integrate dependency into `/analyze` endpoint in src/main.py
- [x] T013 [US1] Implement 429 error handler with Retry-After header in src/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Pro User Rate Limiting (Priority: P1)

**Goal**: Limit users with valid API key to 100 requests/minute.

**Independent Test**: Send >5 requests with key, verify success. Send 101, verify 429.

### Tests for User Story 2 (MANDATORY) ⚠️

- [x] T014 [P] [US2] Create unit test for Pro User limit logic in tests/test_rate_limiter.py
- [x] T015 [P] [US2] Create integration test for /analyze endpoint (Pro User) in tests/test_rate_limiter.py

### Implementation for User Story 2

- [x] T016 [US2] Update `check_rate_limit` to handle API Key logic in src/rate_limiter.py
- [x] T017 [US2] Update dependency to extract `x-api-key` header in src/dependencies.py
- [x] T018 [US2] Verify Pro User flow in src/main.py (ensure logic uses new limiter)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Rate Limit Feedback (Priority: P2)

**Goal**: Provide clear error messages and Retry-After headers.

**Independent Test**: Inspect 429 response body and headers.

### Tests for User Story 3 (MANDATORY) ⚠️

- [x] T019 [P] [US3] Create test for 429 response structure (headers/body) in tests/test_rate_limiter.py

### Implementation for User Story 3

- [x] T020 [US3] Refine exception handler to return JSON body with "detail" in src/main.py
- [x] T021 [US3] Ensure `Retry-After` header is calculated correctly in src/rate_limiter.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T022 [P] Update docstrings in src/rate_limiter.py
- [x] T023 Run full test suite and verify all scenarios pass
- [x] T024 Verify manual test scenarios from quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Extends US1 logic
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Refines error handling

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Create unit test for Free User limit logic in tests/test_rate_limiter.py"
Task: "Create integration test for /analyze endpoint (Free User) in tests/test_rate_limiter.py"

# Launch implementation:
Task: "Implement check_rate_limit function for Free Users in src/rate_limiter.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories
