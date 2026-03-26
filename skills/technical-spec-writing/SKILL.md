---
name: technical-spec-writing
description: Write technical specifications that bridge product requirements and implementation — with problem statements, proposed solutions, data model changes, API changes, migration plans, rollback strategies, and open questions.
metadata:
  displayName: "Technical Spec Writing"
  categories: ["engineering"]
  tags: ["technical-spec", "RFC", "design-doc", "specification", "engineering"]
  worksWellWithAgents: ["api-developer", "developer-experience-engineer", "documentation-architect", "platform-engineer", "software-architect", "tech-lead", "technical-pm"]
  worksWellWithSkills: ["api-design-guide", "architecture-decision-record", "prd-writing", "system-design-document"]
---

# Technical Spec Writing

## Before you start

Gather the following from the user. If anything is missing, ask before writing:

1. **What are you building?** — Feature name and one-sentence summary. Link to the PRD if one exists.
2. **Why now?** — Business driver, user pain, or technical urgency behind this work.
3. **Scope** — New feature, refactor, migration, or extension of an existing system?
4. **Constraints** — Tech stack, timeline, team size, backward-compatibility requirements.
5. **Audience** — Who reviews this spec? (e.g., engineering team, staff engineer, CTO, security)

If the user says "write a spec for X" with no context, push back: "What problem does this solve, and what does the system look like today?"

## Technical spec template

### Title

`[Feature/Change Name] — Technical Specification`

### 1. Problem Statement (3-5 sentences)

State the problem from the user's or system's perspective. Reference the PRD or incident that motivates the work. Describe the current state and why it is insufficient.

### 2. Context

Summarize relevant prior art: existing systems, past decisions, constraints inherited from other teams. A reviewer who has no background should understand the landscape after reading this section.

### 3. Proposed Solution

Describe the approach at a level of detail sufficient for another engineer to implement it. Include component interactions, sequence of operations, and key design decisions. Call out alternatives you considered and why you rejected them.

### 4. Data Model Changes

Document every schema change: new tables, columns, indexes, or type modifications. Use DDL or a clear table format. State whether changes are additive (safe to deploy independently) or breaking.

### 5. API Changes

For each new or modified endpoint: method, path, request/response shapes, error codes, and auth requirements. If no API changes, state "No API changes" explicitly so reviewers know it was considered.

### 6. Migration Plan

Step-by-step plan for moving from current state to target state. Include: ordering of deploys, data backfill strategy, estimated duration, and whether the migration requires downtime.

### 7. Rollback Plan

What happens if this goes wrong after deploy? Cover: feature flag strategy, database rollback steps (are migrations reversible?), and the decision criteria for triggering a rollback.

### 8. Monitoring & Alerting

Define what signals indicate success or failure post-launch. Specify: key metrics to track, alert thresholds, dashboards to create or update, and who gets paged.

### 9. Security Considerations

Address: authentication/authorization changes, new data sensitivity (PII, secrets), input validation, and attack surface changes. If none, state "No security impact" with justification.

### 10. Testing Strategy

Specify: unit tests for new logic, integration tests for cross-service flows, load/stress tests if performance-sensitive, and manual QA scenarios that cannot be automated.

### 11. Open Questions

List unresolved decisions. For each, note who owns the answer and whether it blocks implementation. Do not bury open questions inside other sections.

### 12. Out of Scope

Explicitly list related work you are NOT doing. This prevents scope creep during review and sets expectations for follow-up specs.

## Quality checklist

Before delivering the spec, verify:

- [ ] Problem statement explains WHY, not just WHAT
- [ ] Proposed solution includes rejected alternatives with reasoning
- [ ] Data model changes specify whether they are additive or breaking
- [ ] API changes include error cases, not just happy paths
- [ ] Migration plan has a step-by-step ordering, not just a goal state
- [ ] Rollback plan is concrete — not "we will roll back if needed"
- [ ] Open questions list an owner and blocking status for each item
- [ ] Out of scope is explicit — reviewers should not wonder "what about X?"
- [ ] A teammate unfamiliar with the project can understand the spec without a walkthrough

## Common mistakes to avoid

- **Solution without problem**. Jumping straight to implementation without establishing why the change matters. Reviewers cannot evaluate a solution they do not understand the motivation for.
- **Vague rollback plans**. "Roll back the deploy" is not a plan when you have run a data migration. Specify whether migrations are reversible and what data loss, if any, a rollback entails.
- **Missing the current state**. Describing only the target state. Reviewers need to understand what exists today to evaluate the delta.
- **Conflating spec with design doc**. A tech spec answers "what are we building and how do we ship it safely." A system design doc answers "what is the architecture." If you need both, write both and cross-reference.
- **Burying open questions**. Scattering unresolved decisions across sections instead of surfacing them in a dedicated section. Reviewers miss them and the spec ships with silent assumptions.
