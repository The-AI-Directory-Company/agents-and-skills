# Test Plan Template

Copy this template and fill in for your feature, service, or release.

## Test Plan Metadata

| Field | Value |
|-------|-------|
| Feature / Release | |
| Author | |
| Date | |
| Status | Draft / In Review / Approved |
| Requirements Link | |
| Timeline | |

---

## 1. Scope

### In Scope

<!-- List components, features, and behaviors covered by this test plan. -->

-
-
-

### Out of Scope

<!-- List items explicitly excluded, with reason for each. -->

| Item | Reason |
|------|--------|
| | (separate ticket / future phase / unchanged / other team owns) |
| | |

---

## 2. Risk Analysis

| Component | Likelihood (1-5) | Impact (1-5) | Risk Score | Risk Level | Testing Investment |
|-----------|------------------|-------------|------------|------------|-------------------|
| | | | | | |
| | | | | | |
| | | | | | |

**Risk Level Bands:** Critical (15-25), High (8-14), Medium (4-7), Low (1-3)

**Automatic overrides applied:**
- [ ] PII handling components set to Impact >= 5
- [ ] Money flow components set to Impact >= 5
- [ ] Untested integrations set to Likelihood >= 4
- [ ] Legacy code without tests set to Likelihood >= 4

---

## 3. Test Levels per Component

| Component | Unit | Integration | E2E | Manual | Rationale |
|-----------|------|-------------|-----|--------|-----------|
| | | | | | |
| | | | | | |
| | | | | | |

---

## 4. Coverage Targets

| Risk Level | Line Coverage Target | Acceptance Criteria Coverage | Notes |
|------------|---------------------|----------------------------|-------|
| Critical | 90%+ | 100% of acceptance criteria | |
| High | 75%+ | All happy paths + known edge cases | |
| Medium | 50%+ | Happy path only | |
| Low | Best effort | Happy path only | |

---

## 5. Test Cases

### P0 -- Must pass before release

- [ ]
- [ ]
- [ ]

### P1 -- Should pass, release-blocking if broken

- [ ]
- [ ]
- [ ]

### P2 -- Nice to verify, not release-blocking

- [ ]
- [ ]

---

## 6. Environment Requirements

| Test Level | Environment | Dependencies | Setup Notes |
|------------|-------------|-------------|-------------|
| Unit | Local | None (all I/O mocked) | |
| Integration | CI | | |
| E2E | Staging | | |
| Manual | Staging | | |

**Blockers:**
<!-- List anything that must be configured before testing can begin. -->

-

---

## 7. Pass/Fail Criteria

### Release is GO when:

- [ ] All P0 test cases pass
- [ ] All P1 cases pass OR have documented workarounds approved by eng lead
- [ ] No open P0/P1 bugs
- [ ] Coverage targets met per risk level

### Release is NO-GO when:

- [ ] Any P0 test case fails
- [ ] More than ___ P1 cases fail without workarounds
- [ ] A new Critical/High-risk bug is discovered outside the plan

---

## 8. Schedule

| Phase | Start | End | Owner | Notes |
|-------|-------|-----|-------|-------|
| Test plan review | | | | |
| Unit test writing | | | | |
| Integration test writing | | | | |
| E2E test writing | | | | |
| Test execution (full run) | | | | |
| Bug fix buffer | | | | |
| Regression retest | | | | |
| Sign-off | | | | |

**Note:** Bug fix buffer should be at minimum 20% of total testing time.

---

## Notes

<!-- Additional context, assumptions, known risks, or open questions. -->
