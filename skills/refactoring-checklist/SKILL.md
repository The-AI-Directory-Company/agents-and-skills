---
name: refactoring-checklist
description: Safe refactoring procedures with pre/post verification — covering scope assessment, test coverage checks, incremental transformation, and regression prevention.
metadata:
  displayName: "Refactoring Checklist"
  categories: ["engineering"]
  tags: ["refactoring", "code-quality", "technical-debt", "safe-changes"]
  worksWellWithAgents: ["refactoring-agent", "software-architect", "tech-lead"]
  worksWellWithSkills: ["architecture-decision-record", "code-review-checklist", "test-plan-writing"]
---

# Refactoring Checklist

## Before you start

Gather the following before touching code:

1. **What are you refactoring?** — Specific file, module, function, or pattern
2. **Why?** — Performance, readability, removing duplication, enabling a new feature, reducing complexity
3. **What is the current test coverage?** — Run coverage report on the target code
4. **What depends on this code?** — Callers, importers, API consumers, downstream services
5. **What is the blast radius?** — If this breaks, who is affected?
6. **Is there a deadline?** — Refactoring without time pressure is safer. If rushed, reduce scope.

Do not refactor code you do not understand. Read it first, understand its intent and edge cases, then plan the change.

## Procedure

### 1. Verify test coverage before changing anything

Run the existing test suite against the target code:

```
COVERAGE BEFORE:
- Statements: [X%]
- Branches: [X%]
- Functions: [X%]
- Lines: [X%]
```

If coverage is below 80%, write tests for the existing behavior BEFORE refactoring. These tests are your safety net — they verify the refactoring does not change behavior.

Tests to add before refactoring:
- [ ] Happy path with typical inputs
- [ ] Edge cases: empty input, null, boundary values
- [ ] Error paths: what happens when things fail
- [ ] Integration points: verify interactions with dependencies

### 2. Define the target state

Write down what the code should look like AFTER refactoring:

```
CURRENT: [describe current structure]
TARGET: [describe target structure]
REASON: [why target is better — measurable if possible]
SCOPE: [exactly which files/functions change]
NOT CHANGING: [explicitly list what stays the same]
```

### 3. Make a refactoring plan

Break the refactoring into small, independently verifiable steps. Each step should:

- Be committable on its own
- Pass all tests after completion
- Not change external behavior

Common step sequences:

**Extract**: Identify code to extract -> Write tests for it -> Extract to new function/module -> Update callers -> Verify tests pass

**Rename**: Find all references -> Rename in one commit -> Verify no broken references -> Update documentation

**Simplify**: Identify the complexity -> Write tests covering all branches -> Simplify the logic -> Verify same behavior with simpler code

**Move**: Identify the new location -> Create the target file -> Move code -> Update all imports -> Verify nothing broke

### 4. Execute one step at a time

For each step in the plan:

1. Make the change
2. Run the full test suite
3. Review the diff — does it match your plan?
4. Commit with a message describing the refactoring step

Do NOT batch multiple refactoring steps into one commit. If something breaks, you need to know which step caused it.

### 5. Verify after completion

Run the full verification:

```
COVERAGE AFTER:
- Statements: [X%] (should be >= before)
- Branches: [X%]
- Functions: [X%]
- Lines: [X%]

BEHAVIOR CHECK:
- [ ] All existing tests pass
- [ ] No new warnings or errors in build
- [ ] No changes to public API signatures (unless intentional)
- [ ] Performance benchmarks are within tolerance (if applicable)
- [ ] Dependent services/consumers are unaffected
```

### 6. Clean up

After the refactoring is verified:

- [ ] Remove any temporary scaffolding or compatibility shims
- [ ] Delete dead code that the refactoring replaced
- [ ] Update documentation if public interfaces changed
- [ ] Update related comments that reference the old structure
- [ ] Notify consumers if any API changes were made

## Safe refactoring patterns

| Pattern | When to use | Risk level |
|---------|------------|------------|
| Rename variable/function | Name does not describe purpose | Low |
| Extract function | Block of code has a distinct responsibility | Low |
| Inline function | Function adds indirection without value | Low |
| Move to new file | File has too many responsibilities | Medium |
| Change function signature | Parameters are confusing or incomplete | Medium |
| Replace algorithm | Current implementation is incorrect or slow | High |
| Restructure module boundaries | Architecture needs to change | High |

For high-risk refactoring, consider using a feature flag or parallel implementation that can be toggled.

## Quality checklist

- [ ] Tests existed (or were written) BEFORE the refactoring started
- [ ] Each step was committed independently
- [ ] All tests pass after the refactoring
- [ ] Test coverage did not decrease
- [ ] No external behavior changed (unless that was the explicit goal)
- [ ] Dead code from the old implementation is removed
- [ ] The refactoring achieves the stated goal (measurably, if possible)

## Common mistakes

- **Refactoring without tests.** If there are no tests, you have no way to verify the refactoring is behavior-preserving. Write tests first.
- **Changing behavior during a refactoring.** Refactoring changes structure, not behavior. If you need to fix a bug, do it in a separate commit before or after the refactoring.
- **Making the PR too large.** A refactoring PR with 50 files changed is hard to review and risky to merge. Break it into smaller PRs that each pass tests independently.
- **Refactoring code you do not understand.** If you cannot explain what the code does and why, you cannot safely change it. Read and understand first.
- **Not checking callers.** Changing a function signature without updating all callers produces runtime errors that tests may not catch if coverage is incomplete.
- **Skipping the "why."** Refactoring without a clear reason leads to churn. If you cannot articulate why the new structure is better, the refactoring may not be worth the risk.
