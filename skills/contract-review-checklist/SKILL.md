---
name: contract-review-checklist
description: Systematic contract review checklist — evaluating liability, IP ownership, data handling, termination clauses, SLAs, and compliance requirements with risk-rated findings and suggested protective language.
metadata:
  displayName: "Contract Review Checklist"
  categories: ["business", "security"]
  tags: ["contracts", "legal", "review", "risk", "compliance", "checklist"]
  worksWellWithAgents: ["compliance-officer", "contract-reviewer", "solutions-architect"]
  worksWellWithSkills: ["compliance-assessment"]
---

# Contract Review Checklist

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What type of contract?** (SaaS agreement, vendor contract, partnership, NDA, MSA)
2. **Which party are you?** (Customer, vendor, partner — your review posture changes)
3. **What is the contract value?** (Determines acceptable risk tolerance)
4. **What data is involved?** (PII, PHI, financial data, trade secrets, none)
5. **What regulatory frameworks apply?** (GDPR, HIPAA, SOC 2, industry-specific)
6. **Are there existing terms to compare against?** (Prior version, your standard template)

This skill produces a structured review with risk-rated findings. It is not legal advice. Flag findings rated High or Critical for legal counsel review.

## Review template

### 1. Contract Summary

```
Contract Type:   [SaaS Subscription Agreement]
Parties:         [Your Company] ("Customer") and [Vendor] ("Provider")
Term:            [Initial term + renewal terms]
Total Value:     [Annual or total contract value]
Review Date:     [Date]
```

### 2. Liability and Indemnification

| Clause                | Section | Current Language             | Risk | Recommendation                  |
|-----------------------|---------|------------------------------|------|---------------------------------|
| Liability cap         | 7.1     | 12 months of fees paid       | Low  | Acceptable — standard for SaaS  |
| Indemnification scope | 8.1     | Vendor indemnifies IP only   | High | Add data breach indemnification |
| Consequential damages | 7.3     | Mutual waiver                | Low  | Standard — acceptable           |

Red flags: liability cap below contract value, one-sided indemnification, no carve-outs for gross negligence or willful misconduct.

### 3. Intellectual Property

| Issue                   | Section | Status        | Risk | Notes                           |
|-------------------------|---------|---------------|------|---------------------------------|
| IP ownership of outputs | 4.1     | Customer owns | Low  | Verify includes derivatives     |
| License to customer data| 4.3     | Broad license | High | Narrow to service delivery only |
| Work product rights     | 4.4     | Not addressed | Crit | Must add assignment clause      |

Key questions: Who owns work product? Does the vendor retain rights to use your data for training or benchmarking? Are license grants surviving termination?

### 4. Data Handling and Privacy

| Requirement           | Section | Adequate? | Gap                                |
|-----------------------|---------|-----------|-------------------------------------|
| Data processing terms | 9.1     | Partial   | Missing subprocessor notification   |
| Breach notification   | 9.3     | No        | Timeline is 30 days — require 72 hrs|
| Data return/deletion  | 9.4     | Yes       | 30-day post-termination window      |
| Encryption standards  | 9.5     | N/A       | Add at-rest and in-transit minimums |

If the contract involves PII or regulated data and lacks a Data Processing Agreement, flag as Critical.

### 5. Service Levels and Remedies

| SLA Metric    | Commitment  | Remedy             | Risk |
|---------------|-------------|---------------------|------|
| Uptime        | 99.9%       | 5% credit per 0.1% | Low  |
| Response time | Not defined | None                | High |
| RTO/RPO       | Not defined | None                | Crit |

Verify: Are credits the sole remedy, or can you terminate for persistent SLA failures? Does the vendor self-report uptime?

### 6. Termination and Exit

| Provision                  | Terms                | Risk | Notes                         |
|----------------------------|----------------------|------|-------------------------------|
| Termination for convenience| Not permitted        | High | Add with 90-day notice        |
| Data portability           | CSV export available | Med  | Require API access + format   |
| Transition assistance      | Not addressed        | High | Add 90-day transition period  |

If you cannot exit the contract within a reasonable timeframe with your data intact, the contract creates vendor lock-in.

### 7. Findings Summary

Compile all findings prioritized by risk:

| # | Finding                        | Risk | Section | Action Required                 |
|---|--------------------------------|------|---------|---------------------------------|
| 1 | No work product IP assignment  | Crit | 4.4     | Add IP assignment clause        |
| 2 | No RTO/RPO commitments         | Crit | 6.3     | Define recovery objectives      |
| 3 | Broad license to customer data | High | 4.3     | Narrow to service delivery      |

## Quality checklist

Before delivering a contract review, verify:

- [ ] Every finding cites a specific section number or notes the clause is missing
- [ ] Risk ratings are consistent — Critical means business-threatening, not inconvenient
- [ ] IP ownership is reviewed for both pre-existing IP and work product
- [ ] Data handling covers processing terms, breach notification, and post-termination deletion
- [ ] SLAs have measurable commitments with defined remedies
- [ ] Termination provisions include data portability and transition assistance
- [ ] Findings summary is prioritized with specific recommended actions

## Common mistakes

- **Reviewing only what is written.** Missing clauses are findings. No SLA, no data deletion — these omissions are risks.
- **Treating all risks as equal.** A missing comma is not the same risk as unlimited liability. Rate findings consistently.
- **Ignoring the "other party" position.** If you are the vendor, customer-favorable terms are your risk. Adjust review posture to your role.
- **Skipping auto-renewal terms.** Contracts that silently renew with uncapped price increases are expensive surprises.
- **Reviewing without context.** A $5K SaaS tool and a $2M infrastructure contract require different risk tolerances.
- **Not flagging missing DPAs.** If personal data is processed without a Data Processing Agreement, this is a regulatory gap.
