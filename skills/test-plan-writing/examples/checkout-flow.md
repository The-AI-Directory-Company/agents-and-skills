# Test Plan: E-Commerce Checkout Flow

## 1. Scope

**In scope**: Cart review, shipping address entry, payment processing (Stripe), order confirmation, and email receipt. Covers web (desktop + mobile viewport) and iOS app.

**Out of scope**:
- Product browsing and cart management (unchanged, tested separately in CART-220)
- Loyalty points redemption (Phase 2, not launching until Q1)
- Guest checkout (separate ticket CHK-415)

## 2. Risk Analysis

| Component | Likelihood | Impact | Risk Level | Testing Investment |
|-----------|-----------|--------|------------|-------------------|
| Payment processing (Stripe) | Medium | Critical | **High** | Extensive |
| Shipping cost calculation | Medium | High | **High** | Extensive |
| Promo code application | High | High | **High** | Extensive |
| Address validation (SmartyStreets) | Medium | Medium | **Medium** | Moderate |
| Order confirmation page | Low | Low | **Low** | Minimal |
| Email receipt (SendGrid) | Low | Medium | **Low** | Minimal |

Notes: Payment and promo codes are high-risk because bugs directly cause revenue loss. Promo code likelihood is elevated due to new stacking logic with no existing test coverage.

## 3. Test Levels per Component

| Component | Unit | Integration | E2E | Manual | Rationale |
|-----------|------|-------------|-----|--------|-----------|
| Promo code stacking logic | Yes | No | Yes | No | Pure calculation logic + complex user-facing edge cases |
| Shipping cost calculation | Yes | Yes | No | No | Logic is testable; integration verifies rate API contract |
| Stripe payment | No | Yes | Yes | No | Must verify real Stripe sandbox behavior |
| Address validation | No | Yes | No | No | Third-party API contract test only |
| Order confirmation | No | No | No | Yes | Visual review, low risk |
| Email receipt | No | Yes | No | Yes | Verify template renders; manual spot-check formatting |

## 4. Coverage Targets

```
High-risk (payment, shipping, promo):  90%+ line coverage, 100% acceptance criteria
Medium-risk (address validation):      75%+ line coverage, happy path + known edge cases
Low-risk (confirmation, email):        50%+ line coverage, happy path only
```

## 5. Test Cases

**P0 — Must pass before release:**
- [ ] Valid Visa charge succeeds and returns order confirmation with correct total
- [ ] Declined card shows user-facing error; no order or charge created
- [ ] Stripe timeout (> 5s) retries once, then shows "try again" with no duplicate charge
- [ ] Promo code applies correct discount; cart total, tax, and Stripe charge all match
- [ ] Shipping cost recalculates when address changes from domestic to international

**P1 — Should pass, release-blocking if broken:**
- [ ] Double-click "Place Order" within 2s is idempotent (single charge, single order)
- [ ] Expired promo code returns clear error, does not apply partial discount
- [ ] Two valid promo codes stack correctly (percentage applied before fixed amount)
- [ ] Invalid address rejected by SmartyStreets shows inline validation message

**P2 — Nice to verify, not release-blocking:**
- [ ] Order confirmation email arrives within 60s with correct line items
- [ ] Checkout accessible at mobile viewport (375px) with no horizontal scroll
- [ ] Browser back button from confirmation does not re-submit payment

## 6. Environment Requirements

```
Unit tests:      Local, no external deps, mock Stripe + SmartyStreets
Integration:     CI, Stripe sandbox keys, SmartyStreets test key, test database
E2E:             Staging, seeded catalog (10 products, 3 promo codes), Stripe sandbox
Manual:          Staging with production-like data volume (1k orders)
```

**Blocker**: Staging must have Stripe sandbox webhook configured before E2E tests run. Owner: @devops, due before test cycle starts.

## 7. Pass/Fail Criteria

```
Release is GO when:
- All P0 test cases pass
- All P1 cases pass OR have documented workarounds approved by eng lead
- No open P0/P1 bugs
- Coverage targets met per risk level

Release is NO-GO when:
- Any P0 test case fails
- More than 2 P1 cases fail without approved workarounds
- A payment-related bug is found outside the test plan scope
```

## 8. Schedule

| Day | Activity |
|-----|----------|
| Mon | Unit + integration tests written and passing in CI |
| Tue | E2E tests written; staging environment verified |
| Wed | Full test suite run; bug triage |
| Thu | Bug fixes + re-run failing tests |
| Fri | Manual QA on staging; GO/NO-GO decision by 3pm |
