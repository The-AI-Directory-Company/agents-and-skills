# Test Levels Decision Guide

How to decide between Unit, Integration, E2E, and Manual testing for each component. The goal is to test at the **lowest level that gives you confidence** -- unit tests are fast and reliable, E2E tests are slow and flaky.

## Decision Tree

```
Is it pure logic with no external dependencies?
  YES --> Unit test
  NO  --> Does it interact with exactly one external system (DB, API, file system)?
            YES --> Integration test
            NO  --> Is it a critical user journey across multiple systems?
                      YES --> E2E test
                      NO  --> Is it subjective, exploratory, or visual?
                                YES --> Manual test
                                NO  --> Integration test (default for uncertain cases)
```

## Decision Matrix by Component Type

| Component Type | Unit | Integration | E2E | Manual | Rationale |
|---------------|------|-------------|-----|--------|-----------|
| **Pure calculation / business logic** | Yes | No | No | No | No external deps. Fast, deterministic. Test all edge cases here. |
| **Data validation / parsing** | Yes | No | No | No | Input/output transformation. Exhaustive edge cases are cheap at unit level. |
| **State management (Redux, Zustand)** | Yes | No | No | No | Pure reducers/selectors. Mock actions, assert state. |
| **Utility / helper functions** | Yes | No | No | No | Isolated logic. Unit tests cover the full contract. |
| **Database queries / ORM layer** | No | Yes | No | No | Must verify actual SQL behavior. Use test database, not mocks. |
| **REST / GraphQL API endpoints** | No | Yes | No | No | Test request/response contract with real server, test DB. |
| **Third-party API integrations** | No | Yes | No | No | Verify your code handles real API responses, errors, timeouts. Use sandbox/test mode. |
| **Authentication / authorization** | Yes | Yes | No | No | Unit test permission logic. Integration test actual auth flow (tokens, sessions). |
| **Message queue consumers** | No | Yes | No | No | Must verify real message processing, retries, dead-letter behavior. |
| **Critical user journeys** | No | No | Yes | No | Checkout, signup, onboarding. Cross-system flows where integration tests cannot cover the full chain. |
| **Payment flows** | Yes | Yes | Yes | No | Unit test calculations. Integration test API. E2E test full user flow. All three levels warranted. |
| **Email / notification delivery** | No | Yes | No | Yes | Integration test send logic. Manual verify rendering in real clients. |
| **UI layout / visual design** | No | No | No | Yes | Subjective. Visual regression tools (Chromatic, Percy) can automate partially. |
| **Accessibility** | No | No | No | Yes | Automated tools catch ~30% of issues. Manual testing with screen readers is essential. |
| **Cross-browser compatibility** | No | No | Yes | Yes | E2E on multiple browsers. Manual for edge cases and visual verification. |
| **Performance under load** | No | No | No | Yes | Load testing tools (k6, Locust) are closer to manual/specialized than standard E2E. |

## When to Combine Levels

Some components benefit from testing at multiple levels:

| Scenario | Levels | Why |
|----------|--------|-----|
| Payment processing | Unit + Integration + E2E | Money. Test calculations (unit), API contract (integration), and full user flow (E2E). |
| Auth with role-based access | Unit + Integration | Test permission logic (unit) and actual token/session behavior (integration). |
| Search with complex filters | Unit + Integration | Test filter logic (unit) and actual query results (integration). |
| Data migration | Integration + Manual | Test migration script (integration) and verify data integrity manually on staging. |

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| E2E test for pure logic | Slow, flaky, hard to debug. A calculation bug takes 2 minutes to reproduce instead of 2 ms. | Move to unit test. |
| Unit test with heavy mocking | Mocks pass but real system fails. False confidence. | Move to integration test with real dependencies. |
| No E2E for critical paths | Individual pieces work but the full flow breaks at the seams. | Add E2E for the top 3-5 user journeys. |
| Manual test for repeatable logic | Slow, error-prone, not run consistently. | Automate as unit or integration test. |
| E2E for every feature | Test suite takes 45 minutes, breaks constantly, team ignores failures. | Reserve E2E for critical journeys only. Cover the rest at lower levels. |

## Coverage Target Guidelines by Test Level

| Level | Typical Run Time | Reliability | Suggested Count |
|-------|-----------------|-------------|-----------------|
| Unit | < 5 ms each | > 99% pass rate | Hundreds to thousands. Cover all logic branches. |
| Integration | 50-500 ms each | > 95% pass rate | Tens to low hundreds. Cover contracts and edge cases. |
| E2E | 5-30 s each | > 90% pass rate | 5-20 for the whole app. Critical journeys only. |
| Manual | Minutes each | N/A | As needed. Visual, exploratory, accessibility. |
