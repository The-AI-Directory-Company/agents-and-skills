# Sprint Planning: Payments Team — Sprint 8

- **Sprint dates**: March 16 – March 27, 2026 (2-week sprint)
- **Team**: @alex (tech lead), @maria (backend), @chris (backend), @priya (QA), @lin (devops)
- **Previous sprint velocity**: 34 points (3-sprint average: 31 points)

---

## Capacity Calculation

| Team Member | Available Days | Focus Factor | Effective Days |
|-------------|---------------|-------------|----------------|
| @alex       | 10            | 0.7 (hiring interviews) | 7.0  |
| @maria      | 10            | 0.8         | 8.0            |
| @chris      | 8 (PTO Mar 26-27) | 0.8    | 6.4            |
| @priya      | 10            | 0.8         | 8.0            |
| @lin        | 10            | 0.6 (on-call + infra migration support) | 6.0 |
| **Total**   | **48**        |             | **35.4**       |

Effective capacity is ~88% of typical. Against a 31-point average velocity, plan for **27 points**.

---

## Sprint Goal

**Merchants can view and export their payout history for the last 12 months.**

This is achieved when:
1. The payout history API returns paginated results filtered by date range
2. The dashboard displays payout history with status, amount, and date
3. Merchants can export payout history as CSV
4. Error states (no payouts, failed exports) are handled gracefully

---

## Committed Stories

| ID | Title | Points | Owner | Dependencies |
|----|-------|--------|-------|-------------|
| PAY-401 | Build payout history API endpoint with date range filtering | 5 | @maria | None |
| PAY-402 | Add payout history table to merchant dashboard | 5 | @chris | PAY-401 (API contract only — can stub) |
| PAY-403 | Implement CSV export for payout history | 3 | @maria | PAY-401 |
| PAY-404 | Add pagination to payout history API and UI | 3 | @chris | PAY-401, PAY-402 |
| PAY-405 | Write integration tests for payout history flow | 3 | @priya | PAY-401, PAY-402 |
| PAY-390 | *Carryover*: Fix settlement rounding error on multi-currency payouts | 2 | @alex | None |
| PAY-398 | *Tech debt*: Migrate payment webhook handler from Express callback to async/await | 3 | @alex | None |
| PAY-399 | *Bug*: Payout status webhook not retrying on 5xx from merchant endpoint | 3 | @lin | None |

**Total committed: 27 points** | Capacity: 27 points | 3-sprint velocity avg: 31 points

**Maintenance allocation**: 8 points (30%) — PAY-390, PAY-398, PAY-399. Above the 15-20% guideline due to the carryover bug and a high-severity webhook issue reported by a merchant last week.

---

## Sprint Backlog Notes

- PAY-401 and PAY-402 can start in parallel: @chris will develop against the agreed API contract (documented in PAY-401 ticket) while @maria builds the actual endpoint
- PAY-403 (CSV export) starts after PAY-401 is merged — estimated day 4
- PAY-390 is a carryover from sprint 7. @alex has the fix ready; it needs a code review and a test for the JPY/USD edge case
- PAY-399 was escalated by the Acme Corp merchant. @lin will prioritize this in the first 2 days

---

## Risks

| Risk | Impact on Sprint Goal | Mitigation | Owner |
|------|----------------------|------------|-------|
| Payout data model may need a migration for the date range index | Delays PAY-401 by 1-2 days if index backfill is slow on the 4M-row table | Run `EXPLAIN ANALYZE` on day 1; if full scan, add index concurrently and accept day 2 start for API work | @maria |
| @alex's hiring interviews may consume more than 30% capacity | Carryover bug (PAY-390) slips again | If interviews exceed 3 hours/day, @maria picks up PAY-390 review | @alex |
| Acme Corp may escalate the webhook issue (PAY-399) with additional requirements | Scope creep on the bug fix | @lin will fix the retry logic only; any new webhook features go to a separate ticket | @lin |

---

## What We're NOT Doing This Sprint

- Payout history filtering by status (planned for sprint 9)
- PDF export — CSV only for now
- Real-time payout notifications (separate epic, not started)
- Dashboard redesign — we're adding the table to the existing layout
