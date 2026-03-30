# Assumptions Table Template

Every number in a financial model must trace to a named assumption. This table is the single source of truth for all inputs. If a number does not appear here, it should not appear in the model.

---

## Rules

1. **Every assumption gets a row.** No burying assumptions inside formulas or footnotes.
2. **Source is required.** "Gut feel" is not a source. If the best you have is an estimate, write "Team estimate -- needs validation" and mark confidence as Low.
3. **Confidence drives sensitivity analysis.** Any assumption marked Low confidence must appear in scenario analysis. Medium confidence assumptions should appear in at least one scenario variant.
4. **Review quarterly.** Assumptions drift. Schedule a review every quarter to update values and re-assess confidence levels.
5. **Version the table.** When assumptions change, note the date and prior value so readers can track what shifted.

---

## Assumptions Table

| # | Assumption | Value | Unit | Source | Confidence | Last Updated | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Monthly revenue growth rate | | % | | High / Medium / Low | YYYY-MM-DD | |
| 2 | Monthly churn rate | | % | | High / Medium / Low | YYYY-MM-DD | |
| 3 | Average revenue per user (ARPU) | | $/month | | High / Medium / Low | YYYY-MM-DD | |
| 4 | Customer acquisition cost (CAC) | | $ | | High / Medium / Low | YYYY-MM-DD | |
| 5 | Gross margin | | % | | High / Medium / Low | YYYY-MM-DD | |
| 6 | Starting headcount | | people | | High / Medium / Low | YYYY-MM-DD | |
| 7 | Average fully-loaded salary | | $/year | | High / Medium / Low | YYYY-MM-DD | |
| 8 | Hiring pace | | hires/quarter | | High / Medium / Low | YYYY-MM-DD | |
| 9 | Infrastructure cost per customer | | $/month | | High / Medium / Low | YYYY-MM-DD | |
| 10 | Sales cycle length | | days | | High / Medium / Low | YYYY-MM-DD | |
| 11 | Conversion rate (trial to paid) | | % | | High / Medium / Low | YYYY-MM-DD | |
| 12 | Annual contract value (ACV) | | $/year | | High / Medium / Low | YYYY-MM-DD | |
| 13 | Net revenue retention (NRR) | | % | | High / Medium / Low | YYYY-MM-DD | |
| 14 | Monthly operating expenses (non-headcount) | | $/month | | High / Medium / Low | YYYY-MM-DD | |
| 15 | | | | | High / Medium / Low | YYYY-MM-DD | |
| 16 | | | | | High / Medium / Low | YYYY-MM-DD | |

---

## Confidence Definitions

| Level | Definition | Action Required |
|---|---|---|
| **High** | Based on 6+ months of historical data or verified external benchmarks | Use as-is in base case |
| **Medium** | Based on limited data (1-5 months), industry reports, or comparable companies | Include in at least one scenario variant |
| **Low** | Team estimate, early-stage guess, or single data point | Must appear in sensitivity analysis; flag for validation |

---

## Change Log

| Date | Assumption # | Previous Value | New Value | Reason |
|---|---|---|---|---|
| YYYY-MM-DD | | | | |
| YYYY-MM-DD | | | | |
