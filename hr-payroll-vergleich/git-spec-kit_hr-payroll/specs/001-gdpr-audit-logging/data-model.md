# Data Model: GDPR Audit Logging

## Entities

### AuditLog

Represents a single audit event for compliance tracking.

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `id` | `int` | Yes | Unique identifier | Primary Key, Auto-increment |
| `timestamp` | `datetime` | Yes | Time of the event | UTC, Default: `datetime.utcnow` |
| `employee_id` | `int` | Yes | ID of the accessed employee | Foreign Key to `Employee.id` |
| `action` | `str` | Yes | Type of operation | Enum-like: "VIEW_DETAILS", "CALC_PAYROLL" |
| `details` | `str` | No | Metadata about the event | **NO PII ALLOWED** |

## Relationships

- **AuditLog** (Many) -> (One) **Employee**: Each log entry refers to one employee record.

## Validation Rules

1. **PII Check**: The `details` field must be validated (application logic) to ensure it does not contain patterns resembling IBANs or salary figures.
2. **Action Validity**: `action` must be one of the defined allowed actions.
