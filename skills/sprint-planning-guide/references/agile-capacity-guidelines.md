# Agile Capacity Guidelines

Reference data for sprint capacity planning. Use these norms to calibrate capacity calculations and avoid common planning errors.

---

## Focus Factor Norms

Focus factor represents the percentage of a team member's available time that goes to sprint work. The rest is consumed by meetings, code review, Slack, context switching, and other non-sprint activities.

| Profile | Focus Factor | Rationale |
|---------|-------------|-----------|
| Standard IC | 0.8 | 20% overhead for meetings, reviews, communication |
| On-call engineer | 0.7 | Interrupts from pages, incident investigation, handoff prep |
| Tech lead | 0.6-0.7 | Architecture reviews, cross-team coordination, mentoring |
| Engineering manager (contributing) | 0.3-0.4 | Primarily management duties; sprint work is secondary |
| New hire (first month) | 0.3-0.4 | Onboarding, environment setup, learning codebase |
| New hire (months 2-3) | 0.5-0.6 | Increasing contribution, still ramping |
| Mentor of new hire | Reduce by 0.1 | Pairing, code review, answering questions |
| Interviewer (active hiring) | Reduce by 0.05-0.1 per interview loop | Each interview loop costs ~3 hours (prep, interview, debrief) |

### Calibration

If the team consistently delivers more or less than projected, adjust focus factors:
- Delivered 120% of projection three sprints in a row? Focus factors are too conservative — increase by 0.05.
- Delivered 70% of projection? Focus factors are too optimistic — decrease by 0.05.

Do not adjust by more than 0.1 per sprint. Let the trend stabilize over 3 sprints before changing.

---

## Velocity-to-Commitment Ratios

Velocity is a trailing indicator of capacity. Use it as a sanity check, not a target.

| Scenario | Recommended Commitment | Reasoning |
|----------|----------------------|-----------|
| Full team, no unusual events | 85-90% of average velocity | Leave 10-15% buffer for unknowns |
| Team member on PTO | Pro-rate by capacity ratio | If capacity is 80% of normal, commit to 80% of average velocity |
| First sprint with new team member | 75-80% of average velocity | New member contributes less; mentor contributes less |
| Sprint after an incident | 70-80% of average velocity | Postmortem actions, cleanup, and team recovery consume capacity |
| Sprint with a major release | 80-85% of average velocity | Release prep, monitoring, and hotfix buffer |

### How to Calculate

```
Projected velocity = Average velocity (last 3 sprints) x (This sprint's effective days / Average effective days)
Recommended commitment = Projected velocity x 0.85
```

### Velocity Averaging

- Use the **last 3 completed sprints** for the average
- Exclude outlier sprints (team was 50% capacity due to holidays, or an incident consumed the sprint)
- If the team has fewer than 3 sprints of history, use conservative estimates and adjust quickly

---

## Maintenance Allocation

Every sprint must allocate capacity for non-feature work. Skipping maintenance for three sprints creates a fourth sprint where feature work slows to a crawl.

### Recommended Allocation

| Category | % of Sprint Capacity | What It Covers |
|----------|---------------------|----------------|
| Bug fixes | 10% | User-reported bugs, production issues, regressions |
| Tech debt | 5-10% | Refactoring, dependency updates, test coverage |
| **Total maintenance** | **15-20%** | Combined non-feature work |

### When to Increase Maintenance Allocation

| Signal | Increase To | Duration |
|--------|------------|----------|
| Bug backlog growing sprint over sprint | 25% maintenance | Until backlog stabilizes |
| Major dependency update (e.g., framework version) | 30-40% maintenance for 1 sprint | One sprint |
| Post-incident hardening | 25-30% maintenance | 1-2 sprints |
| Team reports "everything is fragile" | 30% maintenance | 2-3 sprints, then reassess |

### How to Protect Maintenance Allocation

1. Add maintenance items to the sprint backlog as first-class stories with estimates
2. Select maintenance items during planning — do not leave them as "we'll squeeze them in"
3. Track maintenance velocity separately to ensure allocation is actually used
4. If a stakeholder asks to cut maintenance for a feature, make the tradeoff explicit: "We can add Feature X if we skip this month's dependency updates. The risk is [specific consequence]."

---

## Sprint Length Considerations

| Length | Best For | Watch Out For |
|--------|---------|---------------|
| 1 week | Rapid iteration, small teams, well-refined backlogs | Planning overhead is proportionally high; stories must be very small |
| 2 weeks | Most teams; balances planning overhead with feedback cycles | Most common and well-understood cadence |
| 3 weeks | Teams with longer review cycles or complex integrations | Uncommon; may indicate stories are too large |
| 4 weeks | Rarely recommended | Feedback cycles are too slow; problems compound before being detected |

### Adjusting Sprint Length

Change sprint length only when:
- The team consistently cannot complete meaningful work in the current length
- Planning overhead is disproportionate to execution time
- External feedback cycles (design review, stakeholder approval) do not fit the cadence

Do not change sprint length to "fit more in." If stories do not fit, break them down.
