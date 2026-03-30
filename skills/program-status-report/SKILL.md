---
name: program-status-report
description: Write program status reports that surface risks and decisions, not just progress — with executive summaries, workstream tracking, dependency maps, and escalation frameworks.
metadata:
  displayName: "Program Status Report"
  categories: ["project-management"]
  tags: ["status-report", "program-management", "reporting", "risks", "tracking"]
  worksWellWithAgents: ["engineering-manager", "project-manager", "technical-program-manager"]
  worksWellWithSkills: ["okr-writing", "ticket-writing"]
---

# Program Status Report

## Before you start

Gather the following from the user before writing:

1. **What program or initiative does this cover?** (Name, scope, and target completion date)
2. **Who is the audience?** (Executive leadership, steering committee, cross-functional stakeholders, or the working team)
3. **What reporting cadence is this?** (Weekly, biweekly, monthly — this determines the right level of detail)
4. **What happened since the last report?** (Milestones hit, milestones missed, scope changes, team changes)
5. **What decisions or escalations are needed?** (Blockers that the audience has authority to resolve)

If the user says "just summarize where we are," push back: "A status report that only reports progress is a changelog. What risks, blockers, or decisions does your audience need to act on?"

## Status report template

### Program header

State the program name, reporting period, overall status (Green/Yellow/Red), report author, and distribution date. The status color must reflect the worst-case workstream, not an average.

```
Program: Platform Migration    |  Period: Mar 3-14, 2025
Overall Status: YELLOW         |  Author: J. Martinez
Distribution: Steering Committee, Eng Leadership
```

### Executive summary

3-5 sentences maximum. Structure as:

1. **Overall trajectory** — Are we on track to hit the program milestone? State the milestone and date.
2. **Key progress** — The 1-2 most significant accomplishments this period.
3. **Primary risk or blocker** — The single biggest threat to the timeline and what is needed to resolve it.

Executives read this section and nothing else. If the report were only these 5 sentences, the audience should still know whether to worry.

### Status by workstream

Use a table with one row per workstream. Every row must include:

| Workstream | Owner | Status | Progress this period | Next milestone | Risk |
|---|---|---|---|---|---|
| Data migration | @Lee | GREEN | Migrated 3/5 schemas | Schema 4 by Mar 21 | None |
| API cutover | @Patel | YELLOW | Auth integration delayed 3 days | Auth complete by Mar 18 | Vendor response time — see Risks |
| Frontend rebuild | @Chen | GREEN | Search page shipped | Settings page by Mar 25 | None |

Status rules:
- **GREEN**: On track, no blockers, will hit the next milestone on time
- **YELLOW**: At risk — a known issue threatens the milestone but a mitigation plan exists
- **RED**: Off track — the milestone will be missed without intervention from outside the team

Never mark a workstream GREEN when it depends on a YELLOW or RED workstream.

### Milestones

List the next 4-6 milestones in chronological order. For each, state the target date, responsible owner, current confidence level (High/Medium/Low), and any predecessor dependency.

```
1. Auth integration complete — Mar 18 — @Patel — Medium (blocked on vendor)
2. Schema 4 migration — Mar 21 — @Lee — High
3. Settings page shipped — Mar 25 — @Chen — High
4. End-to-end staging test — Mar 28 — @Martinez — Medium (depends on #1, #2)
```

### Risks and mitigations

List every active risk. Each risk entry must include:

- **Risk**: What could go wrong (specific, not vague)
- **Impact**: What happens to the program if it materializes (timeline, scope, or cost)
- **Likelihood**: High, Medium, or Low
- **Mitigation**: What is being done to reduce the likelihood or impact
- **Owner**: Who is responsible for executing the mitigation
- **Escalation trigger**: The condition under which this risk becomes a blocker requiring leadership action

```
Risk: Vendor has not responded to SSO integration questions in 5 business days.
Impact: API cutover delayed 1-2 weeks, pushing program completion past Q1.
Likelihood: Medium
Mitigation: Escalated to vendor account manager; parallel-pathing with in-house SAML implementation.
Owner: @Patel
Escalation trigger: No vendor response by Mar 17 — will need leadership to engage vendor VP.
```

### Decisions needed

List decisions that require action from the report audience. For each, state the decision, the options, the recommendation, and the deadline. If no decisions are needed, state "No decisions required this period" — do not omit the section.

### Key metrics (if applicable)

Include 3-5 quantitative indicators of program health: burn rate vs budget, velocity vs plan, defect count, test coverage, or adoption metrics. Show trend direction.

## Quality checklist

Before delivering the report, verify:

- [ ] Executive summary is 3-5 sentences and conveys trajectory, progress, and the top risk
- [ ] Every workstream has a named owner, a status color with justification, and a next milestone with date
- [ ] Status colors follow the rules — no GREEN workstreams with unresolved dependencies on YELLOW/RED workstreams
- [ ] Every risk has a specific mitigation, an owner, and an escalation trigger
- [ ] Decisions section states options, a recommendation, and a deadline — not just "we need to decide"
- [ ] Milestones include confidence levels and dependency chains
- [ ] The report can be skimmed in under 2 minutes by reading only the header, executive summary, and status table

## Common mistakes

- **Reporting activity instead of progress.** "We had 12 meetings and reviewed 3 design docs" is activity. "Auth integration is 80% complete, on track for Mar 18" is progress. Report outcomes, not effort.
- **Hiding bad news in the middle.** If a workstream is RED, it belongs in the executive summary, not buried in a table footnote. Executives should never be surprised.
- **GREEN status with caveats.** "GREEN — on track assuming the vendor responds by Friday" is YELLOW. If there is a conditional, the status is not GREEN.
- **Risks without mitigations.** Listing a risk without a mitigation plan is complaining, not managing. Every risk needs an action, an owner, and a trigger for escalation.
- **Skipping the decisions section.** If leadership reads the report and does not know what you need from them, the report failed its primary purpose. Be explicit about asks.
- **Inconsistent reporting periods.** Mixing "this week" and "this month" data in the same report makes trends unreadable. Pick one cadence and stick to it.
