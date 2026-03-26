# Metrics Framework: Acme Project Management (B2B SaaS)

## Business Objective

Increase net revenue retention (NRR) from 104% to 115% by Q4 2026 through reduced churn and expansion within existing accounts.

## Metric Tiers

### Primary Metric

```
Metric:             Net Revenue Retention (NRR)
Formula:            (Starting MRR - Contraction - Churn + Expansion) / Starting MRR
Data source:        billing.subscriptions + billing.invoices (Snowflake)
Owner:              @sarah-vp-product
Review cadence:     Monthly (cohort), Quarterly (board-level)
Alerting threshold: < 100% (trailing 3-month avg) triggers Slack alert to #revenue-metrics
Segmentation:       By plan tier (Starter/Pro/Enterprise), by industry, by account age
```

### Guardrail Metrics

| Metric | Formula | Threshold | Why it matters |
|--------|---------|-----------|----------------|
| Support ticket volume per account | Tickets created / active accounts (monthly) | Must stay < 2.5/mo | Prevents retention through friction |
| NPS (quarterly survey) | Standard NPS methodology | Must stay > 35 | Catches satisfaction drops before churn |
| P95 API latency | 95th percentile response time | Must stay < 800ms | Performance degradation drives enterprise churn |

### Diagnostic Metrics

| Metric | Formula | Owner | Cadence |
|--------|---------|-------|---------|
| Feature adoption rate | Users who used feature X in 30 days / total active users | @pm-growth | Weekly |
| Onboarding completion rate | Users completing all 5 setup steps / new users | @pm-onboarding | Weekly |
| Time-to-first-value | Median days from signup to first project created | @pm-onboarding | Weekly |
| Weekly active users (WAU) | Unique users with >= 1 meaningful action per week | @pm-growth | Weekly |
| Seat expansion rate | New seats added / total seats (monthly) | @pm-enterprise | Monthly |
| Contraction signals | Accounts with > 30% usage drop month-over-month | @cs-lead | Weekly |

## Dashboard Specification

**Executive dashboard** (Looker, daily refresh):
- NRR trended (12-month view), guardrail status indicators, MRR waterfall chart
- Owner: @sarah-vp-product
- Access: leadership + board

**Team dashboard** (Looker, hourly refresh):
- All three tiers. NRR and guardrails at top, diagnostics below with segment filters
- Owner: @data-eng-lead
- Access: product, engineering, CS teams

**Investigation view** (Snowflake + Hex notebooks, on-demand):
- Cohort retention curves, feature adoption funnels, churn risk model outputs
- Owner: @data-analyst
- Access: product and data teams

## Review Process

- **Weekly standup** (15 min, Tuesdays): NRR leading indicators + guardrail check. Assign investigation owners for any anomaly.
- **Monthly review** (45 min, first Friday): Cohort deep-dive on NRR. Diagnostic analysis: which features correlate with expansion? Where are contraction signals concentrated?
- **Quarterly calibration** (90 min): Is NRR still the right primary metric? Review guardrail effectiveness. Adjust diagnostic metrics based on product roadmap shifts.

## Anti-Metrics: What We Do NOT Track

- **Total registered users** — vanity metric, only goes up, informs no decisions
- **Page views** — does not correlate with value delivery for a B2B tool
- **"Engagement score"** — composite of unrelated inputs, obscures signal
- **Daily signups** — interesting but not actionable at our stage; focus is retention and expansion, not top-of-funnel
