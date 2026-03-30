# Bad vs Corrected API Design

Side-by-side comparisons across eight design dimensions. Each section shows the problematic pattern, explains why it fails, and provides the corrected version.

---

## 1. Resource Naming

### Bad

```
GET /api/getActiveUsers
GET /api/fetchOrderByID?order_id=42
POST /api/createNewProduct
DELETE /api/removeUser/55
```

**Why it fails:** Verbs in URLs duplicate HTTP method semantics. Mixed casing (`getActiveUsers`, `fetchOrderByID`) breaks consistency. `/api` prefix is redundant when the entire host serves the API.

### Corrected

```
GET /v1/users?status=active
GET /v1/orders/42
POST /v1/products
DELETE /v1/users/55
```

- Plural nouns for collections
- Lowercase with hyphens for multi-word resources (`/order-items`)
- Filters as query parameters, not URL path verbs
- HTTP method conveys the action

---

## 2. Error Handling

### Bad

```json
HTTP 200 OK

{
  "success": false,
  "msg": "bad request"
}
```

**Why it fails:** Returns 200 for errors, forcing clients to parse the body to detect failures. `"msg": "bad request"` gives no actionable detail. No error code for programmatic handling. No request ID for debugging.

### Corrected

```json
HTTP 422 Unprocessable Entity

{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email address is not valid.",
    "details": [
      { "field": "email", "reason": "Must match format user@domain.tld" }
    ],
    "request_id": "req_7xk29m"
  }
}
```

- HTTP status code reflects the error category
- Machine-readable `code` for programmatic handling
- Human-readable `message` for logs and developer UX
- `details` array pinpoints each invalid field
- `request_id` for cross-referencing with server logs

---

## 3. Pagination

### Bad

```
GET /v1/orders
```

Returns all 84,000 orders in a single response. No limit, no pagination metadata.

```json
[
  { "id": 1, "total": 29.99 },
  { "id": 2, "total": 15.00 },
  ...
]
```

**Why it fails:** Unbounded response kills client memory and server throughput. Bare array prevents adding metadata without a breaking change.

### Corrected (cursor-based)

```
GET /v1/orders?limit=20&cursor=eyJpZCI6MTAwfQ
```

```json
{
  "data": [
    { "id": 101, "total": 29.99 },
    { "id": 102, "total": 15.00 }
  ],
  "meta": {
    "per_page": 20,
    "next_cursor": "eyJpZCI6MTIwfQ",
    "has_more": true
  },
  "links": {
    "next": "/v1/orders?limit=20&cursor=eyJpZCI6MTIwfQ"
  }
}
```

- Default limit of 20, max 100
- Wrapped response with `data`, `meta`, and `links`
- Cursor-based for stable pagination across inserts/deletes
- `has_more` flag prevents off-by-one infinite loops

---

## 4. Versioning

### Bad

```
GET /orders
```

Field `user_name` renamed to `customer_name` in the same endpoint without a version bump. Existing clients break silently.

### Corrected

```
GET /v1/orders   -> returns { "user_name": "Alice" }
GET /v2/orders   -> returns { "customer_name": "Alice" }
```

- URL-prefix versioning for public APIs
- Breaking changes require a major version increment
- v1 continues working with a published deprecation timeline
- New fields can be added to an existing version (non-breaking)
- Removed or renamed fields require a new version

**Deprecation header on v1 responses:**

```
Deprecation: Sun, 01 Sep 2025 00:00:00 GMT
Sunset: Sun, 01 Dec 2025 00:00:00 GMT
Link: </v2/orders>; rel="successor-version"
```

---

## 5. Authentication

### Bad

```
GET /v1/users?api_key=sk_live_abc123def456
```

**Why it fails:** API key in the URL is logged in server access logs, browser history, proxy logs, and referrer headers. Plaintext credential exposure.

### Corrected

```
GET /v1/users
Authorization: Bearer sk_live_abc123def456
```

- Credentials in the `Authorization` header, never in URLs or query strings
- HTTPS required for all endpoints (refuse plaintext HTTP)
- Keys scoped to minimum required permissions
- Short-lived tokens (JWT) for user-facing flows; long-lived API keys only for server-to-server with rotation policy

---

## 6. Rate Limiting

### Bad

```
HTTP 500 Internal Server Error

{ "error": "Too many requests, try again later" }
```

**Why it fails:** Returns 500 instead of 429. No rate limit headers. No `Retry-After`. Client has no way to know its quota, remaining budget, or when to retry.

### Corrected

```
HTTP 429 Too Many Requests
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1719878400
Retry-After: 45

{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Request limit exceeded. Retry after 45 seconds.",
    "request_id": "req_9abc12"
  }
}
```

- Correct 429 status code
- `X-RateLimit-*` headers on every response (not just 429)
- `Retry-After` tells the client exactly how long to wait
- Consistent error envelope

**Rate limit headers on successful responses too:**

```
HTTP 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 847
X-RateLimit-Reset: 1719878400
```

---

## 7. Filtering

### Bad

```
POST /v1/users/search
{
  "query": "status=active AND role=admin AND created>2024-01-01"
}
```

**Why it fails:** Custom query language requires documentation, parsing, and is error-prone. POST for a read operation breaks cacheability and idempotency. Clients cannot bookmark or share the URL.

### Corrected

```
GET /v1/users?status=active&role=admin&created_after=2024-01-01&sort=-created_at&fields=id,name,email
```

- Standard query parameters for filtering
- GET for read operations (cacheable, bookmarkable)
- `sort` with `-` prefix for descending
- `fields` for sparse fieldsets (reduces payload)
- Date filters use ISO 8601 format
- Complex filters (if needed): `GET /v1/users?filter[status]=active&filter[role]=admin`

---

## 8. Response Structure

### Bad

```json
{
  "d": [
    { "i": 1, "n": "Alice", "e": "alice@co.com", "c": 1719100000 }
  ],
  "t": 142,
  "p": 1
}
```

**Why it fails:** Abbreviated field names are unreadable without documentation. `"c": 1719100000` — is that a count, a timestamp, a category? Unix timestamps without timezone context are ambiguous. No envelope structure.

### Corrected

```json
{
  "data": [
    {
      "id": "usr_01H8X3K",
      "name": "Alice",
      "email": "alice@co.com",
      "created_at": "2024-06-23T04:26:40Z"
    }
  ],
  "meta": {
    "total": 142,
    "page": 1,
    "per_page": 20
  }
}
```

- Full, descriptive field names
- ISO 8601 timestamps with timezone
- Prefixed IDs (`usr_`) for debuggability across systems
- Consistent envelope: `data` for payload, `meta` for pagination
- `snake_case` for all field names (consistent with URL conventions)
