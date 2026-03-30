---
name: open-source-contributing-guide
description: Write open source contributing guides — with setup instructions, code standards, PR processes, issue templates, and community guidelines that lower the barrier for new contributors.
metadata:
  displayName: "Open Source Contributing Guide"
  categories: ["engineering", "communication"]
  tags: ["open-source", "contributing", "community", "pull-requests", "guidelines"]
  worksWellWithAgents: ["developer-advocate", "open-source-maintainer", "technical-writer"]
  worksWellWithSkills: ["api-design-guide", "code-review-checklist", "git-workflow-guide"]
---

# Open Source Contributing Guide

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What is the project?** (Name, language, framework, repo URL)
2. **What is the project's maturity?** (New, established with existing norms, large ecosystem)
3. **What contributions are welcome?** (Code, docs, tests, design, translations, triage)
4. **What is the tech stack?** (Languages, build tools, test frameworks, CI/CD)
5. **What is the governance model?** (Solo maintainer, core team, foundation-backed)
6. **What license does the project use?** (MIT, Apache 2.0, GPL, etc.)

If the user says "we just need a CONTRIBUTING.md," clarify: a contributing guide without working setup instructions and clear PR expectations creates frustrated contributors who never return.

## Contributing guide template

### 1. Welcome and Orientation

```markdown
# Contributing to [Project Name]

## Ways to Contribute

- **Report bugs** — File an issue with a reproduction case
- **Fix bugs** — Pick up issues labeled `good first issue` or `help wanted`
- **Add features** — Discuss in an issue before starting work
- **Improve docs** — Fix typos, add examples, clarify explanations
- **Write tests** — Increase coverage, add edge cases
- **Review PRs** — Constructive feedback on open pull requests

## Before You Start

1. Read our [Code of Conduct](CODE_OF_CONDUCT.md)
2. Check [existing issues](link) to avoid duplicate work
3. For features or large changes, open an issue first
```

Keep this section short. Contributors decide within 60 seconds whether to keep reading.

### 2. Development Setup

Write setup instructions that work on a fresh machine. Include prerequisites (language version, package manager), fork-and-clone steps, dependency installation, environment setup, and a command to run the test suite that verifies the setup works.

Include a troubleshooting table for known setup issues (common error messages with specific fixes). Every setup problem a contributor solves alone is a contributor who almost left.

### 3. Code Standards

Define standards that tooling enforces:

```
Automated Checks (CI enforces):
- Linting:      [linter] — run `[lint command]` locally
- Formatting:   [formatter] — run `[format command]` to auto-fix
- Type checking: [type checker] — run `[type check command]`
- Tests:        run `[test command]`
```

Specify commit message format (recommend Conventional Commits): `<type>(<scope>): <description>`. Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`. Include 2-3 concrete examples.

If a rule is important enough to write down, it is important enough to enforce with a linter or pre-commit hook.

### 4. Pull Request Process

```
Before opening a PR:
- [ ] Branch is up to date with `main`
- [ ] All tests pass locally
- [ ] Linting passes
- [ ] Tests added for new functionality
- [ ] Documentation updated if behavior changed

PR guidelines:
- One logical change per PR
- Include what changed, why, how to test, and link to related issue
- PR size guide: <100 lines (fast review), 100-500 (standard), 500+ (discuss first)

Review process:
- [N] maintainer approval(s) required
- CI must pass before merge
- Review within [X] business days
```

Set explicit review time expectations. Contributors who wait 3 weeks for a review do not come back.

### 5. Issue Guidelines

**Bug reports** must include: environment details, numbered reproduction steps, expected vs. actual behavior, and a minimal reproduction case.

**Feature requests** must include: problem statement (not solution), proposed approach, alternatives considered, and who benefits.

Define issue labels: `good first issue` (new contributors), `help wanted` (outside contributions welcome), `bug`, `enhancement`, `needs triage`.

### 6. Community

List communication channels (GitHub Issues, chat platform, forum/discussions) with expected response times. Document how contributors are recognized (contributors page, release notes).

## Quality checklist

- [ ] Setup instructions work on a fresh machine — tested, not assumed
- [ ] Every code standard is enforced by tooling or explicitly marked as convention
- [ ] PR process includes size guidelines and explicit review time commitments
- [ ] Issue templates cover bug reports and feature requests
- [ ] Communication channels listed with expected response times
- [ ] Written for someone who has never seen the codebase
- [ ] Troubleshooting section covers known setup pain points
- [ ] Guide links to the Code of Conduct

## Common mistakes

- **Setup that only works on the maintainer's machine.** Test on a fresh environment. "Works for me" loses contributors.
- **Unclear PR scope.** Without size guidelines, contributors submit 2,000-line PRs nobody can review.
- **No response time commitments.** Contributors who wait weeks for review do not return.
- **Code of Conduct without enforcement.** A CoC never referenced or enforced is performative.
- **Missing "good first issue" labels.** New contributors need well-scoped starter issues as entry points.
- **Writing for experts.** The guide is for newcomers. Avoid internal terminology and assumed context.
