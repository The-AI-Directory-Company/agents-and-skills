# Contract Review: Cirrostratus Cloud Infrastructure Agreement

## 1. Contract Summary

```
Contract Type:   Cloud Infrastructure Services Agreement (IaaS + managed database)
Parties:         Lumen Health Technologies ("Customer") and Cirrostratus Inc. ("Provider")
Term:            36 months, auto-renewing for 12-month periods
Total Value:     $264,000/year ($792,000 total)
Review Date:     2026-03-14
Reviewer Role:   Customer (Lumen Health)
Data Involved:   PHI (HIPAA-regulated), PII
```

## 2. Liability and Indemnification

| Clause                  | Section | Current Language                                | Risk | Recommendation                                   |
|-------------------------|---------|--------------------------------------------------|------|--------------------------------------------------|
| Liability cap           | 11.1    | Lesser of $500K or 12 months fees               | High | Cap is below annual contract value; negotiate to 24 months fees |
| Indemnification scope   | 12.1    | Provider indemnifies for IP infringement only    | High | Add indemnification for data breaches and regulatory fines       |
| Consequential damages   | 11.3    | Mutual waiver, no carve-outs                     | Med  | Add carve-outs for confidentiality breach and data loss          |
| Gross negligence        | —       | Not addressed                                    | High | Add carve-out excluding cap for gross negligence/willful misconduct |

## 3. Intellectual Property

| Issue                        | Section | Status                         | Risk | Notes                                            |
|------------------------------|---------|--------------------------------|------|--------------------------------------------------|
| Customer data ownership      | 5.1     | Customer retains ownership     | Low  | Acceptable                                       |
| License to customer data     | 5.3     | "Use for service improvement"  | High | Overly broad — could include ML training on PHI; narrow to "service delivery only" |
| Aggregated/anonymized data   | 5.4     | Provider may use freely        | Med  | Acceptable if truly anonymized per HIPAA Safe Harbor; add explicit standard |
| Custom configuration rights  | —       | Not addressed                  | Med  | Add clause: custom configs are Customer work product |

## 4. Data Handling and Privacy

| Requirement              | Section | Adequate? | Gap                                                     |
|--------------------------|---------|-----------|----------------------------------------------------------|
| BAA (Business Associate) | Exhibit C | Yes     | BAA is attached; review subcontractor flow-down           |
| Breach notification      | 9.2     | No        | 30 business days — HIPAA requires "without unreasonable delay" (≤60 calendar days); best practice is 72 hours |
| Data residency           | 9.4     | Partial   | "Primarily US" — require explicit US-only with written consent for changes |
| Encryption at rest       | 9.5     | Yes       | AES-256; acceptable                                      |
| Encryption in transit    | 9.6     | Yes       | TLS 1.2+; acceptable                                     |
| Subprocessor notification| 9.7     | No        | No advance notice of subprocessor changes — require 30-day notice with opt-out |
| Data deletion            | 9.8     | Partial   | "Commercially reasonable efforts" post-termination — require certified deletion within 30 days |

**Critical:** Breach notification timeline (30 business days) is misaligned with HIPAA obligations. This must be reduced to 72 hours or "without unreasonable delay."

## 5. Service Levels and Remedies

| SLA Metric          | Commitment   | Remedy                         | Risk |
|---------------------|--------------|--------------------------------|------|
| Uptime (compute)    | 99.95%       | 10% credit per 0.05% shortfall | Low  |
| Uptime (database)   | 99.9%        | 5% credit per 0.1% shortfall   | Low  |
| Support response P1 | 1 hour       | None                           | High |
| RTO                 | 4 hours      | None                           | Med  |
| RPO                 | 1 hour       | None                           | Med  |

**Issues:** SLA credits are capped at 30% of monthly fees (Section 7.4) — insufficient for critical healthcare workloads. No right to terminate for persistent SLA failures. Add: 3 consecutive months below SLA triggers termination right without penalty. Support response has no remedy if missed.

## 6. Termination and Exit

| Provision                   | Terms                                | Risk | Notes                                       |
|-----------------------------|--------------------------------------|------|---------------------------------------------|
| Termination for convenience | Customer: 180-day notice + early term fee (remaining term) | Crit | Early termination fee could be $396K; negotiate to 6 months max |
| Termination for cause       | 60-day cure period                   | Med  | Acceptable, but add carve-out: data breach = immediate termination |
| Data portability            | "Standard export formats"            | High | Vague — require API access, documented schema, and migration support |
| Transition assistance       | 30 days post-termination             | Med  | Extend to 90 days for healthcare data migration complexity |
| Auto-renewal opt-out        | 90-day written notice before renewal | Med  | Acceptable; add calendar reminder            |
| Price increases on renewal  | "Market-rate adjustments"            | High | Uncapped; add cap of CPI + 3% maximum        |

## 7. Findings Summary

| #  | Finding                                    | Risk | Section  | Action Required                                    |
|----|--------------------------------------------|------|----------|----------------------------------------------------|
| 1  | Early termination fee = remaining contract | Crit | 14.2     | Cap at 6 months fees maximum                       |
| 2  | Breach notification: 30 business days      | Crit | 9.2      | Reduce to 72 hours per HIPAA alignment             |
| 3  | Broad data license ("service improvement") | High | 5.3      | Narrow to "providing the services" only            |
| 4  | No subprocessor change notification        | High | 9.7      | Add 30-day advance notice with opt-out right       |
| 5  | Liability cap below contract value         | High | 11.1     | Increase to 24 months fees paid                    |
| 6  | No IP indemnification for data breaches    | High | 12.1     | Add data breach and regulatory fine indemnification|
| 7  | Uncapped renewal price increases           | High | 14.5     | Cap at CPI + 3%                                    |
| 8  | Vague data portability language            | High | 14.3     | Require API access and documented export schema    |
| 9  | No termination right for persistent SLA miss| Med | 7.4     | Add termination trigger after 3 consecutive misses |
| 10 | Transition assistance only 30 days         | Med  | 14.4     | Extend to 90 days                                  |

**Recommendation:** Do not execute this agreement without resolving findings 1-4. Findings 1 and 2 are business-critical (financial exposure and regulatory compliance). Escalate to legal counsel for redline preparation.
