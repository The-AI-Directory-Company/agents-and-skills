---
name: threat-model-writing
description: Create STRIDE-based threat models with asset identification, threat actor enumeration, attack surface mapping, risk scoring, and a prioritized mitigation matrix — producing a living security document.
metadata:
  displayName: "Threat Model Writing"
  categories: ["security", "engineering"]
  tags: ["threat-modeling", "STRIDE", "security", "risk-assessment", "attack-surface"]
  worksWellWithAgents: ["cloud-architect", "compliance-officer", "security-auditor", "security-engineer", "software-architect"]
  worksWellWithSkills: ["compliance-assessment", "prd-writing", "system-design-document"]
---

# Threat Model Writing

## Before you start

Gather the following information. If any is missing, ask the user before proceeding:

1. **System description** — What does the system do? Architecture type (monolith, microservices, serverless)?
2. **Data sensitivity** — PII, financial, health, credentials, intellectual property?
3. **Trust boundaries** — Where does trusted meet untrusted? Browser-to-API, service-to-database, internal-to-third-party?
4. **Deployment environment** — Cloud provider, on-prem, hybrid? Network boundaries?
5. **Compliance requirements** — SOC 2, HIPAA, PCI-DSS, GDPR, or none?
6. **Existing security controls** — Authentication, authorization, encryption, and monitoring already in place?

If the user provides only a feature name ("we built a payments API"), push back and ask for architecture details, data flows, and trust boundaries.

## Threat model template

Every section is required unless explicitly marked optional.

### Title

`[System Name] — STRIDE Threat Model`

### 1. System Overview (3-5 sentences)

Describe purpose, architecture, and key data flows. List major components and how they communicate:

```
User Browser → (HTTPS) → API Gateway → (gRPC) → Auth Service → (TLS) → Database
                                      → (gRPC) → Payment Service → (TLS) → Stripe API
```

### 2. Assets

Enumerate what an attacker would target. For each asset, state CIA requirements:

| Asset | Confidentiality | Integrity | Availability | Notes |
|-------|----------------|-----------|--------------|-------|
| User credentials | Critical | Critical | High | Hashed with bcrypt, salted |
| Payment tokens | Critical | Critical | High | Tokenized via Stripe, never stored raw |

### 3. Threat Actors

Identify who might attack the system and their capabilities. Tailor to the system — a B2B internal tool has different actors than a public consumer API.

- **External unauthenticated** — Script kiddies, automated scanners. Low skill, high volume.
- **External authenticated** — Malicious users with valid accounts. Medium skill, targeted.
- **Insider** — Employees or contractors with system access. High skill, privileged.
- **Supply chain** — Compromised dependencies or third-party services.

### 4. Attack Surface

Map every entry point: network endpoints, authentication flows, data inputs (uploads, forms, query params, webhooks), administrative interfaces (admin panels, CI/CD pipelines), and third-party integrations.

### 5. STRIDE Threat Matrix

For each STRIDE category, list threats with concrete attack scenarios. Use one table per category with columns: ID, Threat, Attack scenario, Affected component. Prefix IDs by category (S-, T-, R-, I-, D-, E-).

| ID | Category | Threat | Attack scenario | Component |
|----|----------|--------|-----------------|-----------|
| S-1 | Spoofing | Session hijacking | Attacker steals session cookie via XSS on profile page | Auth Service |
| T-1 | Tampering | Price manipulation | Attacker modifies cart total in client-side request | Payment Service |
| R-1 | Repudiation | Unsigned admin actions | Admin deletes data with no audit log entry | Admin Panel |
| I-1 | Info Disclosure | Verbose errors | Stack traces leak DB schema to unauthenticated users | API Gateway |
| D-1 | Denial of Service | Unthrottled endpoint | 10k req/sec to /search exhausts DB connections | API Gateway |
| E-1 | Elevation of Privilege | IDOR | User accesses other users' data by changing ID in URL | API Gateway |

Every threat must describe a specific attack, not a generic category. "SQL injection" is not a threat; "Attacker injects SQL via the unsanitized `search` param in `/api/products`" is.

### 6. Risk Scoring

Score each threat: Likelihood (1-5) x Impact (1-5) = Risk Score.

| Threat ID | Likelihood | Impact | Risk Score | Priority |
|-----------|-----------|--------|------------|----------|
| E-1 | 4 | 5 | 20 | Critical |
| T-1 | 4 | 4 | 16 | Critical |
| S-1 | 3 | 5 | 15 | Critical |
| I-1 | 3 | 3 | 9 | High |

Priority bands: Critical (15-25), High (8-14), Medium (4-7), Low (1-3).

### 7. Mitigations

For each threat at High or above, specify a concrete mitigation with a named control and current status.

| Threat ID | Mitigation | Control type | Status |
|-----------|-----------|--------------|--------|
| E-1 | Enforce server-side ownership checks on every data access query | Preventive | Not started |
| T-1 | Validate and sign cart totals server-side; reject tampered payloads | Preventive | Not started |
| S-1 | Set CSP headers; sanitize all user-generated content | Preventive | Partial |

Status values: Not started, In progress, Partial, Complete.

### 8. Residual Risk (optional)

After mitigations, list risks that remain accepted. Document why (cost, low likelihood, compensating controls), who approved acceptance, and when it will be re-evaluated.

---

## Quality checklist

Before delivering a threat model, verify:

- [ ] Every asset has CIA ratings, not just a name
- [ ] Threat actors are tailored to this system, not a generic list
- [ ] Every STRIDE threat has a concrete attack scenario
- [ ] Risk scores use both likelihood and impact, not gut feeling
- [ ] Mitigations name specific controls ("add CSP headers"), not vague guidance ("improve security")
- [ ] All Critical and High threats have mitigations with a clear status
- [ ] Trust boundaries and data flows are explicitly documented

## Common mistakes to avoid

- **Generic threats without scenarios**. "SQL injection" is a category. "Attacker injects SQL via the unsanitized `search` param in `/api/products`" is a threat.
- **Ignoring insider threats**. Most models only consider external attackers. Always model what a malicious or compromised insider could do.
- **Mitigations without status tracking**. "Encrypt data" with no owner or status is a wish, not a control.
- **Scoring all threats as Critical**. If everything is critical, nothing is. Use the full scoring range.
- **Treating the model as a one-time artifact**. Note the review cadence (quarterly, per-release) and who owns updates.
