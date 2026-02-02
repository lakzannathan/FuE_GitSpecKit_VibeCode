# Feature Specification: API Rate Limiting

**Feature Branch**: `001-api-rate-limiting`
**Created**: 2025-12-17
**Status**: Draft
**Input**: User description: "Konzeptioniere ein Rate Limiting für die API. Unterscheidung der User-Gruppen: - 'Free User': Hat keinen API Key im Header. Limit: 5 Requests pro Minute. - 'Pro User': Hat Header 'x-api-key' mit Wert 'secret-pro-key'. Limit: 100 Requests pro Minute. Ziel ist es, die Ressourcennutzung der 'analyze' Route zu steuern."

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Free User Rate Limiting (Priority: P1)

As a Free User (without an API key), I want to be able to use the API up to a reasonable limit (5 requests/minute) so that I can test the service without registering, but I accept that I cannot overuse it.

**Why this priority**: Essential to prevent abuse and resource exhaustion from anonymous users, which is the primary goal of this feature.

**Independent Test**: Can be fully tested by sending 6 requests in rapid succession without an API key and verifying the 6th is blocked.

**Acceptance Scenarios**:

1. **Given** a Free User (no `x-api-key` header), **When** they send 5 requests within 1 minute, **Then** all 5 requests are successful (HTTP 200).
2. **Given** a Free User, **When** they send a 6th request within the same minute, **Then** the request is rejected with HTTP 429 Too Many Requests.
3. **Given** a Free User who has been rate-limited, **When** they wait for the minute window to expire, **Then** they can successfully make requests again.

---

### User Story 2 - Pro User Rate Limiting (Priority: P1)

As a Pro User (with a valid API key), I want to have a higher rate limit (100 requests/minute) so that I can integrate the API into my production workflow.

**Why this priority**: Critical to support paying/authenticated users and differentiate service tiers.

**Independent Test**: Can be tested by sending >5 requests with the correct API key and verifying they are NOT blocked until the 100th request.

**Acceptance Scenarios**:

1. **Given** a Pro User (header `x-api-key: secret-pro-key`), **When** they send 6 requests within 1 minute, **Then** all requests are successful (HTTP 200).
2. **Given** a Pro User, **When** they send 101 requests within 1 minute, **Then** the 101st request is rejected with HTTP 429 Too Many Requests.

---

### User Story 3 - Rate Limit Feedback (Priority: P2)

As an API Consumer, I want to receive clear feedback when I am rate limited so that I know why my request failed and when I can try again.

**Why this priority**: Improves developer experience and allows clients to handle backoff gracefully.

**Independent Test**: Inspect the response headers/body of a 429 response.

**Acceptance Scenarios**:

1. **Given** a user exceeds their limit, **When** the system rejects the request, **Then** the response status code is 429.
2. **Given** a user exceeds their limit, **When** the system rejects the request, **Then** the response body contains a helpful error message (e.g., "Rate limit exceeded").

---

### Edge Cases

- What happens when the `x-api-key` is present but invalid (not `secret-pro-key`)? (Assumption: Treat as Free User or Unauthorized? Defaulting to Unauthorized 401 or Forbidden 403 is standard, but for this specific requirement, if the key doesn't match "Pro", they fall back to "Free" rules or get rejected. **Assumption**: Invalid key -> 403 Forbidden to prevent guessing, or treat as Free. Let's assume Invalid Key = 403 Forbidden for security).
- How does the system handle concurrent requests? (Must be thread-safe).
- What happens if the system restarts? (In-memory counters are lost, limits reset - acceptable per "Local Execution" principle).

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST identify "Pro Users" by the presence of the header `x-api-key` with exact value `secret-pro-key`.
- **FR-002**: System MUST treat requests without the `x-api-key` header as "Free Users".
- **FR-003**: System MUST limit "Free Users" to maximum 5 requests per 60-second window.
- **FR-004**: System MUST limit "Pro Users" to maximum 100 requests per 60-second window.
- **FR-005**: System MUST identify "Free Users" by their IP address to apply limits per client.
- **FR-006**: System MUST return HTTP Status 429 "Too Many Requests" when a limit is exceeded.
- **FR-007**: System MUST track request counts in-memory (no external database).

### Key Entities _(include if feature involves data)_

- **RateLimitEntry**: Represents the usage state for a client.
  - `client_identifier` (string): IP address or API Key.
  - `request_count` (integer): Number of requests in current window.
  - `window_start_time` (timestamp): When the current counting window began.

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Free users are strictly blocked at the 6th request within a minute.
- **SC-002**: Rate limiting logic adds <1ms latency to the request processing time (Performance First).
- **SC-003**: Pro users can successfully execute 100 requests/minute without rejection.
- **SC-004**: 100% of rejected requests return HTTP 429.
