# Rate Limit Strategy

Decision tree for choosing a rate limiting algorithm and the client-side strategy for handling API rate limits.

---

## Algorithm Decision Tree

```
What is your rate limiting goal?
│
├─ Smooth, constant request rate (no bursts allowed)
│  └─ Use: Leaky Bucket
│
├─ Allow short bursts but enforce an average rate
│  └─ Use: Token Bucket
│
├─ Simple per-window counting (easy to implement)
│  ├─ Acceptable if clients spike at window boundaries?
│  │  ├─ Yes → Fixed Window Counter
│  │  └─ No  → Sliding Window Log or Sliding Window Counter
│  └─
│
└─ Per-user fairness with global protection
   └─ Use: Token Bucket per user + Global Fixed Window
```

---

## Algorithm Comparison

### Token Bucket

**How it works:** A bucket holds up to `capacity` tokens. Tokens are added at a fixed rate (`refill_rate`). Each request consumes one token. If the bucket is empty, the request is rejected (429).

```
Configuration:
  capacity:    100 tokens (burst size)
  refill_rate: 10 tokens/second (sustained rate)

Timeline:
  t=0   bucket=100  → 50 requests → bucket=50
  t=1   bucket=60   (refilled 10) → 5 requests → bucket=55
  t=5   bucket=95   (refilled 40) → burst of 95 → bucket=0
  t=6   bucket=10   → only 10 requests allowed
```

**Pros:** Allows controlled bursts. Simple to implement. Memory-efficient (one counter + timestamp per key).

**Cons:** Burst size may surprise clients. Harder to reason about exact limits.

**Best for:** APIs that want to allow occasional bursts while enforcing a sustained rate.

### Leaky Bucket

**How it works:** Requests enter a queue (bucket) and are processed at a fixed rate. If the queue is full, new requests are rejected.

```
Configuration:
  queue_size:    50 requests
  drain_rate:    10 requests/second

Timeline:
  t=0   30 requests arrive → queue=30, processing at 10/s
  t=1   queue=20 (drained 10) + 15 new → queue=35
  t=3   queue=15 + 40 new → queue=50 (full), 5 rejected
```

**Pros:** Perfectly smooth output rate. Predictable for downstream services.

**Cons:** No burst tolerance. Adds latency (requests wait in queue). More complex to implement.

**Best for:** APIs protecting a downstream service that cannot handle bursts (e.g., database write path, third-party API with strict limits).

### Fixed Window Counter

**How it works:** Count requests in fixed time windows (e.g., per minute). Reset the counter at each window boundary.

```
Configuration:
  limit:  100 requests
  window: 60 seconds

Timeline:
  12:00:00 - 12:00:59  → 100 requests allowed, counter resets at 12:01:00
  12:00:55             → 80 requests used at 12:00:55
  12:01:01             → counter resets, 100 more requests allowed
  Problem: 80 requests at 12:00:55 + 100 at 12:01:01 = 180 in 6 seconds
```

**Pros:** Very simple. Low memory (one counter per key per window).

**Cons:** Boundary spike problem — clients can send 2x the limit across a window boundary.

**Best for:** Internal APIs where simplicity matters more than precision.

---

## Client-Side Rate Limit Strategy

### Proactive Throttling

Read rate limit headers from every response and throttle before hitting the limit:

```
After every response, read:
  X-RateLimit-Limit:     1000   (total allowed in window)
  X-RateLimit-Remaining: 47     (remaining in current window)
  X-RateLimit-Reset:     1719878400  (Unix timestamp when window resets)

Decision:
  if remaining < threshold (e.g., 5% of limit or 10 requests):
    sleep until reset_timestamp + 1 second jitter
    then continue
```

### Reactive Handling (429 Response)

```
On 429 Too Many Requests:
  1. Read Retry-After header
     - If present (seconds): sleep for that duration + random(0, 1s) jitter
     - If present (HTTP date): sleep until that time + jitter
     - If absent: use exponential backoff

  2. Exponential backoff formula:
     delay = min(base * 2^attempt + random(0, jitter_max), max_delay)
     base = 1 second
     jitter_max = 1 second
     max_delay = 60 seconds

  3. Max retries: 5 for 429 (more generous than 5xx)

  4. After max retries exhausted:
     - Log the failure with request details
     - Return error to caller (do not silently drop)
     - If this is a batch operation, continue with remaining items
```

### Batch Operation Strategy

When sending many requests (e.g., syncing 10,000 records):

```
Strategy: Leaky bucket client-side limiter

  1. Before each request:
     - Acquire a token from the local rate limiter
     - If no token available, sleep until one is refilled

  2. Configure the local limiter to stay under the API's limit:
     - Set capacity to API's burst limit (or limit / 2 for safety)
     - Set refill rate to API's sustained rate * 0.8 (80% headroom)

  3. On 429 despite local limiting:
     - Pause all requests (not just the one that got 429)
     - Sleep for Retry-After duration
     - Resume with the local limiter

  4. On partial failure in batch:
     - Process successful items
     - Queue failed items for retry
     - Apply backoff to the retry queue
```

### Multi-Client Coordination

When multiple instances of your client share the same API quota:

```
Options (from simplest to most robust):

  1. Static partitioning
     - Divide the rate limit evenly across instances
     - 1000 req/min limit, 4 instances → 250 req/min per instance
     - Simple but wastes quota if instances have uneven load

  2. Shared counter (Redis)
     - Use Redis INCR with TTL matching the rate limit window
     - All instances check the shared counter before each request
     - Accurate but adds a Redis dependency and latency

  3. Adaptive throttling
     - Start at (limit / instance_count) per instance
     - If an instance gets a 429, reduce its rate by 50%
     - If no 429 for 5 windows, increase rate by 10%
     - Self-correcting but may overshoot during scaling events
```

---

## Implementation Checklist

- [ ] Read and cache rate limit headers from every API response
- [ ] Implement proactive throttling when `remaining` drops below threshold
- [ ] Handle 429 with `Retry-After` (fallback to exponential backoff)
- [ ] Add jitter to all sleep durations to prevent thundering herd
- [ ] For batch operations, use a client-side token bucket limiter
- [ ] Set a max retry count for 429 (do not retry indefinitely)
- [ ] Log rate limit events for monitoring (how often are you hitting limits?)
- [ ] If multiple clients share a quota, coordinate via static partitioning or shared counter
