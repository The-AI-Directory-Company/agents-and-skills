# Exploration Summary: Acme Billing (Next.js SaaS)

> Repository: `github.com/acme/billing-app`
> Explored: 2025-03-15 | Goal: Onboard new backend engineer | Scope: Full repo

---

## 1. Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | TypeScript | 5.4 |
| Framework | Next.js (App Router) | 14.2 |
| Database | PostgreSQL 16 via Supabase | — |
| ORM | Drizzle ORM | 0.30 |
| Auth | NextAuth.js v5 (Auth.js) | 5.0-beta |
| Payments | Stripe SDK | 14.x |
| Queue | Inngest | 3.x |
| Email | React Email + Resend | — |
| UI | Tailwind CSS + Radix Primitives | — |
| Deployment | Vercel (Edge + Serverless) | — |
| Package manager | pnpm 9.1 | — |

Key observation: The project uses the App Router exclusively — no `pages/` directory. Server Actions handle mutations; there are no standalone API routes except for webhook endpoints.

---

## 2. Architecture

```
Request
  │
  ├─ Middleware (src/middleware.ts)
  │    └─ Auth session check, redirect unauthenticated users
  │
  ├─ App Router (src/app/)
  │    ├─ (marketing)/        ← Public pages (landing, pricing, docs)
  │    ├─ (dashboard)/        ← Authenticated app shell
  │    │    ├─ layout.tsx     ← Sidebar, org switcher, session provider
  │    │    ├─ billing/       ← Subscription management
  │    │    ├─ invoices/      ← Invoice CRUD
  │    │    └─ settings/      ← Org and user settings
  │    └─ api/
  │         ├─ webhooks/stripe/route.ts
  │         └─ webhooks/inngest/route.ts
  │
  ├─ Domain Layer (src/lib/)
  │    ├─ db/                 ← Drizzle schema, migrations, query helpers
  │    ├─ stripe/             ← Stripe client, price sync, webhook handlers
  │    ├─ billing/            ← Subscription lifecycle, usage metering
  │    ├─ auth/               ← Auth.js config, session helpers
  │    └─ email/              ← React Email templates, send functions
  │
  ├─ Background Jobs (src/inngest/)
  │    ├─ functions/          ← Job definitions (invoice.generate, usage.aggregate)
  │    └─ client.ts           ← Inngest client instance
  │
  └─ Shared (src/components/, src/utils/)
       ├─ components/ui/      ← Design system primitives (Button, Dialog, Table)
       ├─ components/billing/ ← Domain-specific components
       └─ utils/              ← Formatting, validation, constants
```

The architecture follows a three-layer pattern: **Route handlers** (thin — parse input, call domain) -> **Domain functions** (business logic in `src/lib/`) -> **Data access** (Drizzle queries, Stripe SDK calls). Route handlers never contain business logic directly.

---

## 3. Entry Points

| Entry point | File | Purpose |
|-------------|------|---------|
| App shell | `src/app/layout.tsx` | Root layout, providers, fonts |
| Auth middleware | `src/middleware.ts` | Session validation, route protection |
| Dashboard layout | `src/app/(dashboard)/layout.tsx` | Sidebar, org context, breadcrumbs |
| Stripe webhook | `src/app/api/webhooks/stripe/route.ts` | Receives Stripe events |
| Inngest webhook | `src/app/api/webhooks/inngest/route.ts` | Inngest job runner endpoint |
| DB schema | `src/lib/db/schema.ts` | Drizzle table definitions (source of truth) |
| Seed script | `scripts/seed.ts` | Populates dev database with test data |

To start the app: `pnpm dev` runs `next dev` on port 3000. Database migrations: `pnpm db:push` (Drizzle push) or `pnpm db:migrate` (versioned migrations).

---

## 4. Primary Data Flow: "Customer Creates an Invoice"

Traced end-to-end through the codebase:

**Step 1 — Route entry**
`src/app/(dashboard)/invoices/new/page.tsx` renders `<InvoiceForm>`, which collects line items, customer, due date, and tax rate.

**Step 2 — Server Action**
Form submission calls `createInvoice` Server Action in `src/app/(dashboard)/invoices/actions.ts`. The action:
1. Validates input with Zod schema (`src/lib/billing/schemas.ts` — `invoiceCreateSchema`)
2. Checks org membership via `requireOrgMember()` from `src/lib/auth/guards.ts`
3. Calls `InvoiceService.create()` from `src/lib/billing/invoice-service.ts`

**Step 3 — Domain logic**
`InvoiceService.create()` in `src/lib/billing/invoice-service.ts`:
1. Generates invoice number via `generateInvoiceNumber()` (format: `INV-{orgSlug}-{YYYY}-{seq}`)
2. Calculates tax using `TaxCalculator.compute()` from `src/lib/billing/tax.ts`
3. Inserts invoice + line items in a Drizzle transaction (`src/lib/db/queries/invoices.ts` — `insertInvoiceWithLineItems`)
4. Dispatches Inngest event `invoice/created` to trigger async jobs

**Step 4 — Background processing**
`src/inngest/functions/invoice-created.ts` listens for `invoice/created`:
1. Generates PDF via `renderInvoicePdf()` (uses `@react-pdf/renderer`)
2. Uploads PDF to Supabase Storage
3. Sends email to customer via `sendInvoiceEmail()` from `src/lib/email/send.ts`
4. If Stripe customer exists, creates a Stripe Invoice for payment tracking

**Step 5 — Response**
Server Action returns `{ success: true, invoiceId }`. The form page calls `router.push(`/invoices/${invoiceId}`)` to redirect to the invoice detail view.

