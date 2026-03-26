---
name: compliance-assessment
description: Conduct regulatory compliance assessments — mapping controls to frameworks (SOC 2, GDPR, HIPAA, ISO 27001), identifying gaps, and producing remediation roadmaps with evidence requirements.
metadata:
  displayName: "Compliance Assessment"
  categories: ["security", "business"]
  tags: ["compliance", "SOC2", "GDPR", "HIPAA", "ISO-27001", "audit"]
  worksWellWithAgents: ["compliance-officer", "contract-reviewer", "security-auditor", "solutions-architect"]
  worksWellWithSkills: ["contract-review-checklist", "employee-handbook-section", "threat-model-writing"]
---

# Compliance Assessment

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **Which frameworks apply?** — SOC 2, GDPR, HIPAA, ISO 27001, PCI DSS, or others
2. **What is the scope?** — Which systems, services, data types, and teams are in scope
3. **What is the driver?** — Customer requirement, regulatory obligation, funding milestone, or internal initiative
4. **What is the timeline?** — Audit date, certification deadline, or customer commitment
5. **What exists today?** — Current policies, controls, prior audit reports, known gaps
6. **Who are the stakeholders?** — Engineering, legal, security, executive sponsor

## Assessment template

### 1. Define Scope Boundary

Document exactly what is in and out of scope:

```
In Scope:
- Systems: [List every system, service, and data store]
- Data types: [PII, PHI, financial data, credentials, logs]
- Teams: [Engineering, DevOps, support, HR]
- Environments: [Production, staging, CI/CD pipelines]
- Third parties: [Cloud providers, SaaS tools, subprocessors]

Out of Scope:
- [System/area]: [Reason]
```

Rules: if a third-party processes in-scope data, they are in scope. If staging has production data copies, staging is in scope. CI/CD pipelines deploying to production are in scope.

### 2. Map Controls to Framework Requirements

For each framework, map existing controls to requirements per control area:

| Requirement | Framework Ref | Current Control | Status | Gap |
|-------------|--------------|-----------------|--------|-----|
| Unique user IDs | SOC 2 CC6.1, ISO A.9.2.1 | SSO via Okta | Compliant | None |
| MFA for privileged access | SOC 2 CC6.1, ISO A.9.4.2 | MFA for admin roles | Compliant | None |
| Access reviews | SOC 2 CC6.2, ISO A.9.2.5 | None | Gap | Quarterly review needed |

Cover at minimum: Access Control, Data Protection (encryption, key management, retention), Logging and Monitoring, Incident Response, Change Management, Business Continuity, Vendor Management, HR Security (training, onboarding/offboarding).

### 3. Evidence Inventory

For every "Compliant" or "Partial" control, document: the control name, evidence type (policy document, configuration screenshot, logs/reports, process records, or third-party certification), evidence location, last verified date, and refresh cadence.

If evidence does not exist for a control marked "Compliant," it is not compliant. Undocumented controls fail audits.

### 4. Gap Analysis

For each gap, document using this format:

```
Gap ID:         GAP-001
Control Area:   Access Control
Requirement:    Quarterly access reviews (SOC 2 CC6.2)
Current State:  No regular access reviews performed
Risk Level:     High
Remediation:    Implement quarterly review with automated user listing
Evidence Needed: Review records, revocation tickets
Estimated Effort: 2 weeks to implement, 4 hours/quarter ongoing
```

Risk levels: **Critical** (regulatory violation, active exposure), **High** (control missing entirely), **Medium** (partially implemented), **Low** (exists but evidence incomplete).

### 5. Remediation Roadmap

Prioritize gaps into phases. Each item must have a single owner, deadline, and evidence deliverable:

- **Phase 1 (0-30 days)**: Critical and High gaps
- **Phase 2 (30-90 days)**: Medium gaps
- **Phase 3 (90-180 days)**: Low gaps and documentation

### 6. Framework-Specific Considerations

**SOC 2**: Type II requires a period of observation (3-12 months). Controls implemented one week before the audit window provide insufficient evidence.

**GDPR**: Requires data processing records (Article 30), DPIAs for high-risk processing (Article 35), and documented lawful basis for each processing activity.

**HIPAA**: Requires formal risk analysis, Business Associate Agreements with all PHI vendors, and minimum necessary access. Breach notification within 60 days.

**ISO 27001**: Requires a formal ISMS with Statement of Applicability, risk treatment plan, and management review. Certification requires accredited external audit.

## Quality checklist

Before delivering a compliance assessment, verify:

- [ ] Scope boundary is documented with explicit in/out decisions
- [ ] Every control area has been assessed against each applicable framework
- [ ] Each compliant control has evidence with location and verification date
- [ ] Gaps include risk level, remediation steps, and evidence requirements
- [ ] Remediation roadmap is phased with owners, deadlines, and deliverables
- [ ] Framework-specific requirements (observation periods, mandatory documents) are addressed
- [ ] Third-party/vendor controls are assessed, not assumed compliant

## Common mistakes

- **Treating compliance as point-in-time.** Controls must remain effective after the audit. Build ongoing processes, not one-time fixes.
- **Assuming vendor compliance covers you.** Your cloud provider's SOC 2 does not make you SOC 2 compliant. You own your configuration.
- **Documenting controls that do not exist.** Auditors verify operation, not just policy documents. A policy without an implemented process is a finding.
- **Ignoring evidence requirements.** A control without evidence is a gap. Every control must produce verifiable proof of operation.
- **Scoping too narrowly.** Excluding systems that process in-scope data creates unassessed risk. Auditors will question exclusions.
- **No single owner for remediation.** "The team will handle it" means no one will. Every gap needs one person accountable by a specific date.
