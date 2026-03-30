---
name: system-design-document
description: Write comprehensive system design documents with architecture diagrams, component breakdowns, API contracts, failure mode analysis, and Architecture Decision Records (ADRs).
metadata:
  displayName: "System Design Document"
  categories: ["engineering"]
  tags: ["architecture", "system-design", "documentation", "ADR", "technical-specs"]
  worksWellWithAgents: ["ai-engineer", "cloud-architect", "cto-advisor", "database-architect", "enterprise-architect"]
  worksWellWithSkills: ["api-design-guide", "architecture-decision-record", "prd-writing", "technical-spec-writing", "threat-model-writing"]
---

# System Design Document

## Before you start

Gather the following information. If any is missing, ask the user before proceeding:

1. **Problem context** — What system or feature is being designed? Link to the PRD if one exists.
2. **Non-functional requirements** — Expected load, latency targets, uptime SLA, data retention, compliance needs.
3. **Constraints** — Existing tech stack, team expertise, budget, timeline, vendor commitments.
4. **Stakeholders** — Who reviews this? (e.g., staff engineer, SRE lead, security team)
5. **Scope boundary** — Is this a new system, a major refactor, or an extension of an existing service?

If the user only gives you a vague ask ("design a notification system"), push back: ask about scale (how many notifications/day?), delivery guarantees (at-least-once? exactly-once?), and latency requirements.

## System design template

Use the following template. Every section is required unless explicitly marked optional.

---

### Title

`[System Name] — System Design Document`

### 1. Context & Motivation (3-5 sentences)

Why does this system need to exist? Reference the PRD or business driver. State what currently exists (if anything) and why it is insufficient.

### 2. Goals & Non-Goals

**Goals** — 3-5 specific outcomes this design achieves. Each must be verifiable.

**Non-goals** — Things this design explicitly does NOT address. This prevents scope creep during review.

### 3. Non-Functional Requirements

| Requirement | Target | Rationale |
|-------------|--------|-----------|
| Availability | 99.9% (8.7h downtime/year) | Customer SLA |
| P99 latency | < 200ms | User-facing endpoint |
| Throughput | 5,000 req/s peak | Black Friday projection |
| Data retention | 90 days hot, 2 years cold | Compliance requirement |

### 4. Architecture Overview

Provide a high-level diagram (Mermaid or ASCII). Show major components, data flow direction, and external dependencies. Label sync vs. async communication. Every box must appear in Section 5.

### 5. Component Design

For each component: **Responsibility** (one sentence — if you need "and", split it), **Interface** (API, queue consumer, cron), **Dependencies**, and **Scaling strategy**.

### 6. Data Model

Define key entities, relationships, and storage choices. Include schema or ER diagram, database choice with justification, indexing strategy for hot paths, and partitioning approach if applicable.

### 7. API Contracts

For each external or cross-service API: method and path, request/response schema (JSON or TypeScript types), error codes, rate limits, and auth method.

### 8. Failure Modes & Mitigation

List at least 3 failure scenarios. For each:

| Failure | Impact | Detection | Mitigation |
|---------|--------|-----------|------------|
| Database primary goes down | Writes fail for ~30s | Health check alert | Automatic failover to replica |
| Upstream API returns 5xx | Degraded results | Error rate monitor | Circuit breaker + cached fallback |
| Message queue backlog | Delayed processing | Queue depth alarm | Auto-scale consumers |

### 9. Security Considerations

Address: authentication & authorization model, encryption (at rest and in transit), sensitive data handling (PII, secrets, audit logging), and attack surface (rate limiting, input validation, injection prevention).

### 10. Migration & Rollout Plan (optional)

If replacing an existing system: migration strategy (big bang, strangler fig, dual-write), feature flag and rollback plan, data migration steps and estimated duration.

### 11. Architecture Decision Records

For each significant decision, write an ADR:

```
ADR-001: Use PostgreSQL over DynamoDB for order storage

Status: Accepted
Context: We need ACID transactions for order state and complex joins for reporting.
Decision: PostgreSQL (RDS) with read replicas.
Consequences: Higher operational cost than DynamoDB. Team has existing expertise.
              Must manage connection pooling at scale.
```

Include at least one ADR. Common ADR topics: database choice, sync vs. async communication, build vs. buy, monolith vs. service split.

### 12. Open Questions

List unresolved questions. For each, note the owner and whether it blocks implementation.

---

## Quality checklist

Before delivering a system design document, verify:

- [ ] Every component in the architecture diagram is described in Section 5
- [ ] Non-functional requirements have numeric targets, not vague qualifiers
- [ ] At least 3 failure modes are analyzed with concrete mitigations
- [ ] API contracts include error cases, not just happy paths
- [ ] ADRs capture trade-offs and consequences, not just the decision
- [ ] Data model includes indexing and partitioning strategy for expected scale
- [ ] The document can be reviewed by someone who was not in the design discussion

## Common mistakes to avoid

- **Architecture astronautics**. Designing for 1M req/s when the system will see 100 req/s. Match the design complexity to the actual scale requirements.
- **Missing failure analysis**. "The database will be highly available" is not a plan. Specify the failover mechanism, expected downtime, and blast radius.
- **Diagrams without explanation**. A box-and-arrow diagram is not a design. Every arrow needs a protocol, every box needs a responsibility statement.
- **ADRs without trade-offs**. "We chose Kafka because it's industry standard" is not a decision record. State what you considered, what you rejected, and what consequences you accept.
- **Ignoring the migration path**. A greenfield design is easy. Explain how you get from the current state to the target state without downtime.
