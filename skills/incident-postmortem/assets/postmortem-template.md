# Postmortem Template

Copy this template for each new incident postmortem. Fill in every section — incomplete sections should be marked `[PENDING — owner, deadline]` rather than left blank.

---

## Metadata

```
Incident ID:       INC-___
Severity:          SEV_ (see severity classification)
Date:              YYYY-MM-DD
Duration:          _h _m (onset to resolution)
Author:            _______________
Reviewers:         _______________
Status:            [ ] Draft  [ ] In Review  [ ] Final
Postmortem date:   YYYY-MM-DD (must be within 5 business days of resolution)
```

**Tags:** `[ ] data-loss` `[ ] security` `[ ] customer-facing` `[ ] internal-only` `[ ] third-party` `[ ] deploy-related` `[ ] config-change` `[ ] capacity`

---

## 1. Incident Summary

_3-5 sentences. What broke, who was affected, how long it lasted, how it was fixed. Written so someone outside the team can understand._

```
On YYYY-MM-DD at HH:MM UTC, [service/system] began [symptoms].
Approximately [number] [users/requests/transactions] were affected over
[duration]. The issue was caused by [root cause summary]. Service was
restored at HH:MM UTC by [mitigation action].
```

---

## 2. Timeline

_All timestamps in UTC. Include detection lag. Tag each entry._

```
HH:MM UTC  [ONSET]
HH:MM UTC  [DETECTION]
HH:MM UTC  [RESPONSE]
HH:MM UTC  [DIAGNOSIS]
HH:MM UTC  [ESCALATION]
HH:MM UTC  [MITIGATION]
HH:MM UTC  [MITIGATION]
HH:MM UTC  [RESOLUTION]
```

**Detection lag:** _ minutes (onset to first alert)

---

## 3. Impact

- **Duration:** Total incident time (onset to resolution): _h _m. User-facing downtime: _h _m.
- **Users affected:** [count or percentage, segmented if applicable]
- **Revenue impact:** [lost transactions, failed payments, SLA credits]
- **Downstream effects:** [other services, teams, or partners impacted]
- **Detection time:** [time between onset and first human awareness]
- **SLA impact:** [effect on monthly/quarterly SLA commitments]

---

## 4. Contributing Factors

_List every factor that contributed to the incident occurring or lasting longer than necessary. Frame as system failures, not personal failures._

1.
2.
3.
4.

---

## 5. Root Cause

_The deepest systemic cause. Not "someone made a mistake" — the system condition that allowed the mistake to have impact._

```
Root cause:
```

---

## 6. Action Items

| Priority | Action Item | Owner | Deadline | Ticket |
|----------|-------------|-------|----------|--------|
| **P0** | | | YYYY-MM-DD | |
| **P1** | | | YYYY-MM-DD | |
| **P1** | | | YYYY-MM-DD | |
| **P2** | | | YYYY-MM-DD | |

**Priority definitions:**
- **P0** — Before next on-call rotation. Prevents immediate recurrence.
- **P1** — Within 2 weeks. Reduces severity or detection time.
- **P2** — Within 30 days. Improves resilience or observability.

---

## 7. Lessons Learned

**What went well:**
-
-

**What went poorly:**
-
-

**Where we got lucky:**
-
-

---

## Tag Legend

| Tag | When to Use |
|-----|-------------|
| `data-loss` | Any incident where user or system data was lost, corrupted, or made inconsistent |
| `security` | Unauthorized access, data exposure, credential compromise, or vulnerability exploitation |
| `customer-facing` | Users experienced errors, degraded performance, or loss of functionality |
| `internal-only` | Impact limited to internal systems, tooling, or workflows — no external user impact |
| `third-party` | Root cause or contributing factor involves an external vendor or service |
| `deploy-related` | Incident triggered by or correlated with a code deployment or release |
| `config-change` | Incident triggered by a configuration change (feature flag, infra config, DNS, etc.) |
| `capacity` | System exceeded capacity limits (CPU, memory, disk, connections, rate limits) |
