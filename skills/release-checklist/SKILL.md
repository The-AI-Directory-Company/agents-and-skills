---
name: release-checklist
description: Create go/no-go release checklists with pre-deploy verification, staged rollout steps, monitoring checkpoints, rollback triggers, and stakeholder communication plans.
metadata:
  displayName: "Release Checklist"
  categories: ["operations", "engineering"]
  tags: ["release", "deployment", "checklist", "go-no-go", "rollout", "rollback"]
  worksWellWithAgents: ["devops-engineer", "open-source-maintainer", "product-operations", "release-manager"]
  worksWellWithSkills: ["runbook-writing", "ticket-writing"]
---

# Release Checklist

## Before you start

Gather the following from the user:

1. **What is being released?** (Service name, version, list of changes or link to changelog)
2. **What environments are involved?** (Staging, canary, production regions)
3. **What is the rollback strategy?** (Feature flags, blue-green, redeploy previous version)
4. **Who are the stakeholders?** (Engineering leads, product owners, support, on-call)
5. **What is the risk level?** (Database migrations, breaking API changes, new infrastructure)

If the user says "just make me a release checklist," push back: "For which release? I need the scope of changes, target environments, and rollback strategy to build a useful checklist."

## Release checklist template

### Pre-Release

#### Scope Inventory

List every change shipping in this release. For each item, note the owner, whether it is behind a feature flag, and whether it touches shared infrastructure or data schemas.

#### Risk Classification

Classify as **low**, **medium**, or **high** risk based on: database migrations, breaking API changes, new third-party dependencies, and blast radius. State the classification and reasons. High-risk releases require a dedicated rollback runbook before proceeding.

#### Dependency Check

- [ ] Dependent services are deployed and healthy
- [ ] Database migrations tested against a production-sized dataset
- [ ] Feature flags configured in all target environments
- [ ] Secrets and environment variables set in target environments

### Go/No-Go Criteria

Every row must be "Go" to proceed. If any item is "No-Go," the release does not ship.

| Criteria | Owner | Status |
|---|---|---|
| All CI checks pass on release branch | Engineer | Go / No-Go |
| Staging smoke tests pass | QA | Go / No-Go |
| Database migration tested and reversible | DBA / Engineer | Go / No-Go |
| Rollback procedure documented and tested | SRE | Go / No-Go |
| On-call engineer identified and available | Engineering lead | Go / No-Go |
| Stakeholders notified of release window | Release manager | Go / No-Go |

### Staged Rollout Plan

Define each stage with traffic percentage, bake time, and metric thresholds. Adjust based on risk classification — high-risk releases start at 1% with longer bake times.

| Stage | Traffic % | Bake Time | Metric Thresholds |
|---|---|---|---|
| Canary | 1-5% | 15-30 min | Error rate < 0.1%, p99 latency < baseline + 20% |
| Partial | 25% | 30-60 min | Error rate < 0.05%, no new error signatures |
| Majority | 75% | 60 min | Same as partial |
| Full | 100% | Ongoing | Same as partial |

### Monitoring Checkpoints

At each rollout stage, check:

- [ ] **Error rates** — Compare canary vs. baseline cohort. New error types are an immediate flag.
- [ ] **Latency** — p50, p95, p99 against pre-release baseline. Watch for gradual degradation, not just spikes.
- [ ] **Resource utilization** — CPU, memory, connection pools. Leaks surface during bake time.
- [ ] **Business metrics** — Conversion rates, checkout completions, or domain-specific KPIs. Drops may not trigger alerts.
- [ ] **Dependency health** — Downstream service error rates and queue depths.

Include specific dashboard URLs and alert names so the engineer can check each item without searching.

### Rollback Triggers

Define explicit conditions that require rollback — never leave this to judgment:

- Error rate exceeds 2x baseline for more than 5 minutes
- p99 latency exceeds 3x baseline
- Any data corruption or consistency issue detected
- Dependent service reports degradation traced to this release
- Feature flag kill switch fails to disable new behavior

**Rollback procedure:**

1. Halt rollout progression immediately
2. Route traffic back to previous version (feature flag off, revert deployment, or DNS switch)
3. Verify rollback by confirming metrics return to baseline within 10 minutes
4. Notify stakeholders with incident channel link
5. Create incident ticket with timeline and root cause hypothesis

### Post-Release

- [ ] **Verification** — Metrics stable for 1 hour at 100%, smoke tests pass, no new alerts
- [ ] **Communication** — Stakeholders notified, release notes published, support team briefed on new behavior
- [ ] **Cleanup** — Feature flags scheduled for removal, old artifacts torn down, retrospective scheduled if high-risk

## Quality checklist

Before delivering the checklist, verify:

- [ ] Every rollout stage has specific traffic percentages, bake times, and metric thresholds
- [ ] Rollback triggers are measurable conditions, not subjective judgments
- [ ] Go/No-Go table covers CI, testing, rollback readiness, and stakeholder notification
- [ ] Monitoring checkpoints reference specific metrics with comparison baselines
- [ ] Post-release section includes verification, communication, and cleanup steps
- [ ] The checklist is scoped to one release, not a generic process document

## Common mistakes

- **Vague rollback criteria.** "Roll back if things look bad" is not a trigger. State the metric, threshold, and time window.
- **Skipping bake time under pressure.** Bake times exist to surface slow-burn issues like memory leaks and connection exhaustion. Cutting them short defeats the purpose of staged rollout.
- **No baseline comparison.** Metric thresholds mean nothing without a baseline. Always compare canary metrics against the existing production cohort, not against arbitrary numbers.
- **Forgetting business metrics.** A release can have zero errors and perfect latency while silently breaking checkout flows. Include domain-specific KPIs in monitoring checkpoints.
- **Missing stakeholder communication.** Engineering may know the release succeeded, but support, product, and leadership need explicit notification — especially if user-facing behavior changed.
- **Treating the checklist as optional.** If a Go/No-Go item is "No-Go," the release does not proceed. The checklist is a gate, not a suggestion.
