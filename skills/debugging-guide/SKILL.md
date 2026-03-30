---
name: debugging-guide
description: Step-by-step debugging methodology for systematic bug finding — covers reproduction, isolation, hypothesis testing, root cause analysis, and fix verification.
metadata:
  displayName: "Debugging Guide"
  categories: ["engineering"]
  tags: ["debugging", "troubleshooting", "bug-fixing", "methodology"]
  worksWellWithAgents: ["debugger", "qa-engineer", "sre-engineer"]
  worksWellWithSkills: ["bug-report-writing", "incident-postmortem", "test-plan-writing"]
---

# Debugging Guide

## Before you start

Gather the following before investigating:

1. **What is the expected behavior?** — What should happen
2. **What is the actual behavior?** — What happens instead (exact error message, wrong output, crash)
3. **When did it start?** — Was it always broken, or did it work before a specific change?
4. **What changed recently?** — Deployments, config changes, dependency updates, data migrations
5. **Who is affected?** — All users, specific accounts, specific environments
6. **Can you reproduce it?** — Consistent or intermittent? Steps to trigger?

Do not start guessing at fixes until you can reproduce the bug or have clear evidence of the root cause.

## Procedure

### 1. Reproduce the bug

Before anything else, make the bug happen on demand.

- Follow the exact steps from the bug report
- Use the same environment (OS, browser, API version) as the reporter
- If the bug is intermittent, identify the conditions that increase its likelihood (load, timing, specific data)
- If you cannot reproduce it, gather more data — logs, screenshots, network traces — before proceeding

A bug you cannot reproduce is a bug you cannot verify as fixed.

### 2. Isolate the scope

Narrow down where the bug lives:

- **Layer**: Is it frontend, backend, database, infrastructure, or third-party?
- **Component**: Which module, service, or function?
- **Input**: Which specific inputs trigger the bug? Which inputs do NOT trigger it?

Techniques for isolation:
- **Binary search**: Comment out or bypass half the code path. Does the bug persist? Narrow to the half that matters.
- **Minimal reproduction**: Strip away everything unrelated until you have the smallest code/input that triggers the bug.
- **Environment comparison**: Does it happen in staging but not local? Diff the configs.
- **Git bisect**: If it worked before, use `git bisect` to find the exact commit that introduced it.

### 3. Form a hypothesis

State your hypothesis explicitly before testing it:

```
HYPOTHESIS: [what you think is wrong]
EVIDENCE: [what makes you think so]
TEST: [how to confirm or disprove it]
PREDICTION: [what you expect to see if the hypothesis is correct]
```

One hypothesis at a time. If you test multiple changes simultaneously, you will not know which one mattered.

### 4. Test the hypothesis

Run the test you defined. Compare the result to your prediction.

- **Prediction matches** — Your hypothesis is likely correct. Proceed to fix.
- **Prediction does not match** — Your hypothesis is wrong. Do not force it. Return to step 2 with new information.
- **Partial match** — There may be multiple contributing factors. Isolate further.

### 5. Find the root cause

The first fix that makes symptoms disappear is not necessarily the root cause. Ask:

- **Why** does this input cause this behavior? (not just "what" happens)
- Is this a symptom of a deeper issue? (fixing the symptom may leave the real bug)
- Are there other code paths with the same underlying flaw?

Use the "5 Whys" technique:
1. Why did the request fail? — The response was 500.
2. Why was it 500? — An unhandled null reference.
3. Why was the value null? — The database query returned no rows.
4. Why were there no rows? — The user ID was from a deleted account.
5. Why was a deleted account ID used? — The session was not invalidated on deletion.

Root cause: sessions are not invalidated when accounts are deleted.

### 6. Implement and verify the fix

1. Write a test that reproduces the bug (it should fail before the fix)
2. Apply the minimal fix — change the least amount of code possible
3. Run the reproduction test — it should pass now
4. Run the full test suite — no regressions
5. Check related code paths for the same pattern

### 7. Document the finding

Record for future reference:

```
BUG: [one-line summary]
ROOT CAUSE: [what was actually wrong]
FIX: [what was changed]
RELATED: [other areas that might have the same issue]
PREVENTION: [what would have caught this earlier — test, lint rule, type constraint]
```

## Quality checklist

- [ ] The bug is reproducible with a defined set of steps
- [ ] The root cause is identified, not just the symptom
- [ ] A test exists that fails before the fix and passes after
- [ ] The fix changes the minimum necessary code
- [ ] Related code paths were checked for the same pattern
- [ ] The full test suite passes with no regressions
- [ ] The fix is documented with root cause and prevention notes

## Common mistakes

- **Fixing symptoms instead of root causes.** Adding a null check hides the bug — ask WHY the value is null in the first place.
- **Changing multiple things at once.** If you change three things and the bug disappears, you do not know which change fixed it. Change one thing at a time.
- **Skipping reproduction.** Fixing a bug you cannot reproduce means you cannot verify the fix works. Reproduce first, always.
- **Blaming the environment.** "It works on my machine" is not a diagnosis. If it fails in production, the difference between your machine and production IS the bug.
- **Stopping at the first fix that works.** The first fix may mask the real issue. Verify the root cause before declaring victory.
- **Not checking for related instances.** If a bug exists in one place, the same pattern likely exists elsewhere. Search the codebase for similar code.
