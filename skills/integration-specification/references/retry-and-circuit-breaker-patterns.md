# Retry and Circuit Breaker Patterns

Exponential backoff, jitter strategies, circuit breaker state machines, and dead-letter queue design for integration specifications.

---

## Exponential Backoff

### Formula

```
delay = min(base_delay * 2^attempt + jitter, max_delay)
```

### Configuration

| Parameter | Recommended Default | Description |
|-----------|-------------------|-------------|
| `base_delay` | 1 second | Delay before the first retry |
| `max_delay` | 60 seconds | Upper bound on any single delay |
| `max_retries` | 5 | Total retry attempts before giving up |
| `jitter` | See strategies below | Randomization to prevent thundering herd |

### Delay Progression (base=1s, no jitter)

| Attempt | Delay | Cumulative Wait |
|---------|-------|-----------------|
| 1 | 1s | 1s |
| 2 | 2s | 3s |
| 3 | 4s | 7s |
| 4 | 8s | 15s |
| 5 | 16s | 31s |

---

## Jitter Strategies

### Full Jitter (Recommended)

```
delay = random(0, min(base_delay * 2^attempt, max_delay))
```

Spreads retries across the entire delay window. Best for reducing contention when many clients retry simultaneously.

### Equal Jitter

```
half = min(base_delay * 2^attempt, max_delay) / 2
delay = half + random(0, half)
```

Guarantees a minimum delay of half the calculated backoff. Balances spread with a floor.

### Decorrelated Jitter

```
delay = min(random(base_delay, previous_delay * 3), max_delay)
```

Each delay is based on the previous delay, not the attempt number. Produces more varied retry timing.

### Comparison

| Strategy | Min Delay | Max Delay | Spread | Best For |
|----------|-----------|-----------|--------|----------|
| No jitter | Exact backoff | Exact backoff | None | Single client (never use in distributed systems) |
| Full jitter | 0 | Backoff value | Maximum | High-contention scenarios (many clients) |
| Equal jitter | Backoff / 2 | Backoff | Moderate | When a minimum wait is needed |
| Decorrelated | base_delay | 3x previous | High | When retry patterns should be unpredictable |

---

## Circuit Breaker

### State Machine

```
         success_count >= threshold
    ┌─────────────────────────────────────┐
    │                                     ▼
┌───────┐    failure >= threshold    ┌────────┐    timeout elapsed    ┌───────────┐
│ CLOSED │ ──────────────────────── │  OPEN  │ ──────────────────── │ HALF-OPEN │
│(normal)│                          │(reject)│                      │  (probe)  │
└───────┘                           └────────┘                      └───────────┘
    ▲                                    ▲                               │
    │                                    │         probe fails           │
    │                                    └───────────────────────────────┘
    │                                                                    │
    │              probe succeeds                                        │
    └────────────────────────────────────────────────────────────────────┘
```

### States

| State | Behavior | Transitions |
|-------|----------|-------------|
| **Closed** | All requests pass through. Failures are counted. | If `failure_count >= failure_threshold` within `window`, transition to **Open**. |
| **Open** | All requests are immediately rejected without calling the downstream service. Returns a fallback or error. | After `open_timeout` elapses, transition to **Half-Open**. |
| **Half-Open** | Allow a limited number of probe requests through. | If probe succeeds (`success_threshold` times), transition to **Closed**. If probe fails, transition back to **Open**. |

### Configuration

| Parameter | Recommended Default | Description |
|-----------|-------------------|-------------|
| `failure_threshold` | 5-10 consecutive failures | Number of failures to trip the circuit |
| `failure_window` | 60 seconds | Time window for counting failures |
| `open_timeout` | 30-300 seconds | How long to stay open before probing |
| `success_threshold` | 3 | Probe successes needed to close the circuit |
| `half_open_max_calls` | 3 | Max concurrent requests in half-open state |

### What Counts as a Failure

Include:
- HTTP 5xx responses
- Connection timeouts
- Connection refused errors
- Read timeouts

Exclude:
- HTTP 4xx responses (client errors are not downstream failures)
- HTTP 429 (rate limiting is not a failure; handle separately)
- Intentional rejections (e.g., validation errors)

### Fallback Strategies When Circuit is Open

| Strategy | When to Use | Example |
|----------|-------------|---------|
| Cached response | Read operations with stale-tolerant data | Return last successful inventory count |
| Default value | Non-critical enrichment data | Return empty recommendations |
| Queue for later | Write operations that can be deferred | Write to a retry queue, process when circuit closes |
| Fail fast | Critical operations with no fallback | Return 503 to the caller immediately |

---

## Dead-Letter Queue (DLQ) Design

### When Messages Go to the DLQ

A message enters the DLQ when:

1. All retry attempts are exhausted (e.g., 5 retries with backoff)
2. The error is classified as permanent (400, 422, schema validation failure)
3. The message has been in the retry queue longer than the maximum retention period
4. The circuit breaker is open and the message's deadline has passed

### DLQ Schema

Each DLQ entry should capture:

```json
{
  "id": "dlq_abc123",
  "original_message": { ... },
  "source_queue": "orders.sync",
  "destination": "https://api.warehouse.com/v1/orders",
  "first_attempt_at": "2024-06-23T10:00:00Z",
  "last_attempt_at": "2024-06-23T10:15:32Z",
  "attempt_count": 5,
  "last_error": {
    "status_code": 500,
    "code": "INTERNAL_ERROR",
    "message": "Database connection pool exhausted",
    "request_id": "req_xyz789"
  },
  "error_category": "transient",
  "expires_at": "2024-06-30T10:00:00Z"
}
```

### DLQ Operations

| Operation | Description |
|-----------|-------------|
| **Inspect** | View DLQ messages with filtering by error category, source, date range |
| **Replay** | Re-submit a single message or batch back to the original queue |
| **Replay all** | Re-submit all messages (use after fixing the root cause) |
| **Purge** | Delete messages older than the retention period |
| **Alert** | Trigger alert when DLQ depth exceeds threshold |

### DLQ Alerting

| Metric | Threshold | Severity |
|--------|-----------|----------|
| DLQ depth > 0 | Any new message | Warning (first occurrence) |
| DLQ depth > 100 | Sustained for 10 minutes | Critical |
| DLQ growth rate | > 10 messages/minute | Critical |
| Oldest message age | > 24 hours unreplayed | Warning |

---

## Putting It Together: Retry Pipeline

```
Request arrives
  │
  ▼
Is circuit breaker OPEN?
  Yes → Fallback or fast-fail (do not attempt the request)
  No  ↓
  │
  Attempt request
  │
  Success? → Done
  │
  Failure → Is the error retryable? (5xx, timeout, 429)
    No  → Send to DLQ immediately (permanent error)
    Yes ↓
    │
    Retries remaining?
      No  → Send to DLQ (exhausted retries)
      Yes → Sleep (exponential backoff + jitter)
            │
            Retry request
            │
            Update circuit breaker failure count
            │
            Loop back to "Attempt request"
```
