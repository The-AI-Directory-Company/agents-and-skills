# Severity Classification

Definitions for SEV1 through SEV4, with blast radius indicators, detection lag benchmarks, and SLA expectations. Use this classification when tagging incidents and setting priority for action items.

---

## Severity Levels

### SEV1 — Critical

**Definition:** Complete loss of a critical business function for all or most users. Revenue-generating or safety-critical systems are fully unavailable.

| Attribute | Benchmark |
|-----------|-----------|
| **Blast radius** | >50% of users or >50% of revenue-generating transactions affected |
| **Detection lag target** | <5 minutes |
| **Response time SLA** | On-call acknowledges within 5 minutes; incident commander assigned within 15 minutes |
| **Resolution target** | Mitigation within 1 hour; full resolution within 4 hours |
| **Communication cadence** | Status updates every 15 minutes to stakeholders during active incident |
| **Postmortem deadline** | Draft within 2 business days; final within 5 business days |
| **Examples** | Full site outage, data breach with confirmed exposure, payment processing completely down, authentication system unavailable |

**Escalation:** Automatically pages engineering leadership and incident commander. External communications (status page, customer notification) initiated within 30 minutes.

---

### SEV2 — Major

**Definition:** Significant degradation of a critical business function. The system is partially operational but a substantial portion of users experience failures, elevated latency, or loss of key features.

| Attribute | Benchmark |
|-----------|-----------|
| **Blast radius** | 10-50% of users affected, or a critical function degraded but not fully down |
| **Detection lag target** | <10 minutes |
| **Response time SLA** | On-call acknowledges within 10 minutes; secondary on-call looped in within 20 minutes |
| **Resolution target** | Mitigation within 2 hours; full resolution within 8 hours |
| **Communication cadence** | Status updates every 30 minutes to stakeholders during active incident |
| **Postmortem deadline** | Draft within 3 business days; final within 5 business days |
| **Examples** | Checkout succeeding at 60% rate, search returning partial results, third-party integration degraded affecting subset of users, elevated error rates on a core API |

**Escalation:** Pages primary and secondary on-call. Engineering manager notified. Status page updated if customer-facing impact exceeds 30 minutes.

---

### SEV3 — Minor

**Definition:** Limited degradation affecting a non-critical function or a small subset of users. Core business functions remain operational. The issue is noticeable but does not prevent users from completing primary workflows.

| Attribute | Benchmark |
|-----------|-----------|
| **Blast radius** | <10% of users, or a secondary feature degraded |
| **Detection lag target** | <30 minutes |
| **Response time SLA** | On-call acknowledges within 30 minutes; may be deferred to business hours |
| **Resolution target** | Mitigation within 4 hours; full resolution within 24 hours |
| **Communication cadence** | Status update at acknowledgment and resolution; no cadence required during |
| **Postmortem deadline** | Postmortem optional; lightweight incident review within 5 business days |
| **Examples** | Non-critical dashboard slow, image upload failing for one file type, email notifications delayed by 15 minutes, admin tool partially broken |

**Escalation:** Primary on-call only. No automatic leadership notification. Escalate if the issue widens or if it is not mitigated within the resolution target.

---

### SEV4 — Low

**Definition:** Cosmetic issue, minor inconvenience, or internal-only impact. No user-facing degradation of functionality. No revenue or SLA impact.

| Attribute | Benchmark |
|-----------|-----------|
| **Blast radius** | No external users affected, or impact is cosmetic only |
| **Detection lag target** | No strict target — may be found during regular monitoring review |
| **Response time SLA** | Addressed during normal business hours; no paging required |
| **Resolution target** | Within 1 week, prioritized alongside regular sprint work |
| **Communication cadence** | Logged in incident tracker; no active status updates required |
| **Postmortem deadline** | No postmortem required; note in incident log sufficient |
| **Examples** | Internal dashboard displaying incorrect timezone, staging environment flaky test, log noise from deprecated endpoint, minor UI alignment issue |

**Escalation:** None. Tracked as a standard ticket.

---

## Classification Decision Tree

Use this when you are unsure which severity to assign:

```
Is a revenue-generating or safety-critical system fully unavailable?
  YES → SEV1
  NO  ↓

Are >10% of users experiencing failures or unable to complete a primary workflow?
  YES → SEV2
  NO  ↓

Are users experiencing a noticeable degradation in a secondary feature?
  YES → SEV3
  NO  ↓

Is the impact internal-only or cosmetic?
  YES → SEV4
```

**When in doubt, round up.** It is easier to downgrade a SEV2 to a SEV3 after investigation than to upgrade a SEV3 after the damage is done. Severity can be adjusted during the incident as more information becomes available.

## Severity vs. Priority

Severity and priority are not the same:

- **Severity** describes the current impact. It is an objective assessment of blast radius and business impact.
- **Priority** describes how urgently the root cause needs to be fixed. A SEV2 incident with a simple workaround may have P2 action items. A SEV4 incident that reveals a latent SEV1 risk may have P0 action items.

Always classify severity based on the incident itself. Assign priority to action items based on the risk of recurrence and the potential severity of that recurrence.
