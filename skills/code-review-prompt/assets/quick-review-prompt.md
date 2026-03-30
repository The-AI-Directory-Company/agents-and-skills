# Quick Code Review Prompt Template

Ready-to-use AI prompt for reviewing small-to-medium code changes. Fill in the bracketed slots, paste the diff, and submit.

---

## The Prompt

```
Review this code change.

## Context
- **What changed**: [ONE SENTENCE — e.g., "Added email validation to the signup form"]
- **Why**: [TICKET/REASON — e.g., "Users were submitting invalid emails causing bounce-backs (PROJ-1234)"]
- **What must NOT change**: [PRESERVED BEHAVIOR — e.g., "Existing users with already-stored emails must not be affected"]

## Review focus
1. Correctness — does the code do what the description says?
2. Safety — any security issues, null access, data integrity risks, or unhandled errors?
3. Edge cases — what inputs or conditions would break this?
4. Missing pieces — is there validation, error handling, or a test that should exist but does not?

## Output format
For each issue found, respond with:
- **Severity**: BLOCK (must fix) / WARN (should fix) / NOTE (optional)
- **Location**: file:line
- **What**: what is wrong
- **Why**: why it matters
- **Fix**: specific suggestion

If no issues are found, say "No issues found" — do not invent problems to appear thorough.

End with a one-line summary:
- "Approve" — no issues
- "Approve with notes" — only NOTE/WARN items, no blockers
- "Request changes" — BLOCK items exist, list them

## The diff

[PASTE YOUR DIFF OR CODE HERE]
```

---

## Slot Reference

| Slot | Required | Example |
|------|----------|---------|
| `[ONE SENTENCE]` | Yes | "Refactored the payment retry logic to use exponential backoff" |
| `[TICKET/REASON]` | Yes | "BUG-892: Payment retries were happening too fast, causing rate limiting" |
| `[PRESERVED BEHAVIOR]` | Recommended | "Successful first-attempt payments must still process identically" |
| `[PASTE YOUR DIFF OR CODE HERE]` | Yes | The actual `git diff` output or file contents |

## Tips for Better Results

- **Include the diff, not a description of the diff.** "I changed the retry logic" is vague. The actual diff is specific.
- **State what must NOT change.** This focuses the review on regressions, which are the most valuable thing to catch.
- **Keep the scope tight.** If you are reviewing 500 lines, use the full code-review-checklist skill instead.
- **Provide file paths.** If the diff does not include paths, add them — `src/payments/retry.ts` gives the reviewer context about the module.
