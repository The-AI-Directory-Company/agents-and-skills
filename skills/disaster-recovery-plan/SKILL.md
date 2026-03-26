---
name: disaster-recovery-plan
description: Write disaster recovery plans with RPO/RTO targets, failover procedures, communication protocols, and testing schedules — ensuring business continuity when systems fail.
metadata:
  displayName: "Disaster Recovery Plan"
  categories: ["operations", "engineering"]
  tags: ["disaster-recovery", "business-continuity", "failover", "RPO", "RTO", "resilience"]
  worksWellWithAgents: ["cloud-architect", "site-reliability-architect", "sre-engineer"]
  worksWellWithSkills: ["incident-postmortem", "runbook-writing"]
---

# Disaster Recovery Plan

## Before you start

Gather the following from the user before writing:

1. **What systems does this plan cover?** (Service names, data stores, and their business functions)
2. **What are the business-critical operations?** (Revenue-generating flows, regulatory obligations, customer-facing services)
3. **What is the acceptable data loss?** (RPO — Recovery Point Objective: can you lose 0 seconds, 5 minutes, 1 hour, or 24 hours of data?)
4. **What is the acceptable downtime?** (RTO — Recovery Time Objective: how long can the system be unavailable before business impact is severe?)
5. **What disaster scenarios must be covered?** (Region outage, database corruption, ransomware, vendor failure, physical site loss)

If the user says "write a DR plan for our app," push back: "Which failure scenario? A database corruption recovery is a different plan from a full region failover. Each scenario gets its own procedure with its own RPO/RTO targets."

## Disaster recovery plan template

### 1. Scope and objectives

State what this plan covers and what it does not. Define the specific systems, environments, and failure scenarios in scope. List any systems explicitly excluded and reference their separate DR plans if they exist.

Define recovery objectives for each system:

| System | RPO | RTO | Tier | Justification |
|---|---|---|---|---|
| Payment processing | 0 (zero data loss) | 15 minutes | Tier 1 | Revenue-critical, regulatory requirement |
| User database | 5 minutes | 30 minutes | Tier 1 | All services depend on auth |
| Analytics pipeline | 24 hours | 4 hours | Tier 2 | No revenue impact, can reprocess |
| Internal wiki | 24 hours | 48 hours | Tier 3 | Low urgency, daily backups sufficient |

Tier definitions:
- **Tier 1**: Restore first. Business stops without this system.
- **Tier 2**: Restore after Tier 1. Degraded operations are tolerable short-term.
- **Tier 3**: Restore last. No immediate business impact.

### 2. Backup strategy

For each system, document:

- **Backup method**: Continuous replication, point-in-time snapshots, file-level backups
- **Backup frequency**: Real-time, every N minutes/hours, daily
- **Retention period**: How long backups are kept and the rotation schedule
- **Storage location**: Region, provider, and whether it is geographically separate from primary
- **Encryption**: At-rest and in-transit encryption standards
- **Verification**: How and how often backup integrity is tested (not just "we assume it works")

```
User database:
  Method: Continuous WAL replication to standby + daily full snapshot
  Frequency: Real-time replication; snapshots at 02:00 UTC daily
  Retention: 30 daily snapshots, 12 weekly snapshots
  Storage: AWS S3 us-west-2 (primary in us-east-1) — cross-region
  Encryption: AES-256 at rest, TLS 1.3 in transit
  Verification: Weekly automated restore test to staging; quarterly manual validation
```

### 3. Failover procedures

Write step-by-step procedures for each disaster scenario. Each procedure must include:

- **Detection**: How the failure is identified (monitoring alert, customer report, manual check)
- **Decision authority**: Who authorizes the failover (name/role, not "management")
- **Step-by-step execution**: Numbered steps with exact commands, expected outputs, and decision branches
- **Data validation**: How to confirm data integrity after failover
- **Traffic cutover**: How traffic is redirected to the recovery environment

Use the same step format as a runbook — copy-pasteable commands, expected output, and if/then branches at every decision point. Reference runbooks for detailed per-service procedures.

### 4. Communication protocol

Define who is notified, when, and how:

| Audience | Channel | Timing | Message owner |
|---|---|---|---|
| Incident commander | PagerDuty | Immediate (automated) | Monitoring system |
| Engineering leadership | Slack #incidents | Within 5 minutes | Incident commander |
| Customer support | Email + Slack | Within 15 minutes | Comms lead |
| Affected customers | Status page + email | Within 30 minutes | Comms lead |
| Executive team | Email summary | Within 1 hour | Program owner |

Include message templates for customer-facing communications at each stage: initial acknowledgment, progress update, and resolution confirmation.

### 5. Testing schedule

A plan that has never been tested is a hypothesis, not a plan. Define:

- **Tabletop exercises**: Quarterly walk-throughs of the plan with all stakeholders
- **Component tests**: Monthly restoration of individual backups to verify recoverability
- **Full failover drills**: Semi-annual or annual end-to-end failover to the recovery environment
- **Chaos engineering**: Ongoing injection of controlled failures in production (if applicable)

Each test must produce a written report documenting: what was tested, pass/fail per step, time to complete each phase, and issues discovered with remediation owners.

### 6. Plan maintenance

- **Review cadence**: Quarterly review or after any infrastructure change
- **Change triggers**: New system added, provider changed, RTO/RPO targets updated, post-incident findings
- **Version control and ownership**: Store in version control (not a wiki that silently drifts) with a named owner responsible for keeping it current

## Quality checklist

Before delivering the plan, verify:

- [ ] RPO and RTO are defined per system with business justification, not just technical preference
- [ ] Every system has a documented backup method, frequency, storage location, and verification process
- [ ] Failover procedures are step-by-step with commands, expected outputs, and decision authority
- [ ] Communication protocol specifies audience, channel, timing, and message owner — no gaps
- [ ] Testing schedule includes at least tabletop, component, and full failover tests with defined frequency
- [ ] Tier classifications are assigned and restoration order is explicit
- [ ] The plan names specific people or roles, not "the team" or "management"
- [ ] A maintenance owner and review cadence are defined

## Common mistakes

- **Setting RPO/RTO without business input.** Engineers pick technically convenient targets. The business must define how much downtime and data loss it can tolerate, then engineering designs to meet those targets.
- **Untested backups.** "We have daily backups" means nothing if you have never restored one. Backups that cannot be restored are not backups.
- **Single-region recovery storage.** Storing backups in the same region as production means a region outage destroys both. Cross-region or cross-provider storage is mandatory.
- **No communication plan.** Technical recovery without customer communication creates a second crisis. Customers who see downtime with no explanation lose trust faster than customers who get timely updates.
- **Plan lives in a wiki nobody reads.** If the plan is not tested regularly and updated after infrastructure changes, it will be wrong when you need it most. Treat it as a living document with a named owner.
- **Skipping decision authority.** In a crisis, "who decides to fail over?" cannot be an open question. Name the role and the backup if that person is unreachable.
