# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a custom in-memory rate limiting middleware/dependency for FastAPI.

- **Free Users**: 5 req/min (identified by IP)
- **Pro Users**: 100 req/min (identified by `x-api-key`)
- **Storage**: In-memory dictionaries (no Redis).
- **Response**: HTTP 429 with error details.

## Technical Context

**Language/Version**: Python 3.10+ (inferred from `src/main.py` usage)
**Primary Dependencies**: FastAPI, Uvicorn, Pydantic
**Storage**: In-Memory (Python `dict` / `time`) - **Strictly Local**
**Testing**: `pytest`, `httpx` (Standard for FastAPI)
**Target Platform**: Local Execution (Windows/Linux)
**Project Type**: Web Application (FastAPI)
**Performance Goals**: <1ms latency overhead per request (SC-002)
**Constraints**: No external database/cache (Redis, Memcached forbidden)
**Scale/Scope**: Low scale (Proof of Concept), 2 user tiers

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

- **Local Execution**: Does this feature require external services? **NO** (In-memory only)
- **Performance**: Is the rate limiting efficient? **YES** (Simple dictionary lookups)
- **Test-First**: Are tests planned before implementation? **YES** (pytest suite required)

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation                  | Why Needed         | Simpler Alternative Rejected Because |
| -------------------------- | ------------------ | ------------------------------------ |
| [e.g., 4th project]        | [current need]     | [why 3 projects insufficient]        |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient]  |
