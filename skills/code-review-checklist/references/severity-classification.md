# Severity Classification Reference

Standalone reference for code review severity levels. Apply one label to every finding in a review. Using consistent severity labels eliminates ambiguity about what must be fixed before merge vs. what can be deferred.

## Severity Table

| Severity | Definition | Action Required | Merge Policy |
|----------|-----------|-----------------|--------------|
| **Blocker** | A defect that will cause incorrect behavior, data loss, security vulnerability, or production outage. The code is wrong, not just suboptimal. | Must fix before merge. No exceptions. | PR cannot merge with open Blockers. |
| **Major** | A significant issue that degrades quality, performance, or reliability but does not cause immediate breakage. A workaround or fallback may exist. | Should fix before merge. Author may push back with justification, but the default expectation is to fix. | PR should not merge with open Majors unless the author explicitly acknowledges and documents the risk. |
| **Minor** | A real issue that affects readability, maintainability, or follows a suboptimal pattern, but does not affect correctness or production behavior. | Fix or acknowledge. Author can defer with a brief explanation. | PR can merge with open Minors. |
| **Nit** | A stylistic preference, optional suggestion, or subjective improvement. Reasonable people would disagree on whether this is better. | Author decides. No discussion needed. | PR can always merge with open Nits. |

## Decision Criteria

Use this flowchart to classify a finding:

1. **Will this cause a bug, crash, data loss, or security flaw in production?** Yes -> **Blocker**
2. **Will this cause performance degradation, missing validation, poor error handling, or reliability issues that could affect users?** Yes -> **Major**
3. **Is this a real code quality issue (naming, structure, duplication, readability) that makes future maintenance harder?** Yes -> **Minor**
4. **Is this a personal preference or style suggestion where both approaches are valid?** Yes -> **Nit**

## Examples by Severity

### Blocker Examples

- **SQL injection**: Query uses string concatenation with user input instead of parameterized statements.
- **Missing auth check**: New API endpoint has no authentication middleware — any unauthenticated user can access it.
- **Data loss**: `DELETE` operation has no WHERE clause filter, or a migration drops a column without data preservation.
- **Race condition**: Two concurrent requests can both read-modify-write the same row, causing lost updates.
- **Null pointer**: Function accesses `.property` on a value that can be `null` or `undefined` without a guard.
- **Wrong comparison**: `if (status = 'active')` (assignment instead of comparison).

### Major Examples

- **N+1 query**: Loop issues one database query per item. Works in dev with 10 items, will time out in production with 10,000.
- **Missing input validation**: API accepts a `quantity` field but does not check if it is negative or exceeds stock limits.
- **Generic error handling**: `catch (e) { return res.status(500).send('Error') }` swallows the actual error, making debugging impossible.
- **Missing index**: Query filters on a column that has no database index. Full table scan on a table expected to grow large.
- **No timeout**: External HTTP call has no timeout configured, risking hung requests that consume connection pool.
- **Missing rate limiting**: Public-facing endpoint has no rate limiting, allowing abuse.

### Minor Examples

- **Poor naming**: Function called `processData` when it specifically validates and normalizes shipping addresses.
- **Magic number**: `if (retries > 3)` — the `3` should be a named constant like `MAX_RETRIES`.
- **Dead code**: Commented-out block of 20 lines from a previous approach that was abandoned.
- **Missing JSDoc**: Public API function has no documentation for its parameters or return value.
- **Large function**: 80-line function that does input validation, business logic, and response formatting — could be split for readability.
- **Inconsistent pattern**: This module uses callbacks while the rest of the codebase uses async/await.

### Nit Examples

- **Variable naming style**: `userData` vs `user` — both are clear, the reviewer just prefers the shorter name.
- **Ternary vs. if-else**: `const label = isActive ? 'Active' : 'Inactive'` vs. an if-else block. Both readable.
- **Import ordering**: Imports are not grouped by external/internal. Works fine, but the reviewer prefers grouping.
- **Early return preference**: Reviewer would invert the condition and return early. Current nesting is fine.
- **Comment phrasing**: "Calculate the total" could be "Compute the sum of line item prices." Both communicate the intent.

## Anti-Patterns in Severity Classification

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Everything is a Blocker | Author feels attacked, stops reading feedback | Reserve Blocker for genuine defects. If you find 10 Blockers, re-examine — some are probably Majors or Minors. |
| No labels at all | Author cannot tell what to prioritize | Label every comment. Even "Nit:" takes 4 characters and saves a round-trip conversation. |
| Blocking on Nits | PR waits days for a variable rename | Approve with Nits. Use the "Approve with comments" state in your review tool. |
| Inconsistent severity | Same type of issue (e.g., missing null check) classified as Blocker in one place and Minor in another | Define once, apply uniformly. If a null check is a Blocker on line 42, it is a Blocker on line 87. |
| Severity inflation to get attention | Labeling a naming preference as Major to force a change | This erodes trust. If you feel strongly about a Minor, explain why it matters — do not inflate the label. |
