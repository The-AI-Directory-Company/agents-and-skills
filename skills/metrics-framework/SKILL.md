---
name: metrics-framework
description: Define product and engineering metrics frameworks — choosing primary, guardrail, and diagnostic metrics with measurement methodology, review cadence, ownership, and dashboard specifications.
metadata:
  displayName: "Metrics Framework"
  categories: ["data", "product-management"]
  tags: ["metrics", "KPIs", "measurement", "dashboards", "analytics", "OKRs"]
  worksWellWithAgents: ["account-executive", "bi-analyst", "customer-success-manager", "data-scientist", "data-visualization-specialist", "engineering-manager", "financial-analyst"]
  worksWellWithSkills: ["bi-report", "dashboard-design", "experiment-design", "financial-model", "go-to-market-plan", "ml-model-evaluation", "prd-writing", "pricing-analysis"]
---

# Metrics Framework

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **Business objective** — What outcome are you trying to drive? (e.g., increase retention, reduce cost-to-serve, grow revenue per user)
2. **Product or team scope** — Which product, feature area, or team does this framework cover?
3. **Current state** — Do metrics exist today? What is being tracked, and what is missing?
4. **Audience** — Who will consume these metrics? (executives, PMs, engineers, cross-functional reviews)
5. **Data infrastructure** — What tools are in place? (warehouse, event tracking, BI layer, alerting)
6. **Review cadence** — How often does the team review metrics today? How often should they?

If the user says "we need a dashboard," push back and ask what decisions the dashboard should inform. Dashboards without decision context become decoration.

## Metrics framework template

### 1. Business Objective

State the business objective in one sentence. This anchors every metric choice — if a metric does not connect to this objective, it does not belong in the framework.

```
Objective: Increase 90-day user retention from 34% to 45% by Q3,
           driving ARR expansion through reduced churn.
```

### 2. Metric Types

Every framework needs exactly three tiers. No more, no fewer.

| Type | Purpose | Count | Example |
|------|---------|-------|---------|
| **Primary** | The single metric that defines success for this objective | 1 | 90-day retention rate |
| **Guardrail** | Metrics that must not degrade while pursuing the primary metric | 2-4 | Support ticket volume, NPS, p95 latency |
| **Diagnostic** | Metrics that explain *why* the primary metric is moving | 4-8 | Feature adoption rate, onboarding completion, time-to-value |

**Primary metric rules:**
- Exactly one. If you have two primary metrics, you have zero — pick one or combine them into a composite.
- Must be directly measurable, not derived from surveys or estimates.
- Must move on the timescale of your review cadence. A quarterly metric reviewed weekly creates noise, not signal.

**Guardrail metric rules:**
- Protect against perverse incentives. If your primary metric is retention, a guardrail should catch cases where you retain users by making cancellation harder rather than making the product better.
- Each guardrail has a threshold, not a target. You are not optimizing guardrails — you are ensuring they stay within acceptable bounds.

**Diagnostic metric rules:**
- Diagnostics are investigation tools, not success measures. They answer "why is the primary metric moving?"
- Organize diagnostics in a causal chain: input metrics (actions) lead to output metrics (results).

### 3. Metric Definition Card

Define every metric using this template. Ambiguity in definitions is the #1 reason metrics frameworks fail — two people looking at the same dashboard should never disagree on what a number means.

```
Metric:             90-day retention rate
Formula:            Users active on day 90 / Users who completed onboarding 90 days ago
Data source:        events.user_activity + events.onboarding_completed (warehouse)
Owner:              @product-lead (Growth)
Review cadence:     Weekly (trended), Monthly (cohort deep-dive)
Alerting threshold: < 30% (7-day rolling avg) triggers Slack alert to #growth-metrics
Segmentation:       By plan tier, signup source, onboarding path
```

Every metric in the framework gets a card. No exceptions. If you cannot fill out the formula and data source fields, the metric is aspirational, not operational — flag it as a gap to close.

### 4. Dashboard Specification

Dashboards serve decisions, not aesthetics. Structure by audience:

- **Executive dashboard:** 3-5 metrics, trended over time, updated daily. Primary metric front and center, guardrails visible at a glance. No diagnostic metrics — executives do not debug.
- **Team dashboard:** All three tiers. Primary and guardrails at top, diagnostics below. Include filters for key segments. Updated in real-time or hourly.
- **Investigation view:** Diagnostic metrics with drill-down capability. Cohort breakdowns, funnel analysis, event-level detail. Used ad hoc, not on a schedule.

For each dashboard, specify: tool (Looker, Metabase, Tableau, etc.), refresh frequency, access control, and the one person responsible for keeping it accurate.

### 5. Review Process

Define how metrics are reviewed, not just displayed:

- **Weekly standup** (15 min): Primary metric trend + any guardrail violations. Action: assign investigation owners for anomalies.
- **Monthly review** (45 min): Cohort analysis on primary metric. Diagnostic deep-dive. Action: update priorities based on what diagnostics reveal.
- **Quarterly calibration** (90 min): Is the primary metric still the right one? Have guardrails caught real problems? Action: revise the framework if objectives have shifted.

Every review must produce either "no action needed" or a named owner with a deadline. Reviews without outcomes are status theater.

### 6. Anti-Metrics: What NOT to Measure

Explicitly list metrics you considered and rejected. This prevents them from creeping back in.

- **Vanity metrics** that move in only one direction (total signups, cumulative revenue) — these feel good but inform no decisions.
- **Proxy metrics** where the proxy has diverged from the real outcome (DAU as a proxy for engagement when users open the app but do not complete any action).
- **Lagging-only metrics** that cannot be influenced within your review cadence (annual churn measured weekly).
- **Composite scores** that obscure signal by blending unrelated inputs (a "health score" averaging NPS, usage, and support tickets).

## Quality checklist

Before delivering a metrics framework, verify:

- [ ] Exactly one primary metric is defined — not two, not a composite
- [ ] Every metric has a complete definition card with formula, data source, and owner
- [ ] Guardrail metrics protect against perverse incentives of the primary metric
- [ ] Diagnostic metrics form a causal chain that explains primary metric movement
- [ ] Every metric moves on a timescale compatible with its review cadence
- [ ] Dashboard spec names the tool, refresh rate, and a single person responsible for accuracy
- [ ] Review process defines outcomes, not just meetings
- [ ] Anti-metrics section documents what was excluded and why

## Common mistakes to avoid

- **Vanity metrics as primary metrics.** Total signups, page views, or "engagement score" feel good but drive no decisions. A primary metric must be something you can act on and would change your priorities if it moved.
- **Too many metrics.** Frameworks with 20+ metrics get ignored. If everything is a KPI, nothing is. Constrain to 1 primary + 3 guardrails + 6 diagnostics maximum.
- **No ownership.** A metric without an owner is a metric nobody acts on. Every metric card must name a person — not a team, not a channel, a person.
- **Missing guardrails.** Optimizing a primary metric without guardrails invites Goodhart's Law. If your primary metric is time-on-site, you need guardrails for task completion and satisfaction — otherwise you are incentivizing confusion, not engagement.
- **Measuring what is easy instead of what matters.** Click counts are easy to track. Whether users achieved their goal is harder but more valuable. Do the hard instrumentation work.
- **No review cadence.** Dashboards without scheduled reviews become wallpaper. Define who looks at what, when, and what decisions they make as a result.
