---
name: api-integration-guide
description: Create REST and GraphQL integration guides covering authentication flows, pagination strategies, rate limiting, error handling, retry logic, and SDK wrapper patterns. Produces implementation-ready reference documents with code examples.
metadata:
  displayName: "API Integration Guide"
  categories: ["engineering"]
  tags: ["api", "rest", "graphql", "integration", "authentication", "rate-limiting", "pagination"]
  worksWellWithAgents: ["api-developer", "integration-engineer", "solutions-architect"]
  worksWellWithSkills: ["api-design-guide", "integration-specification", "technical-spec-writing"]
---

# API Integration Guide

## Before you start

Gather the following from the user:

1. **Which API?** (Service name, base URL, documentation link)
2. **REST or GraphQL?** (Or both)
3. **Authentication method?** (API key, OAuth 2.0, JWT, mTLS)
4. **Which operations?** (List the endpoints or queries/mutations needed)
5. **Client environment?** (Server-side, browser, mobile, CLI)
6. **Error budget?** (Acceptable failure rate, timeout thresholds)

If the user says "integrate with X API," push back: "Which specific operations do you need? I need the endpoints, auth method, and where this runs to write a useful guide."

## Procedure

### Step 1: Document the authentication flow

For each auth method, produce the exact sequence:

**API Key:** Document header name (`Authorization: Bearer <key>` or `X-API-Key`), storage (environment variable, never committed), and rotation procedure.

**OAuth 2.0 (Authorization Code):** Document the full redirect-exchange-refresh cycle: authorize URL with state param, code exchange at token endpoint, refresh_token storage (encrypted), and proactive refresh before `expires_in`.

**OAuth 2.0 (Client Credentials):** Document token endpoint call, cache duration (`expires_in` minus 60s buffer), and re-fetch on 401.

### Step 2: Map each operation

For every endpoint or query, document:

```
Operation: [Human-readable name]
Method: [GET/POST/PUT/PATCH/DELETE] or [Query/Mutation]
Path: [/resource/:id] or [GraphQL operation name]
Request:
  Headers: [Required headers beyond auth]
  Params: [Path, query, or body params with types and constraints]
  Body example: [JSON]
Response:
  Success (2xx): [Shape with field types]
  Error codes: [4xx/5xx with meaning and action]
Rate limit: [Requests per window, header names for remaining/reset]
```

### Step 3: Design pagination handling

Document the pagination pattern the API uses and how to consume it:

- **Offset-based:** `GET /items?limit=100&offset=0`. Stop when response count < limit or offset >= total_count.
- **Cursor-based:** `GET /items?limit=100&cursor=<next_cursor>`. Stop when next_cursor is null.
- **GraphQL relay:** Use `pageInfo { hasNextPage endCursor }`. Stop when `hasNextPage` is false.

For all patterns: state the maximum page size, recommend a default, and note whether the API supports parallel page fetching safely.

### Step 4: Implement rate limiting

Document the API's rate limit response and the client-side strategy:

```
Rate limit signal:
  HTTP 429 Too Many Requests
  Headers: X-RateLimit-Remaining, X-RateLimit-Reset (Unix timestamp)

Client strategy:
  1. Before each request: check remaining count from last response headers.
  2. If remaining < 5: sleep until reset timestamp + 1 second jitter.
  3. On 429 response: read Retry-After header. Sleep for that duration.
  4. If no Retry-After: exponential backoff starting at 1s, max 60s.
  5. For batch operations: use a token bucket or leaky bucket limiter.
```

### Step 5: Design error handling and retries

Classify errors and define behavior for each:

| Status | Category | Retryable | Action |
|--------|----------|-----------|--------|
| 400 | Client error | No | Log payload, fix request, do not retry |
| 401 | Auth expired | Once | Refresh token, retry once |
| 403 | Forbidden | No | Log, alert, check permissions |
| 404 | Not found | No | Handle as missing resource |
| 409 | Conflict | Maybe | Re-fetch resource, resolve, retry |
| 429 | Rate limited | Yes | Backoff per rate limit strategy |
| 500 | Server error | Yes | Exponential backoff, max 3 retries |
| 502/503 | Unavailable | Yes | Exponential backoff, max 5 retries |
| Timeout | Network | Yes | Retry with same backoff as 5xx |

Retry formula: `delay = min(base * 2^attempt + random_jitter_ms, max_delay)`

### Step 6: Write the SDK wrapper pattern

The client wrapper should encapsulate: rate limiter wait before each request, retry loop with exponential backoff, automatic token refresh on 401 (once), error classification (retryable vs terminal), and a `paginate` method that loops cursor-based requests until exhausted. Constructor validates base_url, credentials, timeout, and max_retries.

## Quality checklist

Before delivering the integration guide, verify:

- [ ] Auth flow documents every step from credential acquisition to token refresh
- [ ] Every operation lists request shape, success response, error codes, and rate limit
- [ ] Pagination strategy handles the last page correctly and avoids infinite loops
- [ ] Rate limiting covers both proactive throttling and reactive 429 handling
- [ ] Error classification covers all common status codes with retry/no-retry decisions
- [ ] Retry logic uses exponential backoff with jitter, not fixed delays
- [ ] Credentials are never hardcoded; storage and rotation are documented

## Common mistakes

- **Ignoring token expiry.** Caching an access token without monitoring `expires_in` leads to cascading 401s. Always refresh proactively.
- **Retrying 400 errors.** A malformed request will fail every time. Retrying wastes quota and delays error detection.
- **Fixed retry delays.** `sleep(5)` between retries causes thundering herd when multiple clients hit rate limits simultaneously. Use exponential backoff with random jitter.
- **Pagination off-by-one.** Forgetting to check the last page condition causes either an infinite loop or a missed final page. Test with 0, 1, and exactly-one-page result sets.
- **No timeout on HTTP calls.** A missing timeout means a hung connection blocks the caller indefinitely. Set connect and read timeouts explicitly.
- **Swallowing error response bodies.** The API often returns structured error details in the body. Log the full response, not just the status code.
