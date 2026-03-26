---
name: test-plan-writing
description: Write risk-based test plans with coverage matrices, test level decisions, pass/fail criteria, and environment requirements — deciding what to test, at which level, and why.
metadata:
  displayName: "Test Plan Writing"
  categories: ["engineering"]
  tags: ["testing", "test-plan", "coverage", "quality-assurance", "test-strategy"]
  worksWellWithAgents: ["code-reviewer", "embedded-engineer", "mobile-engineer", "performance-engineer", "prompt-engineer", "qa-engineer", "test-strategist"]
  worksWellWithSkills: ["performance-audit", "prd-writing", "prompt-engineering-guide", "ticket-writing"]
---

# Test Plan Writing

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What is being tested?** (Feature, service, migration, integration, or full release)
2. **What are the requirements?** (Link to PRD, tickets, or acceptance criteria)
3. **What is the risk profile?** (User-facing? Payment flow? Data migration? First launch or incremental?)
4. **What is the tech stack?** (Languages, frameworks, third-party integrations, data stores)
5. **What testing infrastructure exists?** (CI pipeline, staging environments, test data factories)
6. **What is the timeline?** (Release date, testing window, hard deadlines)

## Test plan template

### 1. Scope

Define what is in scope and what is explicitly out of scope. Every out-of-scope item should explain why (separate ticket, future phase, unchanged).

### 2. Risk Analysis

Rank components by risk. This drives where you invest testing effort.

| Component | Likelihood | Impact | Risk Level | Testing Investment |
|-----------|-----------|--------|------------|-------------------|
| Payment processing | Medium | Critical | **High** | Extensive |
| Cart calculations | Low | High | **Medium** | Moderate |
| Confirmation page | Low | Low | **Low** | Minimal |

Rules:
- Anything involving money, PII, or data loss is automatically High impact
- New third-party integrations are Medium likelihood minimum
- Components with no existing test coverage get a likelihood bump

### 3. Test Levels per Component

For each component, decide which test levels apply and why.

| Component | Unit | Integration | E2E | Manual | Rationale |
|-----------|------|-------------|-----|--------|-----------|
| Price calculation | Yes | No | No | No | Pure logic, no external deps |
| Stripe integration | No | Yes | Yes | No | Must verify real API contract |
| Checkout flow | No | No | Yes | Yes | User-facing critical path |

Key principle: **test at the lowest level that gives you confidence.** Unit tests for logic, integration tests for contracts, E2E for critical user journeys only.

### 4. Coverage Targets

Set targets per risk level, not a single blanket number:

```
High-risk:   90%+ line coverage, 100% of acceptance criteria
Medium-risk: 75%+ line coverage, all happy paths + known edge cases
Low-risk:    50%+ line coverage, happy path only
```

A single "80% coverage" target incentivizes testing easy code instead of risky code.

### 5. Test Cases

Group by component and priority. Each case must have a clear pass/fail condition:

```
P0 — Must pass before release:
- [ ] Successful charge with valid card returns order confirmation
- [ ] Declined card shows user-facing error, no order created
- [ ] Network timeout triggers retry (max 2), then fails gracefully

P1 — Should pass, release-blocking if broken:
- [ ] Duplicate submission within 5s is idempotent
- [ ] Partial failure (charge succeeds, DB write fails) triggers compensation

P2 — Nice to verify, not release-blocking:
- [ ] Charge amount matches cart total across currency formats
```

### 6. Environment Requirements

Specify what each test level needs to run:

```
Unit tests:   Local, no external deps, mock all I/O
Integration:  CI environment, test-mode API keys, test database
E2E:          Staging environment, seeded test data, service sandboxes
Manual:       Staging with production-like data volume
```

Call out blockers explicitly: "Staging must have Stripe sandbox keys configured before E2E tests can run."

### 7. Pass/Fail Criteria

```
Release is GO when:
- All P0 test cases pass
- All P1 cases pass OR have documented workarounds approved by eng lead
- No open P0/P1 bugs
- Coverage targets met per risk level

Release is NO-GO when:
- Any P0 test case fails
- More than 2 P1 cases fail without workarounds
- A new High-risk bug is discovered outside the original plan
```

### 8. Schedule

Map testing activities to the timeline. Always include buffer for bug fixes — plans that allocate 100% of time to writing tests and 0% to fixing failures are fiction.

## Quality checklist

Before delivering a test plan, verify:

- [ ] Every in-scope component has a risk rating with reasoning
- [ ] Test levels are justified per component, not applied uniformly
- [ ] Coverage targets vary by risk level, not a single blanket number
- [ ] Every test case has a clear pass/fail condition, not just a description
- [ ] Pass/fail criteria define both GO and NO-GO conditions
- [ ] Environment requirements call out setup dependencies and blockers
- [ ] Out-of-scope items are listed explicitly, not just omitted silently
- [ ] P0 test cases cover failure modes, not just happy paths
- [ ] Schedule accounts for bug-fix time, not just initial test writing

## Common mistakes to avoid

- **Testing everything at E2E level.** E2E tests are slow and flaky. Reserve them for critical user journeys. Test logic with unit tests, contracts with integration tests.
- **Flat priority lists.** If every test case is "high priority," none are. Use P0/P1/P2 to force real prioritization.
- **Missing failure modes.** For every success case, ask: "What happens when this fails? Times out? Returns unexpected data?"
- **Coverage theater.** Hitting 80% by testing getters while ignoring retry logic. Coverage targets must pair with risk analysis.
- **No exit criteria.** Without pass/fail criteria, "are we done?" becomes a judgment call. Define the gate up front.
- **Ignoring test data.** Plans that assume test data exists without specifying who creates it, how, and when.
