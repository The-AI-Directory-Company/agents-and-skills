# Disaster Recovery Plan: Multi-Region Failover — Storefront Application

## Scope

This plan covers full-region failover of the Storefront web application from **us-east-1** (primary) to **us-west-2** (secondary). In scope: API servers, PostgreSQL database, Redis cache, CDN origin, and background job workers.

**Not in scope**: Third-party payment gateway (covered by `payment-gateway-dr-plan`), analytics pipeline (Tier 3, restored separately).

## Recovery Objectives

| System | RPO | RTO | Tier |
|--------|-----|-----|------|
| PostgreSQL (orders, users) | 1 minute | 15 minutes | Tier 1 |
| API servers | 0 (stateless) | 10 minutes | Tier 1 |
| Redis cache | 30 minutes | 10 minutes | Tier 2 |
| Background job workers | 1 hour | 30 minutes | Tier 2 |
| CDN origin | 0 (static assets in S3) | 5 minutes | Tier 1 |

## Backup Strategy

```
PostgreSQL:
  Method:       Streaming replication to us-west-2 standby + hourly WAL archive to S3
  Lag target:   < 30 seconds under normal load
  Retention:    7 days of WAL archives, 30 daily snapshots
  Storage:      S3 us-west-2 (cross-region from primary)
  Encryption:   AES-256 at rest, TLS 1.3 in transit
  Verification: Automated restore test every Sunday at 04:00 UTC; quarterly manual validation

Redis:
  Method:       RDB snapshots every 30 minutes, replicated to us-west-2 S3
  Retention:    48 hours of snapshots
  Note:         Cache can be rebuilt from database; snapshot is a warm-start optimization
```

## Failover Procedure

**Detection**: CloudWatch alarm `region-health-us-east-1` fires when API success rate < 95% for 5 minutes. PagerDuty escalation: `storefront-critical`.

**Decision authority**: VP Engineering (@dthompson) or SRE Tech Lead (@rgarcia). Either can authorize failover. If neither is reachable within 10 minutes, the on-call SRE may proceed.

### Steps

1. Confirm us-east-1 is down (not a transient blip):
   ```bash
   curl -s -o /dev/null -w "%{http_code}" https://api-east.storefront.internal/healthz
   ```
   - IF 200: false alarm. Monitor for 5 more minutes.
   - IF non-200 or timeout: proceed.

2. Verify us-west-2 standby database replication status:
   ```bash
   psql -h db-standby.us-west-2.internal -U sre_admin -c "SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;"
   ```
   - Expected: lag < 60 seconds. Note the exact lag for the incident record.
   - IF lag > 5 minutes: data loss exceeds RPO. Escalate to VP Engineering for go/no-go.

3. Promote standby database to primary:
   ```bash
   aws rds promote-read-replica --db-instance-identifier storefront-standby-west2
   ```
   - Wait for status to change to `available` (~2-5 minutes).

4. Update API server configuration to point to new primary database:
   ```bash
   kubectl set env deployment/storefront-api -n storefront DATABASE_URL="postgresql://app:$DB_PASS@db-primary.us-west-2.internal:5432/storefront" --context=us-west-2
   ```

5. Verify API servers are healthy in us-west-2:
   ```bash
   kubectl get pods -n storefront --context=us-west-2 -l app=storefront-api
   ```

6. Switch DNS to us-west-2:
   ```bash
   aws route53 change-resource-record-sets --hosted-zone-id <ZONE_ID> --change-batch file://failover-dns-west2.json
   ```
   - DNS TTL is 60 seconds. Full propagation within 2-3 minutes.

7. Start background workers in us-west-2:
   ```bash
   kubectl scale deployment/storefront-workers -n storefront --replicas=4 --context=us-west-2
   ```

## Data Validation (post-failover)

- [ ] Run `SELECT count(*) FROM orders WHERE created_at > now() - interval '1 hour'` — compare against last known metric
- [ ] Place a test order through the full checkout flow
- [ ] Verify user authentication works (login, session creation)
- [ ] Confirm background jobs are processing (check Sidekiq dashboard)

## Communication Protocol

| Audience | Channel | Timing | Owner |
|----------|---------|--------|-------|
| Incident commander | PagerDuty `storefront-critical` | Immediate | Automated |
| Engineering leadership | Slack #incidents | Within 5 min | Incident commander |
| Customer support | Slack #support-alerts + email template | Within 15 min | Comms lead |
| Customers | status.storefront.com + email | Within 20 min | Comms lead |
| Executive team | Email summary | Within 1 hour | VP Engineering |

## Testing Schedule

- **Tabletop exercise**: Quarterly (next: 2026-04-15), walk through this plan with all stakeholders
- **Database failover drill**: Semi-annual, promote standby and verify data integrity
- **Full failover drill**: Annual, complete DNS cutover to us-west-2 during low-traffic window (Sunday 05:00 UTC)
- **Replication lag monitoring**: Continuous — alert if lag > 60 seconds

## Plan Maintenance

- **Owner**: @rgarcia (SRE Tech Lead)
- **Review cadence**: Quarterly or after any infrastructure change
- **Last reviewed**: 2026-03-15
- **Next review**: 2026-06-15
