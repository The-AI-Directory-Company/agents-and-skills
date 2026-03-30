# Risk Matrix Guide

How to score Likelihood x Impact for test planning. Use this to drive testing investment -- high-risk components get more coverage, low-risk components get less.

## Scoring Scales

### Likelihood (1-5): How likely is a bug in this component?

| Score | Label | Description |
|-------|-------|-------------|
| 1 | Rare | Stable, well-tested code with no recent changes |
| 2 | Unlikely | Minor changes to well-understood code |
| 3 | Possible | New feature with moderate complexity, or code with partial test coverage |
| 4 | Likely | Complex logic, multiple integrations, or significant refactoring |
| 5 | Almost Certain | Brand-new untested code, legacy code with no tests, or known fragile area |

### Impact (1-5): What happens if a bug reaches production?

| Score | Label | Description |
|-------|-------|-------------|
| 1 | Negligible | Cosmetic issue, no user impact, easy to fix |
| 2 | Minor | Small UX degradation, workaround exists, affects few users |
| 3 | Moderate | Feature partially broken, no data loss, affects a user segment |
| 4 | Major | Feature fully broken, potential data corruption, affects many users |
| 5 | Critical | Data loss, security breach, financial loss, regulatory violation |

## Risk Score Calculation

```
Risk Score = Likelihood x Impact
```

| Risk Score | Risk Level | Testing Investment |
|------------|------------|-------------------|
| 15-25 | **Critical** | Extensive -- unit + integration + E2E + manual exploratory |
| 8-14 | **High** | Thorough -- unit + integration, E2E for critical paths |
| 4-7 | **Medium** | Moderate -- unit tests + happy-path integration |
| 1-3 | **Low** | Minimal -- happy-path unit tests only |

## Automatic Risk Classifications

Some component types have predetermined minimum scores regardless of other factors.

### Automatic Impact = 5 (Critical)

- **PII handling** -- User data exposure violates privacy regulations (GDPR, CCPA). Any component that reads, writes, transforms, or transmits personally identifiable information.
- **Money flows** -- Payment processing, billing, refunds, balance calculations. Errors cause direct financial loss or regulatory issues (PCI-DSS).
- **Authentication and authorization** -- Login, session management, role checks, API key validation. Failures enable unauthorized access.
- **Data deletion or migration** -- Irreversible operations. A bug means permanent data loss.

### Automatic Likelihood >= 4 (Likely)

- **Untested third-party integrations** -- External APIs you have not integration-tested in your environment. Their behavior is outside your control.
- **Legacy code with no test coverage** -- Code that has survived by luck. Any change to it or its dependencies is high-risk.
- **First-time implementations** -- New patterns, new libraries, new infrastructure. No institutional knowledge yet.
- **Code with known tech debt** -- Areas flagged in retrospectives, marked with TODO/HACK comments, or on the refactoring backlog.

### Automatic Likelihood >= 3 (Possible)

- **Recently refactored code** -- Even clean refactors introduce risk. Behavior may have subtly changed.
- **Code with complex branching** -- High cyclomatic complexity means more paths to cover and more edge cases to miss.
- **Multi-service interactions** -- Distributed systems fail in ways single services do not: timeouts, partial failures, ordering issues.

## Worked Example

| Component | Likelihood | Rationale | Impact | Rationale | Risk Score | Risk Level |
|-----------|-----------|-----------|--------|-----------|------------|------------|
| Stripe checkout | 4 | New integration, first implementation | 5 | Money flow (auto-Critical) | 20 | Critical |
| User profile update | 3 | Moderate changes, some existing tests | 5 | PII handling (auto-Critical) | 15 | Critical |
| Search results page | 3 | New filtering logic | 3 | Feature degradation, no data risk | 9 | High |
| Email template | 2 | Minor copy change | 2 | Cosmetic, easy to hotfix | 4 | Medium |
| Footer links | 1 | No changes planned | 1 | Cosmetic only | 1 | Low |

## Using the Matrix to Allocate Effort

Once you have scored all components:

1. **Sort by risk score descending.** This is your testing priority order.
2. **Set coverage targets by risk level** (see test plan template Section 4).
3. **Assign test levels by risk level** -- Critical components get all levels; Low components get unit tests only.
4. **Time-box low-risk testing.** If you are running out of time, cut Low and Medium items first. Never cut Critical.
