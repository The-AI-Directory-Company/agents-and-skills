---
name: prd-writing
description: Write clear, comprehensive Product Requirements Documents with problem statements, success metrics, scope boundaries, and actionable requirements.
metadata:
  displayName: "PRD Writing"
  categories: ["product-management"]
  tags: ["prd", "requirements", "documentation", "product"]
  worksWellWithAgents: ["brand-manager", "business-analyst", "compliance-officer", "content-strategist", "copywriter", "cto-advisor", "developer-advocate"]
  worksWellWithSkills: ["content-calendar", "create-agent-markdown", "experiment-design", "financial-model", "go-to-market-plan", "metrics-framework", "product-launch-brief", "stakeholder-interview", "system-design-document", "technical-spec-writing", "test-plan-writing", "threat-model-writing", "ticket-writing", "user-story-mapping", "ux-copy-guidelines"]
---

# PRD Writing

## Before you start

Gather the following information. If any is missing, ask the user before proceeding:

1. **Problem statement** — What user pain or business need are we addressing?
2. **Target users** — Which user segments are affected? How many?
3. **Constraints** — Timeline, budget, team size, technical limitations
4. **Prior art** — Has this been attempted before? What happened?
5. **Stakeholders** — Who needs to approve this? Who has opinions?

If the user only gives you a feature idea ("we need dark mode"), push back and ask for the problem ("what user need does dark mode serve?").

## PRD template

Use the following template. Every section is required unless explicitly marked optional.

---

### Title

`[Feature Name] — Product Requirements Document`

### 1. Problem Statement (2-3 sentences)

State the problem from the user's perspective. Include:
- Who is affected (specific user segment, not "users")
- What they're struggling with (observable behavior, not assumed feelings)
- How severe and frequent the problem is (data if available)

**Good**: "Enterprise customers with 50+ team members report spending 20+ minutes per week manually reassigning tickets when team members go on PTO, leading to SLA breaches in 12% of cases."

**Bad**: "Users want better ticket management."

### 2. Goals & Success Metrics

Define 2-4 measurable outcomes. Each must have:
- A metric name
- A current baseline (if known)
- A target value
- A measurement method

| Metric | Baseline | Target | How to measure |
|--------|----------|--------|----------------|
| Time to reassign tickets | 20 min/week | < 2 min/week | Avg from activity logs |
| SLA breach rate | 12% | < 3% | Monthly SLA report |

### 3. User Stories

Write 3-8 user stories in standard format:

> As a [user type], I want [action] so that [outcome].

Order by priority. Mark each as P0 (must have), P1 (should have), or P2 (nice to have).

### 4. Scope

**In scope** — List specific capabilities included in this work.

**Out of scope** — Explicitly list things that might be assumed but are NOT included. This section prevents scope creep and is as important as the in-scope list.

**Future considerations** — Things deliberately deferred to a later phase.

### 5. Functional Requirements

Number each requirement. Use RFC 2119 language:
- **MUST** — Non-negotiable for launch
- **SHOULD** — Expected but can be deferred with justification
- **MAY** — Optional enhancement

```
FR-1: The system MUST automatically reassign open tickets when a team member's
      OOO status is detected via calendar integration.
FR-2: The system SHOULD notify the original assignee when their tickets are
      reassigned.
FR-3: The system MAY suggest the best reassignment target based on workload.
```

### 6. Non-Functional Requirements

Address at minimum:
- **Performance** — Response time, throughput expectations
- **Scale** — Expected volume (users, data, requests)
- **Security** — Auth requirements, data sensitivity, compliance
- **Accessibility** — WCAG level, supported devices

### 7. Design Considerations (optional)

UX constraints, existing patterns to follow, key user flows. Reference wireframes or prototypes if they exist. Do NOT design the UI — describe the user outcomes.

### 8. Open Questions

List unresolved questions that could change scope or approach. For each:
- State the question
- Note who can answer it
- Flag the decision's impact (blocks implementation? changes scope?)

### 9. Timeline (optional)

If the user has provided timeline constraints, include rough milestones. Otherwise, note that engineering will estimate after reviewing the spec.

---

## Quality checklist

Before delivering a PRD, verify:

- [ ] Problem statement is based on user behavior, not assumed needs
- [ ] Every success metric has a baseline and target
- [ ] Out-of-scope section explicitly addresses likely scope creep areas
- [ ] Requirements use MUST/SHOULD/MAY consistently
- [ ] No UI design decisions are made (that's design's job)
- [ ] Open questions have owners and impact assessments
- [ ] The document can stand alone — someone not in the room could understand it

## Common mistakes to avoid

- **Writing solutions, not problems**. The problem statement should not contain the word "should" or describe a feature. It describes a pain.
- **Vague success metrics**. "Improve user satisfaction" is not a metric. "Increase NPS from 32 to 45 within 3 months" is.
- **Empty out-of-scope sections**. If nothing is out of scope, you haven't thought hard enough. Every feature has adjacent features that could creep in.
- **Requirements that are actually design**. "Add a dropdown menu with..." is design. "The user MUST be able to select from predefined options" is a requirement.
