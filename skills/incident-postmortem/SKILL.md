---
name: incident-postmortem
description: Write blameless incident postmortems with structured timeline reconstruction, impact quantification, contributing factor analysis, and actionable follow-up items with owners and deadlines.
metadata:
  displayName: "Incident Postmortem"
  categories: ["operations", "engineering"]
  tags: ["incidents", "postmortem", "blameless", "reliability", "incident-response"]
  worksWellWithAgents: ["devops-engineer", "engineering-manager", "incident-commander", "release-manager", "site-reliability-architect", "sre-engineer"]
  worksWellWithSkills: ["disaster-recovery-plan", "runbook-writing", "ticket-writing"]
---

# Incident Postmortem

## Before you start

Gather the following from the user:

1. **What happened?** (Service name, symptoms, error messages, alerts that fired)
2. **When did it happen?** (Detection time, start time if known, resolution time — all in UTC)
3. **Who was involved?** (On-call responder, escalation chain, any external parties)
4. **What was the blast radius?** (Affected users, regions, services, revenue impact)
5. **What fixed it?** (Mitigation steps taken, in order)

If the user gives you a vague summary ("the site went down for a bit"), push back: "What specific errors did users see? Which services were affected? When exactly did alerts fire vs. when was the issue resolved?"

## Postmortem template

Use the following structure for every postmortem:

### Incident Summary

Write 3-5 sentences covering: what broke, who was affected, how long it lasted, and how it was resolved. This should be understandable by someone outside the team.

```
On 2024-03-12 at 14:32 UTC, the checkout service began returning 500 errors
for all payment processing requests. Approximately 12,000 users were unable to
complete purchases during the 47-minute outage. The issue was caused by an
expired TLS certificate on the payment gateway. Service was restored at 15:19
UTC by rotating the certificate.
```

### Timeline

Use UTC timestamps. Include detection lag (time between incident start and first alert). Mark each entry with a category tag.

```
14:32 UTC  [ONSET]     First 500 errors appear in payment service logs
14:38 UTC  [DETECTION] PagerDuty alert fires for checkout error rate > 5%
14:40 UTC  [RESPONSE]  On-call engineer acknowledges alert
14:45 UTC  [DIAGNOSIS] Engineer identifies TLS handshake failures in logs
14:52 UTC  [ESCALATION] Platform team paged for certificate access
15:10 UTC  [MITIGATION] New certificate issued and deployed to staging
15:15 UTC  [MITIGATION] Certificate deployed to production
15:19 UTC  [RESOLUTION] Error rates return to baseline, incident closed
```

### Impact

Quantify impact with actual numbers, not vague language:

- **Duration**: Total outage time (onset to resolution) and user-facing downtime
- **Users affected**: Count or percentage, segmented if possible
- **Revenue impact**: Lost transactions, failed payments, SLA credits issued
- **Downstream effects**: Other services or teams that were impacted
- **Detection time**: How long between onset and first alert

### Contributing Factors

List every factor that contributed to the incident occurring or lasting longer than it should have. Frame these as system failures, not personal failures.

```
- Certificate expiry was tracked in a spreadsheet with no automated alerting
- The payment service had no fallback path when TLS negotiation fails
- Runbook for certificate rotation was last updated 18 months ago and
  referenced a deprecated tool
- On-call engineer did not have permissions to rotate certificates,
  requiring escalation
```

### Root Cause

Identify the deepest systemic cause. The root cause is never "someone made a mistake" — it is the system condition that allowed the mistake to have impact.

```
Root cause: Certificate lifecycle management relied on manual tracking without
automated expiry alerts or rotation. The system had no defense against expiry
because it was treated as a one-time setup rather than an ongoing concern.
```

### Action Items

Every action item must have an owner, a deadline, and a priority. Use this format:

| Priority | Action Item | Owner | Deadline | Ticket |
|----------|-------------|-------|----------|--------|
| **P0** | Add automated certificate expiry alerting (30/14/7 day warnings) | @platform-team | 2024-03-19 | OPS-891 |
| **P1** | Implement certificate auto-rotation for payment service | @platform-team | 2024-04-01 | OPS-892 |
| **P1** | Grant on-call engineers certificate rotation permissions | @security-team | 2024-03-15 | SEC-234 |
| **P2** | Add TLS handshake failure to checkout service health check | @checkout-team | 2024-04-15 | CHK-567 |

Priority definitions: **P0** — before next on-call rotation, prevents recurrence. **P1** — within 2 weeks, reduces severity or detection time. **P2** — within 30 days, improves resilience or observability.

### Lessons Learned

Include three categories:

- **What went well**: Response actions, tools, or processes that worked as intended
- **What went poorly**: Gaps that made the incident worse or slower to resolve
- **Where we got lucky**: Things that could have made this much worse but didn't

## Quality checklist

Before delivering the postmortem, verify:

- [ ] Summary is understandable by someone outside the engineering team
- [ ] Timeline uses UTC and includes detection lag
- [ ] Impact section contains actual numbers, not "some users were affected"
- [ ] Contributing factors describe system failures, not individual mistakes
- [ ] Root cause identifies a systemic issue, not "human error"
- [ ] Every action item has an owner, deadline, priority, and ticket reference
- [ ] At least one P0 action item exists that prevents immediate recurrence
- [ ] Lessons learned include all three categories (well, poorly, lucky)

## Common mistakes to avoid

- **Blaming individuals**. "John forgot to renew the certificate" is a blame statement. "Certificate renewal depended on manual tracking with no automated alerts" is a system observation. Always describe the system gap, not the person.
- **Vague action items**. "Improve monitoring" is not actionable. "Add PagerDuty alert when certificate expiry is within 30 days (OPS-891, @platform-team, due 2024-03-19)" is actionable.
- **Missing the detection gap**. Always call out how long the incident was occurring before anyone noticed. A 2-minute outage with a 45-minute detection gap is a monitoring problem, not just an infrastructure problem.
- **Action items without owners**. An action item assigned to a team mailing list or "TBD" will not get done. Every item needs a specific person or team lead who is accountable.
- **Skipping "where we got lucky"**. This section surfaces near-misses that deserve preventive action even though they didn't cause damage this time.
