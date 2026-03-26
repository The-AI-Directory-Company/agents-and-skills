# Task Management API — Design Specification

## Overview

RESTful API for a task management system. Consumers: SPA frontend, mobile apps, third-party integrations via API keys. Auth: OAuth 2.0 + PKCE for users, API keys for service accounts.

## 1. Resources

| Resource | Path | Description |
|----------|------|-------------|
| Projects | `/v1/projects` | Top-level container for tasks |
| Tasks | `/v1/projects/{project_id}/tasks` | Work items within a project |
| Comments | `/v1/tasks/{task_id}/comments` | Discussion on a task |
| Labels | `/v1/labels` | Shared labels across projects |

## 2. Endpoints

### Projects

| Method | Path | Description | Auth | Success |
|--------|------|-------------|------|---------|
| GET | `/v1/projects` | List user's projects | Bearer | 200 |
| POST | `/v1/projects` | Create a project | Bearer | 201 |
| GET | `/v1/projects/{id}` | Get project details | Bearer | 200 |
| PATCH | `/v1/projects/{id}` | Update project fields | Bearer | 200 |
| DELETE | `/v1/projects/{id}` | Archive project (soft delete) | Bearer | 204 |

### Tasks

| Method | Path | Description | Auth | Success |
|--------|------|-------------|------|---------|
| GET | `/v1/projects/{id}/tasks` | List tasks (filterable) | Bearer | 200 |
| POST | `/v1/projects/{id}/tasks` | Create a task | Bearer | 201 |
| GET | `/v1/tasks/{id}` | Get task details | Bearer | 200 |
| PATCH | `/v1/tasks/{id}` | Update task fields | Bearer | 200 |
| DELETE | `/v1/tasks/{id}` | Delete task | Bearer | 204 |
| POST | `/v1/tasks/{id}/complete` | Mark task complete | Bearer | 200 |

## 3. Request/Response Examples

**Create Task** — `POST /v1/projects/proj_01/tasks`
```json
{
  "title": "Design login page",
  "description": "Implement OAuth flow with Google and GitHub providers",
  "assignee_id": "usr_42",
  "due_date": "2025-10-15",
  "priority": "high",
  "label_ids": ["lbl_03", "lbl_07"]
}
```

**Response** — `201 Created`
```json
{
  "data": {
    "id": "tsk_291",
    "title": "Design login page",
    "status": "open",
    "priority": "high",
    "assignee": { "id": "usr_42", "name": "Priya Sharma" },
    "due_date": "2025-10-15",
    "created_at": "2025-09-01T14:32:00Z"
  }
}
```

**List Tasks** — `GET /v1/projects/proj_01/tasks?status=open&priority=high&cursor=eyJpZCI6MzB9&limit=20`

**Response** — `200 OK`
```json
{
  "data": [{ "id": "tsk_291", "title": "Design login page", "status": "open" }],
  "meta": { "total": 84, "limit": 20, "next_cursor": "eyJpZCI6NTB9" }
}
```

## 4. Error Handling

All errors use a consistent envelope:
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Task tsk_999 does not exist or you do not have access.",
    "request_id": "req_abc123"
  }
}
```

| Status | Code | When |
|--------|------|------|
| 400 | VALIDATION_ERROR | Missing required field, invalid date format |
| 401 | UNAUTHENTICATED | Missing or expired token |
| 403 | FORBIDDEN | User lacks permission on this project |
| 404 | RESOURCE_NOT_FOUND | Task/project does not exist or no access |
| 409 | CONFLICT | Task already completed (idempotency) |
| 429 | RATE_LIMITED | Exceeded request quota |

## 5. Pagination

Cursor-based for all collection endpoints. Default limit: 20, max: 100. Responses include `next_cursor` (null on last page). Filtering via query params: `status`, `priority`, `assignee_id`, `due_before`, `due_after`.

## 6. Rate Limiting

| Tier | Limit | Window |
|------|-------|--------|
| Free | 100 req | 1 minute |
| Pro | 1,000 req | 1 minute |
| API key (service) | 5,000 req | 1 minute |

Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` (Unix timestamp).

## 7. Versioning

URL-prefix versioning (`/v1/`). Breaking changes require a new major version. Field additions within a version are non-breaking. Deprecated versions supported for 12 months with 90-day advance notice via changelog and `Sunset` header.
