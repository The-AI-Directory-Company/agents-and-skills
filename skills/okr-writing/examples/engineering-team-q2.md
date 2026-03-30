# Example: Engineering Team Q2 OKRs

This is a fully worked OKR set for a platform engineering team at a mid-stage SaaS company. It demonstrates alignment chains, measurable KRs with baselines, and proper objective framing.

---

## Context

- **Company:** B2B SaaS, 200 employees, Series C
- **Company-level Q2 objective:** "Accelerate enterprise adoption to reach $20M ARR by year-end"
- **Department (Engineering) Q2 objective:** "Improve platform reliability and developer velocity to support 3x enterprise workload growth"
- **This team:** Platform Engineering (8 engineers, 1 EM, 1 SRE)

---

## Q2 2025 OKRs -- Platform Engineering

### Objective 1: Establish production reliability that earns enterprise customer confidence

**Alignment:**
```
Company: "Accelerate enterprise adoption to reach $20M ARR by year-end"
  -> Eng Dept: "Improve platform reliability and developer velocity"
    -> This team: "Establish production reliability that earns enterprise customer confidence"
```

_Rationale: Enterprise prospects cited reliability concerns in 4 of 6 recent lost deals (per Sales). Improving uptime and incident response directly supports enterprise adoption._

| KR# | Key Result | Baseline | Target | Owner |
|-----|-----------|----------|--------|-------|
| 1.1 | Increase production uptime (p50, monthly) from 99.7% to 99.95% | 99.7% | 99.95% | @priya-n (SRE) |
| 1.2 | Reduce mean time to recovery (MTTR) for P1 incidents from 47 minutes to under 15 minutes | 47 min | < 15 min | @david-c (Platform Lead) |
| 1.3 | Reduce customer-facing error rate (5xx responses / total requests, daily) from 0.8% to under 0.2% | 0.8% | < 0.2% | @sam-w (Backend) |

**Why these KRs work:**
- Each measures an outcome, not a task. "Deploy redundant failover" would be a task; uptime improvement is the outcome.
- KR 1.1 and KR 1.3 both measure reliability but from different angles (availability vs. error rate). They are independently valuable.
- KR 1.2 addresses incident response, which matters even when incidents still occur.

---

### Objective 2: Accelerate developer shipping velocity across all product teams

**Alignment:**
```
Company: "Accelerate enterprise adoption to reach $20M ARR by year-end"
  -> Eng Dept: "Improve platform reliability and developer velocity"
    -> This team: "Accelerate developer shipping velocity across all product teams"
```

_Rationale: Internal developer survey (Q1) showed CI/CD pipeline and environment spin-up as the top two friction points. Product teams estimate 15-20% of sprint capacity is lost to infrastructure friction._

| KR# | Key Result | Baseline | Target | Owner |
|-----|-----------|----------|--------|-------|
| 2.1 | Reduce median CI pipeline duration from 22 minutes to under 8 minutes | 22 min | < 8 min | @alex-r (DevEx) |
| 2.2 | Reduce staging environment provisioning time from 45 minutes to under 5 minutes | 45 min | < 5 min | @maria-l (Platform) |
| 2.3 | Increase deployment frequency (company-wide median, per team per week) from 2.1 to 5+ | 2.1/week | 5+/week | @david-c (Platform Lead) |

**Why these KRs work:**
- KR 2.1 and KR 2.2 are input metrics the platform team directly controls.
- KR 2.3 is an outcome metric that depends on product teams adopting the improvements. It creates accountability for adoption, not just delivery.
- The baseline data comes from observable systems (CI logs, provisioning timestamps, deploy tracking), so scoring at end-of-quarter is straightforward.

---

### Objective 3: Build the observability foundation for data-driven engineering decisions

**Alignment:**
```
Company: "Accelerate enterprise adoption to reach $20M ARR by year-end"
  -> Eng Dept: "Improve platform reliability and developer velocity"
    -> This team: "Build the observability foundation for data-driven engineering decisions"
```

_Rationale: Objective 1 (reliability) and Objective 2 (velocity) both require better instrumentation. Today, 60% of P1 incidents are detected by customers before internal monitoring. Without observability, the team is flying blind._

| KR# | Key Result | Baseline | Target | Owner |
|-----|-----------|----------|--------|-------|
| 3.1 | Increase the percentage of P1 incidents detected by monitoring (before customer report) from 40% to 90% | 40% | 90% | @priya-n (SRE) |
| 3.2 | Achieve distributed tracing coverage across services handling > 1% of traffic, from 35% of services to 100% | 35% | 100% | @sam-w (Backend) |
| 3.3 | Reduce mean time to root cause identification for P1/P2 incidents from 2.5 hours to under 30 minutes | 2.5 hrs | < 30 min | @alex-r (DevEx) |

**Why these KRs work:**
- KR 3.1 measures detection quality, not just "did we add alerts." Adding 50 alerts that fire false positives would not improve this number.
- KR 3.2 has a clear, verifiable completion criterion (100% of qualifying services).
- KR 3.3 measures the downstream impact of observability investment, connecting tooling to incident resolution.

---

## Alignment Summary

| This Team's Objective | Dept Objective It Supports | Company Objective It Supports |
|---|---|---|
| O1: Establish production reliability | Improve platform reliability and developer velocity | Accelerate enterprise adoption |
| O2: Accelerate developer shipping velocity | Improve platform reliability and developer velocity | Accelerate enterprise adoption |
| O3: Build observability foundation | Improve platform reliability and developer velocity | Accelerate enterprise adoption |

All three objectives trace to the same department and company objectives. This is appropriate for a platform team whose work is horizontally enabling. A product team would typically align to multiple company objectives.

---

## What Makes This Set Well-Calibrated

1. **Three objectives, nine KRs.** Within the recommended bounds (3-5 objectives, 2-5 KRs each).
2. **Every KR has a baseline.** No guessing at the starting point.
3. **Mix of difficulty.** KR 3.2 (100% tracing coverage) is aggressive. KR 2.3 (5+ deploys/week) depends on other teams adopting changes. KR 1.1 (99.95% uptime) requires systemic improvement, not a single fix. A 0.7 average score would represent genuine success.
4. **No tasks disguised as KRs.** None of these say "ship X" or "complete Y project." They all measure the outcome the project should produce.
5. **Each KR has a single owner.** The owner is a person, not a team or channel.
