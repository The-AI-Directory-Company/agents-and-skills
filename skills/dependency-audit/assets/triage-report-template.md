# Dependency Audit Triage Report

> **Project:** [project name]
> **Date:** [YYYY-MM-DD]
> **Auditor:** [name or AI agent]
> **Package manager:** [npm/yarn/pnpm/pip/cargo/go]
> **Lockfile present:** [yes/no — version date]

---

## Dependency Inventory

| Category | Count |
|----------|-------|
| Direct dependencies | |
| Dev dependencies | |
| Transitive dependencies | |
| **Total** | |

Complexity flag: Projects with >500 transitive dependencies are high-complexity and warrant ongoing monitoring.

---

## Priority Definitions

| Priority | Meaning | SLA | Examples |
|----------|---------|-----|---------|
| **P0 — Critical** | Actively exploitable vulnerability with a fix available, or a dependency with a known supply-chain compromise. Must be remediated before next deploy. | **Immediate** (same day) | Critical RCE in production dep, compromised maintainer account, malicious package version |
| **P1 — High** | High-severity vulnerability, license violation that creates legal exposure, or supply-chain risk requiring mitigation. | **This sprint** (1-2 weeks) | High-severity CVE with fix available, GPL dep in proprietary project, single-maintainer critical dep |
| **P2 — Moderate** | Medium-severity vulnerability, major version lag, or unmaintained dependency. No immediate exploit risk but creates technical debt. | **This quarter** | Medium CVE, dep 2+ major versions behind, no release in 12+ months, deprecated package |
| **P3 — Low** | Low-severity vulnerability, minor version lag, or informational finding. Acceptable risk — track and batch. | **Backlog** | Low-severity ReDoS in dev dep, minor version behind, license edge case in test-only dep |

---

## Findings

### P0 — Critical

| # | Package | Current | Fixed | Category | Finding | Remediation | Effort |
|---|---------|---------|-------|----------|---------|-------------|--------|
| 1 | `lodash` | 4.17.15 | 4.17.21 | Security | Prototype pollution — CVE-2021-23337 (CVSS 7.2). Reachable via `_.set()` in `src/utils/transform.ts`. | `npm install lodash@4.17.21` — no breaking changes | Low |
| 2 | `node-fetch` | 2.6.0 | 2.6.7 | Security | Header leak — CVE-2022-0235 (CVSS 8.8). Used in `src/lib/api-client.ts` for external API calls. | `npm install node-fetch@2.6.7` — no breaking changes | Low |

### P1 — High

| # | Package | Current | Fixed | Category | Finding | Remediation | Effort |
|---|---------|---------|-------|----------|---------|-------------|--------|
| 3 | `colors` | 1.4.0 | — | Supply-chain | Maintainer sabotage in v1.4.1 (infinite loop). Currently pinned to 1.4.0 but at risk. | Replace with `chalk` or `picocolors`. Used in 2 files. | Medium |
| 4 | `bcrypt` | 5.0.0 | — | License | Dual-licensed MIT/Apache-2.0 but native binding `node-pre-gyp` pulls in GPL-2.0 transitive dep. Proprietary project. | Switch to `bcryptjs` (pure JS, MIT). API-compatible drop-in. | Medium |

### P2 — Moderate

| # | Package | Current | Latest | Category | Finding | Remediation | Effort |
|---|---------|---------|--------|----------|---------|-------------|--------|
| 5 | `express` | 4.18.2 | 5.0.1 | Outdated | Major version behind. Express 5 drops callback-style error handling and changes `req.query` parsing. | Evaluate migration — test router compatibility. 12 route files affected. | High |
| 6 | `moment` | 2.29.4 | — | Unmaintained | In maintenance mode since 2020. 67KB gzipped. | Replace with `date-fns` or `dayjs`. Used in 8 files for date formatting. | High |
| 7 | `jsonwebtoken` | 8.5.1 | 9.0.2 | Security | CVE-2022-23529 (CVSS 6.4) — insecure default algorithm. Medium severity because auth middleware hardcodes `RS256`. | `npm install jsonwebtoken@9.0.2` — breaking: `decode()` returns null instead of throwing for invalid tokens. | Medium |

### P3 — Low

| # | Package | Current | Latest | Category | Finding | Remediation | Effort |
|---|---------|---------|--------|----------|---------|-------------|--------|
| 8 | `semver` | 7.5.0 | 7.6.0 | Outdated | Patch behind. No security issues. | Batch update with other minor deps. | Low |
| 9 | `@types/node` | 20.8.0 | 20.11.5 | Outdated | Type definitions behind. No runtime impact. | `npm install @types/node@latest` | Low |
| 10 | `eslint-plugin-import` | 2.28.0 | 2.29.1 | Outdated | Minor version behind. Dev-only dependency. | Batch update with other dev deps. | Low |

---

## License Summary

| License | Count | Status |
|---------|-------|--------|
| MIT | 342 | Approved |
| ISC | 87 | Approved |
| Apache-2.0 | 45 | Approved |
| BSD-2-Clause | 23 | Approved |
| BSD-3-Clause | 18 | Approved |
| 0BSD | 5 | Approved |
| MPL-2.0 | 2 | Needs review |
| GPL-2.0 | 1 | **Violation** (see P1 #4) |
| UNKNOWN | 1 | **Needs investigation** |

---

## Remediation Plan

### Immediate (before next deploy)
- [ ] P0 #1: Update lodash to 4.17.21
- [ ] P0 #2: Update node-fetch to 2.6.7
- [ ] Run tests after each update individually

### This sprint
- [ ] P1 #3: Replace `colors` with `picocolors`
- [ ] P1 #4: Replace `bcrypt` with `bcryptjs`, verify hash compatibility

### This quarter
- [ ] P2 #5: Spike on Express 5 migration (allocate 2-3 days)
- [ ] P2 #6: Replace `moment` with `date-fns` (allocate 1 day)
- [ ] P2 #7: Update `jsonwebtoken` to 9.x, update error handling in auth middleware

### Backlog
- [ ] P3 #8-10: Batch minor updates in a single PR
