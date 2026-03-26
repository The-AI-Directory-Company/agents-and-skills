---
name: api-design-guide
description: Design RESTful and GraphQL APIs with consistent naming conventions, versioning strategy, pagination patterns, error response formats, authentication schemes, and rate limiting — producing a complete API specification.
metadata:
  displayName: "API Design Guide"
  categories: ["engineering"]
  tags: ["api-design", "REST", "GraphQL", "endpoints", "versioning", "documentation"]
  worksWellWithAgents: ["api-developer", "code-reviewer", "developer-advocate", "frontend-engineer", "integration-engineer", "open-source-maintainer", "software-architect"]
  worksWellWithSkills: ["integration-specification", "open-source-contributing-guide", "system-design-document", "technical-spec-writing"]
---

# API Design Guide

## Before you start

Gather the following from the user:

1. **What resources does the API expose?** (Users, orders, products, etc.)
2. **Who are the consumers?** (Internal services, third-party developers, mobile apps, SPAs)
3. **REST, GraphQL, or both?** Default to REST for CRUD-heavy services, GraphQL for query-heavy frontends.
4. **Auth requirements?** (API keys, OAuth 2.0, JWT, session-based)
5. **Expected traffic volume?** (Drives rate limiting and pagination decisions)
6. **Versioning constraints?** (Breaking changes expected? Public vs. internal?)

If the user says "design an API for X" without specifics, push back: "What operations do consumers need to perform? What data do they send and receive?"

## API design template

### 1. Resource Naming

Use plural nouns for collections. Resources are things, not actions.

**Good**: `/users`, `/orders`, `/order-items`
**Bad**: `/getUsers`, `/createOrder`, `/user_list`, `/OrderItem`

- Lowercase with hyphens for multi-word resources (`/order-items`, not `/orderItems`)
- Nouns only — never verbs in the URL path
- Nest to express ownership: `/users/{id}/orders` — limit nesting to two levels

### 2. HTTP Methods

| Method | Purpose | Idempotent | Success Code |
|--------|---------|------------|--------------|
| GET | Read resource(s) | Yes | 200 |
| POST | Create resource | No | 201 |
| PUT | Full replace | Yes | 200 |
| PATCH | Partial update | No | 200 |
| DELETE | Remove resource | Yes | 204 |

Use POST for actions that don't map to CRUD: `POST /orders/{id}/cancel`.

### 3. Request/Response Formats

Always use JSON. Wrap collection responses — never return a bare array:

```json
{
  "data": [{ "id": "usr_01", "name": "Alice" }],
  "meta": { "total": 142, "page": 1, "per_page": 20 }
}
```

### 4. Error Handling

Return a consistent error envelope on every failure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email address is invalid.",
    "details": [{ "field": "email", "reason": "Must be a valid email address." }],
    "request_id": "req_abc123"
  }
}
```

Status code mapping: 400 (validation), 401 (unauthenticated), 403 (unauthorized), 404 (not found), 409 (conflict), 422 (semantically invalid), 429 (rate limited), 500 (server error — never expose internals).

### 5. Pagination

Use cursor-based pagination for large or real-time datasets, offset-based for simple UIs. Always include pagination metadata and a `next` link. Default `per_page` to 20, cap at 100.

- **Cursor**: `GET /orders?cursor=eyJpZCI6MTAwfQ&limit=20`
- **Offset**: `GET /orders?page=2&per_page=20`

### 6. Versioning

Use URL-prefix versioning (`/v1/`) for public APIs. Use header versioning only for per-endpoint granularity. Increment the major version only for breaking changes. Never remove or rename a field within the same version. Support at least N-1 versions with a published deprecation timeline.

### 7. Authentication

| Scheme | Best for |
|--------|----------|
| API keys | Server-to-server, internal services |
| OAuth 2.0 + PKCE | Third-party integrations, user-facing apps |
| JWT (short-lived) | Stateless auth between microservices |
| Session cookies | Traditional web apps with same-origin frontend |

Always use HTTPS. Never accept auth tokens in query strings — use the `Authorization` header.

### 8. Rate Limiting

Return rate limit headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`). Define tiers by consumer type (free, paid, internal). Return `429` with `Retry-After` when the limit is hit.

## Good vs. bad API design

| Aspect | Bad | Good |
|--------|-----|------|
| URL | `GET /api/getUsersByStatus?s=active` | `GET /v1/users?status=active` |
| Error | `{ "success": false, "msg": "bad" }` | `{ "error": { "code": "VALIDATION_ERROR", "message": "..." } }` |
| Pagination | Returning 10,000 records with no limit | Cursor pagination with default limit of 20 |
| Versioning | Changing field names without a new version | Adding fields to existing version, removing via new version |
| Auth | API key in the URL (`?key=abc`) | `Authorization: Bearer <token>` header |

## Quality checklist

Before delivering the API specification, verify:

- [ ] Every resource uses plural nouns, lowercase, hyphen-separated
- [ ] HTTP methods match their semantic purpose (GET reads, POST creates)
- [ ] All endpoints document request body, query params, and response shape
- [ ] Error responses follow a single consistent envelope format
- [ ] Pagination is implemented for every collection endpoint
- [ ] Versioning strategy is documented with a deprecation policy
- [ ] Auth scheme is specified for every endpoint (public endpoints explicitly marked)
- [ ] Rate limits are defined per consumer tier with documented headers
- [ ] No endpoint returns unbounded data — every list has a max page size
- [ ] Breaking vs. non-breaking changes are clearly defined
