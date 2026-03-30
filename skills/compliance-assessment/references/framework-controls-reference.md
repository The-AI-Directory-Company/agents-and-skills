# Framework Controls Reference

Quick-lookup tables for the four frameworks most commonly encountered in compliance assessments. Use these tables to verify coverage during control mapping (Step 2 of the assessment template).

---

## SOC 2 — Trust Services Criteria

SOC 2 organizes controls into nine Common Criteria (CC) series under five Trust Services Categories.

| CC Series | Category | Focus Area | Key Questions |
|-----------|----------|------------|---------------|
| CC1 | Control Environment | Governance, ethics, oversight | Is there a security policy? Who owns it? Is there a code of conduct? |
| CC2 | Communication & Information | Internal/external communication | Are security responsibilities communicated? Are incidents reported? |
| CC3 | Risk Assessment | Risk identification and management | Is there a formal risk assessment? How often is it updated? |
| CC4 | Monitoring Activities | Ongoing and separate evaluations | Are controls tested regularly? Are deficiencies tracked to resolution? |
| CC5 | Control Activities | Policies and procedures | Are logical access controls in place? Is change management formalized? |
| CC6 | Logical and Physical Access | Authentication, authorization, physical | MFA, RBAC, access reviews, physical security of data centers |
| CC7 | System Operations | Monitoring, incident detection | Are systems monitored? Is there an incident response plan? |
| CC8 | Change Management | Development, testing, deployment | Are changes tested before production? Is there a rollback process? |
| CC9 | Risk Mitigation | Vendor management, business continuity | Are vendors assessed? Is there a BCP/DR plan? |

### Type I vs. Type II

- **Type I**: Controls are designed and implemented as of a specific date.
- **Type II**: Controls are designed, implemented, and operating effectively over a period (typically 3-12 months). Type II is what customers and auditors expect.

---

## GDPR — Key Articles for Compliance Assessments

| Article | Title | What It Requires | Common Gaps |
|---------|-------|------------------|-------------|
| Art. 5 | Principles of Processing | Lawfulness, fairness, transparency, purpose limitation, data minimization, accuracy, storage limitation, integrity/confidentiality, accountability | No documented lawful basis per processing activity |
| Art. 6 | Lawful Basis | At least one of: consent, contract, legal obligation, vital interests, public task, legitimate interests | Relying on consent when legitimate interest applies (or vice versa) |
| Art. 13 | Information to Data Subjects | Privacy notice at point of collection: identity, purpose, lawful basis, retention, rights, transfers | Privacy policy missing required fields or buried in terms of service |
| Art. 30 | Records of Processing | Maintain a register of all processing activities: purpose, categories, recipients, transfers, retention, security measures | No processing register, or register is incomplete/outdated |
| Art. 32 | Security of Processing | Appropriate technical and organizational measures: encryption, pseudonymization, resilience, restore ability, regular testing | No documented security measures; no regular testing of controls |
| Art. 33 | Breach Notification (Authority) | Notify supervisory authority within 72 hours of becoming aware of a personal data breach (unless unlikely to result in risk) | No breach response procedure; notification timeline undefined |
| Art. 35 | Data Protection Impact Assessment | DPIA required for high-risk processing: large-scale profiling, systematic monitoring, sensitive data at scale | No DPIA process; DPIAs not performed for qualifying activities |

### GDPR Assessment Shortcut

If the organization processes EU personal data, verify at minimum: (1) lawful basis documented per Art. 6, (2) privacy notices per Art. 13, (3) processing register per Art. 30, (4) security measures per Art. 32, (5) breach procedure per Art. 33, (6) DPIA process per Art. 35.

---

## HIPAA — Safeguard Categories

HIPAA Security Rule organizes requirements into three safeguard types. Each contains required and addressable implementation specifications.

### Administrative Safeguards (45 CFR 164.308)

| Specification | Required/Addressable | What It Requires |
|--------------|---------------------|------------------|
| Security Management Process | Required | Risk analysis, risk management, sanction policy, information system activity review |
| Assigned Security Responsibility | Required | Designate a security official |
| Workforce Security | Addressable | Authorization/supervision, workforce clearance, termination procedures |
| Information Access Management | Required + Addressable | Access authorization, access establishment/modification, isolating healthcare clearinghouse functions |
| Security Awareness Training | Addressable | Security reminders, protection from malicious software, log-in monitoring, password management |
| Security Incident Procedures | Required | Response and reporting |
| Contingency Plan | Required + Addressable | Data backup, disaster recovery, emergency mode operation, testing, criticality analysis |
| Evaluation | Required | Periodic technical and nontechnical evaluation |
| Business Associate Agreements | Required | Written contract with every entity that creates, receives, maintains, or transmits PHI |

### Physical Safeguards (45 CFR 164.310)

| Specification | Required/Addressable | What It Requires |
|--------------|---------------------|------------------|
| Facility Access Controls | Addressable | Contingency operations, facility security plan, access control/validation, maintenance records |
| Workstation Use | Required | Policies for workstation functions and physical attributes |
| Workstation Security | Required | Physical safeguards restricting access to workstations |
| Device and Media Controls | Required + Addressable | Disposal, media re-use, accountability, data backup/storage |

### Technical Safeguards (45 CFR 164.312)

| Specification | Required/Addressable | What It Requires |
|--------------|---------------------|------------------|
| Access Control | Required + Addressable | Unique user identification, emergency access, automatic logoff, encryption/decryption |
| Audit Controls | Required | Hardware, software, and procedural mechanisms to record and examine access |
| Integrity | Addressable | Mechanisms to authenticate ePHI, protect from improper alteration/destruction |
| Person/Entity Authentication | Required | Verify identity of persons/entities seeking access |
| Transmission Security | Addressable | Integrity controls, encryption for ePHI in transit |

### HIPAA "Addressable" Does Not Mean Optional

"Addressable" means the organization must assess whether the specification is reasonable and appropriate. If it is, implement it. If not, document why and implement an equivalent alternative. Ignoring addressable specifications is a finding.

---

## ISO 27001:2022 — Annex A Control Categories

ISO 27001 Annex A contains 93 controls organized into four themes.

| Theme | Control Count | Scope |
|-------|--------------|-------|
| Organizational (A.5) | 37 | Policies, roles, asset management, access control, supplier relationships, incident management, business continuity, compliance |
| People (A.6) | 8 | Screening, terms of employment, awareness/training, disciplinary, termination, remote working, event reporting |
| Physical (A.7) | 14 | Perimeters, entry controls, securing areas, equipment protection, clear desk, off-site security, secure disposal, cabling |
| Technological (A.8) | 34 | User endpoints, privileged access, access restriction, source code, authentication, capacity, malware, vulnerabilities, logging, network security, web filtering, cryptography, SDLC, testing, change management, data masking, data leakage prevention, monitoring |

### Statement of Applicability (SoA)

The SoA is a mandatory document that lists every Annex A control with a justification for inclusion or exclusion. Controls can only be excluded if the associated risk does not exist in the organization's scope. "We have not implemented it yet" is not a valid exclusion reason.

### ISO 27001 Certification Path

1. Implement the ISMS (management system clauses 4-10)
2. Complete risk assessment and risk treatment plan
3. Produce Statement of Applicability
4. Operate controls for a sufficient period
5. Conduct internal audit and management review
6. Stage 1 audit (documentation review) by accredited certification body
7. Stage 2 audit (implementation and effectiveness) by accredited certification body
8. Surveillance audits annually; recertification every 3 years
