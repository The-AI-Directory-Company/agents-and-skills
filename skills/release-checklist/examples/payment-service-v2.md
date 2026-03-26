# Release Checklist: payment-service v2.4.0

**Release date**: 2026-03-25
**Release manager**: @jchen
**On-call engineer**: @mpatel

## Scope Inventory

| Change | Owner | Feature flag | Touches shared infra |
|--------|-------|-------------|---------------------|
| Stripe SDK upgrade (v12 -> v14) | @lnguyen | No | Yes — payment gateway |
| Idempotency key refactor | @akim | `idempotency_v2` | Yes — Redis cache layer |
| PCI audit logging enhancement | @jchen | No | No |
| Retry policy tuning (3 -> 5 retries, exponential backoff) | @mpatel | `retry_v2` | No |

## Risk Classification: HIGH

- Stripe SDK major version upgrade — breaking API changes in webhook signature verification
- Idempotency refactor touches every write path in the payment flow
- Revenue-critical service: $2.3M daily transaction volume

**Required**: Dedicated rollback runbook reviewed and approved before go/no-go.

## Dependency Check

- [ ] Stripe API v2024-12 compatibility verified in staging
- [ ] Redis 7.2 cluster healthy in all target environments
- [ ] Feature flags `idempotency_v2` and `retry_v2` configured (default: off) in production
- [ ] PCI audit log sink verified in compliance-logging service
- [ ] Secrets rotated: Stripe API keys in Vault (`payment-service/prod/stripe`)

## Go/No-Go

| Criteria | Owner | Status |
|----------|-------|--------|
| All CI checks pass on `release/v2.4.0` branch | @lnguyen | ___ |
| Staging smoke tests pass (50 test transactions) | @akim | ___ |
| Stripe webhook signature verification passes on staging | @lnguyen | ___ |
| Rollback runbook reviewed by SRE | @mpatel | ___ |
| On-call engineer confirmed and available through release window | @jchen | ___ |
| Stakeholders notified: product, support, finance | @jchen | ___ |
| PCI compliance officer sign-off on audit log changes | @jchen | ___ |

## Staged Rollout Plan

| Stage | Traffic % | Bake time | Metric thresholds |
|-------|----------|-----------|-------------------|
| Canary | 1% | 30 min | Error rate < 0.05%, P99 < 450ms, zero failed charges |
| Partial | 10% | 1 hour | Error rate < 0.03%, no new error signatures |
| Half | 50% | 2 hours | Error rate < 0.02%, revenue per tx within 1% of baseline |
| Full | 100% | 4 hours soak | All thresholds hold, zero duplicate charges |

## Monitoring Checkpoints

At each rollout stage, verify:

- [ ] **Error rates**: `https://grafana.internal/d/payment-svc` — canary vs. baseline cohort
- [ ] **Latency**: P50, P95, P99 on `payment.process` span — baseline: P50=120ms, P99=380ms
- [ ] **Duplicate charges**: `SELECT count(*) FROM charges WHERE is_duplicate = true AND created_at > now() - interval '1 hour'` — must be 0
- [ ] **Stripe webhook success rate**: Grafana panel `stripe-webhooks` — must remain > 99.9%
- [ ] **Redis connection pool**: `payment-redis-pool-utilization` alert — must remain < 80%

## Rollback Triggers

Initiate rollback immediately if any condition is met:

- 5xx error rate > 0.1% for 3+ minutes
- Any duplicate charge detected
- Stripe webhook verification failure rate > 0.5%
- P99 latency > 1000ms (2.6x baseline)
- Redis connection pool utilization > 95%

**Rollback procedure**:

1. Set feature flags `idempotency_v2` and `retry_v2` to `off`
2. Roll back deployment: `kubectl rollout undo deployment/payment-service -n payments`
3. Verify metrics return to baseline within 10 minutes
4. Notify #payments-incidents channel with timeline
5. Page finance-oncall if any duplicate charges were processed

## Post-Release

- [ ] Metrics stable at 100% for 4 hours, smoke tests pass
- [ ] Support team briefed on new retry behavior (customers may see longer processing times)
- [ ] Finance team notified of PCI audit log format changes
- [ ] Feature flags `idempotency_v2` and `retry_v2` scheduled for cleanup (target: v2.5.0)
- [ ] Retrospective scheduled for 2026-03-27 (high-risk release)
