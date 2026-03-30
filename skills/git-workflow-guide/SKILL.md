---
name: git-workflow-guide
description: Git workflow reference covering branch naming, commit message conventions, PR templates, merge strategies, and common operations — for consistent team collaboration.
metadata:
  displayName: "Git Workflow Guide"
  categories: ["engineering"]
  tags: ["git", "version-control", "workflow", "pull-requests", "branching"]
  worksWellWithAgents: ["engineering-manager", "git-specialist", "tech-lead"]
  worksWellWithSkills: ["code-review-checklist", "open-source-contributing-guide", "release-checklist"]
---

# Git Workflow Guide

## Before you start

Confirm the following for the project:

1. **What is the branching model?** — Trunk-based, GitFlow, or GitHub Flow
2. **What is the main branch name?** — `main` or `master`
3. **Are there branch protection rules?** — Required reviews, CI checks, linear history
4. **What is the merge strategy?** — Squash, rebase, or merge commit
5. **Is there a commit message convention?** — Conventional Commits, Angular, or custom

If these are not documented, ask the team lead before establishing your own pattern. Inconsistency in git workflows creates merge conflicts and confusion.

## Branch naming

Use this format:

```
<type>/<ticket-id>-<short-description>
```

Types:
- `feat/` — New feature
- `fix/` — Bug fix
- `refactor/` — Code restructuring without behavior change
- `docs/` — Documentation only
- `test/` — Adding or updating tests
- `chore/` — Build, CI, dependency updates

Examples:
```
feat/PROJ-123-add-user-search
fix/PROJ-456-null-check-login
refactor/PROJ-789-extract-auth-module
chore/update-eslint-config
```

Rules:
- Lowercase only
- Hyphens between words, not underscores
- Include ticket ID when one exists
- Keep the description under 5 words
- Delete branches after merging

## Commit messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type (required)

`feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`, `style`

### Scope (optional)

The module, component, or area affected: `auth`, `api`, `ui`, `db`, `ci`

### Subject (required)

- Imperative mood: "add" not "added" or "adds"
- Lowercase first letter
- No period at the end
- Max 72 characters

### Examples

```
feat(auth): add password reset flow         ← feature with scope
fix(api): handle null user ID in session    ← bug fix with scope
chore: update TypeScript to 5.4             ← chore, no scope needed
refactor(db): extract query builder module  ← refactor with scope
```

Add a body for non-trivial changes explaining WHY, not HOW. Reference tickets in the footer: `Closes #234`.

## Pull request template

Use this structure for PR descriptions:

```markdown
## What
[1-2 sentences: what this PR does]

## Why
[Why this change is needed — link to ticket]

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing performed

## Notes for reviewers
[Anything the reviewer should pay attention to]
```

## Merge strategies

| Strategy | When to use | Command |
|----------|------------|---------|
| **Squash merge** | Messy branch history, want clean main | `git merge --squash branch` then commit |
| **Rebase merge** | Each commit is meaningful and clean | `git rebase main` then `git merge --ff-only` |
| **Merge commit** | Long-lived branches, need diverge/converge history | `git merge --no-ff branch` |

Squash is the safest default for feature branches. Use rebase when commits are well-structured. Use merge commits for release branches.

## Key operations

```bash
# Sync branch with main (use --force-with-lease, never --force)
git checkout main && git pull && git checkout feat/my-branch && git rebase main

# Undo last commit, keep changes
git reset --soft HEAD~1

# Stash work in progress
git stash push -m "description"
```

## Quality checklist

Before opening a PR, verify:

- [ ] Branch name follows the naming convention
- [ ] Commits are meaningful — no WIP, fixup, or "oops" messages left
- [ ] PR description follows the template with What/Why/Testing/Notes
- [ ] Branch is rebased on the latest main (no unnecessary merge commits)
- [ ] CI passes on the branch
- [ ] The diff contains only changes related to the stated purpose

## Common mistakes

- **Committing to main directly.** Always work on a branch, even for small changes. Direct commits bypass review and CI.
- **Writing vague commit messages.** "Fix bug" and "Update code" tell reviewers nothing. State what changed and why.
- **Using force push on shared branches.** Force push overwrites remote history. Use `--force-with-lease` and never force push to main.
- **Letting branches go stale.** Rebase on main regularly. A branch that diverges for weeks will have painful merge conflicts.
- **Including unrelated changes in a PR.** One PR should do one thing. Refactoring plus a bug fix plus a new feature in one PR is unreviewable.
- **Not deleting merged branches.** Stale branches clutter the repository. Delete branches after they are merged.
