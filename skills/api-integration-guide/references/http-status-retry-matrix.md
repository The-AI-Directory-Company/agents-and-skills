# HTTP Status Code Retry Matrix

Error classification table for API integration clients. Defines whether each status code is retryable, the recommended action, and the retry strategy.

---

## Classification Table

| Status | Name | Category | Retryable | Max Retries | Action |
|--------|------|----------|-----------|-------------|--------|
| 400 | Bad Request | Client error | No | 0 | Log the full request payload and response body. Fix the request. Do not retry — the same payload will fail every time. |
| 401 | Unauthorized | Auth error | Once | 1 | Refresh the access token (or re-authenticate). Retry the original request once with the new token. If it fails again, escalate — credentials may be revoked. |
| 403 | Forbidden | Permission error | No | 0 | Log the endpoint and scopes. Alert the team. Check API key permissions or OAuth scopes. Do not retry — the client lacks permission. |
| 404 | Not Found | Client error | No | 0 | Handle as a missing resource in application logic. Do not retry — the resource does not exist. If unexpected, verify the URL construction. |
| 405 | Method Not Allowed | Client error | No | 0 | Check the HTTP method against API documentation. Log and fix. |
| 409 | Conflict | State conflict | Conditional | 1-2 | Re-fetch the current resource state, resolve the conflict (e.g., update the version field), and retry. If the conflict persists after 2 attempts, alert. |
| 410 | Gone | Client error | No | 0 | The resource has been permanently removed. Remove references to it. Do not retry. |
| 415 | Unsupported Media Type | Client error | No | 0 | Check Content-Type header. Fix the request format. |
| 422 | Unprocessable Entity | Validation error | No | 0 | Parse the error details array. Log field-level errors. Fix input data. Do not retry — the data is semantically invalid. |
| 429 | Too Many Requests | Rate limit | Yes | 5 | Read `Retry-After` header. Sleep for that duration plus random jitter (0-1s). If no `Retry-After`, use exponential backoff starting at 1s. |
| 500 | Internal Server Error | Server error | Yes | 3 | Exponential backoff: `delay = min(base * 2^attempt + jitter, max_delay)`. Base = 1s, max = 30s. Log the request_id from the response for support. |
| 502 | Bad Gateway | Infrastructure | Yes | 5 | Same backoff as 500. Likely a transient proxy or load balancer issue. |
| 503 | Service Unavailable | Infrastructure | Yes | 5 | Read `Retry-After` if present. Otherwise, exponential backoff. The service is temporarily down (deployment, maintenance, overload). |
| 504 | Gateway Timeout | Infrastructure | Yes | 3 | Same backoff as 500. Consider increasing the client timeout if this is frequent. For long operations, switch to async polling pattern. |
| Timeout | Connection/Read timeout | Network | Yes | 3 | Same backoff as 5xx. Verify the request is idempotent before retrying — non-idempotent requests (POST without idempotency key) risk duplicate side effects. |
| Connection refused | TCP error | Network | Yes | 5 | Host is unreachable. Backoff and retry. If persistent, check DNS resolution and firewall rules. |
| SSL/TLS error | Certificate error | Security | No | 0 | Do not retry. Certificate validation failures indicate misconfiguration or a potential MITM attack. Alert immediately. |

---

## Retry Formula

```
delay = min(base_delay * 2^attempt + random(0, jitter_max), max_delay)
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `base_delay` | 1 second | Initial delay before first retry |
| `jitter_max` | 1 second | Random jitter added to prevent thundering herd |
| `max_delay` | 60 seconds | Upper bound on delay between retries |
| `max_retries` | 3 (5xx) / 5 (429, 502, 503) | Total retry attempts before giving up |

**Example progression (base=1s, jitter up to 1s):**

| Attempt | Calculated Delay | With Jitter (example) |
|---------|------------------|-----------------------|
| 1 | 1s | 1.4s |
| 2 | 2s | 2.7s |
| 3 | 4s | 4.2s |
| 4 | 8s | 8.9s |
| 5 | 16s | 16.3s |

---

## Decision Flowchart

```
Received HTTP response
  |
  Is status 2xx?
    Yes -> Success. Process response.
    No  -> Is status 401?
      Yes -> Have we already refreshed the token this request?
        Yes -> Fail. Credentials are invalid.
        No  -> Refresh token. Retry once.
      No  -> Is status 429?
        Yes -> Read Retry-After. Sleep. Retry (up to 5 times).
        No  -> Is status 5xx or network error?
          Yes -> Is the request idempotent (GET, PUT, DELETE, or has idempotency key)?
            Yes -> Exponential backoff. Retry (up to max_retries).
            No  -> Log the failure. Do NOT retry. Alert for manual resolution.
          No  -> Is status 409?
            Yes -> Re-fetch resource. Resolve conflict. Retry (up to 2 times).
            No  -> Permanent client error (400, 403, 404, 422). Do not retry.
```

---

## Idempotency Warning

Before retrying any non-GET request, verify idempotency:

| Method | Idempotent by Spec | Safe to Retry |
|--------|-------------------|---------------|
| GET | Yes | Always |
| PUT | Yes | Always |
| DELETE | Yes | Always |
| PATCH | No | Only with idempotency key |
| POST | No | Only with idempotency key |

For POST and PATCH without an idempotency key, a retry after a timeout may create a duplicate resource or apply the operation twice. Either add an `Idempotency-Key` header or accept the risk and handle duplicates downstream.
