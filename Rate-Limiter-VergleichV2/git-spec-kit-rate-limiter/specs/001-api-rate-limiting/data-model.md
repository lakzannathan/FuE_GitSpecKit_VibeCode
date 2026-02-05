# Data Model: In-Memory Rate Limiter

## Entities

### RateLimitEntry

Represents the usage state for a single client (IP or API Key).

| Field               | Type    | Description                                             |
| ------------------- | ------- | ------------------------------------------------------- |
| `request_count`     | `int`   | Number of requests made in the current window.          |
| `window_start_time` | `float` | Timestamp (Unix epoch) when the current window started. |

## Storage Structure

The application will maintain a global dictionary to store these entries.

```python
# Type Definition
type ClientID = str  # IP Address or API Key

# Global Store
rate_limit_store: dict[ClientID, RateLimitEntry] = {}
```

## Constants

| Constant              | Value              | Description                             |
| --------------------- | ------------------ | --------------------------------------- |
| `WINDOW_SIZE_SECONDS` | `60`               | Duration of the rate limiting window.   |
| `LIMIT_FREE`          | `5`                | Max requests per window for Free users. |
| `LIMIT_PRO`           | `100`              | Max requests per window for Pro users.  |
| `PRO_KEY`             | `"secret-pro-key"` | The API key value for Pro users.        |
