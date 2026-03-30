# Example: Data Platform Migration -- RED Status Report

This example demonstrates how to write a RED-status report that leads with bad news, presents clear options for decisions needed, and sets deadlines for resolution.

---

```
Program: Data Platform Migration (Postgres -> Snowflake)
Period: Mar 17-28, 2025
Overall Status: RED
Author: T. Nakamura (Technical Program Manager)
Distribution: VP Engineering, CTO, Steering Committee
```

---

## Executive Summary

The Data Platform Migration is **off track**. The originally planned March 28 cutover milestone will be missed by an estimated 3-4 weeks due to two compounding issues: (1) the legacy ETL pipeline produces data inconsistencies that must be resolved before cutover, and (2) the vendor providing the CDC (Change Data Capture) connector has delayed delivery of a critical patch from March 14 to "early April" with no firm date. If the steering committee does not approve the revised timeline and additional contractor budget by April 4, downstream programs (Q2 analytics launch, enterprise reporting) will also miss their dates. The team has identified three options presented in the Decisions Needed section below.

---

## Status by Workstream

| Workstream | Owner | Status | Progress This Period | Next Milestone | Risk |
|---|---|---|---|---|---|
| Schema migration | @R. Okafor | GREEN | 14/14 schemas migrated and validated | Final integrity check -- Apr 1 | None |
| ETL pipeline rebuild | @J. Pham | RED | Data reconciliation found 3 critical discrepancies in revenue tables | Discrepancies resolved -- est. Apr 11 | Discrepancies block cutover -- see Risks |
| CDC connector | @A. Mehta | RED | Vendor patch delayed; workaround under evaluation | Vendor patch delivery -- TBD (vendor says "early April") | No firm delivery date -- see Risks |
| Dashboard migration | @L. Torres | YELLOW | 8/12 dashboards rebuilt; 4 blocked on ETL fixes | All dashboards rebuilt -- Apr 18 (revised) | Depends on ETL workstream |
| User acceptance testing | @K. Singh | YELLOW | Test plan complete; execution blocked until ETL and CDC are stable | UAT start -- Apr 14 (revised) | Cannot begin until RED workstreams resolve |

---

## Milestones

| # | Milestone | Original Date | Revised Date | Owner | Confidence | Dependency |
|---|-----------|--------------|-------------|-------|------------|------------|
| 1 | Schema migration validated | Mar 21 | Mar 21 (DONE) | @R. Okafor | Complete | -- |
| 2 | ETL discrepancies resolved | Mar 25 | Apr 11 | @J. Pham | Low | Root cause analysis in progress |
| 3 | CDC vendor patch delivered | Mar 14 | TBD ("early April") | @A. Mehta | Low | Vendor-dependent |
| 4 | All dashboards rebuilt | Mar 28 | Apr 18 | @L. Torres | Medium | Depends on #2 |
| 5 | UAT complete | Apr 4 | Apr 25 | @K. Singh | Medium | Depends on #2, #3 |
| 6 | Production cutover | Mar 28 | Apr 28 (proposed) | @T. Nakamura | Low | Depends on #2, #3, #5 |

---

## Risks and Mitigations

### Risk 1: ETL data discrepancies in revenue tables

- **Risk:** Three revenue-related tables show row-count mismatches (2-5%) between legacy Postgres and Snowflake after full ETL run. Root cause is suspected to be timezone handling in the legacy extraction scripts.
- **Impact:** Production cutover cannot proceed with revenue data discrepancies. Finance and enterprise reporting depend on exact parity. Any discrepancy in revenue numbers will be escalated by the CFO.
- **Likelihood:** High (discrepancies are confirmed; only resolution timeline is uncertain)
- **Mitigation:** @J. Pham is running row-level diff analysis to isolate the timezone issue. A contractor with legacy ETL experience has been identified (available Apr 1, $18K for 3 weeks).
- **Owner:** @J. Pham
- **Escalation trigger:** If root cause is not identified by Apr 4, request steering committee approval for contractor engagement.

