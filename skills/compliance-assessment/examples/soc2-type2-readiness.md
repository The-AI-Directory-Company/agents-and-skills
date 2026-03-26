# SOC 2 Type II Readiness Assessment: Vantage Analytics Platform

- **Assessment date**: 2025-09-15
- **Framework**: SOC 2 Type II (Trust Services Criteria — Security, Availability, Confidentiality)
- **Scope**: Vantage Analytics SaaS platform, AWS production environment, CI/CD pipeline
- **Audit window target**: March 1 – August 31, 2026 (6-month observation period)
- **Driver**: Enterprise customer requirement (Meridian Financial, $840K ARR deal blocked pending SOC 2 report)
- **Stakeholders**: @elena (CISO), @raj (Engineering VP), @nina (Legal), @tom (CEO — exec sponsor)

---

## Scope Boundary

**In Scope:**
- Systems: Vantage API (ECS), PostgreSQL (RDS), Redis (ElastiCache), S3 data lake, CloudFront CDN
- Data types: Customer PII (names, emails), analytics data, API credentials, audit logs
- Teams: Engineering (12), DevOps (3), Support (4), HR (2)
- Environments: Production, staging, CI/CD (GitHub Actions)
- Third parties: AWS, Datadog, PagerDuty, GitHub, Slack, Google Workspace, Stripe

**Out of Scope:**
- Marketing website (static site, no customer data)
- Internal Notion workspace (no customer data after policy enforcement)
- Development local environments (no production data access)

---

## Control Mapping

| Requirement | SOC 2 Ref | Current Control | Status | Gap |
|-------------|-----------|-----------------|--------|-----|
| Unique user identification | CC6.1 | Google Workspace SSO via SAML | Compliant | None |
| MFA for all access | CC6.1 | Google Workspace enforces MFA | Compliant | None |
| Quarterly access reviews | CC6.2 | None | Gap | No review process |
| Terminated user deprovisioning | CC6.3 | Manual, ad-hoc | Partial | No SLA, no audit trail |
| Encryption at rest | CC6.7 | RDS/S3 AES-256 encryption enabled | Compliant | None |
| Encryption in transit | CC6.7 | TLS 1.2+ enforced on all endpoints | Compliant | None |
| Audit logging | CC7.2 | Application logs in Datadog (30-day retention) | Partial | Retention too short; no tamper protection |
| Intrusion detection | CC7.2 | AWS GuardDuty enabled | Compliant | None |
| Incident response plan | CC7.3 | Informal PagerDuty escalation | Partial | No documented plan or post-incident process |
| Change management | CC8.1 | PR reviews required; no deploy approval | Partial | No segregation of duties for deploys |
| System monitoring | CC7.2 | Datadog APM + alerts | Compliant | None |
| Backup and recovery | A1.2 | Nightly RDS snapshots, 7-day retention | Partial | No tested restore procedure |
| Vendor risk management | CC9.2 | None | Gap | No vendor inventory or assessments |
| Security awareness training | CC1.4 | None | Gap | No training program |
| Data retention policy | C1.2 | None | Gap | No documented retention schedule |

---

## Gap Analysis

```
Gap ID:         GAP-001
Control Area:   Access Control
Requirement:    Quarterly access reviews (CC6.2)
Current State:  No periodic review of user access; stale accounts discovered ad-hoc
Risk Level:     High
Remediation:    Implement quarterly access review using Google Workspace admin reports
Evidence Needed: Review completion records, revocation tickets, manager sign-offs
Estimated Effort: 2 weeks to implement tooling, 4 hours/quarter ongoing
```

```
Gap ID:         GAP-002
Control Area:   Access Control
Requirement:    Timely offboarding with audit trail (CC6.3)
Current State:  Manual Slack-based offboarding, no SLA, no evidence
Risk Level:     High
Remediation:    Create offboarding checklist; deprovision within 24 hours; log to ticketing system
Evidence Needed: Offboarding tickets with timestamps, access removal confirmations
Estimated Effort: 1 week to document process, ongoing per departure
```

