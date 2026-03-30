---
name: code-review-checklist
description: Systematic code review checklist covering correctness, security, performance, maintainability, and testing — with severity-based prioritization and actionable feedback templates.
metadata:
  displayName: "Code Review Checklist"
  categories: ["engineering"]
  tags: ["code-review", "checklist", "security", "quality", "pull-requests"]
  worksWellWithAgents: ["api-developer", "autonomous-coding-agent", "code-generator", "code-migrator", "frontend-engineer"]
  worksWellWithSkills: ["ai-prompt-writing", "bug-report-writing", "code-review-prompt", "open-source-contributing-guide", "ticket-writing"]
---

# Code Review Checklist

## Before you start

Gather the following from the reviewer or PR author. If anything is missing, ask before proceeding:

1. **What does the PR do?** — The specific change, not "fixes stuff"
2. **Why is it needed?** — Link to ticket, bug report, or requirement
3. **What is the blast radius?** — Which systems, APIs, or users are affected
4. **Are there tests?** — New, modified, or explicitly skipped (with justification)
5. **Is there a deploy plan?** — Feature flag, migration, rollback strategy

## Review template

### 1. First Pass: Understand Intent

Read the PR description and linked ticket before touching code. Answer:

- What is the expected behavior change?
- What should NOT change?
- Are there edge cases called out by the author?

If the PR description is empty or vague, stop and request one. Reviewing code without context produces shallow feedback.

### 2. Correctness

Check each item:

- [ ] Logic matches the stated requirement — not just "runs without errors"
- [ ] Edge cases are handled: empty inputs, null values, boundary conditions, concurrent access
- [ ] Error paths return meaningful messages, not silent failures or generic 500s
- [ ] State mutations are atomic where required — no partial updates on failure
- [ ] Data types are correct: string vs number, nullable vs required, timezone-aware dates

### 3. Security

- [ ] User input is validated and sanitized before use
- [ ] Authentication and authorization checks are present on new endpoints
- [ ] Secrets are not hardcoded or logged — check for API keys, tokens, passwords
- [ ] SQL queries use parameterized statements, not string concatenation
- [ ] File uploads validate type, size, and content — not just extension
- [ ] CORS, CSP, and rate limiting are configured for new routes

### 4. Performance

- [ ] Database queries use indexes — check for full table scans on large tables
- [ ] N+1 queries are eliminated — look for loops that issue individual queries
- [ ] Large datasets are paginated, not loaded entirely into memory
- [ ] Expensive computations are cached or debounced where appropriate
- [ ] New API endpoints have timeout and retry policies defined

### 5. Maintainability

- [ ] Names describe intent: `calculateTotalPrice` not `doStuff` or `handleData`
- [ ] Functions do one thing — if a function has "and" in its description, split it
- [ ] Magic numbers and strings are extracted to named constants
- [ ] Complex logic has comments explaining WHY, not WHAT
- [ ] Dead code, commented-out blocks, and TODO-without-tickets are removed

### 6. Testing

- [ ] Happy path is covered with assertions on expected output
- [ ] Failure modes are tested: invalid input, network errors, timeout, auth failures
- [ ] Tests are deterministic — no reliance on wall clock, random data, or external services
- [ ] Test names describe the scenario and expected outcome
- [ ] Mocks are minimal — over-mocking hides integration bugs

### 7. Compatibility and Deployment

- [ ] Database migrations are backward-compatible (no column drops without migration plan)
- [ ] API changes are versioned or backward-compatible
- [ ] Feature flags gate incomplete or risky functionality
- [ ] Environment-specific configuration is externalized, not hardcoded

## Severity classification for findings

Classify every finding. Mixed-severity comments without labels waste the author's time.

| Severity | Meaning | Action required |
|----------|---------|----------------|
| **Blocker** | Bug, security flaw, or data loss risk | Must fix before merge |
| **Major** | Performance issue, missing validation, poor error handling | Should fix before merge |
| **Minor** | Style, naming, minor readability improvement | Fix or acknowledge |
| **Nit** | Preference, optional suggestion | Author decides |

## Feedback templates

Use these formats to keep comments actionable:

**Blocker**: "This query has no auth check. An unauthenticated user can access other users' data via `GET /api/users/:id`. Add the `requireAuth` middleware before this handler."

**Major**: "This loop issues one query per item (N+1). For 500 items, that is 500 queries. Consider using `WHERE id IN (...)` with a single batch query."

**Minor**: "`processData` does not describe what this function does. Consider `validateAndNormalizeAddress` to match the actual behavior."

**Nit**: "Personal preference: I would extract this ternary into a named variable for readability. Up to you."

## Quality checklist

Before submitting your review, verify:

- [ ] Every comment has a severity label (Blocker, Major, Minor, Nit)
- [ ] Blockers include a specific fix suggestion, not just "this is wrong"
- [ ] You reviewed the test changes, not just the implementation
- [ ] You checked for what is MISSING, not just what is present
- [ ] You verified the PR does not introduce regressions in existing behavior
- [ ] Your feedback is directed at the code, not the person

## Common mistakes

- **Reviewing style instead of substance.** Nitpicking formatting while missing a SQL injection is a failed review. Check correctness and security first, style last.
- **Approving without understanding.** If you cannot explain what the PR does, you cannot verify it is correct. Ask questions instead of rubber-stamping.
- **Giving vague feedback.** "This could be better" is not actionable. State what is wrong, why it matters, and how to fix it.
- **Ignoring the test diff.** Tests that do not assert meaningful behavior give false confidence. Verify test quality, not just test existence.
- **Blocking on nits.** Holding up a PR for variable naming while a production bug waits is poor prioritization. Approve with nits when blockers are absent.
- **Skipping the "what is missing" check.** The most dangerous bugs are in the code that was never written: missing validation, missing error handling, missing auth checks.
