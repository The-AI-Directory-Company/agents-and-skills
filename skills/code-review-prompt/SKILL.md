---
name: code-review-prompt
description: Lightweight quick code review template for fast feedback on small changes — covers correctness, safety, and readability in a single pass without full checklist overhead.
metadata:
  displayName: "Code Review Prompt"
  categories: ["engineering"]
  tags: ["code-review", "prompt-engineering", "ai-prompts", "quick-review"]
  worksWellWithAgents: ["code-reviewer", "frontend-engineer", "tech-lead"]
  worksWellWithSkills: ["bug-report-writing", "code-review-checklist"]
---

# Code Review Prompt

## Before you start

Gather the following before reviewing:

1. **What changed?** — The diff or file(s) to review
2. **Why did it change?** — Link to ticket, bug report, or one-sentence explanation
3. **What is the scope?** — Quick fix, new feature, refactor, or dependency update
4. **What should NOT change?** — Existing behavior that must be preserved

If the reviewer cannot explain what the change does in one sentence, the PR description is insufficient. Request clarification first.

## Procedure

### 1. Classify the change size

Pick the review depth based on scope:

| Change size | Lines changed | Review approach |
|-------------|---------------|-----------------|
| **Tiny** | 1-10 lines | Scan for correctness and typos. 2 minutes. |
| **Small** | 11-50 lines | Single-pass review. Check logic, errors, naming. 5 minutes. |
| **Medium** | 51-200 lines | Two-pass review. First pass for intent, second for details. 15 minutes. |
| **Large** | 200+ lines | Use the full code-review-checklist skill instead. |

This skill is optimized for tiny-to-medium changes. For large changes, switch to the full code-review-checklist.

### 2. First pass — intent and safety

Read the entire diff once. Answer these questions:

1. Does this change do what the description says it does?
2. Does it change anything it should NOT change?
3. Are there obvious security issues? (user input used unsanitized, secrets exposed, auth bypassed)
4. Are there obvious correctness issues? (off-by-one, null access, wrong comparison operator)

If any answer is concerning, stop and flag it before continuing.

### 3. Second pass — details

Go through the diff line by line:

- **Logic**: Does each conditional and loop behave correctly at boundaries?
- **Errors**: Are failure cases handled? Are error messages specific?
- **Naming**: Do variable and function names describe their purpose?
- **Duplication**: Is new code duplicating existing utilities?
- **Types**: Are types correct and specific? (no unnecessary `any` or `object`)

### 4. Write the review

Use this format for each finding:

```
[SEVERITY] file.ts:LINE — DESCRIPTION

What: [what is wrong]
Why: [why it matters]
Fix: [specific suggestion]
```

Severity labels:
- **BLOCK** — Must fix. Bug, security flaw, or data loss risk.
- **WARN** — Should fix. Missing validation, poor error handling, performance issue.
- **NOTE** — Optional. Naming, readability, minor improvement.

### 5. Summarize

End the review with a one-line summary:

- **Approve**: "Looks good. No issues found."
- **Approve with notes**: "Approve — 2 optional suggestions, no blockers."
- **Request changes**: "Blocking on [N] issues: [brief list]."

## Quick review prompt template

Use this template when asking an AI to review code:

```
Review this code change. The change [DESCRIPTION OF WHAT IT DOES].

Focus on:
1. Correctness — does it do what it claims?
2. Safety — any security, null access, or data issues?
3. Edge cases — what inputs would break this?

For each issue found, state:
- Severity (BLOCK / WARN / NOTE)
- File and line
- What is wrong and how to fix it

If no issues, say "No issues found" — do not invent problems.

[PASTE DIFF OR CODE HERE]
```

## Quality checklist

Before submitting your review, verify:

- [ ] Every finding has a severity label
- [ ] BLOCK findings include a specific fix, not just "this is wrong"
- [ ] You checked for what is MISSING, not just what is present
- [ ] You did not invent issues that do not exist — false positives waste trust
- [ ] Your review matches the change scope — do not audit the entire file for a one-line fix
- [ ] Feedback is about the code, not the person

## Common mistakes

- **Reviewing the entire file instead of the diff.** A quick review covers WHAT CHANGED. Auditing unchanged code belongs in a separate task.
- **Flagging style when there are bugs.** If you see a correctness issue and a naming issue, lead with the correctness issue. Style feedback on buggy code is noise.
- **Approving without understanding.** "LGTM" without reading the diff is not a review. If you cannot explain the change, you cannot verify it.
- **Inventing problems to seem thorough.** Flagging non-issues erodes trust and slows the team. If the code is correct and clear, say so.
- **Skipping the "what is missing" check.** The most dangerous issues are not in the code that was written — they are in the validation, error handling, or edge case that was never added.
- **Using this template for large changes.** This is a quick review tool. Changes over 200 lines need the full code-review-checklist with section-by-section analysis.
