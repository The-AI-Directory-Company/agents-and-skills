# Template B: API Endpoint

Prompt template for generating a complete API endpoint with request validation, response schema, error handling, and authentication. Best for REST endpoints, RPC handlers, and server actions.

---

## The Template

```
Write a [FRAMEWORK] [METHOD] endpoint at [PATH] that:

- Accepts: [REQUEST BODY/PARAMS SCHEMA]
- Returns: [RESPONSE SCHEMA] with status [CODE]
- Validation: [RULES FOR EACH FIELD]
- Error responses: [STATUS CODE + BODY FOR EACH ERROR CASE]
- Authentication: [REQUIRED/OPTIONAL, METHOD]
- Follow the existing patterns in [REFERENCE FILE].
```

---

## Slot Reference

| Slot | What to write | Example |
|------|--------------|---------|
| `[FRAMEWORK]` | Framework and version | Express 4, Next.js 15 App Router, FastAPI 0.111 |
| `[METHOD]` | HTTP method | POST, GET, PATCH, DELETE |
| `[PATH]` | Route path with parameters | `/api/orders/:orderId/refund`, `/api/v2/users` |
| `[REQUEST BODY/PARAMS SCHEMA]` | Every field with type, required/optional, and example value | `{ orderId: string (from URL), reason: string (required, max 500 chars), amount: number (optional, defaults to full order amount) }` |
| `[RESPONSE SCHEMA]` | Success response shape with example | `{ refund: { id: string, amount: number, status: "pending" } }` with status 201 |
| `[VALIDATION RULES]` | Specific rules per field, not "validate inputs" | `reason: required, string, 1-500 chars, no HTML. amount: if provided, must be > 0 and <= order total.` |
| `[ERROR RESPONSES]` | Each error case with status code and response body | `400: { error: "Reason is required" }. 404: { error: "Order not found" }. 409: { error: "Refund already processed" }. 422: { error: "Refund amount exceeds order total" }.` |
| `[AUTHENTICATION]` | Auth requirement and method | "Required. Bearer token validated by authMiddleware. User must own the order." |
| `[REFERENCE FILE]` | Existing code to match patterns from | `src/api/orders/create.ts` |

---

## Filled Example

```
Write a Next.js 15 App Router POST endpoint at /api/orders/[orderId]/refund that:

- Accepts:
  - orderId: string (from URL path, UUID format)
  - reason: string (required, 1-500 characters)
  - amount: number (optional, cents, defaults to full order amount)

- Returns: { refund: { id: string, orderId: string, amount: number, status: "pending", createdAt: string } } with status 201

- Validation:
  - orderId: required, valid UUID v4 format
  - reason: required, string, 1-500 chars, trimmed, reject if empty after trimming
  - amount: if present, must be a positive integer (cents), must not exceed the order's total minus any previous refunds

- Error responses:
  - 400: { error: "Reason is required" } — missing or empty reason
  - 400: { error: "Invalid order ID format" } — orderId is not a valid UUID
  - 401: { error: "Authentication required" } — no valid session
  - 403: { error: "Not authorized" } — user does not own this order
  - 404: { error: "Order not found" } — no order with this ID exists
  - 409: { error: "Refund already pending" } — an active refund already exists for this order
  - 422: { error: "Refund amount exceeds refundable balance" } — amount > (order total - previous refunds)

- Authentication: Required. Use getServerSession(authOptions) to get the current user. User must be the order owner.

- Follow the existing patterns in src/app/api/orders/[orderId]/route.ts — use the same error response format, database client initialization, and logging pattern.
```

---

## When to Use This Template

- REST API endpoints (CRUD operations, business actions)
- Next.js route handlers / API routes
- Express, Fastify, or Hono route handlers
- GraphQL resolvers (adapt the schema section)
- Server actions that handle form submissions

## When NOT to Use This Template

- Pure functions with no HTTP context -- use Template A (Standalone Function)
- UI rendering logic -- use Template C (UI Component)
- Background jobs or cron tasks -- adapt this template but remove the HTTP-specific sections and add scheduling/retry semantics
