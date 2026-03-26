# Payment Processing Flow — STRIDE Threat Model

## 1. System Overview

The checkout flow accepts payment details from a React SPA, submits them to a backend API (Node.js), which creates a PaymentIntent via Stripe's API and records the transaction in PostgreSQL. Webhook callbacks from Stripe confirm or reject charges asynchronously.

```
Browser → (HTTPS) → API Gateway → (internal TLS) → Payment API → (TLS) → Stripe
                                                         ↓
                                                   PostgreSQL (RDS)
                                    Stripe → (webhook HTTPS) → Payment API
```

## 2. Assets

| Asset | Confidentiality | Integrity | Availability | Notes |
|-------|----------------|-----------|--------------|-------|
| Card details (transient) | Critical | Critical | N/A | Never stored; passed directly to Stripe via client-side SDK |
| Stripe secret keys | Critical | Critical | High | Stored in AWS Secrets Manager |
| Payment records | High | Critical | High | Order amounts, status, customer ID |
| Webhook signing secret | Critical | Critical | High | Validates Stripe callback authenticity |
| Session tokens | High | High | Medium | JWT, 15-min expiry, HttpOnly cookies |

## 3. Threat Actors

- **External unauthenticated** — Automated scanners, carders testing stolen card numbers at scale
- **External authenticated** — Malicious user with a valid account attempting price manipulation or refund fraud
- **Insider** — Engineer or support agent with production database access
- **Supply chain** — Compromised npm dependency in the payment API

## 4. Attack Surface

- Public endpoint: `POST /v1/payments` (accepts amount, currency, payment method token)
- Stripe webhook endpoint: `POST /webhooks/stripe` (accepts signed payloads)
- Admin dashboard: internal tool for viewing payment records and issuing refunds
- CI/CD pipeline: deploys payment service; has access to Stripe keys during build

## 5. STRIDE Threat Matrix

| ID | Category | Threat | Attack Scenario | Component |
|----|----------|--------|-----------------|-----------|
| S-1 | Spoofing | Forged webhook | Attacker sends fake Stripe webhook to `POST /webhooks/stripe` without valid signature, marking unpaid orders as paid | Payment API |
| T-1 | Tampering | Price manipulation | Authenticated user modifies `amount_cents` in the `POST /v1/payments` request body to pay $0.01 for a $99 item | Payment API |
| T-2 | Tampering | Replay attack | Attacker replays a captured payment request to trigger duplicate charges | Payment API |
| R-1 | Repudiation | Unlogged refund | Support agent issues a refund via admin dashboard with no audit trail | Admin Dashboard |
| I-1 | Info Disclosure | Error stack trace | Payment failure returns Stripe API key fragment in verbose error message to browser | API Gateway |
| D-1 | Denial of Service | Webhook flooding | Attacker sends 50k fake webhook requests/sec, exhausting API server threads | Payment API |
| E-1 | Elevation | IDOR on refunds | User changes `payment_id` in refund request to access another user's payment record | Payment API |

## 6. Risk Scoring

| Threat ID | Likelihood | Impact | Risk Score | Priority |
|-----------|-----------|--------|------------|----------|
| T-1 | 5 | 5 | 25 | Critical |
| S-1 | 4 | 5 | 20 | Critical |
| E-1 | 4 | 4 | 16 | Critical |
| I-1 | 3 | 4 | 12 | High |
| R-1 | 3 | 3 | 9 | High |
| D-1 | 3 | 3 | 9 | High |
| T-2 | 2 | 4 | 8 | High |

## 7. Mitigations

| Threat ID | Mitigation | Control Type | Status |
|-----------|-----------|--------------|--------|
| T-1 | Server-side price validation: compare `amount_cents` against cart total from database before creating PaymentIntent | Preventive | Complete |
| S-1 | Verify Stripe webhook signature using `stripe.webhooks.constructEvent()` with the signing secret | Preventive | Complete |
| E-1 | Enforce ownership check: `WHERE payment.user_id = current_user.id` on all payment queries | Preventive | In progress |
| I-1 | Structured error responses only; strip stack traces in production via error middleware | Preventive | Complete |
| R-1 | Immutable audit log for all refund actions with actor ID, timestamp, and reason | Detective | Not started |
| D-1 | Rate limit webhook endpoint to 200 req/s; validate signature before processing | Preventive | Partial |
| T-2 | Idempotency key required on `POST /v1/payments`; reject duplicate keys within 24h | Preventive | Complete |

## 8. Residual Risk

- **Stripe account compromise**: If Stripe's systems are breached, payment data may be exposed. Accepted risk — mitigated by Stripe's PCI Level 1 compliance. Review annually.
- **Insider DB access**: Engineers with production read access can view payment metadata. Compensating control: query audit logging via pgAudit. Full mitigation (column-level encryption) deferred to Q2.
