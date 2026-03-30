# Release Checklist Template

Fill in all sections before scheduling the release window. Every Go/No-Go row must be "Go" to proceed.

## Release Summary

| Field | Value |
|-------|-------|
| Release name / version | |
| Service(s) | |
| Release manager | |
| On-call engineer | |
| Scheduled date/time (UTC) | |
| Risk classification | Low / Medium / High |
| Rollback strategy | Feature flag / Blue-green / Canary / Redeploy |

---

## Go/No-Go Table

| # | Criteria | Owner | Status | Notes |
|---|----------|-------|--------|-------|
| 1 | All CI checks pass on release branch | | Go / No-Go | |
| 2 | Staging smoke tests pass | | Go / No-Go | |
| 3 | Database migration tested and reversible | | Go / No-Go | |
| 4 | Rollback procedure documented and tested | | Go / No-Go | |
| 5 | On-call engineer identified and available | | Go / No-Go | |
| 6 | Feature flags configured in all target environments | | Go / No-Go | |
| 7 | Secrets and env vars set in target environments | | Go / No-Go | |
| 8 | Dependent services deployed and healthy | | Go / No-Go | |
| 9 | Stakeholders notified of release window | | Go / No-Go | |
| 10 | Support team briefed on new behavior | | Go / No-Go | |

**Decision**: [ ] GO -- [ ] NO-GO

**Decision made by**: _____________________ **Time (UTC)**: _____________________

---

## Staged Rollout Plan

| Stage | Traffic % | Bake Time | Start Time (UTC) | Metric Thresholds | Proceed? |
|-------|-----------|-----------|-------------------|--------------------|----------|
| Canary | 1-5% | 15-30 min | | Error rate < 0.1%, p99 < baseline + 20% | Y / N |
| Partial | 25% | 30-60 min | | Error rate < 0.05%, no new error signatures | Y / N |
| Majority | 75% | 60 min | | Same as partial | Y / N |
| Full | 100% | Ongoing | | Same as partial | Y / N |

---

## Monitoring Checkpoints

Complete at each rollout stage. Record the actual values, not just pass/fail.

| Checkpoint | Baseline | Canary | 25% | 75% | 100% |
|------------|----------|--------|-----|-----|------|
| Error rate (%) | | | | | |
| p50 latency (ms) | | | | | |
| p95 latency (ms) | | | | | |
| p99 latency (ms) | | | | | |
| CPU utilization (%) | | | | | |
| Memory utilization (%) | | | | | |
| Connection pool usage (%) | | | | | |
| Business KPI: _____________ | | | | | |
| Downstream svc error rate (%) | | | | | |

**Dashboard URL**: _____________________

**Alert channel**: _____________________

---

## Rollback Triggers

If **any** of these conditions are met, initiate rollback immediately:

- [ ] Error rate exceeds 2x baseline for > 5 minutes
- [ ] p99 latency exceeds 3x baseline
- [ ] Data corruption or consistency issue detected
- [ ] Dependent service reports degradation traced to this release
- [ ] Feature flag kill switch fails to disable new behavior

**Rollback initiated?** [ ] Yes / [ ] No

**Rollback initiated by**: _____________________ **Time (UTC)**: _____________________

**Rollback reason**: _____________________

---

## Post-Release Verification

| Check | Status | Completed by | Time (UTC) |
|-------|--------|--------------|------------|
| Metrics stable for 1 hour at 100% | | | |
| Smoke tests pass in production | | | |
| No new alerts firing | | | |
| Stakeholders notified of success | | | |
| Release notes published | | | |
| Support team briefed | | | |
| Feature flags scheduled for removal | | | |
| Old artifacts scheduled for teardown | | | |
| Retrospective scheduled (if high-risk) | | | |
