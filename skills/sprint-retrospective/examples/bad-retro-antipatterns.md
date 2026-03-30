# Bad Retro Anti-patterns — Annotated Example

This is a deliberately bad retrospective output, annotated with what went wrong and how to fix it. Use this as a reference when reviewing retro quality.

---

## Example: Sprint 14 Retrospective (Everything Wrong)

**Date:** March 15
**Participants:** The team
**Sprint goal:** Missed

---

### Previous Action Items

*[Not reviewed]*

**What's wrong:** The retro skipped reviewing last sprint's commitments entirely. This teaches the team that retro outcomes do not matter and nothing will be followed up on.

**Fix:** Always start by reviewing each previous action item with explicit status (Completed / In Progress / Not Started / Abandoned) and measurable results.

---

### What Went Well

- "Things were generally okay"
- "We shipped some stuff"
- "Communication was better"

**What's wrong:** Every observation is vague. "Generally okay" conveys no information. "Some stuff" does not specify what was shipped or why it mattered. "Better" compared to what?

**Fix:** Require specific observations with data. "We shipped the checkout redesign 2 days ahead of schedule" or "Cross-team syncs reduced blocked stories from 5 to 1."

---

### What Didn't Go Well

- "Deploys were slow"
- "DevOps didn't prioritize our tickets"
- "QA was a bottleneck again"
- "We didn't have enough time"

**What's wrong:**

1. **"Deploys were slow"** — No data. How slow? Compared to what? This is a feeling, not an observation.
2. **"DevOps didn't prioritize our tickets"** — This is blame directed at another team. It frames the problem as someone else's fault rather than identifying what the team can control.
3. **"QA was a bottleneck again"** — "Again" suggests this has come up before and was never addressed. Also blame-framed.
4. **"We didn't have enough time"** — This is always true. It says nothing about what specifically was underestimated or what could change.

**Fix:**
1. "Deploy pipeline averaged 47 minutes this sprint, up from 30 minutes last sprint. The increase correlates with [specific change]."
2. "We submitted 3 infrastructure tickets; average resolution time was 8 days. What can we change about how we submit or scope these requests?"
3. "4 of 7 stories entered QA in the last 2 days of the sprint. QA had 2 days to test 70% of the sprint scope. How do we spread testing more evenly?"
4. "We committed to 35 points with a velocity average of 28. We overcommitted by 25%."

---

### Action Items

1. "Improve deploys"
2. "Better communication with DevOps"
3. "Write more tests"
4. "Be more careful with estimates"
5. "Document things better"
6. "Have fewer meetings"
7. "Fix the flaky tests"

**What's wrong (every item):**

| # | Problem | Missing |
|---|---------|---------|
| 1 | Vague — improve how? By how much? | Specific action, owner, deadline, success metric |
| 2 | Vague — what communication, about what? | Specific action (e.g., "Attend DevOps standup Tuesdays") |
| 3 | Not targeted — which tests for what? | Scope, owner, timeline |
| 4 | Not actionable — how? | Specific technique (e.g., "Break stories over 5 points into sub-tasks") |
| 5 | Classic "document things" — never happens | Which documents, who writes them, by when |
| 6 | No specifics — which meetings? | Identify the meetings, propose alternatives |
| 7 | Could be legitimate but lacks context | Which tests, who owns the fix, by when |

**Additional problems:**
- **7 action items.** Teams that commit to 7 items complete 0. Maximum is 3 per retro.
- **No owners.** Not a single action item has a named person responsible. "The team will handle it" is code for "no one will do it."
- **No timelines.** No deadlines or durations. These will drift indefinitely.
- **No success criteria.** How will the team know if "improve deploys" worked? Without measurement, it cannot be evaluated at the next retro.

**Fix — rewrite as proper experiments (pick top 2-3 only):**

```
Theme: Deploy pipeline speed
Hypothesis: If we add build caching to the CI pipeline, then average deploy
time will drop from 47 minutes to under 25 minutes, measured by CI metrics.
Experiment: Alex will implement build caching for the main pipeline by March 22.
Owner: Alex
Duration: 2 sprints
Success Criteria: Average deploy time < 25 minutes over 2 sprints.
```

```
Theme: Late-sprint QA crunch
Hypothesis: If developers move stories to QA by Wednesday of week 2 (instead
of Friday), then QA will have 3 full days for testing instead of 1, measured by
the date stories enter the QA column.
Experiment: During sprint 15, the team will treat Wednesday EOD as the soft
deadline for moving stories to QA. Stories not in QA by Thursday standup will
be flagged.
Owner: Jamie (facilitates daily check)
Duration: 1 sprint
Success Criteria: 80%+ of stories enter QA by Wednesday of week 2.
```

---

## Anti-pattern Summary

| Anti-pattern | Signal | Consequence |
|-------------|--------|-------------|
| Skipping previous action review | "We'll get to those later" | Team learns retro outcomes are disposable |
| Vague observations | "Things were okay," "it was slow" | No root cause identified, no targeted action possible |
| Blame framing | "[Other team] didn't..." | Defensive reactions, no ownership of what the team can control |
| Too many action items | 5+ items per retro | None get done; team experiences learned helplessness |
| No owners | "We should..." / "The team will..." | Nobody is accountable; items evaporate between sprints |
| No success criteria | "Improve X" | Cannot evaluate whether the action worked at next retro |
| No timeline | Open-ended commitments | Items drift indefinitely with no urgency |
| Same complaints every sprint | "Deploys are still slow" (sprint after sprint) | Indicates actions are not being followed through or root cause is not addressed |
