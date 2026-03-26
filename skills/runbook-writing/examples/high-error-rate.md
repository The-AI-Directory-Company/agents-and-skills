# Runbook: High API Error Rate — checkout-service

**Alert name**: `checkout-service-5xx-rate-high`
**Last verified**: 2026-03-10

## Purpose

Diagnose and resolve elevated 5xx error rates on the checkout-service API. Use this runbook when the `checkout-service-5xx-rate-high` alert fires (threshold: > 1% of requests returning 5xx for 3 consecutive minutes).

## Prerequisites

- [ ] VPN connected to production network
- [ ] `kubectl` access to `prod-us-east` cluster (role: `sre-oncall`)
- [ ] Read access to Datadog dashboard: `https://app.datadoghq.com/dash/checkout-prod`
- [ ] Database read-only credentials in 1Password vault `SRE-Prod` (entry: `checkout-db-readonly`)

## Symptoms and Triggers

- PagerDuty alert: `checkout-service-5xx-rate-high`
- Datadog: `checkout-service` error rate panel turns red (> 1%)
- Log pattern: `level=error msg="request failed" service=checkout status=500`
- User reports: "Payment page shows an error" or "Checkout is broken"

## Step-by-Step Procedure

1. Confirm the alert is real — open the Datadog dashboard and verify error rate:
   ```
   https://app.datadoghq.com/dash/checkout-prod
   ```
   - IF error rate < 1% and falling: monitor for 5 minutes. If it recovers, acknowledge the alert and close.
   - IF error rate >= 1%: proceed to step 2.

2. Check pod health:
   ```bash
   kubectl get pods -n checkout -l app=checkout-service
   ```
   - Expected: 6/6 pods in `Running` state, 0 restarts.
   - IF pods are in `CrashLoopBackOff`: proceed to step 3.
   - IF all pods are healthy: skip to step 4.

3. Inspect crashing pod logs:
   ```bash
   kubectl logs -n checkout -l app=checkout-service --tail=100 | grep "level=error"
   ```
   - IF logs show `connection refused` to database: skip to step 5.
   - IF logs show `OOMKilled`: restart the deployment and escalate to checkout-team.
     ```bash
     kubectl rollout restart deployment/checkout-service -n checkout
     ```
   - IF logs show a different error: escalate (see Escalation section).

4. Check downstream dependency health:
   ```bash
   kubectl exec -n checkout deploy/checkout-service -- curl -s http://localhost:8080/healthz
   ```
   - Expected: `{"status":"ok","db":"connected","cache":"connected","payment_gateway":"connected"}`
   - IF `db` shows `disconnected`: proceed to step 5.
   - IF `payment_gateway` shows `disconnected`: this is a payment-gateway outage. Escalate to payments-team and switch to the `payment-gateway-outage` runbook.
   - IF `cache` shows `disconnected`: proceed to step 6.

5. Investigate database connectivity:
   ```bash
   psql -h <CHECKOUT_DB_HOST> -U readonly -d checkout -c "SELECT count(*) FROM pg_stat_activity WHERE datname = 'checkout';"
   ```
   - IF connection count > 90 (pool max is 100): kill idle connections:
     ```sql
     SELECT pg_terminate_backend(pid) FROM pg_stat_activity
     WHERE datname = 'checkout' AND state = 'idle' AND query_start < now() - interval '5 minutes';
     ```
   - IF cannot connect at all: this is a database outage. Escalate to dba-team immediately.

6. Check Redis cache:
   ```bash
   kubectl exec -n checkout deploy/checkout-service -- redis-cli -h <CACHE_HOST> ping
   ```
   - Expected: `PONG`
   - IF no response: restart the cache connection by rolling the deployment:
     ```bash
     kubectl rollout restart deployment/checkout-service -n checkout
     ```

## Verification

After taking corrective action, confirm resolution:

- [ ] Error rate < 0.5% for 5 consecutive minutes on Datadog dashboard
- [ ] All 6 pods in `Running` state with 0 recent restarts
- [ ] `/healthz` endpoint returns all dependencies `connected`
- [ ] PagerDuty alert auto-resolves within 10 minutes

## Rollback

- **Step 3 (restart)**: No rollback needed — restart is non-destructive.
- **Step 5 (kill connections)**: No rollback needed — application reconnects automatically.
- **Step 6 (restart)**: If restart makes things worse, roll back to previous image:
  ```bash
  kubectl rollout undo deployment/checkout-service -n checkout
  ```

## Escalation

Escalate if:
- Issue is not resolved within 15 minutes of starting this runbook
- Root cause is outside checkout-service (database, payment gateway, infrastructure)
- You lack the required access or permissions

| Contact | Method | Fallback |
|---------|--------|----------|
| checkout-team | PagerDuty policy: `checkout-primary` | Slack: `#checkout-eng` |
| dba-team | PagerDuty policy: `dba-oncall` | Slack: `#dba-support` |
| payments-team | PagerDuty policy: `payments-primary` | Slack: `#payments-eng` |

If primary contact does not respond within 10 minutes, use the fallback channel.

## Related Runbooks

- `payment-gateway-outage` — When the payment provider is down
- `checkout-db-connection-exhaustion` — Detailed database connection pool debugging
- `checkout-service-high-latency` — When errors are low but response times are elevated
