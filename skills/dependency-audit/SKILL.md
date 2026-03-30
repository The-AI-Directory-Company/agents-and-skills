---
name: dependency-audit
description: Audit project dependencies for security vulnerabilities, license compliance, outdated versions, and supply-chain risks. Produces a prioritized triage report with update recommendations and risk mitigation steps.
metadata:
  displayName: "Dependency Audit"
  categories: ["engineering", "security"]
  tags: ["dependencies", "security", "vulnerabilities", "license", "supply-chain", "npm", "audit"]
  worksWellWithAgents: ["dependency-manager", "devops-engineer", "security-auditor", "security-engineer"]
  worksWellWithSkills: ["compliance-assessment", "release-checklist", "threat-model-writing"]
---

# Dependency Audit

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What is the project?** — Repository path or URL
2. **What package manager?** — npm, yarn, pnpm, pip, cargo, go modules, maven, etc.
3. **What environment?** — Production app, internal tool, library published to a registry
4. **What is the license policy?** — Allowed licenses (e.g., MIT, Apache-2.0) and banned licenses (e.g., GPL-3.0 for proprietary projects)
5. **What is the risk tolerance?** — Zero critical vulns allowed, or acceptable thresholds per severity
6. **Is there a lockfile?** — Presence and freshness of `package-lock.json`, `yarn.lock`, `Cargo.lock`, etc.

## Audit procedure

### 1. Inventory Dependencies

Generate a complete dependency list with versions:

- **Direct dependencies**: Listed in the manifest file (package.json, requirements.txt, Cargo.toml)
- **Transitive dependencies**: Resolved from the lockfile — these are the majority of your attack surface
- **Dev-only dependencies**: Separate from production deps — lower risk but still relevant for CI supply-chain attacks

Record total counts: direct, transitive, dev-only. Flag projects with more than 500 transitive dependencies as high-complexity.

### 2. Security Vulnerability Scan

Run the ecosystem's built-in audit tool:

- npm/yarn/pnpm: `npm audit`, `yarn audit`, `pnpm audit`
- pip: `pip-audit` or `safety check`
- cargo: `cargo audit`
- go: `govulncheck ./...`

For each vulnerability found, record: package name, installed version, severity (critical/high/medium/low), CVE ID, fixed version, and whether the vulnerable code path is reachable.

### 3. License Compliance Check

Extract the license for every dependency (direct and transitive):

- Use `license-checker` (npm), `pip-licenses` (Python), `cargo-license` (Rust), or equivalent
- Flag any dependency with: no declared license, a copyleft license in a proprietary project, a license not on the approved list
- Check for license conflicts — e.g., combining LGPL and Apache-2.0 has specific requirements

Produce a license summary table: license type, count of packages, compliance status.

### 4. Outdated Version Analysis

Check how far behind each dependency is from its latest version:

- Run `npm outdated`, `pip list --outdated`, `cargo outdated`, or equivalent
- Classify each outdated package: patch behind (low risk), minor behind (medium), major behind (high, likely breaking changes)
- Flag dependencies that are unmaintained: no release in 12+ months, archived repository, or no response to open security issues

### 5. Supply-Chain Risk Assessment

Evaluate supply-chain risks for direct dependencies:

- **Maintainer count**: Single-maintainer packages are higher risk for abandonment or account compromise
- **Download/usage trends**: Sudden drops may indicate a fork or deprecation
- **Typosquatting**: Verify package names match the intended library — check for similar-named malicious packages
- **Install scripts**: Flag packages with `preinstall`/`postinstall` scripts that execute arbitrary code
- **Dependency depth**: Flag packages that pull in 50+ transitive dependencies for a simple task

### 6. Prioritized Triage Report

Rank all findings by severity and actionability:

| Priority | Finding | Category | Action | Effort |
|----------|---------|----------|--------|--------|
| P0 | lodash 4.17.15 — prototype pollution (CVE-2021-23337) | Security | Update to 4.17.21 | Low |
| P1 | colors 1.4.0 — maintainer sabotage incident | Supply-chain | Pin to 1.3.0 or replace | Medium |
| P2 | GPL-3.0 dep in proprietary project | License | Replace with MIT alternative | High |
| P3 | express 4.x — major version 5.x available | Outdated | Evaluate migration | High |

- **P0**: Critical/high security vulns with a fix available — update immediately
- **P1**: Supply-chain risks or license violations — address this sprint
- **P2**: High-severity outdated deps or medium vulns — schedule within the quarter
- **P3**: Minor version lag or low-severity findings — backlog

### 7. Remediation Steps

For each P0/P1 finding, provide specific remediation:

- Exact command to update (e.g., `npm install lodash@4.17.21`)
- Whether the update requires code changes (breaking API differences)
- If no fix exists: workaround, alternative package, or version pinning strategy
- For license issues: list 2-3 alternative packages with compatible licenses

## Quality checklist

Before delivering the audit report, verify:

- [ ] All direct and transitive dependencies are inventoried with version numbers
- [ ] Vulnerability scan ran against the lockfile, not just the manifest
- [ ] Every vulnerability includes CVE ID, severity, and fix version
- [ ] License compliance checked against the project's stated policy
- [ ] Outdated packages classified by how far behind they are
- [ ] Supply-chain risks assessed for at least all direct dependencies
- [ ] Findings are prioritized by severity and effort, not listed in discovery order
- [ ] P0/P1 items include specific remediation commands

## Common mistakes

- **Auditing the manifest without a lockfile.** The manifest says `^4.0.0` but the lockfile resolves to `4.0.1` which has a known vuln. Always audit the lockfile.
- **Ignoring transitive dependencies.** Most vulnerabilities are in transitive deps you never explicitly chose. The audit must cover the full dependency tree.
- **Treating all vulnerabilities equally.** A critical RCE in a production dependency is not the same as a low-severity ReDoS in a dev-only test helper. Triage by reachability and environment.
- **Skipping license checks.** A GPL-3.0 transitive dependency in a proprietary SaaS can create legal exposure. License compliance is not optional.
- **Updating everything at once.** Batch updates hide which change broke something. Update P0 items individually, run tests after each, then batch lower-priority updates.
- **Ignoring unmaintained packages.** A dependency with no commits in two years will not get security patches. Plan a replacement before the vulnerability arrives.
