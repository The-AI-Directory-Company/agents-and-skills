---
name: bug-report-writing
description: Write actionable bug reports with precise reproduction steps, expected vs actual behavior, environment details, severity classification, and root cause analysis templates.
metadata:
  displayName: "Bug Report Writing"
  categories: ["engineering"]
  tags: ["bugs", "bug-reports", "reproduction", "debugging", "quality-assurance"]
  worksWellWithAgents: ["code-reviewer", "debugger", "qa-engineer", "support-engineer", "test-strategist"]
  worksWellWithSkills: ["code-review-checklist", "knowledge-base-article", "ticket-writing"]
---

# Bug Report Writing

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What broke?** — The specific behavior that is wrong (not "it doesn't work")
2. **Where?** — URL, screen, API endpoint, CLI command, or code path
3. **When did it start?** — First observed date, or the deploy/commit that introduced it
4. **Who is affected?** — All users, specific roles, certain browsers, percentage of requests
5. **How severe?** — Is there a workaround? Is data at risk? Is revenue impacted?

If the user says something vague like "search is broken," push back: "What did you search for, what did you expect to see, and what appeared instead?"

## Bug report template

### Title

Use the format: `[Component] Verb describing the failure — [trigger condition]`

**Good**: "[Checkout] Payment form submits twice when user double-clicks Pay button"
**Bad**: "Payment bug" or "Checkout issue" or "Double charge problem"

### Summary

2-3 sentences covering WHAT is broken, WHO it affects, and WHEN it started. Include impact metrics if available.

### Reproduction Steps

Write numbered steps that a developer with no context can follow to trigger the bug every time. Each step must describe exactly one action.

Precision rules:
- State exact inputs, not "enter some data"
- Include the starting state ("logged in as admin," "empty database," "feature flag X enabled")
- Note timing if relevant ("within 500ms," "after waiting 30 seconds")
- Specify the reproduction rate: always, intermittent (X/10 attempts), or one-time

### Expected vs Actual Behavior

State both explicitly. Never assume the reader knows what "correct" means.

```
Expected: Clicking Pay multiple times submits only one payment.
Actual: Each click submits an independent payment request. User is charged per click.
```

### Environment

Include every detail needed to reproduce: app version/commit, browser, OS, device, account type, feature flags, and API environment. The missing detail is always the one that matters.

### Severity Classification

Assign one level with justification:

| Severity | Definition | Response expectation |
|----------|-----------|---------------------|
| **Critical** | Data loss, security breach, complete feature outage, revenue loss | Drop everything. Fix or mitigate within hours. |
| **High** | Major feature degraded, no workaround, affects many users | Fix within the current sprint. |
| **Medium** | Feature partially broken, workaround exists, affects some users | Schedule in next 1-2 sprints. |
| **Low** | Cosmetic issue, minor inconvenience, affects few users | Backlog. Fix when convenient. |

Always include a justification, not just the label: "Critical — active revenue loss, no automated mitigation, requires manual refunds."

### Screenshots / Logs

Attach evidence: screenshots, screen recordings, log entries with timestamps, network request/response pairs, and verbatim error messages. Redact secrets, never diagnostics.

### Root Cause Analysis (post-investigation)

Fill this section after debugging. Leave it as a placeholder in the initial report. Cover three things:

- **Root cause**: The specific code path, configuration, or interaction that caused the failure
- **Fix**: What was changed and why it resolves the issue
- **Prevention**: What test, check, or safeguard will prevent recurrence

## Good vs bad examples

**Bad**: "The page is slow sometimes."
**Good**: "The /dashboard page takes 8-12 seconds to load for accounts with >500 projects. Query `SELECT * FROM projects WHERE account_id = ?` runs a full table scan (see EXPLAIN output attached). Accounts with <50 projects load in <1s."

**Bad**: "Login doesn't work on mobile."
**Good**: "[Auth] Login form fails to submit on iOS Safari 17 — keyboard 'Go' button does not trigger form submission. Tapping the Login button directly works. Affects all iOS Safari users. Workaround: tap the Login button instead of using keyboard submit."

## Quality checklist

Before submitting a bug report, verify:

- [ ] Title identifies the component, the failure, and the trigger
- [ ] Reproduction steps are numbered, specific, and independently followable
- [ ] Expected and actual behavior are both stated explicitly
- [ ] Environment section includes version, browser/OS, account type, and feature flags
- [ ] Severity is assigned with a justification, not just a label
- [ ] Screenshots or logs are attached as evidence, not just described
- [ ] No assumptions are embedded — every claim is backed by an observation

## Common mistakes

- **Combining multiple bugs in one report.** "Login is slow AND the forgot-password link is broken" is two bugs. File them separately so they can be triaged, assigned, and resolved independently.
- **Reproduction steps that require telepathy.** "Do the thing that causes the error" is not a step. Write steps so that someone who has never seen the product can reproduce the issue.
- **Skipping the expected behavior.** "It shows an error" means nothing without "It should show the user's dashboard." Developers cannot fix what they do not know is wrong.
- **Severity inflation.** Not every bug is critical. Mislabeling severity erodes trust and causes real critical bugs to be deprioritized. Use the definitions above honestly.
- **Redacting too much.** Removing the error message, stack trace, or request payload "for brevity" removes the information engineers need most. Redact secrets, not diagnostics.
