---
name: okr-writing
description: Write OKRs (Objectives and Key Results) with measurable outcomes, scoring rubrics, and alignment checks across team and company levels.
metadata:
  displayName: "OKR Writing"
  categories: ["leadership", "project-management"]
  tags: ["okr", "objectives", "key-results", "goal-setting", "alignment"]
  worksWellWithAgents: ["engineering-manager", "people-ops-manager", "project-manager", "scrum-master", "vp-product"]
  worksWellWithSkills: ["metrics-framework", "program-status-report", "sprint-planning-guide", "stakeholder-interview"]
---

# OKR Writing

## Before you start

Gather the following from the user:

1. **What level are these OKRs for?** (Company, department, team, individual)
2. **What time period?** (Quarterly is standard; annual for company-level only)
3. **What are the company or department OKRs?** (Team OKRs must align upward)
4. **What was the outcome of last quarter's OKRs?** (Scores, lessons, carryovers)
5. **How many objectives?** (3-5 per level is the practical maximum)

If the user wants to write 8+ objectives, push back: "OKRs are about focus, not coverage. If everything is a priority, nothing is. Choose the 3-5 things that would make this quarter a success if you achieved nothing else."

## OKR structure

Each OKR set follows this format:

```
OBJECTIVE: [Qualitative, inspiring, time-bound statement of what you want to achieve]

  KR1: [Quantitative metric] from [baseline] to [target]
  KR2: [Quantitative metric] from [baseline] to [target]
  KR3: [Quantitative metric] from [baseline] to [target]
```

### Objective rules
- Qualitative and motivating — describes a desired end state
- Ambitious but not impossible — should feel uncomfortable at 70% confidence
- Time-bound (implicitly by the OKR cycle, e.g., Q2 2025)
- No metrics in the objective — that is what Key Results are for
- Starts with a verb: "Establish," "Accelerate," "Reduce," "Build"

### Key Result rules
- Quantitative and measurable — a number that can be verified
- States a baseline ("from") and target ("to")
- 2-5 Key Results per Objective
- Measures outcomes, not tasks — "Ship feature X" is a task, "Increase activation rate from 30% to 45%" is a Key Result
- Each KR is independently valuable — achieving 2 of 3 should still matter

## OKR template

```
## Q2 2025 OKRs — [Team Name]

### Objective 1: [Verb + desired end state]
Alignment: Supports [Company/Dept Objective name or number]

| KR# | Key Result                                      | Baseline | Target | Owner    |
|-----|-------------------------------------------------|----------|--------|----------|
| 1.1 | [Metric description]                            | [X]      | [Y]    | @person  |
| 1.2 | [Metric description]                            | [X]      | [Y]    | @person  |
| 1.3 | [Metric description]                            | [X]      | [Y]    | @person  |

### Objective 2: [Verb + desired end state]
Alignment: Supports [Company/Dept Objective name or number]

| KR# | Key Result                                      | Baseline | Target | Owner    |
|-----|-------------------------------------------------|----------|--------|----------|
| 2.1 | [Metric description]                            | [X]      | [Y]    | @person  |
| 2.2 | [Metric description]                            | [X]      | [Y]    | @person  |
| 2.3 | [Metric description]                            | [X]      | [Y]    | @person  |
```

## Scoring rubric

Score each Key Result at the end of the cycle using this scale:

```
| Score     | Meaning                                               |
|-----------|-------------------------------------------------------|
| 0.0       | No progress                                           |
| 0.1 - 0.3 | Some progress but fell significantly short            |
| 0.4 - 0.6 | Made meaningful progress — partial achievement        |
| 0.7       | Delivered — this is the expected "success" score      |
| 0.8 - 0.9 | Exceeded expectations                                 |
| 1.0       | Fully achieved or exceeded — may indicate sandbagging |
```

A healthy average OKR score across a team is 0.6-0.7. If the team consistently scores 0.9+, the OKRs are not ambitious enough.

## Alignment check

Every team OKR must connect to a company or department objective. Use this format to verify alignment.

```
Company Objective: "Become the market leader in developer tools"
  └─ Dept Objective: "Accelerate product-led growth"
      └─ Team Objective: "Improve new user activation experience"
          └─ KR: Increase Day-7 activation rate from 30% to 45%
```

If a team objective does not trace up to a company objective, either:
1. The team is working on something the company has not prioritized — escalate the misalignment
2. The company OKRs are missing a priority — propose adding it

## Mid-cycle check-in template

Review OKRs at the halfway point (week 6 of a 12-week quarter).

```
| KR#  | Key Result              | Baseline | Current | Target | Status      | Action Needed      |
|------|------------------------|----------|---------|--------|-------------|---------------------|
| 1.1  | [Metric]               | 100      | 130     | 200    | On track    | None                |
| 1.2  | [Metric]               | 5%       | 5.5%    | 10%    | At risk     | Reassign resources  |
| 1.3  | [Metric]               | 0        | 0       | 3      | Off track   | Scope discussion    |
```

Status definitions:
- **On track**: Current trajectory reaches the target
- **At risk**: Behind pace but recoverable with intervention
- **Off track**: Will not reach target without significant change

## Quality checklist

Before finalizing OKRs, verify:

- [ ] Each objective is qualitative — no numbers in the objective statement
- [ ] Each key result has a numeric baseline and target
- [ ] 3-5 objectives maximum per level
- [ ] 2-5 key results per objective
- [ ] Every team OKR traces to a company or department objective
- [ ] Key results measure outcomes, not outputs or tasks
- [ ] At least one KR per objective would be uncomfortable to commit to (stretch)
- [ ] Each KR has a single owner

## Common mistakes

- **Key results that are tasks.** "Launch the new dashboard" is a task. "Increase weekly active dashboard users from 200 to 500" is a key result. OKRs measure outcomes, not deliverables.
- **Sandbagging targets.** If every KR scores 1.0, the team set easy targets. A 0.7 average means the OKRs were properly ambitious. Normalize this expectation with the team.
- **No baseline.** "Improve NPS to 50" is meaningless without knowing the current NPS. Every KR needs a "from X" starting point, even if it's zero.
- **Too many objectives.** Five objectives with four KRs each means 20 things to track. That is not focus — that is a wish list. Ruthlessly cut to 3-4 objectives.
- **OKRs written in isolation.** If engineering, product, and marketing each write OKRs without coordinating, you get misaligned priorities. Run an alignment session before finalizing.
