# Metric Definition Card Schema

Every metric in a framework must have a definition card. This document explains each field, provides annotated examples for all three metric tiers, and offers guidance on handling aspirational metrics.

## Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| **Metric** | Yes | Human-readable name. Use consistent casing across all cards. |
| **Type** | Yes | One of: Primary, Guardrail, Diagnostic. |
| **Formula** | Yes | Exact calculation. Specify numerator, denominator, and any filters. Two people reading this formula should produce the same number from the same data. |
| **Data source** | Yes | Table(s), event(s), or system(s) the metric pulls from. Include the warehouse or tool name. |
| **Owner** | Yes | A single person (not a team). This person is accountable for the metric's accuracy and for investigating anomalies. |
| **Review cadence** | Yes | How often this metric is reviewed and by whom. Separate operational review from deep-dive review if they differ. |
| **Alerting threshold** | Conditional | Required for Primary and Guardrail metrics. The value or condition that triggers an alert. Specify the channel and audience. |
| **Segmentation** | Recommended | Dimensions by which this metric should be breakable (plan tier, geography, cohort, platform, etc.). |
| **Baseline** | Recommended | Current value at the time the framework is established. Without a baseline, movement is uninterpretable. |
| **Target** | Conditional | Required for Primary metrics. Guardrails have thresholds (floors/ceilings), not targets. Diagnostics typically have neither. |
| **Notes** | Optional | Known caveats, seasonality effects, data freshness limitations, or planned instrumentation changes. |

---

## Annotated Examples

### Primary Metric Card

```
Metric:             90-day retention rate
Type:               Primary
Formula:            COUNT(users active on day 90) / COUNT(users who completed onboarding 90 days ago)
                    Active = at least one core action (create, edit, or share) in a session.
                    Excludes internal/test accounts (email domain filter).
Data source:        events.user_activity + events.onboarding_completed (Snowflake)
Owner:              @jordan-lee (Growth PM)
Review cadence:     Weekly (7-day rolling trend in #growth-standup)
                    Monthly (cohort deep-dive in Growth Review)
Alerting threshold: < 30% on 7-day rolling average -> Slack #growth-alerts
Segmentation:       Plan tier, signup source, onboarding path, platform (web/mobile)
Baseline:           34% (as of 2025-01-15, all-user cohort)
Target:             45% by end of Q3 2025
Notes:              Retention denominator resets each cohort. Holiday weeks
                    (Dec 20 - Jan 5) excluded from trend analysis due to
                    seasonal drop.
```

**Why this works:** The formula is unambiguous -- it defines "active," specifies exclusions, and names the exact tables. The alert threshold is a rolling average, not a single-day number, which avoids false positives from weekend dips.

---

### Guardrail Metric Card

```
Metric:             Support ticket volume (product-related)
Type:               Guardrail
Formula:            COUNT(tickets created) WHERE category IN ('bug', 'usability', 'feature-confusion')
                    per calendar week. Excludes billing and account-access tickets.
Data source:        zendesk.tickets (synced to Snowflake nightly)
Owner:              @maria-santos (Support Lead)
Review cadence:     Weekly (threshold check in #growth-standup)
Alerting threshold: > 120% of 4-week rolling average -> Slack #support-escalations
Segmentation:       Ticket category, product area, user plan tier
Baseline:           ~85 tickets/week (4-week avg as of 2025-01-15)
Target:             None (guardrail -- threshold only, not optimized)
Notes:              Zendesk sync has a 6-hour lag. Spikes on Monday reflect
                    weekend accumulation -- compare week-over-week, not
                    day-over-day.
```

**Why this works:** Guardrails have thresholds, not targets. The 120%-of-rolling-average trigger adapts to organic growth instead of using a fixed number that becomes stale.

---

### Diagnostic Metric Card

```
Metric:             Onboarding completion rate
Type:               Diagnostic
Formula:            COUNT(users reaching onboarding step 'complete') /
                    COUNT(users reaching onboarding step 'start')
                    within 7 days of signup.
Data source:        events.onboarding_funnel (Snowflake)
Owner:              @alex-kumar (Growth Engineer)
Review cadence:     Weekly (included in Growth standup when retention trend is anomalous)
                    Monthly (always reviewed in cohort deep-dive)
Alerting threshold: None (diagnostic -- investigated on demand, not alerted)
Segmentation:       Signup source, onboarding path variant, platform
Baseline:           62% (as of 2025-01-15)
Target:             None (diagnostic -- explains primary metric movement)
Notes:              This metric sits upstream of retention in the causal chain.
                    A drop here often precedes a retention drop by 2-3 weeks.
                    If onboarding completion drops but retention holds,
                    investigate whether users are finding alternative activation
                    paths.
```

**Why this works:** Diagnostics explain movement in the primary metric. The notes field documents the causal relationship, which helps future readers understand why this metric is in the framework.

---

## Aspirational vs. Operational Metrics

A metric is **operational** when every field on the card can be filled with verified information -- the data source exists, the formula runs, and the number appears on a dashboard today.

A metric is **aspirational** when one or more of these conditions is true:

- The data source does not exist yet (instrumentation needed)
- The formula cannot be computed with current data (missing events or joins)
- The owner has not been assigned or has not agreed to ownership
- The baseline is unknown because the metric has never been measured

### How to handle aspirational metrics

Do not exclude them from the framework. Instead:

1. Fill out what you can on the definition card.
2. Mark incomplete fields explicitly:
   ```
   Data source:   [INSTRUMENTATION NEEDED] Requires new event: user.value_moment
                   Tracking ticket: ENG-1234 — Target: 2025-03-01
   ```
3. Add the metric to a separate "Instrumentation Gaps" section in the framework document.
4. Assign an owner for closing the gap, with a deadline.
5. Do not include aspirational metrics on dashboards or in review processes until they become operational. Showing a metric that reads "No Data" trains the team to ignore dashboards.

The gap between aspirational and operational is where most frameworks stall. Track these gaps as first-class work items, not footnotes.
