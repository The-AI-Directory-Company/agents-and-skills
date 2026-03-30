# Capacity Worksheet Template

Fill in for each sprint to calculate realistic team capacity before selecting stories.

---

## Sprint Information

| Field | Value |
|-------|-------|
| **Sprint name** | [e.g., Sprint 24] |
| **Sprint dates** | [Start date] — [End date] |
| **Working days in sprint** | [e.g., 10] |
| **Company holidays in sprint** | [List or "None"] |

---

## Team Capacity

| Team Member | Role | Available Days | Reason for Reduction | Focus Factor | Effective Days |
|-------------|------|---------------|---------------------|-------------|----------------|
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| **Total** | | **___** | | | **___** |

### How to Fill In

- **Available Days**: Sprint length minus PTO, holidays, and known absences.
- **Reason for Reduction**: PTO, conference, on-call rotation, half-sprint allocation, etc. Leave blank if full sprint.
- **Focus Factor**: See reference table below.
- **Effective Days**: Available Days x Focus Factor.

---

## Focus Factor Reference

| Factor | When to Use |
|--------|------------|
| **0.8** | Standard — accounts for meetings, code review, Slack, and context switching |
| **0.7** | On-call rotation, heavy meeting week, or significant code review load |
| **0.6** | Major non-sprint responsibilities: hiring panels, cross-team support, training delivery |
| **0.5** | Split between two teams, or onboarding a new team member (mentor's factor) |

### Notes

- New team members (first 2-4 sprints): use 0.4-0.5 for the new hire; reduce mentor's factor by 0.1.
- If someone is "available for half the sprint," set Available Days to half, then apply the normal focus factor.
- Do not use 1.0 as a focus factor. No one spends 100% of their time on sprint work.

---

## Capacity vs. Velocity Sanity Check

| Metric | Value |
|--------|-------|
| **Effective days this sprint** | [From total above] |
| **Average effective days (last 3 sprints)** | [Calculate from past worksheets] |
| **Capacity ratio** | [This sprint / Average] |
| **Average velocity (last 3 sprints)** | [Story points completed] |
| **Projected velocity this sprint** | [Average velocity x Capacity ratio] |
| **Planned commitment** | [Story points selected in planning] |

### Validation

- [ ] Planned commitment is at or below projected velocity
- [ ] If commitment exceeds projected velocity, the team has explicitly discussed and accepted the risk
- [ ] Carryover items from last sprint are included in the commitment count
