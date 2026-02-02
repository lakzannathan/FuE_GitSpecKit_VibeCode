# Quickstart: API Rate Limiting

## Prerequisites

- Python 3.10+
- Virtual environment activated

## Installation

```bash
pip install -r requirement.txt
```

## Running the Service

```bash
uvicorn src.main:app --reload
```

## Testing Rate Limits

### Free User (No Key)

Limit: 5 requests / minute

```bash
# Run 6 times to trigger 429
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World"}'
```

### Pro User (With Key)

Limit: 100 requests / minute

```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -H "x-api-key: secret-pro-key" \
  -d '{"text": "Hello World"}'
```

## Running Tests

```bash
pytest
```
