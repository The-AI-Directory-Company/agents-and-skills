# Contributing to @fastform/core

Thank you for your interest in contributing to fastform, a TypeScript form validation library. This guide covers everything you need to get started.

## Ways to Contribute

- **Report bugs** — File an issue with a minimal reproduction
- **Fix bugs** — Issues labeled `good first issue` are a great starting point
- **Add features** — Open an issue to discuss before writing code
- **Improve docs** — Fix typos, add examples, clarify API descriptions
- **Write tests** — Increase coverage or add edge case tests
- **Review PRs** — Constructive feedback is always welcome

Before starting, read our [Code of Conduct](CODE_OF_CONDUCT.md) and check [open issues](https://github.com/fastform/core/issues) to avoid duplicate work.

## Development Setup

**Prerequisites**: Node.js 20+, pnpm 9+

```bash
# 1. Fork and clone
git clone https://github.com/<your-username>/core.git
cd core

# 2. Install dependencies
pnpm install

# 3. Build the library
pnpm build

# 4. Run the test suite to verify setup
pnpm test
```

**Troubleshooting**

| Error | Fix |
|-------|-----|
| `ERR_PNPM_NO_MATCHING_VERSION` | Ensure you are on Node 20+: `node -v` |
| `vitest: command not found` | Run `pnpm install` again — dev dependencies may not have installed |
| Type errors after pulling latest | Run `pnpm build` to regenerate type declarations |

## Code Standards

```
Automated (CI enforces):
- Linting:       ESLint — run `pnpm lint` locally
- Formatting:    Prettier — run `pnpm format` to auto-fix
- Type checking: tsc --noEmit — run `pnpm typecheck`
- Tests:         Vitest — run `pnpm test`
```

**Commit messages** follow Conventional Commits: `<type>(<scope>): <description>`

- `feat(validators): add minLength validator for arrays`
- `fix(core): handle undefined field values in nested schemas`
- `docs(readme): add usage example for async validation`

## Pull Request Process

Before opening a PR:
- Branch is up to date with `main`
- All checks pass: `pnpm lint && pnpm typecheck && pnpm test`
- Tests added for new functionality
- API docs updated if public API changed (`docs/api.md`)

**PR size guide**: Under 200 lines gets reviewed fastest. Over 500 lines — open an issue to discuss breaking it up.

**Review process**: 1 maintainer approval required. CI must pass. Reviews happen within 5 business days. If you have not heard back after 5 days, comment on the PR to bump it.

## Issue Templates

**Bug reports** must include:
- fastform version and Node.js version
- Minimal code snippet reproducing the issue
- Expected vs. actual behavior
- Error message or stack trace if applicable

**Feature requests** must include:
- The problem you are trying to solve (not just the solution)
- A proposed API or usage example
- Alternatives you considered

## Issue Labels

| Label | Meaning |
|-------|---------|
| `good first issue` | Scoped for new contributors, includes guidance in the description |
| `help wanted` | Maintainers welcome outside contributions on this |
| `bug` | Confirmed defect |
| `enhancement` | Approved feature request |
| `needs triage` | Not yet reviewed by a maintainer |

## Community

- **GitHub Issues** — Bug reports, feature requests, and design discussions
- **GitHub Discussions** — Questions, ideas, and show-and-tell (response within 3 business days)
- **Discord** — `#fastform` channel for real-time help (best-effort, not guaranteed)

Contributors are recognized in the release notes and on the [Contributors page](https://fastform.dev/contributors).
