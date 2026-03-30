# Postmortem Example: Third-Party API Degradation

This example covers a partial outage caused by an upstream dependency — a scenario where the primary contributing factors are outside your direct control but the response, detection, and resilience gaps are yours.

---

## Incident Summary

On 2024-06-18 at 09:14 UTC, the order fulfillment service began experiencing elevated latency and intermittent 503 errors due to degraded performance from our shipping rate provider (ShipCalc API). Approximately 35% of checkout attempts failed or timed out during the 2-hour, 12-minute incident window. The issue was not a full outage — ShipCalc responded to approximately 65% of requests normally, while the remaining requests either timed out (>8s) or returned malformed JSON. Service was restored at 11:26 UTC after enabling a cached-rate fallback that had been implemented but never activated in production.

## Timeline

```
09:14 UTC  [ONSET]      ShipCalc API response times begin increasing (p99 jumps from 200ms to 4.2s)
09:22 UTC  [ONSET]      First 503 errors appear in order fulfillment service logs
09:31 UTC  [DETECTION]  PagerDuty alert fires: checkout error rate > 3%
09:34 UTC  [RESPONSE]   On-call engineer acknowledges alert
09:38 UTC  [DIAGNOSIS]  Engineer observes fulfillment service timeouts; initially suspects internal DB
09:47 UTC  [DIAGNOSIS]  DB metrics normal; engineer traces to ShipCalc API call latency
09:52 UTC  [ESCALATION] Engineer checks ShipCalc status page — shows "All Systems Operational"
09:55 UTC  [DIAGNOSIS]  Engineer confirms ~35% of ShipCalc requests timing out via request logs
10:05 UTC  [ESCALATION] Support ticket filed with ShipCalc; no immediate response
10:12 UTC  [ESCALATION] Engineering manager paged; decision to pursue internal mitigation
10:25 UTC  [MITIGATION] Team identifies cached-rate fallback exists in code but is disabled (feature flag OFF)
10:38 UTC  [MITIGATION] Fallback flag enabled in staging; smoke test passes
10:52 UTC  [MITIGATION] Fallback flag enabled in production for 10% of traffic
11:05 UTC  [MITIGATION] Monitoring confirms fallback working; rolled to 50%
11:18 UTC  [MITIGATION] Rolled to 100% of traffic using fallback for timed-out requests
11:26 UTC  [RESOLUTION] Error rates return to baseline; incident closed
12:45 UTC  [EXTERNAL]   ShipCalc acknowledges degradation on their status page
14:30 UTC  [EXTERNAL]   ShipCalc reports issue resolved on their end
```

**Detection lag:** 17 minutes (09:14 onset to 09:31 first alert). The alert triggered on checkout error rate, not on upstream API latency — a more specific alert would have fired sooner.

## Impact

- **Duration:** 2 hours, 12 minutes (09:14 - 11:26 UTC)
- **Users affected:** ~8,400 checkout attempts during the window. ~2,940 (35%) received errors or timeouts.
- **Revenue impact:** Estimated $47,000 in delayed or abandoned orders. Post-incident analysis showed 60% of affected users retried successfully after resolution; 40% did not return within 24 hours.
- **Downstream effects:** Customer support received 156 tickets about checkout failures. Fulfillment queue backlog delayed ~200 orders by 1-3 hours after resolution.
- **Detection time:** 17 minutes to first alert. 33 minutes to correctly identify the upstream dependency as the cause.
- **SLA impact:** Monthly uptime dropped to 99.89% against a 99.95% target.

## Contributing Factors

- **No direct monitoring of upstream API health.** The fulfillment service had no alerting on ShipCalc response times or error rates. The only signal was the downstream effect on checkout errors, which introduced a 17-minute detection delay.
- **Lack of circuit breaker on the ShipCalc integration.** The fulfillment service retried failed ShipCalc requests up to 3 times with no backoff, amplifying the load on an already degraded service and increasing end-user latency.
- **Cached-rate fallback existed but was never production-tested.** The feature flag for the fallback had been implemented 4 months earlier but left OFF. No runbook documented its existence or activation procedure. The on-call engineer discovered it by searching the codebase.
- **ShipCalc status page did not reflect the degradation.** The vendor's status page showed "All Systems Operational" for over 3 hours after the issue began. This delayed the team's confidence in diagnosing an external cause.
- **Partial failure was harder to diagnose than a full outage.** Because 65% of requests succeeded, initial metrics looked like intermittent internal errors rather than a dependency failure. A full outage would have been identified immediately.

## Root Cause

The root cause was the absence of resilience patterns (circuit breakers, fallback activation, upstream health monitoring) around a critical third-party dependency. The system treated ShipCalc as if it were an internal service with guaranteed reliability, despite it being outside our operational control. When ShipCalc degraded partially, the fulfillment service had no mechanism to detect, isolate, or mitigate the impact.

## Action Items

| Priority | Action Item | Owner | Deadline | Ticket |
|----------|-------------|-------|----------|--------|
| **P0** | Enable cached-rate fallback in production with automatic activation when ShipCalc error rate exceeds 10% | @fulfillment-team | 2024-06-25 | FUL-412 |
| **P0** | Add PagerDuty alert on ShipCalc API p99 latency > 1s and error rate > 5% | @platform-team | 2024-06-21 | OPS-934 |
| **P1** | Implement circuit breaker on ShipCalc integration with exponential backoff | @fulfillment-team | 2024-07-05 | FUL-413 |
| **P1** | Add ShipCalc health check to service dependency dashboard | @platform-team | 2024-07-01 | OPS-935 |
| **P1** | Document fallback activation procedure in on-call runbook | @fulfillment-team | 2024-06-24 | FUL-414 |
| **P2** | Evaluate backup shipping rate provider for multi-vendor redundancy | @fulfillment-team | 2024-07-31 | FUL-420 |
| **P2** | Establish SLA expectations with ShipCalc and require status page webhook notifications | @vendor-management | 2024-07-15 | VM-089 |

## Lessons Learned

**What went well:**
- The cached-rate fallback, although never activated, worked correctly when enabled. The 4-month-old implementation required no code changes.
- The gradual rollout (10% -> 50% -> 100%) allowed the team to validate the fallback safely under production traffic.
- The on-call engineer's decision to search the codebase for existing fallback mechanisms, rather than building one from scratch, saved approximately 90 minutes.

**What went poorly:**
- 17-minute detection lag because upstream API health was not monitored directly.
- 33 additional minutes to correctly attribute the issue to ShipCalc (initial investigation focused on internal DB).
- The fallback existed but no one on the current on-call rotation knew about it. Institutional knowledge had not been captured in the runbook.
- ShipCalc's status page was unreliable as a diagnostic signal, and we had no independent verification mechanism.

**Where we got lucky:**
- The cached shipping rates were recent enough (< 48 hours old) to be commercially acceptable. If the last cache refresh had failed, the fallback would have served stale or empty rates.
- The incident occurred during a low-traffic window (Tuesday morning UTC). Peak traffic would have tripled the revenue impact.
- The partial nature of the failure (35% of requests) meant 65% of users were unaffected. A full ShipCalc outage with the same response time would have caused 100% checkout failure.
