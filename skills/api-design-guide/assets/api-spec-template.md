# API Specification: [Service Name]

> **Version:** v1
> **Base URL:** `https://api.example.com/v1`
> **Last updated:** YYYY-MM-DD
> **Status:** Draft | Review | Approved

---

## Overview

_2-3 sentences: what this API does, who it serves, and what integration pattern it uses._

---

## Authentication

| Scheme | Header | Format |
|--------|--------|--------|
| _e.g., Bearer Token_ | `Authorization` | `Bearer <access_token>` |

**Token acquisition:** _Describe how clients obtain credentials._

**Token refresh:** _Describe the refresh flow and token lifetime._

**Scopes:**

| Scope | Description |
|-------|-------------|
| `read:users` | _Read user profiles_ |
| `write:users` | _Create and update users_ |

---

## Rate Limits

| Tier | Requests/Minute | Burst | Headers |
|------|-----------------|-------|---------|
| Free | _100_ | _10_ | `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` |
| Pro | _1000_ | _50_ | Same |
| Internal | _10000_ | _200_ | Same |

**On limit exceeded:** HTTP 429 with `Retry-After` header (seconds).

---

## Versioning

- **Strategy:** URL prefix (`/v1/`, `/v2/`)
- **Breaking change policy:** _New major version required. N-1 supported for [X] months._
- **Deprecation notice:** `Deprecation` and `Sunset` headers on deprecated endpoints.

---

## Common Response Format

### Success (collection)

```json
{
  "data": [],
  "meta": {
    "total": 0,
    "page": 1,
    "per_page": 20
  },
  "links": {
    "next": null,
    "prev": null
  }
}
```

### Success (single resource)

```json
{
  "data": {}
}
```

### Error

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description.",
    "details": [],
    "request_id": "req_xxx"
  }
}
```

---

## Resources

### [Resource Name] (e.g., Users)

_Brief description of this resource._

**Object schema:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes (read-only) | Unique identifier, prefixed (e.g., `usr_`) |
| `email` | string | Yes | |
| `name` | string | Yes | |
| `created_at` | string (ISO 8601) | Yes (read-only) | |
| `updated_at` | string (ISO 8601) | Yes (read-only) | |

---

#### List [Resources]

```
GET /v1/[resources]
```

**Query parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | integer | 1 | Page number (offset pagination) |
| `per_page` | integer | 20 | Items per page (max 100) |
| `sort` | string | `-created_at` | Sort field. Prefix `-` for descending. |
| `status` | string | | Filter by status |

**Response:** 200 OK

```json
{
  "data": [
    {
      "id": "usr_01H8X3K",
      "email": "alice@example.com",
      "name": "Alice",
      "created_at": "2024-06-23T04:26:40Z",
      "updated_at": "2024-06-23T04:26:40Z"
    }
  ],
  "meta": { "total": 142, "page": 1, "per_page": 20 },
  "links": { "next": "/v1/users?page=2&per_page=20" }
}
```

---

#### Get [Resource]

```
GET /v1/[resources]/{id}
```

**Response:** 200 OK

```json
{
  "data": {
    "id": "usr_01H8X3K",
    "email": "alice@example.com",
    "name": "Alice",
    "created_at": "2024-06-23T04:26:40Z",
    "updated_at": "2024-06-23T04:26:40Z"
  }
}
```

**Errors:**

| Status | Code | When |
|--------|------|------|
| 404 | `NOT_FOUND` | Resource does not exist |

---

#### Create [Resource]

```
POST /v1/[resources]
```

**Request body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | |
| `name` | string | Yes | |

**Example:**

```json
{
  "email": "alice@example.com",
  "name": "Alice"
}
```

**Response:** 201 Created

**Headers:** `Location: /v1/users/usr_01H8X3K`

**Errors:**

| Status | Code | When |
|--------|------|------|
| 400 | `BAD_REQUEST` | Malformed JSON |
| 409 | `CONFLICT` | Email already exists |
| 422 | `VALIDATION_ERROR` | Invalid field values |

---

#### Update [Resource]

```
PATCH /v1/[resources]/{id}
```

**Request body:** Include only the fields to update.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | No | |

**Response:** 200 OK (returns updated resource)

**Errors:**

| Status | Code | When |
|--------|------|------|
| 404 | `NOT_FOUND` | Resource does not exist |
| 422 | `VALIDATION_ERROR` | Invalid field values |

---

#### Delete [Resource]

```
DELETE /v1/[resources]/{id}
```

**Response:** 204 No Content

**Errors:**

| Status | Code | When |
|--------|------|------|
| 404 | `NOT_FOUND` | Resource does not exist |

---

## Webhooks

_If applicable, document webhook events._

| Event | Trigger | Payload |
|-------|---------|---------|
| `[resource].created` | _When a new resource is created_ | _Full resource object_ |
| `[resource].updated` | _When a resource is modified_ | _Full resource object_ |
| `[resource].deleted` | _When a resource is removed_ | `{ "id": "..." }` |

**Delivery:** POST to registered URL with `Content-Type: application/json` and `X-Webhook-Signature` header (HMAC-SHA256).

**Retry policy:** 3 retries with exponential backoff (1s, 4s, 16s). Dead-letter after all retries fail.

---

## Changelog

| Date | Version | Change |
|------|---------|--------|
| _YYYY-MM-DD_ | _v1.0_ | _Initial release_ |
