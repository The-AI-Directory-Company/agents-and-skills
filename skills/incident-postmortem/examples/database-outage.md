# Incident Postmortem: Database Connection Pool Exhaustion

## Incident Summary

On 2025-08-14 at 09:17 UTC, the primary API service began returning 503 errors to approximately 34,000 users over a 62-minute period. The root cause was connection pool exhaustion on the PostgreSQL primary database, triggered by a long-running analytics query that acquired and held connections without a statement timeout. Service was restored at 10:19 UTC by killing the offending queries and restarting application pods.

## Timeline

```
08:45 UTC  [ONSET]      Analytics team runs ad-hoc query against production replica
09:02 UTC  [ONSET]      Replica lag triggers failover; query re-routes to primary
09:17 UTC  [ONSET]      Primary connection pool (max 100) saturated; API requests queue
09:23 UTC  [DETECTION]  PagerDuty alert: API error rate > 10% (6 min detection lag)
09:25 UTC  [RESPONSE]   On-call SRE acknowledges, begins investigating
09:34 UTC  [DIAGNOSIS]  SRE identifies 47 idle-in-transaction connections from analytics
09:41 UTC  [ESCALATION] Database team paged for pg_terminate_backend access
09:55 UTC  [MITIGATION] Long-running queries terminated; pool begins draining
10:05 UTC  [MITIGATION] Application pods restarted to reset connection state
10:19 UTC  [RESOLUTION] Error rate returns to baseline, all health checks green
```

## Impact

- **Duration**: 62 minutes (09:17 – 10:19 UTC)
- **Users affected**: ~34,000 (18% of active users during window)
- **Revenue impact**: ~$127,000 in failed transactions; $8,200 in SLA credits issued
- **Downstream effects**: Mobile app showed blank screens; webhook deliveries delayed 45 min
- **Detection lag**: 6 minutes between first 503 and PagerDuty alert

## Contributing Factors

- Production replica had no query timeout configured, allowing unbounded queries
- Replica-to-primary failover automatically re-routed the analytics query without guardrails
- Connection pool (max 100) was sized for API traffic only, with no reservation or priority lanes
- On-call SRE lacked `pg_terminate_backend` permissions, requiring a 7-minute escalation
- No runbook existed for connection pool exhaustion — diagnosis relied on tribal knowledge

## Root Cause

The database had no statement timeout enforced at the connection level. When an ad-hoc analytics query failed over from replica to primary, it consumed connections indefinitely. The system lacked any mechanism to isolate analytical workloads from transactional traffic on the primary database.

## Action Items

| Priority | Action Item | Owner | Deadline | Ticket |
|----------|-------------|-------|----------|--------|
| **P0** | Set `statement_timeout = 30s` on all primary DB connections | @database-team | 2025-08-16 | DB-1204 |
| **P0** | Add connection pool utilization alert at 80% threshold | @sre-team | 2025-08-16 | SRE-445 |
| **P1** | Block replica-to-primary query failover for analytics role | @database-team | 2025-08-28 | DB-1205 |
| **P1** | Grant on-call SREs `pg_terminate_backend` permission | @security-team | 2025-08-21 | SEC-312 |
| **P2** | Create connection pool exhaustion runbook | @sre-team | 2025-09-15 | SRE-448 |
| **P2** | Provision dedicated analytics database for ad-hoc queries | @platform-team | 2025-09-30 | PLAT-89 |

## Lessons Learned

**What went well**
- SRE correctly identified the root cause within 9 minutes of engaging
- Application pods recovered cleanly after restart with no data corruption
- Customer support team communicated status page updates within 10 minutes

**What went poorly**
- No alert on connection pool saturation — we only caught it via downstream error rates
- Escalation to database team added 7 minutes because of missing permissions
- No separation between analytical and transactional database workloads

**Where we got lucky**
- The analytics query was read-only — a write-heavy query could have caused data corruption
- The incident occurred during off-peak hours (09:17 UTC); during US peak it would have affected 3x more users
- No data was lost — all failed transactions returned clean errors and users could retry
