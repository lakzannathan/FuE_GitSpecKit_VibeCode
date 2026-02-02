# Research & Design Decisions: API Rate Limiting

## 1. Rate Limiting Algorithm

**Decision**: **Fixed Window Counter**

**Rationale**:

- The Feature Specification explicitly defines `RateLimitEntry` with `window_start_time` and `request_count`. This structure is characteristic of the Fixed Window algorithm.
- **Simplicity**: It is the simplest algorithm to implement using standard Python dictionaries (`dict`).
- **Memory Efficiency**: Requires storing only a timestamp and a counter per user/IP, satisfying the "Performance First" principle.
- **Compliance**: Directly satisfies FR-003 and FR-004 (limits per 60-second window).

**Alternatives Considered**:

- _Sliding Window Log_: More accurate (smoother limiting) but requires storing a timestamp for _every_ request, which grows linearly with traffic. Rejected due to higher memory overhead.
- _Token Bucket_: Good for allowing bursts, but slightly more complex to implement correctly with the "reset every minute" requirement. The Fixed Window maps better to "X requests per minute".

## 2. Concurrency & Thread Safety

**Decision**: **Single-Threaded Async (Event Loop)**

**Rationale**:

- FastAPI with `uvicorn` (default configuration) runs in a single process with a single event loop.
- `async def` endpoints run on the main thread.
- Python's `dict` operations are atomic enough for this use case within a single thread.
- Since we are not using `await` inside the critical section (checking and incrementing the counter), we do not need explicit `threading.Lock` or `asyncio.Lock`.
- **Constraint**: This solution applies to **Single Worker** deployments only. Multi-worker deployments would require an external store (Redis) or IPC, which violates the "Local Execution Only" / "In-Memory" constitution.

## 3. Testing Strategy

**Decision**: **pytest + httpx**

**Rationale**:

- **Standard**: `pytest` is the de-facto standard for Python testing. `httpx` is the recommended test client for FastAPI (supports async).
- **Integration**: Allows testing the full middleware chain including the rate limiter.
- **Mocking**: We can mock `time.time()` to deterministically test window resets without actually waiting 60 seconds.

## 4. Error Handling

**Decision**: **HTTP 429 with Retry-After**

**Rationale**:

- **Standard**: HTTP 429 is the correct status code.
- **UX**: Including a `Retry-After` header (calculated as `window_start + 60 - current_time`) gives clients precise information on when to retry, satisfying User Story 3.

## 5. Identification

**Decision**:

- **Pro User**: `x-api-key` header (exact match).
- **Free User**: `client.host` (IP address) from the FastAPI `Request` object.
