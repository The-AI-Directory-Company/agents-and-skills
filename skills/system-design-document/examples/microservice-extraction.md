# Payment Service Extraction — System Design Document

## 1. Context & Motivation

The monolithic OrderApp handles checkout, payment processing, inventory, and shipping in a single Rails application. Payment logic is tightly coupled to order creation, making it impossible to scale payment retries independently or comply with PCI-DSS without certifying the entire monolith. Extracting payments into a standalone service allows independent scaling, a smaller PCI audit scope, and faster iteration on payment features.

## 2. Goals & Non-Goals

**Goals**
- Process payments independently of the order lifecycle with < 300ms P99 latency
- Reduce PCI-DSS audit scope from the full monolith to one isolated service
- Support adding new payment providers (Apple Pay, Klarna) without monolith deploys
- Achieve 99.95% availability for payment processing

**Non-goals**
- Refactoring the order service (separate initiative, Q3)
- Supporting cryptocurrency payments (no current business need)
- Real-time fraud scoring (handled by Stripe Radar)

## 3. Non-Functional Requirements

| Requirement | Target | Rationale |
|-------------|--------|-----------|
| Availability | 99.95% (4.4h downtime/year) | Revenue-critical path |
| P99 latency | < 300ms | Checkout UX requirement |
| Throughput | 1,200 req/s peak | 2x Black Friday 2025 traffic |
| Data retention | 7 years (financial records) | SOX compliance |

## 4. Architecture Overview

```
Browser → API Gateway → Order Service (monolith)
                            │
                            ▼ (async, SQS)
                      Payment Service ──→ Stripe API
                            │
                            ▼ (TLS)
                      PostgreSQL (RDS)
                            │
                      Payment Events ──→ SQS ──→ Order Service (webhook)
```

## 5. Component Design

**Payment Service** — Accepts payment intents, orchestrates charges via Stripe, emits payment events. gRPC interface. Scales horizontally behind ALB; auto-scales on CPU > 60%.

**Payment Database** — Stores payment records, idempotency keys, and audit logs. PostgreSQL on RDS Multi-AZ.

**Event Publisher** — Publishes payment state changes (created, succeeded, failed, refunded) to SQS. Consumers: Order Service, Analytics, Notifications.

## 6. Data Model

```sql
CREATE TABLE payments (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id      UUID NOT NULL,
    amount_cents  BIGINT NOT NULL,
    currency      VARCHAR(3) NOT NULL DEFAULT 'USD',
    status        VARCHAR(20) NOT NULL DEFAULT 'pending',
    stripe_id     VARCHAR(64),
    idempotency_key VARCHAR(64) UNIQUE NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_payments_order ON payments(order_id);
CREATE INDEX idx_payments_status_created ON payments(status, created_at);
```

## 7. Failure Modes & Mitigation

| Failure | Impact | Detection | Mitigation |
|---------|--------|-----------|------------|
| Stripe API timeout | Payment hangs | P99 latency alert > 2s | 5s timeout + retry with exponential backoff (max 3). Idempotency key ensures no double charges |
| Payment DB failover | Writes fail ~30s | RDS event + health check | Multi-AZ automatic failover; service returns 503, client retries |
| SQS delivery failure | Order not updated | Dead-letter queue depth alarm | DLQ with alert; reconciliation job runs hourly |

## 8. Architecture Decision Record

```
ADR-001: Use SQS over direct HTTP callbacks for payment events

Status: Accepted
Context: The order service needs to know when payments succeed or fail.
         Direct HTTP callbacks couple the two services and fail silently
         if the order service is down.
Decision: Publish payment events to SQS. Order service consumes async.
Consequences: Eventual consistency (< 5s typical). Order status may lag
              payment status briefly. Simpler failure handling — messages
              retry automatically. Adds SQS as an infrastructure dependency.
```

## 9. Open Questions

| Question | Owner | Blocks? |
|----------|-------|---------|
| Should we support partial refunds in V1? | @product | Yes |
| Multi-currency conversion — service-side or Stripe-side? | @payments-lead | No |