```
Gap ID:         GAP-003
Control Area:   Logging and Monitoring
Requirement:    Tamper-proof audit logs with 1-year retention (CC7.2)
Current State:  Datadog logs at 30-day retention, mutable
Risk Level:     High
Remediation:    Ship audit logs to S3 with Object Lock (WORM); extend retention to 13 months
Evidence Needed: S3 bucket policy, Object Lock configuration, log completeness checks
Estimated Effort: 3 weeks
```

```
Gap ID:         GAP-004
Control Area:   Incident Response
Requirement:    Documented incident response plan (CC7.3)
Current State:  PagerDuty routing exists but no written plan, roles, or post-incident process
Risk Level:     Medium
Remediation:    Write IR plan covering detection, triage, escalation, communication, post-incident review
Evidence Needed: IR plan document, incident records, postmortem reports
Estimated Effort: 2 weeks to draft and approve
```

```
Gap ID:         GAP-005
Control Area:   Change Management
Requirement:    Segregation of duties for production deploys (CC8.1)
Current State:  Any engineer with repo access can merge and deploy
Risk Level:     Medium
Remediation:    Require PR approval from non-author; restrict deploy pipeline to lead/devops approval
Evidence Needed: Branch protection rules, deploy approval logs
Estimated Effort: 1 week
```

```
Gap ID:         GAP-006
Control Area:   Vendor Management
Requirement:    Vendor risk assessments (CC9.2)
Current State:  No vendor inventory; no review of subprocessor security posture
Risk Level:     High
Remediation:    Build vendor inventory; collect SOC 2 reports from critical vendors; review annually
Evidence Needed: Vendor register, SOC 2 reports or security questionnaires, review records
Estimated Effort: 4 weeks for initial inventory and collection
```

```
Gap ID:         GAP-007
Control Area:   HR Security
Requirement:    Security awareness training (CC1.4)
Current State:  No training program exists
Risk Level:     Medium
Remediation:    Implement annual security training with phishing simulation; track completion
Evidence Needed: Training completion records, quiz scores, phishing simulation results
Estimated Effort: 2 weeks to select vendor and deploy; annual renewal
```

```
Gap ID:         GAP-008
Control Area:   Data Protection
Requirement:    Data retention and disposal policy (C1.2)
Current State:  No documented retention schedule; customer data retained indefinitely
Risk Level:     Medium
Remediation:    Define retention periods per data type; implement automated deletion for expired data
Evidence Needed: Retention policy document, deletion job logs, audit of data stores
Estimated Effort: 3 weeks
```

---

## Remediation Roadmap

### Phase 1: Critical and High Gaps (0-30 days) — Deadline: October 15, 2025

| Gap | Action | Owner | Deliverable |
|-----|--------|-------|-------------|
| GAP-001 | Implement quarterly access review process | @raj | First review completed with records |
| GAP-002 | Create offboarding SLA and checklist | @nina | Offboarding policy + 2 completed examples |
| GAP-003 | Ship audit logs to S3 with Object Lock | @devops-lead | S3 bucket with WORM, log pipeline verified |
| GAP-006 | Build vendor inventory and collect SOC 2 reports | @elena | Vendor register with risk tiers |

### Phase 2: Medium Gaps (30-90 days) — Deadline: December 15, 2025

| Gap | Action | Owner | Deliverable |
|-----|--------|-------|-------------|
| GAP-004 | Write and approve incident response plan | @elena | IR plan document, tabletop exercise completed |
| GAP-005 | Enforce deploy approval gates | @devops-lead | Branch protection + deploy pipeline configs |
| GAP-007 | Launch security awareness training | @nina | Training vendor selected, first session completed |
| GAP-008 | Define data retention policy and automate deletion | @raj | Policy document, deletion job in production |

### Phase 3: Evidence Accumulation (December 2025 – February 2026)

All controls must be operational by December 2025 to accumulate 3+ months of evidence before the March 2026 audit window opens. During this phase: run the first two quarterly access reviews, collect incident response records, gather deploy approval logs, and verify log retention integrity.

### Audit Window: March 1 – August 31, 2026

Controls must remain consistently operational throughout. Any control failure during the observation period will appear as an exception in the Type II report.