### Risk 2: CDC vendor patch has no firm delivery date

- **Risk:** The CDC connector vendor (StreamSync) acknowledged a bug affecting our configuration on Feb 28. They committed to a patch by Mar 14, then pushed to "early April" without a specific date. Our account rep has stopped responding within SLA.
- **Impact:** Without the patch, real-time data sync is unavailable. The workaround (batch sync every 15 minutes) is functional but degrades the experience for 3 enterprise customers who require near-real-time dashboards.
- **Likelihood:** Medium-High (vendor has missed one deadline already)
- **Mitigation:** (a) @A. Mehta is evaluating the 15-minute batch workaround as a permanent fallback. (b) @T. Nakamura has requested a call with the vendor's VP of Engineering for the week of Mar 31. (c) If the vendor cannot commit by Apr 7, the team will evaluate switching to Debezium (open source), estimated 2-week integration effort.
- **Owner:** @A. Mehta (technical), @T. Nakamura (vendor relationship)
- **Escalation trigger:** No firm vendor commitment by Apr 7 -- will need CTO to authorize Debezium pivot and associated 2-week delay.

### Risk 3: Dashboard migration blocked by upstream workstreams

- **Risk:** 4 of 12 dashboards depend on the revenue tables affected by Risk 1. They cannot be validated until ETL discrepancies are resolved.
- **Impact:** Dashboard migration extends by the same duration as the ETL delay, plus 3-5 days for validation.
- **Likelihood:** High (direct dependency)
- **Mitigation:** @L. Torres is completing all non-blocked dashboards now. Blocked dashboards are pre-built and will be validated as soon as ETL is fixed -- estimated 3-5 day validation sprint.
- **Owner:** @L. Torres
- **Escalation trigger:** None -- this risk resolves when Risk 1 resolves.

---

## Decisions Needed

### Decision 1: Approve revised program timeline

**Context:** The original Mar 28 cutover date is no longer achievable. Three options are presented below.

| Option | Cutover Date | Cost Impact | Risk Level | Trade-off |
|--------|-------------|-------------|------------|-----------|
| **A. Wait for vendor + fix ETL** | Apr 28 | +$18K (contractor) | Medium | Safest path but delays Q2 analytics launch by 4 weeks |
| **B. Batch workaround + fix ETL** | Apr 18 | +$18K (contractor) | Medium-High | Meets a tighter date but 3 enterprise customers get degraded real-time experience |
| **C. Pivot to Debezium + fix ETL** | May 9 | +$18K (contractor) + ~$30K (Debezium integration) | Low (eliminates vendor dependency) | Longest timeline but removes ongoing vendor risk entirely |

**Recommendation:** Option A as the baseline plan, with automatic escalation to Option C if the vendor does not deliver by Apr 7.

**Decision deadline:** Apr 4 steering committee meeting.

---

### Decision 2: Approve contractor budget for ETL specialist

**Context:** The ETL discrepancy root cause analysis requires legacy system expertise that the current team lacks. A contractor with relevant experience is available starting Apr 1.

- **Budget:** $18,000 for 3 weeks
- **Alternative:** Current team continues investigation, adding an estimated 2-3 additional weeks to resolution with lower confidence.
- **Recommendation:** Approve the contractor. The cost is small relative to the program delay cost ($~50K/week in delayed enterprise revenue enablement).
- **Decision deadline:** Mar 31 (contractor availability expires Apr 2).

---

## Key Metrics

| Metric | Last Period | This Period | Trend | Note |
|--------|-----------|-------------|-------|------|
| Schemas migrated | 12/14 | 14/14 | Complete | |
| ETL data parity (table-level) | 89% | 91% | Improving slowly | 3 critical tables remain |
| Dashboards rebuilt | 5/12 | 8/12 | On track (for non-blocked) | 4 blocked on ETL |
| Days since vendor patch commitment | 14 | 28 | Worsening | No firm date |
| Program budget consumed | 62% | 71% | On track | Does not include proposed contractor |
