# Non-Functional Requirement Target Ranges

Reference ranges by system type. Use these as starting points --- adjust based on your SLAs, user expectations, and business context.

---

## Availability

| System Type | Target | Downtime / Year | Typical Use |
|-------------|--------|-----------------|-------------|
| Internal tooling | 99.0% | ~87 hours | Admin dashboards, back-office tools |
| Standard SaaS (B2B) | 99.9% | ~8.7 hours | Business applications, CRM, project management |
| User-facing consumer | 99.95% | ~4.4 hours | E-commerce, social platforms, content delivery |
| Financial / payments | 99.99% | ~52 minutes | Payment processing, trading, banking |
| Infrastructure / platform | 99.99% | ~52 minutes | Cloud providers, DNS, auth services |
| Safety-critical | 99.999% | ~5 minutes | Healthcare monitoring, aviation, emergency services |

**Notes:**
- Availability targets apply to the critical path. Non-critical features (analytics dashboard, export) can have lower targets.
- Measure availability over a rolling 30-day window, not calendar month.
- Distinguish between partial degradation and full outage. A system returning cached results is degraded, not down.

---

## Latency (P99)

| System Type | P50 | P95 | P99 | Notes |
|-------------|-----|-----|-----|-------|
| Static content / CDN | < 20ms | < 50ms | < 100ms | Measured at edge |
| User-facing API (read) | < 50ms | < 150ms | < 300ms | Excludes network RTT |
| User-facing API (write) | < 100ms | < 300ms | < 500ms | Includes DB write |
| Search / query | < 100ms | < 300ms | < 500ms | Depends on index size |
| Real-time / WebSocket | < 50ms | < 100ms | < 200ms | Message delivery latency |
| Internal service-to-service | < 10ms | < 30ms | < 50ms | Same region, direct call |
| Batch / async processing | < 1s | < 5s | < 30s | Queue-to-completion |
| Report generation | < 5s | < 15s | < 60s | Depends on data volume |
| ML inference (online) | < 50ms | < 150ms | < 300ms | Single request |
| ML inference (batch) | N/A | N/A | < 1 min / 1K items | Throughput-oriented |

**Notes:**
- Always measure P99, not average. Average latency hides tail behavior that affects real users.
- Latency budgets should account for the full request chain. If three services each take P99 = 100ms, the end-to-end P99 is NOT 300ms --- it is worse due to tail correlation.
- Set an error budget: if P99 exceeds the target more than X% of the time in a measurement window, trigger investigation.

---

## Throughput

| System Type | Baseline | Peak (2-3x) | Burst (10x, seconds) | Sizing Method |
|-------------|----------|-------------|----------------------|---------------|
| Internal tool | 10-50 req/s | 100 req/s | 200 req/s | Active users x actions/min |
| Standard B2B SaaS | 100-500 req/s | 1,500 req/s | 5,000 req/s | DAU x avg requests/session / seconds in peak hour |
| Consumer web app | 1,000-5,000 req/s | 15,000 req/s | 50,000 req/s | Same, with higher DAU |
| API platform | 5,000-50,000 req/s | 150,000 req/s | 500,000 req/s | Sum of client consumption rates |
| Event ingestion | 10,000-100,000 events/s | 300,000 events/s | 1M events/s | Telemetry volume |

**Sizing formula:**

```
Peak RPS = (DAU x avg_requests_per_session) / (peak_hour_seconds)
         = (DAU x RPSession) / 3600

Headroom = Peak RPS x 3 (for traffic spikes)
```

**Notes:**
- Design for peak, not average. If Black Friday is 5x normal, size for 5x.
- Async workloads (queues, batch) should be sized for sustained throughput, not burst.
- Load test to 2x your expected peak before launch.

---

## Data Retention

| Data Type | Hot Storage | Warm Storage | Cold / Archive | Deletion |
|-----------|-------------|--------------|----------------|----------|
| User session data | 24 hours | 7 days | 30 days | After 30 days |
| Application logs | 7 days | 30 days | 1 year | After 1 year |
| Audit logs | 90 days | 1 year | 7 years | Per compliance |
| Transaction records | 90 days | 1 year | 7 years | Per compliance |
| User-generated content | Indefinite | N/A | N/A | On user deletion request |
| Analytics / metrics | 30 days (raw) | 1 year (aggregated) | 3 years (aggregated) | After retention period |
| ML training data | Duration of project | 1 year | 3 years | Per data governance policy |
| Backups | 7 days (hourly) | 30 days (daily) | 90 days (weekly) | Rolling |

**Notes:**
- GDPR requires deletion capability for personal data. Design for it from the start.
- Hot = primary database. Warm = read replica or cheaper storage. Cold = object storage (S3/GCS).
- Cost difference: hot storage can be 10-50x more expensive than cold. Tiering saves money at scale.

---

## Error Budgets

| Availability Target | Error Budget / Month | Error Budget / Quarter |
|--------------------|-----------------------|------------------------|
| 99.0% | 7.3 hours | 21.9 hours |
| 99.9% | 43.8 minutes | 2.2 hours |
| 99.95% | 21.9 minutes | 1.1 hours |
| 99.99% | 4.4 minutes | 13.1 minutes |
| 99.999% | 26 seconds | 1.3 minutes |

Use error budgets to make deployment decisions: if the budget is nearly exhausted, freeze risky deployments until the next window.

---

## Capacity Planning Rules of Thumb

1. **Never run above 70% utilization** on any resource (CPU, memory, disk, connections). Headroom absorbs spikes.
2. **Plan for 2x current peak** when provisioning new infrastructure.
3. **Database connections** are expensive. Use connection pooling. Target: max connections = 2x the number of application instances x connections per instance.
4. **Queue depth** should trend toward zero. If it grows consistently, consumers are undersized.
5. **Cache hit rate** should be > 90% for read-heavy workloads. Below 80% means the cache is not effective.
