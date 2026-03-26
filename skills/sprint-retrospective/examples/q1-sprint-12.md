# Sprint Retrospective: Sprint 12

- **Sprint dates**: February 24 – March 7, 2026
- **Team**: Payments squad — @alex (tech lead), @maria, @chris, @priya, @lin
- **Facilitator**: @maria
- **Format**: Start/Stop/Continue
- **Sprint goal**: "Merchants can process refunds through the dashboard without contacting support"
- **Goal status**: Partially met — refund processing works, but the confirmation email is not yet sending

---

## Previous Action Items Review

| Action Item | Owner | Status | Result |
|------------|-------|--------|--------|
| Add deploy smoke tests for payments service | @chris | Completed | Smoke tests caught a breaking config change in this sprint — prevented a production incident |
| Document the settlement reconciliation process | @alex | In Progress | Draft written, pending review from finance team |
| Reduce staging environment spin-up time from 12 min to under 5 min | @lin | Not Started | Deprioritized due to refund feature deadline pressure |

**Note**: 1 of 3 items completed. The team discussed whether this indicates overcommitment. Consensus: the staging spin-up item was knowingly deprioritized for the sprint goal, which is acceptable. The documentation item needs a deadline.

---

## Data Gathering

### Start

- Start pairing on complex database migration work — @maria and @chris both spent time debugging the same refund state machine issue independently before realizing it
- Start writing ADRs for payment flow decisions — we made 3 architectural choices this sprint with no written rationale
- Start including QA in sprint planning — @priya found acceptance criteria gaps on day 3 that could have been caught in planning

### Stop

- Stop deploying after 3pm on Fridays — the refund endpoint deploy at 4:15pm last Friday caused an alert at 5:30pm that @alex had to handle over the weekend
- Stop carrying incomplete stories across sprints without re-estimating — the refund email story was "almost done" for 2 sprints and kept getting underestimated
- Stop using Slack DMs for technical decisions — @lin discovered on day 6 that @alex and @chris had agreed on a refund state model in DMs that contradicted the ticket

### Continue

- Continue the 15-minute deploy verification step after each release — caught 2 issues this sprint before users were affected
- Continue daily async standups in the team channel — worked well for the 3 days @priya was in a different timezone
- Continue dedicating 20% of capacity to tech debt — the Redis connection pooling fix from tech debt allocation eliminated the intermittent timeout errors

---

## Themes

**Theme 1: Knowledge silos and invisible decisions (7 votes)**
Three technical decisions were made in DMs or ad-hoc calls without documentation. Two engineers duplicated debugging effort. Information is not flowing to the full team.

**Theme 2: Late-sprint deploys creating weekend pressure (5 votes)**
Two of the last three sprints had Friday afternoon deploys that generated off-hours alerts. The team feels pressure to ship before sprint end, leading to risky timing.

**Theme 3: QA involvement too late (4 votes)**
Acceptance criteria gaps discovered mid-sprint cost an estimated 1.5 days of rework on the refund flow. Earlier QA input would have caught ambiguities.

---

## Experiments

### Experiment 1: Channel-first decisions

**Theme**: Knowledge silos and invisible decisions
**Hypothesis**: If we post all technical decisions to #payments-decisions (even small ones) before implementing, then the team will have shared context and reduce duplicate work, measured by zero instances of "I didn't know we decided that" in the next sprint.
**Experiment**: Any technical decision — API shape, state model, library choice — gets a 2-3 sentence post in #payments-decisions before code is written. Reactions count as acknowledgment.
**Owner**: @alex
**Duration**: 2 sprints
**Success criteria**: Zero surprises in sprint 13 and 14 standups; the team can describe current architectural decisions without checking DMs.

### Experiment 2: Deploy freeze after 2pm Friday

**Theme**: Late-sprint deploys creating weekend pressure
**Hypothesis**: If we institute a Friday 2pm deploy cutoff, then weekend on-call alerts from fresh deploys will drop to zero, measured by PagerDuty incident count on Saturdays.
**Experiment**: No production deploys after 2pm Friday. If a story isn't deployed by 2pm, it carries to Monday. CI/CD pipeline will post a reminder at 1pm.
**Owner**: @lin
**Duration**: 2 sprints
**Success criteria**: Zero weekend PagerDuty incidents caused by same-day deploys in sprints 13 and 14.

### Experiment 3: QA review of acceptance criteria in refinement

**Theme**: QA involvement too late
**Hypothesis**: If @priya reviews acceptance criteria during backlog refinement (2 days before planning), then mid-sprint AC rework will decrease, measured by tracking rework hours.
**Experiment**: @priya attends Wednesday refinement sessions and flags ambiguous or untestable acceptance criteria before stories enter the sprint.
**Owner**: @priya
**Duration**: 2 sprints
**Success criteria**: Zero stories require acceptance criteria changes after sprint planning in sprints 13 and 14.

---

## Action Items Carried Forward

| Action Item | Owner | Deadline |
|------------|-------|----------|
| Complete settlement reconciliation documentation | @alex | March 14, 2026 |
| Reduce staging spin-up time to under 5 min | @lin | March 28, 2026 |
