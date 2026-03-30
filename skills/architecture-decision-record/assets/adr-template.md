# ADR Template

Copy this template to create a new Architecture Decision Record.

---

```markdown
# ADR-[NNNN]: [Decision title — state the decision, not the topic]

- **Status**: [Proposed / Accepted / Deprecated / Superseded by ADR-NNNN]
- **Date**: [YYYY-MM-DD]
- **Decision makers**: [@person1 (role), @person2 (role)]
- **Consulted**: [Teams or individuals who provided input]
- **Supersedes**: [ADR-NNNN, if replacing a previous decision — otherwise remove this line]

## 1. Context

[Describe the situation that requires a decision. Write for an engineer joining the team 12 months from now who was not in the room.]

[Include:]
- [The business or technical driver that created the need for this decision]
- [Current state and its specific limitations or pain points]
- [Constraints: timeline, budget, team expertise, compliance requirements]
- [Non-functional requirements that influence the decision (performance, scalability, security)]

## 2. Options Considered

### Option A: [Name]

[One paragraph describing how this option addresses the problem.]

**Pros:**
- [Specific benefit with evidence or reasoning]
- [...]

**Cons:**
- [Specific drawback with evidence or reasoning]
- [...]

**Estimated effort:** [T-shirt size or time estimate, e.g., "~2 sprints, 1 backend + 1 infra engineer"]

---

### Option B: [Name]

[One paragraph describing how this option addresses the problem.]

**Pros:**
- [...]

**Cons:**
- [...]

**Estimated effort:** [...]

---

### Option C: Do Nothing

[Describe what happens if no change is made. Quantify the ongoing cost of the current state.]

**Pros:**
- No migration effort or risk
- [...]

**Cons:**
- [The specific pain or limitation that continues]
- [...]

**Estimated effort:** Zero upfront, but [ongoing cost description].

## 3. Decision

[State the chosen option in one sentence.]

[Then explain the rationale — why this option over the alternatives. Connect the reasoning to the constraints in the Context section.]

[Explicitly state why each rejected option was not chosen:]
- [Option X was rejected because...]
- [Do Nothing was rejected because...]

## 4. Consequences

### Positive
- [Specific benefit gained, with measurable impact if possible]
- [...]

### Negative
- [Specific cost or limitation accepted]
- [...]

### Risks
- **[Risk description]** — Mitigation: [How you will reduce or monitor this risk]
- **[Risk description]** — Mitigation: [...]

## 5. Follow-Up Actions

| Action | Owner | Deadline |
|--------|-------|----------|
| [Concrete next step] | @[person] | [YYYY-MM-DD] |
| [Concrete next step] | @[person] | [YYYY-MM-DD] |
| [Concrete next step] | @[person] | [YYYY-MM-DD] |
```
