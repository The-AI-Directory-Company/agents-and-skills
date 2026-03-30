# Idempotency Patterns

Patterns for ensuring operations can be safely retried without side effects: idempotency keys, webhook deduplication, Redis TTL strategies, and batch partial-failure handling.

---

## Why Idempotency Matters

In distributed systems, at-least-once delivery is the norm. Networks drop packets, services restart, and clients retry. Without idempotency:

- A retried `POST /orders` creates a duplicate order
- A re-delivered webhook triggers a double charge
- A retry after timeout applies a credit twice

Idempotency guarantees: performing the same operation N times produces the same result as performing it once.

---

## 1. Idempotency Keys

### How It Works

The client generates a unique key for each logical operation and sends it with the request. The server checks whether it has already processed that key.

```http
POST /v1/payments HTTP/1.1
Idempotency-Key: idk_8f14e45f-ceea-4f5a-a1c0-9e3d2d
Content-Type: application/json

{
  "amount": 2999,
  "currency": "usd",
  "customer_id": "cus_abc123"
}
```

### Server-Side Flow

```
Receive request with Idempotency-Key
  │
  ▼
Look up key in idempotency store
  │
  ├─ Key not found:
  │    1. Store key with status "processing"
  │    2. Execute the operation
  │    3. Store the response alongside the key with status "completed"
  │    4. Return the response
  │
  ├─ Key found, status "completed":
  │    1. Return the stored response (same status code, same body)
  │    2. Do NOT re-execute the operation
  │
  └─ Key found, status "processing":
       1. Return 409 Conflict or 425 Too Early
       2. Client should wait and retry
```

### Key Generation Rules

| Rule | Rationale |
|------|-----------|
| Use UUIDv4 or ULID | Globally unique without coordination |
| Generate client-side | Server cannot know the client's intent |
| One key per logical operation | Changing the amount but reusing the key should fail |
| Never reuse keys across different operations | A key is bound to one specific request payload |

### Storage Schema

```sql
CREATE TABLE idempotency_keys (
    key          VARCHAR(255) PRIMARY KEY,
    status       VARCHAR(20) NOT NULL,  -- 'processing', 'completed', 'failed'
    request_hash VARCHAR(64),           -- SHA-256 of request body (to detect misuse)
    response_code INTEGER,
    response_body JSONB,
    created_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at   TIMESTAMP NOT NULL     -- TTL for cleanup
);

CREATE INDEX idx_idempotency_expires ON idempotency_keys (expires_at);
```

### TTL Recommendations

| Use Case | TTL | Rationale |
|----------|-----|-----------|
| Payment processing | 24-48 hours | Covers retry windows and support investigation |
| Order creation | 24 hours | Client retry windows are typically < 1 hour |
| Data sync operations | 1-4 hours | Frequent operations; short retry window |
| Webhook delivery | 72 hours | Webhooks may be retried over extended periods |

---

## 2. Webhook Deduplication

### The Problem

Webhook providers guarantee at-least-once delivery. The same event may be delivered 2-5 times due to timeouts, retries, or infrastructure issues.

### Deduplication Strategy

```
Receive webhook
  │
  ▼
Extract the event ID (e.g., evt_abc123 or X-Webhook-ID header)
  │
  ▼
Check deduplication store:
  │
  ├─ Event ID not seen:
  │    1. Store event ID with status "processing"
  │    2. Process the webhook
  │    3. Update status to "processed"
  │    4. Return 200 OK
  │
  ├─ Event ID seen, status "processed":
  │    1. Return 200 OK (acknowledge without reprocessing)
  │
  └─ Event ID seen, status "processing":
       1. Return 200 OK (another instance is handling it)
       2. Or return 409 if you want the provider to retry later
```

### Implementation with Redis

```
# Check and claim in one atomic operation
result = SETNX webhook:{event_id} "processing"
EXPIRE webhook:{event_id} 259200  # 72 hours TTL

if result == 1:
    # First time seeing this event — process it
    process_webhook(event)
    SET webhook:{event_id} "processed"
    EXPIRE webhook:{event_id} 259200
else:
    # Duplicate — already processing or processed
    return 200 OK
```

### Important: Always Return 200 for Duplicates

If you return a non-2xx status for a duplicate webhook, the provider will keep retrying — creating more duplicates. Always acknowledge receipt, even if you skip processing.

