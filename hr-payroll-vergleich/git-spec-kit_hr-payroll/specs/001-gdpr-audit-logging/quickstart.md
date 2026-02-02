# Quickstart: GDPR Audit Logging

## Prerequisites

- Python 3.x
- Dependencies installed (`pip install -r requirements.txt`)
- Database initialized (`sqlite:///payroll.db`)

## Verification Steps

### 1. Verify Database Schema

Ensure the `auditlog` table exists.

```bash
# Run a script to check tables (or inspect via sqlite3 CLI)
sqlite3 payroll.db ".schema auditlog"
# Expected output: CREATE TABLE auditlog (...)
```

### 2. Verify Logging (View Details)

Trigger a read action and check the log.

```bash
# 1. Start the server
uvicorn src.main:app --reload

# 2. Make a request (in another terminal)
curl -X GET http://localhost:8000/hr/employees/1

# 3. Check the database
sqlite3 payroll.db "SELECT * FROM auditlog WHERE action='VIEW_DETAILS' ORDER BY id DESC LIMIT 1;"
```

### 3. Verify Logging (Payroll Calculation)

Trigger a payroll calculation and check the log.

```bash
# 1. Make a request
curl -X POST http://localhost:8000/hr/payroll/calculate/1

# 2. Check the database
sqlite3 payroll.db "SELECT * FROM auditlog WHERE action='CALC_PAYROLL' ORDER BY id DESC LIMIT 1;"
```

### 4. Verify PII Absence

Ensure no sensitive data is in the logs.

```bash
# Check for potential leaks (should return nothing)
sqlite3 payroll.db "SELECT * FROM auditlog WHERE details LIKE '%DE%';" 
# Note: Simple check, manual inspection recommended during development.
```
