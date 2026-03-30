# Regulatory Frameworks for Contract Review

Reference for evaluating data handling, privacy, and compliance clauses in contracts. Use this when reviewing Section 4 (Data Handling and Privacy) and cross-checking against regulatory obligations.

---

## GDPR Obligations in Contracts

### When GDPR Applies

GDPR applies when the contract involves processing personal data of EU/EEA residents, regardless of where the processing organization is located.

### Required Contract Provisions

| Obligation | GDPR Reference | What the Contract Must Include |
|-----------|---------------|-------------------------------|
| Data Processing Agreement | Art. 28 | A DPA is mandatory when a controller engages a processor. Must specify: subject matter, duration, nature/purpose, data types, data subject categories, controller obligations, processor obligations. |
| Lawful basis | Art. 6 | The contract should state the lawful basis for processing (e.g., contractual necessity, legitimate interest, consent). |
| Subprocessor controls | Art. 28(2), 28(4) | Processor must not engage subprocessors without prior written authorization from the controller. Must impose equivalent data protection obligations on subprocessors. |
| Breach notification | Art. 33 | Processor must notify controller **without undue delay** after becoming aware of a personal data breach. Best practice: require notification within **72 hours** to align with controller's obligation to the supervisory authority. |
| Data transfers | Art. 46 | If data transfers outside the EEA, the contract must specify the transfer mechanism: Standard Contractual Clauses (SCCs), adequacy decision, or Binding Corporate Rules. |
| Data subject rights | Art. 28(3)(e) | Processor must assist controller in responding to data subject requests (access, deletion, portability). |
| Return and deletion | Art. 28(3)(g) | At contract end, processor must delete or return all personal data and certify deletion, unless retention is required by law. |
| Audit rights | Art. 28(3)(h) | Controller must have the right to audit the processor's compliance, either directly or through a third-party auditor. |

### Red Flags

- No DPA attached to a contract involving personal data processing
- Breach notification window longer than 72 hours
- No subprocessor notification or approval mechanism
- Data transfers outside EEA with no transfer mechanism specified
- No data deletion clause at contract termination

---

## HIPAA Obligations in Contracts

### When HIPAA Applies

HIPAA applies when the contract involves creating, receiving, maintaining, or transmitting Protected Health Information (PHI) on behalf of a covered entity.

### Business Associate Agreement (BAA) Requirements

A BAA is mandatory. The contract (or a separate BAA document) must include:

| Obligation | HIPAA Reference | What the Contract Must Include |
|-----------|----------------|-------------------------------|
| Permitted uses/disclosures | 45 CFR 164.504(e)(2) | Specify exactly what the business associate can and cannot do with PHI. Broad grants are a finding. |
| Safeguards | 45 CFR 164.504(e)(2)(ii)(B) | Business associate must implement appropriate safeguards to prevent unauthorized use/disclosure. |
| Breach notification | 45 CFR 164.410 | Business associate must notify covered entity of a breach of unsecured PHI **within 60 days** of discovery. Best practice: negotiate to 30 days or less. |
| Subcontractor flow-down | 45 CFR 164.502(e)(1)(ii) | Business associate must ensure subcontractors handling PHI agree to equivalent restrictions and conditions. |
| Individual rights support | 45 CFR 164.504(e)(2)(ii)(E-F) | Business associate must make PHI available for individual access requests and support amendments. |
| Return/destruction | 45 CFR 164.504(e)(2)(ii)(I) | At termination, return or destroy all PHI. If not feasible, extend protections indefinitely. |
| Minimum necessary | 45 CFR 164.502(b) | Access to PHI must be limited to the minimum necessary to perform contracted services. |

### Red Flags

- No BAA when PHI is involved — this is a HIPAA violation, not just a gap
- Breach notification window exceeding 60 days
- No subcontractor flow-down requirements
- Broad access to PHI beyond what is needed for contracted services
- No PHI return/destruction clause at termination

---

## SOC 2 Obligations in Contracts

### When SOC 2 Matters

SOC 2 is not a regulatory requirement — it is a market expectation. Contracts should address SOC 2 when the vendor processes, stores, or transmits customer data and the customer requires assurance of the vendor's controls.

### Contract Provisions Related to SOC 2

| Obligation | What the Contract Should Address |
|-----------|--------------------------------|
| SOC 2 report delivery | Vendor must provide a current SOC 2 Type II report upon request (at least annually). Specify whether Type I is acceptable for initial engagement. |
| Complementary User Entity Controls (CUECs) | The SOC 2 report will list controls the customer must implement. The contract should reference the obligation to review and implement CUECs. |
| Scope coverage | The SOC 2 report scope must cover the specific services provided under the contract. A vendor-level SOC 2 that excludes the product you use is insufficient. |
| Gap remediation | If the SOC 2 report contains qualified opinions or noted exceptions, the vendor should have a remediation plan with timelines. |
| Right to audit | For critical vendors, retain the right to audit beyond the SOC 2 report — particularly for controls not covered in the report scope. |
| Incident notification | SOC 2 CC7 covers incident management, but the contract should separately define notification timelines. Do not rely on the SOC 2 report alone for incident response commitments. |

### Red Flags

- Vendor claims "SOC 2 compliant" but cannot produce the report
- SOC 2 report scope does not cover the contracted service
- Type I report only, with no timeline to Type II
- Report contains exceptions with no remediation plan
- No contractual commitment to deliver updated reports annually

---

## Data Residency and Cross-Border Transfers

When the contract involves international data flows, verify:

| Check | Details |
|-------|---------|
| Data storage location | Where will data be stored at rest? Specify regions or countries. |
| Processing location | Where will data be processed? This may differ from storage. |
| Transfer mechanism | For EU data leaving the EEA: SCCs, adequacy decision, or BCRs. Post-Schrems II, assess supplementary measures. |
| Government access risk | Does the jurisdiction allow government access to data without customer notification? Assess under the destination country's laws. |
| Contractual commitments | The contract should commit to specific storage/processing locations and require notice before any change. |

---

## Breach Notification Windows — Quick Reference

| Framework | Notification Deadline | Who Notifies Whom |
|-----------|-----------------------|-------------------|
| GDPR | 72 hours (controller to authority); without undue delay (processor to controller) | Processor notifies controller, controller notifies supervisory authority |
| HIPAA | 60 days (business associate to covered entity); 60 days (covered entity to individuals) | Business associate notifies covered entity, covered entity notifies individuals and HHS |
| SOC 2 | Not prescribed — contractually defined | Per contract terms |
| State breach laws (US) | Varies: 30-90 days depending on state | Entity holding data notifies affected individuals and state AG |

**Contract recommendation:** Always negotiate notification timelines shorter than the regulatory maximum. If the vendor takes the full 72 hours (GDPR) to notify you, you have zero buffer before your own 72-hour obligation begins.