**Files touched in this flow:**
- `src/app/(dashboard)/invoices/new/page.tsx`
- `src/app/(dashboard)/invoices/actions.ts`
- `src/lib/billing/schemas.ts`
- `src/lib/auth/guards.ts`
- `src/lib/billing/invoice-service.ts`
- `src/lib/billing/tax.ts`
- `src/lib/db/queries/invoices.ts`
- `src/inngest/functions/invoice-created.ts`
- `src/lib/email/send.ts`
- `src/lib/email/templates/invoice-email.tsx`

---

## 5. Patterns and Conventions

### Naming
- **Files**: kebab-case (`invoice-service.ts`, `stripe-webhook.ts`)
- **Components**: PascalCase files in `components/` (`InvoiceForm.tsx`, `PricingCard.tsx`)
- **Database columns**: snake_case in schema, camelCase in TypeScript via Drizzle's `.$inferSelect()`
- **Server Actions**: named exports, verb-noun (`createInvoice`, `updateSubscription`, `cancelPlan`)

### Error handling
The project uses a custom `AppError` class (`src/utils/errors.ts`) with error codes:
```typescript
throw new AppError("INVOICE_NOT_FOUND", "Invoice does not exist", 404);
```
Server Actions catch errors and return `{ success: false, error: string }` — never throw to the client. Background jobs use Inngest's built-in retry with exponential backoff (max 3 retries). Stripe webhook handlers return 200 even on processing errors to prevent Stripe retry storms; errors are logged and alerted via Sentry.

### State management
- Server-side: React Server Components fetch data directly in `page.tsx` using async functions. No client-side data fetching library.
- Client-side: `nuqs` for URL query state (filters, pagination). React `useState` for ephemeral UI state. No global store.
- Forms: `react-hook-form` with Zod resolvers. Server Actions for submission.

### Auth and authorization
- Authentication: NextAuth.js v5 with Google and email magic link providers. Session stored in JWT.
- Authorization: `requireOrgMember(orgId)` and `requireOrgAdmin(orgId)` guard functions called at the start of every Server Action. These throw `AppError("UNAUTHORIZED")` if the check fails. There are no role-based middleware — authorization is always inline in the action.

### Testing style
- Unit tests for domain logic (`src/lib/**/*.test.ts`) using Vitest
- Integration tests for Server Actions (`src/app/**/*.test.ts`) using Vitest + a test database
- E2E tests in `e2e/` using Playwright (login flow, invoice creation, subscription upgrade)
- No snapshot tests. No tests for pure UI components.
- Test utilities in `src/test/` — `createTestOrg()`, `createTestUser()`, `withTestDb()` (per-test schema isolation)

---

## 6. External Dependencies

| System | Integration module | Error handling | Fallback |
|--------|-------------------|----------------|----------|
| PostgreSQL (Supabase) | `src/lib/db/client.ts` | Connection pool retry (3x) | None — hard dependency |
| Stripe | `src/lib/stripe/client.ts` | SDK exceptions caught per-call | Webhook replay via Stripe dashboard |
| Inngest | `src/inngest/client.ts` | Built-in retry (3x, exponential) | Dead letter queue (manual) |
| Resend (email) | `src/lib/email/send.ts` | Retry 2x, log failure | Email marked "pending" in DB for retry |
| Supabase Storage | `src/lib/storage/client.ts` | Retry 2x | Invoice PDF generated on-demand if missing |
| Sentry | `sentry.client.config.ts`, `sentry.server.config.ts` | Fire-and-forget | None needed |
| Google OAuth | NextAuth.js provider config | Auth.js handles errors | Falls back to email magic link |

---

## 7. Test Coverage and Gaps

**Well-covered areas:**
- Invoice creation and calculation logic (unit + integration): 14 test files
- Stripe webhook event processing: 8 test files covering all event types
- Tax calculation edge cases: 6 test files
- E2E: Login, invoice creation, subscription upgrade (3 Playwright specs)

**Coverage gaps:**
- No tests for email template rendering — emails could break silently
- No tests for Inngest job orchestration (individual functions tested, but not the chain)
- Settings pages have zero test coverage
- No load testing or performance benchmarks
- No contract tests for the Stripe webhook payload shape — a Stripe API version upgrade could break parsing silently

**Test infrastructure:**
- `pnpm test` runs Vitest in the `src/` directory
- `pnpm test:e2e` runs Playwright against a local dev server
- CI runs both on every PR (GitHub Actions, ~4 min total)
- Test database is a Supabase local instance via Docker (`supabase start`)

---

## Risks and Concerns

1. **Single point of failure on Inngest.** All async processing (PDF generation, email, Stripe sync) routes through Inngest. If Inngest is down, invoices are created but customers receive no email and no PDF. There is no fallback queue.

2. **No rate limiting on Server Actions.** The `createInvoice` action has auth checks but no rate limiting. A compromised session could generate thousands of invoices.

3. **Tight coupling to Supabase Storage.** PDF upload uses Supabase Storage directly — no abstraction layer. Migrating to S3 would require changes in 4 files.

4. **Stale Stripe price data.** `src/lib/stripe/price-sync.ts` runs on a cron (daily) but the app reads prices from the local DB. If Stripe prices change mid-day, the app shows stale pricing until the next sync.

5. **No database migration versioning in CI.** The project uses `drizzle-kit push` (schema diffing) instead of versioned migration files. This works for development but is risky for production — a schema diff against prod could generate destructive DDL.
