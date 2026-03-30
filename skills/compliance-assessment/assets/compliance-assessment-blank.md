# Compliance Assessment — Blank Template

Fill in each section. Delete example text in brackets before finalizing.

---

## 1. Scope Boundary

**Assessment date:** [YYYY-MM-DD]
**Assessor:** [Name / Role]
**Frameworks in scope:** [SOC 2 / GDPR / HIPAA / ISO 27001 / Other]

### In Scope

| Category | Items |
|----------|-------|
| Systems | [List every system, service, and data store] |
| Data types | [PII, PHI, financial data, credentials, logs] |
| Teams | [Engineering, DevOps, Support, HR, etc.] |
| Environments | [Production, staging, CI/CD pipelines] |
| Third parties | [Cloud providers, SaaS tools, subprocessors] |

### Out of Scope

| System / Area | Reason for Exclusion |
|---------------|---------------------|
| [Item] | [Justification — must be defensible to an auditor] |
| [Item] | [Justification] |

### Scope Validation Rules

- [ ] Every third party that processes in-scope data is listed in scope
- [ ] Staging environments with production data copies are in scope
- [ ] CI/CD pipelines deploying to production are in scope

---

## 2. Control Mapping

Map existing controls to framework requirements. Add rows as needed.

| Requirement | Framework Ref | Current Control | Status | Gap |
|-------------|--------------|-----------------|--------|-----|
| [Requirement description] | [e.g., SOC 2 CC6.1] | [What exists today] | [Compliant / Partial / Gap] | [What is missing] |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

### Control Areas Checklist

Ensure every area below has at least one row in the mapping table:

- [ ] Access Control (authentication, authorization, reviews)
- [ ] Data Protection (encryption at rest, in transit, key management, retention)
- [ ] Logging and Monitoring (audit logs, alerting, log retention)
- [ ] Incident Response (plan, notification, post-incident review)
- [ ] Change Management (approval, testing, rollback)
- [ ] Business Continuity (backup, disaster recovery, RTO/RPO)
- [ ] Vendor Management (assessment, contracts, monitoring)
- [ ] HR Security (training, onboarding, offboarding)

---

## 3. Evidence Inventory

For every control marked Compliant or Partial, document proof of operation.

| Control Name | Evidence Type | Evidence Location | Last Verified | Refresh Cadence |
|-------------|--------------|-------------------|---------------|-----------------|
| [Control] | [Policy / Config screenshot / Logs / Process record / Third-party cert] | [URL, file path, or system] | [YYYY-MM-DD] | [Quarterly / Annually / Continuous] |
| | | | | |
| | | | | |

**Reminder:** A control without evidence is a gap, regardless of what the policy says.

---

## 4. Gap Analysis

Document each gap using the format below. Assign a unique ID and risk level.

### Gap: GAP-___

| Field | Value |
|-------|-------|
| **Gap ID** | GAP-___ |
| **Control Area** | [e.g., Access Control] |
| **Requirement** | [Framework reference and requirement description] |
| **Current State** | [What exists today — or "Nothing"] |
| **Risk Level** | [Critical / High / Medium / Low] |
| **Remediation** | [Specific action to close the gap] |
| **Evidence Needed** | [What proof of operation this control must produce] |
| **Estimated Effort** | [Implementation time + ongoing maintenance time] |

### Risk Level Definitions

| Level | Meaning |
|-------|---------|
| **Critical** | Active regulatory violation or data exposure |
| **High** | Required control missing entirely |
| **Medium** | Control partially implemented |
| **Low** | Control exists but evidence is incomplete |

*(Copy the gap block above for each additional gap.)*

---

## 5. Remediation Roadmap

Assign every gap to a phase. Each item must have one owner and one deadline.

### Phase 1 — Immediate (0-30 days)

Target: Critical and High gaps.

| Gap ID | Remediation Action | Owner | Deadline | Evidence Deliverable |
|--------|-------------------|-------|----------|---------------------|
| GAP-___ | [Action] | [Name] | [Date] | [What proof looks like] |
| | | | | |

### Phase 2 — Short-term (30-90 days)

Target: Medium gaps.

| Gap ID | Remediation Action | Owner | Deadline | Evidence Deliverable |
|--------|-------------------|-------|----------|---------------------|
| GAP-___ | [Action] | [Name] | [Date] | [What proof looks like] |
| | | | | |

### Phase 3 — Long-term (90-180 days)

Target: Low gaps and documentation improvements.

| Gap ID | Remediation Action | Owner | Deadline | Evidence Deliverable |
|--------|-------------------|-------|----------|---------------------|
| GAP-___ | [Action] | [Name] | [Date] | [What proof looks like] |
| | | | | |

---

## Assessment Summary

| Metric | Count |
|--------|-------|
| Total controls assessed | |
| Compliant | |
| Partially compliant | |
| Gaps identified | |
| Critical gaps | |
| High gaps | |
| Medium gaps | |
| Low gaps | |

**Next review date:** [Date — schedule before this assessment goes stale]
