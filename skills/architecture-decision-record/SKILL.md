---
name: architecture-decision-record
description: Write Architecture Decision Records (ADRs) that capture context, options considered, decision rationale, and consequences — creating a searchable decision log for future engineers.
metadata:
  displayName: "Architecture Decision Record"
  categories: ["engineering"]
  tags: ["ADR", "architecture", "decisions", "documentation", "technical-decisions"]
  worksWellWithAgents: ["autonomous-coding-agent", "code-generator", "code-migrator", "cto-advisor", "enterprise-architect"]
  worksWellWithSkills: ["codebase-exploration", "monorepo-setup-guide", "refactoring-checklist", "system-design-document", "technical-spec-writing"]
---

# Architecture Decision Record

## Before you start

Gather the following from the user:

1. **What decision needs to be recorded?** (Technology choice, pattern adoption, architectural change)
2. **What problem triggered this decision?** (The constraint, requirement, or pain point)
3. **What options were considered?** (At least 2-3 alternatives, including "do nothing")
4. **Who are the stakeholders?** (Teams or individuals affected by this decision)
5. **Is the decision already made or still in proposal?** (Status: proposed, accepted, deprecated, superseded)

If the user says "we decided to use Kafka," push back: "What problem does Kafka solve that your current approach doesn't? What alternatives did you evaluate? An ADR without alternatives considered is just an announcement."

## ADR template

### Header

Every ADR starts with a sequential number, title, and metadata.

```
# ADR-0017: Use PostgreSQL for Event Storage Instead of DynamoDB

- **Status**: Accepted
- **Date**: 2025-01-15
- **Decision makers**: @alice (tech lead), @bob (architect), @carol (DBA)
- **Consulted**: Platform team, Data engineering team
- **Supersedes**: ADR-0008 (if applicable)
```

Use a descriptive title that states the decision, not the problem. "Use PostgreSQL for Event Storage" is a decision. "Event Storage" is a topic.

### 1. Context

Describe the situation that requires a decision. Include:

- The business or technical driver
- Current state and its limitations
- Constraints (timeline, budget, team expertise, compliance)
- Non-functional requirements that influence the decision

Write this for an engineer joining the team 12 months from now. They were not in the room — give them enough context to understand why this decision was even necessary.

### 2. Options Considered

List every option evaluated, including "do nothing." For each option, describe how it addresses the problem and its tradeoffs.

For each option, include pros, cons, and an estimated cost or effort. Always include "do nothing" as an option — sometimes the cost of change exceeds the cost of the current pain.

### 3. Decision

State the chosen option clearly and concisely.

State the chosen option in one sentence. Then explain the rationale — why this option over the alternatives. Connect the reasoning to the constraints stated in the context. Explicitly address why each rejected option was not chosen.

### 5. Consequences

Document what changes as a result of this decision — both positive and negative.

Include three categories: **Positive consequences** (benefits gained), **Negative consequences** (costs and limitations accepted), and **Risks** (what could go wrong, with mitigation strategies).

### 6. Follow-Up Actions

List concrete next steps. Every action needs an owner and a deadline.

## ADR numbering and filing

- Number ADRs sequentially: ADR-0001, ADR-0002, etc.
- Store ADRs in a dedicated directory: `docs/adr/` or `decisions/`
- Use filenames that match: `0017-use-postgresql-for-event-storage.md`
- Maintain an index file (`README.md` or `INDEX.md`) linking to all ADRs with title, status, and date

When a decision is reversed, don't delete the original ADR. Mark it as **Superseded** and link to the new ADR that replaces it.

## Quality checklist

Before finalizing the ADR, verify:

- [ ] Title states the decision, not just the topic
- [ ] Context explains the problem without jumping to the solution
- [ ] At least 3 options are evaluated, including "do nothing"
- [ ] Each option includes pros, cons, and cost or effort estimate
- [ ] Rationale explicitly explains why rejected options were not chosen
- [ ] Consequences include both positive and negative outcomes
- [ ] Risks are identified with mitigation strategies
- [ ] Follow-up actions have owners and deadlines
- [ ] Status is clearly marked (proposed, accepted, deprecated, superseded)

## Common mistakes to avoid

- **Writing the ADR after the decision is forgotten.** Write the ADR while the context is fresh — ideally as part of the decision-making process, not weeks later. Retrospective ADRs lose the "why" behind rejected options.
- **Only documenting the chosen option.** The value of an ADR is understanding why alternatives were rejected. Without options considered, a future engineer can't tell if circumstances have changed enough to revisit the decision.
- **Confusing ADRs with design docs.** An ADR captures a decision and its rationale. A design doc describes how to implement it. Keep ADRs focused on the what and why, not the implementation details.
- **No "do nothing" option.** Always include it. Sometimes the cost of change exceeds the cost of the current pain. Making that explicit prevents unnecessary migrations.
- **Vague consequences.** "There may be some performance impact" is not useful. "Write throughput ceiling drops from 500K to 200K ops/sec, requiring sharding above that threshold" gives future engineers something actionable.
