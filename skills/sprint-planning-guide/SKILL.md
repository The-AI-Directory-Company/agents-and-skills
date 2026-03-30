---
name: sprint-planning-guide
description: Run effective sprint planning sessions — from backlog refinement through capacity allocation, commitment, and sprint goal definition with clear acceptance criteria.
metadata:
  displayName: "Sprint Planning Guide"
  categories: ["project-management"]
  tags: ["sprint-planning", "agile", "backlog", "capacity", "commitment"]
  worksWellWithAgents: ["scrum-master", "technical-pm"]
  worksWellWithSkills: ["okr-writing", "ticket-writing", "user-story-mapping"]
---

# Sprint Planning Guide

## Before you start

Gather the following from the user:

1. **Sprint length** (1 week, 2 weeks, or custom)
2. **Team size and composition** (How many engineers, designers, QA — and who is out this sprint)
3. **Backlog state** (Is the backlog refined? Are the top items estimated and acceptance-criteria-ready?)
4. **Carryover from last sprint** (Incomplete stories, bugs, or tech debt items that must continue)
5. **External commitments** (Deadlines, cross-team dependencies, or stakeholder promises)

If the user says "we just pull from the top of the backlog," push back: "Without a sprint goal, the team is doing task execution, not sprint planning. What outcome should be true at the end of this sprint that isn't true today?"

## Sprint planning template

### 1. Pre-Planning: Backlog Refinement

Complete this **before** the planning meeting — not during it.

**Refinement checklist (done 2-3 days before planning):**

- [ ] Top 15-20 backlog items have clear descriptions and acceptance criteria
- [ ] Stories are estimated (story points, T-shirt sizes, or hours — pick one, stay consistent)
- [ ] Dependencies between stories are identified and documented
- [ ] Stories that require design, research, or external input are flagged
- [ ] Tech debt and bug items are groomed and prioritized alongside feature work

If the backlog isn't refined, don't hold planning. Hold a refinement session instead. Planning with unrefined stories wastes everyone's time and produces unreliable commitments.

### 2. Capacity Calculation

Calculate how much the team can realistically take on.

```
Team capacity worksheet:

| Team Member  | Available Days | Focus Factor | Effective Days |
|-------------|---------------|-------------|----------------|
| Alice       | 10            | 0.8         | 8.0            |
| Bob         | 8 (PTO Fri)  | 0.8         | 6.4            |
| Carol       | 10            | 0.7 (on-call)| 7.0           |
| Dave        | 5 (half sprint)| 0.8        | 4.0            |
| **Total**   | **33**        |             | **25.4**       |
```

**Focus factor guidelines:**
- 0.8 = standard (accounts for meetings, code review, Slack)
- 0.7 = on-call rotation or heavy meeting week
- 0.6 = significant non-sprint responsibilities (hiring, cross-team support)

Compare effective days to the team's historical velocity. If the team averages 30 story points per sprint at full capacity but has 80% capacity this sprint, plan for ~24 points.

### 3. Sprint Goal Definition

Define 1-2 sprint goals before selecting stories. The goal answers: "What is the most important outcome of this sprint?"

```
Sprint Goal: Users can complete checkout with saved payment methods.

This is achieved when:
1. Saved payment method selection is functional in checkout flow
2. Payment processing works end-to-end with saved cards
3. Error handling covers expired cards and declined transactions
```

A good sprint goal is:
- **Outcome-oriented**: Describes what users can do, not what engineers will build
- **Achievable in one sprint**: Not a multi-sprint epic restated as a goal
- **Falsifiable**: At sprint review, you can definitively say "yes, we achieved this" or "no, we didn't"

### 4. Story Selection and Commitment

With the goal defined and capacity known, select stories.

**Selection process:**

1. Start with carryover items — these are already in progress and get priority
2. Pull stories that directly support the sprint goal
3. Add maintenance items (bugs, tech debt) — allocate 15-20% of capacity
4. Check for dependencies — flag any story that's blocked by external teams
5. Stop when you hit capacity. Do not overcommit.

Record the final commitment as a table with columns: ID, Title, Points, Owner, Dependencies. Include the total points, capacity, and velocity average at the bottom for a sanity check.

### 5. Sprint Planning Meeting Agenda

Run the meeting in 60 minutes or less for a 2-week sprint.

Structure: 5 min reviewing last sprint results, 5 min announcing capacity/constraints, 10 min aligning on sprint goal, 25 min walking through stories and assigning owners, 10 min finalizing commitment, 5 min identifying risks. Key rules: no story refinement during planning (if it's not ready, it doesn't enter the sprint), every story must have an owner before the meeting ends.

### 6. Risk and Dependency Tracking

At the end of planning, identify risks and assign mitigation owners. For each risk, document: what the risk is, its impact on the sprint goal, the mitigation plan, and who owns it.

## Quality checklist

Before closing the planning session, verify:

- [ ] A sprint goal is defined and the team can state it without reading notes
- [ ] Every story has an owner, an estimate, and acceptance criteria
- [ ] Total commitment is at or below team capacity (never above historical velocity)
- [ ] Carryover items from last sprint are accounted for
- [ ] At least 15% of capacity is reserved for bugs and tech debt
- [ ] Dependencies are identified with mitigation plans
- [ ] The planning meeting stayed under 60 minutes

## Common mistakes to avoid

- **No sprint goal.** Without a goal, the team is executing a task list, not working toward an outcome. A sprint with 10 unrelated stories has no coherence and no way to make tradeoff decisions mid-sprint.
- **Planning without refined stories.** If the team spends 30 minutes debating what a story means during planning, it wasn't refined. Refinement and planning are separate ceremonies — never combine them.
- **Overcommitting.** Teams that commit to 110% of capacity every sprint build a culture of failure. Plan to 80-85% of historical velocity to leave room for the unexpected.
- **Ignoring carryover.** Incomplete stories from last sprint don't disappear. Account for them first — they consume capacity whether you acknowledge them or not.
- **Skipping the capacity calculation.** "We usually do about 30 points" ignores that two people are on PTO and one is on-call. Calculate capacity for this specific sprint.
- **All features, no maintenance.** Skipping tech debt and bug fixes for three sprints creates a fourth sprint where you can't ship features because the codebase is falling apart. Protect 15-20% for maintenance every sprint.
