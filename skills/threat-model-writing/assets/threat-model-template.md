# Threat Model Template

Copy this template and fill in for your system or feature.

## [System Name] -- STRIDE Threat Model

| Field | Value |
|-------|-------|
| Author | |
| Date | |
| Status | Draft / In Review / Approved |
| Review Cadence | (quarterly / per-release / on architecture change) |
| Next Review | |

---

## 1. System Overview

<!-- 3-5 sentences: purpose, architecture type, key data flows. Include a data flow diagram. -->

```
[Client] --> (protocol) --> [Component A] --> (protocol) --> [Component B] --> (protocol) --> [Data Store]
                                           --> (protocol) --> [External Service]
```

---

## 2. Assets

| Asset | Confidentiality | Integrity | Availability | Notes |
|-------|----------------|-----------|--------------|-------|
| | | | | |
| | | | | |
| | | | | |

**CIA ratings:** Critical / High / Medium / Low

---

## 3. Threat Actors

<!-- Tailor to your system. Remove actors that do not apply; add specific ones if relevant. -->

| Actor | Skill Level | Motivation | Access Level |
|-------|------------|------------|-------------|
| External unauthenticated | | | |
| External authenticated | | | |
| Insider (employee/contractor) | | | |
| Supply chain (compromised dependency) | | | |
| | | | |

---

## 4. Attack Surface

### Network Endpoints

| Endpoint | Protocol | Authentication | Notes |
|----------|----------|---------------|-------|
| | | | |
| | | | |

### Data Inputs

| Input | Source | Validation | Notes |
|-------|--------|-----------|-------|
| | | | |
| | | | |

### Administrative Interfaces

| Interface | Access Control | Notes |
|-----------|---------------|-------|
| | | |

### Third-Party Integrations

| Integration | Data Exchanged | Trust Level | Notes |
|-------------|---------------|-------------|-------|
| | | | |

---

## 5. STRIDE Threat Matrix

### Spoofing

| ID | Threat | Attack Scenario | Affected Component |
|----|--------|-----------------|-------------------|
| S-1 | | | |
| S-2 | | | |

### Tampering

| ID | Threat | Attack Scenario | Affected Component |
|----|--------|-----------------|-------------------|
| T-1 | | | |
| T-2 | | | |

### Repudiation

| ID | Threat | Attack Scenario | Affected Component |
|----|--------|-----------------|-------------------|
| R-1 | | | |
| R-2 | | | |

### Information Disclosure

| ID | Threat | Attack Scenario | Affected Component |
|----|--------|-----------------|-------------------|
| I-1 | | | |
| I-2 | | | |

### Denial of Service

| ID | Threat | Attack Scenario | Affected Component |
|----|--------|-----------------|-------------------|
| D-1 | | | |
| D-2 | | | |

### Elevation of Privilege

| ID | Threat | Attack Scenario | Affected Component |
|----|--------|-----------------|-------------------|
| E-1 | | | |
| E-2 | | | |

---

## 6. Risk Scoring

| Threat ID | Likelihood (1-5) | Impact (1-5) | Risk Score | Priority |
|-----------|------------------|-------------|------------|----------|
| | | | | |
| | | | | |
| | | | | |

**Priority bands:** Critical (15-25), High (8-14), Medium (4-7), Low (1-3)

---

## 7. Mitigations

<!-- Required for all Critical and High threats. -->

| Threat ID | Mitigation | Control Type | Owner | Status |
|-----------|-----------|--------------|-------|--------|
| | | Preventive / Detective / Corrective | | Not started / In progress / Partial / Complete |
| | | | | |
| | | | | |

---

## 8. Residual Risk (optional)

<!-- Risks accepted after mitigations. Document why, who approved, and when to re-evaluate. -->

| Threat ID | Residual Risk Description | Reason for Acceptance | Approved By | Re-evaluate Date |
|-----------|--------------------------|----------------------|-------------|-----------------|
| | | | | |

---

## Notes

<!-- Additional context, assumptions, compliance requirements, or open questions. -->
