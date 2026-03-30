# HTTP Status Codes for API Design

Status codes mapped to API semantics with when-to-use rules.

---

## 2xx Success

| Code | Name | When to Use | Example |
|------|------|-------------|---------|
| 200 | OK | Successful GET, PUT, PATCH, or POST that returns data | `GET /users/42` returns the user |
| 201 | Created | Successful POST that creates a resource | `POST /users` returns the new user with `Location` header |
| 202 | Accepted | Request accepted for async processing (not yet completed) | `POST /reports/generate` queues a job |
| 204 | No Content | Successful DELETE or PUT/PATCH with no response body | `DELETE /users/42` — no body needed |

**Rules:**
- Never return 200 for a creation — use 201 with a `Location` header pointing to the new resource.
- Use 202 only when the operation is genuinely asynchronous. Include a URL to poll for status.
- 204 means "success, nothing to show." Do not return a body with 204.

---

## 3xx Redirection

| Code | Name | When to Use | Example |
|------|------|-------------|---------|
| 301 | Moved Permanently | Resource URL has permanently changed | Old versioned endpoint redirects to new |
| 304 | Not Modified | Client cache is still valid (ETag/If-None-Match) | Conditional GET with matching ETag |

**Rules:**
- Use 301 for permanent URL changes (e.g., deprecated endpoint paths). Clients and caches update their references.
- 304 is for conditional requests only. Never return it without checking `If-None-Match` or `If-Modified-Since`.

---

## 4xx Client Errors

| Code | Name | When to Use | Retryable | Example |
|------|------|-------------|-----------|---------|
| 400 | Bad Request | Malformed syntax (invalid JSON, wrong content type) | No | Unparseable JSON body |
| 401 | Unauthorized | Missing or invalid authentication credentials | Once (refresh token) | Expired JWT, missing API key |
| 403 | Forbidden | Authenticated but lacks permission for this resource | No | User tries to access admin endpoint |
| 404 | Not Found | Resource does not exist at this URL | No | `GET /users/999` when user 999 is deleted |
| 405 | Method Not Allowed | HTTP method not supported for this endpoint | No | `DELETE /users` (collection delete not allowed) |
| 409 | Conflict | Request conflicts with current resource state | Maybe (re-fetch, resolve, retry) | Creating a user with a duplicate email |
| 410 | Gone | Resource existed but has been permanently removed | No | Accessing a soft-deleted resource past retention |
| 415 | Unsupported Media Type | Content-Type header is not accepted | No | Sending XML to a JSON-only endpoint |
| 422 | Unprocessable Entity | Valid syntax but semantically invalid data | No | Email format valid JSON but fails business rules |
| 429 | Too Many Requests | Rate limit exceeded | Yes (after `Retry-After`) | Client exceeded 1000 req/min quota |

**Rules:**
- **400 vs 422:** Use 400 for syntax errors (cannot parse). Use 422 for valid syntax with invalid semantics (parsed but rejected by business logic).
- **401 vs 403:** 401 means "who are you?" (identity unknown). 403 means "I know who you are, but you cannot do this" (identity known, permission denied).
- **404 vs 410:** Use 404 when you do not want to confirm the resource ever existed. Use 410 when the client should stop requesting this resource.
- **409:** Always include enough detail for the client to resolve the conflict (e.g., which field conflicts and with what).
- **429:** Always include `Retry-After` header (seconds until the client can retry).

---

## 5xx Server Errors

| Code | Name | When to Use | Retryable | Example |
|------|------|-------------|-----------|---------|
| 500 | Internal Server Error | Unexpected server failure | Yes (with backoff) | Unhandled exception |
| 502 | Bad Gateway | Upstream service returned invalid response | Yes (with backoff) | Reverse proxy got garbage from backend |
| 503 | Service Unavailable | Server temporarily unable to handle requests | Yes (after `Retry-After`) | During deployment or maintenance |
| 504 | Gateway Timeout | Upstream service did not respond in time | Yes (with backoff) | Database query timed out behind proxy |

**Rules:**
- Never expose internal error details (stack traces, database errors) in 5xx responses. Log them server-side; return a generic message with a `request_id`.
- Always include `Retry-After` on 503 if you know when the service will recover.
- 500 is the catch-all. If you are returning 500 frequently, you are missing specific error handling.

---

## Decision Tree

```
Is the request parseable?
  No  -> 400 Bad Request
  Yes -> Is the client authenticated?
    No  -> 401 Unauthorized
    Yes -> Is the client authorized?
      No  -> 403 Forbidden
      Yes -> Does the resource exist?
        No  -> 404 Not Found
        Yes -> Is the data valid?
          No  -> 422 Unprocessable Entity
          Yes -> Does it conflict with current state?
            Yes -> 409 Conflict
            No  -> Process the request
              Server error? -> 500
              Success?
                Created? -> 201
                Async?   -> 202
                No body? -> 204
                Default  -> 200
```

---

## Headers to Include with Error Responses

| Header | When | Purpose |
|--------|------|---------|
| `Retry-After` | 429, 503 | Seconds until the client should retry |
| `WWW-Authenticate` | 401 | Describes the auth scheme expected |
| `Allow` | 405 | Lists permitted HTTP methods |
| `X-Request-Id` | All errors | Correlation ID for server-side log lookup |
