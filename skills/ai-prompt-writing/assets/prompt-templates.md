# Prompt Templates

Three fill-in templates for common AI coding tasks, plus a quality checklist to run before sending any prompt.

---

## Template 1: Bug Fix

```
Fix this bug: [describe the symptom — what the user sees or what the test reports].

Reproduction steps:
1. [Step 1]
2. [Step 2]
3. [Expected: X. Actual: Y.]

The relevant code is in [file path(s)].

Root cause hypothesis: [your best guess, or "unknown"].

Constraints:
- Do not change the function signature or public API.
- Do not add new dependencies.
- [Any additional constraints specific to your project.]

Output: Only the modified function(s). Include a brief comment explaining the fix.
```

**When to use**: When you can reproduce the bug and want the AI to propose a targeted fix.

**Tips**:
- Include the error message or stack trace verbatim — do not paraphrase.
- If you have a hypothesis, state it. Even a wrong guess narrows the search space.
- Point to the specific file and function, not the entire codebase.

---

## Template 2: Code Review

```
Review this diff for:
- Correctness bugs (logic errors, off-by-one, null handling)
- Performance issues (unnecessary re-renders, O(n^2) patterns, missing indexes)
- Security concerns (injection, auth bypass, data leaks)
- Style violations against [project conventions or style guide reference]

For each issue found, report:
- File and line number
- Severity: critical / warning / nit
- What is wrong (1 sentence)
- A specific fix (code snippet or instruction)

Do not comment on things that are correct. Do not summarize the diff.

Diff:
[paste the diff, or reference the file paths if the tool can read them]
```

**When to use**: Before merging a PR, or when reviewing your own code before requesting human review.

**Tips**:
- Specify what categories to review. Without this, the AI covers everything shallowly instead of anything deeply.
- "Do not comment on things that are correct" prevents filler praise that buries real issues.
- Severity levels help you triage — not every nit needs to block a merge.

---

## Template 3: Refactoring

```
Refactor [function/component/module name] to [specific goal].

Goals:
- [e.g., Extract the data-fetching logic into a custom hook]
- [e.g., Reduce cyclomatic complexity below 10]
- [e.g., Split this 300-line component into 3 focused components]

Constraints:
- Preserve all existing behavior — the existing tests in [test file path] must pass without modification.
- Follow the pattern established in [reference file path].
- Do not rename exported symbols (other modules depend on them).
- Do not add new dependencies.

Output: Complete modified file(s). If multiple files are created, show each with its full path.
```

**When to use**: When you know what needs to change structurally but want the AI to handle the mechanical refactoring.

**Tips**:
- "Existing tests must pass" is the single most important constraint. It anchors the refactor to correct behavior.
- Reference an existing file that already follows the target pattern. One example communicates more than a paragraph of instructions.
- Be explicit about what should NOT change — AI tools are eager to "improve" things you did not ask about.

---

## 7-Step Prompt Quality Checklist

Run through this checklist before sending any prompt to an AI coding tool.

1. **Task first?** The prompt leads with what to do, before context and examples. The AI should know the goal by sentence two.

2. **At least 2 constraints?** The prompt includes specific boundaries: format, scope, style, exclusions, or dependencies. Each constraint eliminates a category of wrong output.

3. **Examples provided?** For pattern-based tasks, the prompt includes a concrete reference implementation — not a description of the pattern.

4. **Context scoped?** Only relevant files and information are included. No unrelated modules, no full codebase dumps.

5. **Output format specified?** The prompt states exactly how the result should be delivered: full file, diff, function only, list of changes, etc.

6. **Negatives stated?** The prompt includes at least one "do not" — what the AI should avoid changing, adding, or assuming.

7. **Tested and refined?** After the first attempt, you identified a specific gap, added a constraint, and re-ran. Most prompts need 2-3 iterations.

If fewer than 5 of 7 items are checked, revise the prompt before sending.