---

## 3. Redis TTL Patterns for Idempotency

### Pattern A: Simple SETNX

For lightweight deduplication where you only need to track "seen or not seen."

```
SET idempotent:{key} "1" NX EX 3600
```

- `NX` — only set if the key does not exist (atomic check-and-set)
- `EX 3600` — expire after 1 hour
- Returns OK if set (first time), nil if already exists (duplicate)

### Pattern B: SETNX + Stored Response

For full idempotency where duplicates must return the original response.

```
# Attempt to claim
SETNX idempotent:{key} '{"status":"processing"}'
EXPIRE idempotent:{key} 86400

# After processing, store the response
SET idempotent:{key} '{"status":"completed","response":{"id":"ord_123","total":2999}}'
EXPIRE idempotent:{key} 86400

# On duplicate request
GET idempotent:{key}
# Returns the stored response
```

### Pattern C: Lua Script for Atomicity

When the check-and-set must be truly atomic (no race condition between SETNX and EXPIRE):

```lua
-- KEYS[1] = idempotency key
-- ARGV[1] = TTL in seconds
-- ARGV[2] = initial value

local exists = redis.call('EXISTS', KEYS[1])
if exists == 1 then
    return redis.call('GET', KEYS[1])
else
    redis.call('SET', KEYS[1], ARGV[2], 'EX', ARGV[1])
    return nil
end
```

### TTL Cleanup

Redis handles TTL expiration automatically. For database-backed stores, run periodic cleanup:

```sql
DELETE FROM idempotency_keys WHERE expires_at < NOW();
```

Run this as a scheduled job (e.g., every hour). Index on `expires_at` for performance.

---

## 4. Batch Partial-Failure Handling

### The Problem

A batch of 100 records is submitted. 97 succeed, 3 fail. What happens?

### Strategy: Process Successes, Isolate Failures

```json
POST /v1/orders/batch
{
  "items": [
    { "product_id": "prod_1", "quantity": 2 },
    { "product_id": "prod_2", "quantity": 1 },
    { "product_id": "prod_3", "quantity": -1 }
  ]
}
```

Response (HTTP 207 Multi-Status):

```json
{
  "summary": {
    "total": 3,
    "succeeded": 2,
    "failed": 1
  },
  "results": [
    { "index": 0, "status": 201, "data": { "id": "ord_001" } },
    { "index": 1, "status": 201, "data": { "id": "ord_002" } },
    {
      "index": 2,
      "status": 422,
      "error": {
        "code": "VALIDATION_ERROR",
        "message": "Quantity must be positive",
        "details": [{ "field": "quantity", "reason": "Must be >= 1" }]
      }
    }
  ]
}
```

### Design Decisions

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| Atomicity | All-or-nothing (transaction) | Partial success | Partial success for large batches; all-or-nothing for small, related items |
| Status code | 200 (always) | 207 Multi-Status | 207 when results are mixed; 200 when all succeed; 422 when all fail |
| Failed items | Inline in response | Separate error array | Inline with `index` field to correlate with the request |
| Retry | Client retries failed items only | Client retries entire batch | Retry failed items only (with their idempotency keys) |

### Idempotency for Batch Items

Assign an idempotency key per item, not per batch:

```json
{
  "items": [
    { "idempotency_key": "idk_001", "product_id": "prod_1", "quantity": 2 },
    { "idempotency_key": "idk_002", "product_id": "prod_2", "quantity": 1 },
    { "idempotency_key": "idk_003", "product_id": "prod_3", "quantity": 5 }
  ]
}
```

On retry, the server skips items whose idempotency keys are already completed and only processes new or failed items. The client can safely retry the entire batch without duplicating previously successful items.

---

## Checklist

- [ ] Every non-idempotent endpoint (POST, PATCH) accepts an `Idempotency-Key` header
- [ ] Server stores idempotency keys with TTL and returns cached responses for duplicates
- [ ] Request body hash is stored to detect key reuse with different payloads
- [ ] Webhook handler deduplicates by event ID before processing
- [ ] Duplicate webhooks always return 200 (never trigger reprocessing)
- [ ] Batch endpoints return per-item status with index correlation
- [ ] Failed batch items can be retried independently with per-item idempotency keys
- [ ] Idempotency store has TTL cleanup (Redis expiry or scheduled database purge)
