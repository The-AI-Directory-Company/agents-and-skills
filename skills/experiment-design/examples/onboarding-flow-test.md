# Experiment Design: Guided Onboarding Flow

## Hypothesis

If we replace the current self-serve onboarding (5-step form) with an interactive guided tour that demonstrates core features in context, then the 14-day activation rate will increase by at least 5 percentage points, because users who experience value during onboarding are more likely to complete setup and return within the first two weeks.

## Metrics

| Role | Metric | Baseline | MDE | Direction |
|------|--------|----------|-----|-----------|
| Primary | 14-day activation rate (user completes 2+ core actions within 14 days of signup) | 32% | +5pp | Increase |
| Guardrail | Onboarding completion rate | 68% | -5pp | Must not decrease |
| Guardrail | Support ticket rate (first 14 days) | 3.1% | +1pp | Must not increase |
| Guardrail | Time-to-complete onboarding | 4.2 min | +2 min | Must not increase |

## Sample Size Calculation

```
Baseline rate:              32%
Minimum detectable effect:  +5pp (absolute) -> 37%
Significance level (alpha): 0.05 (two-sided)
Power (1 - beta):           0.80
Sample size per variant:    ~1,530 users
Total sample:               ~3,060 users
Tool:                       Evan Miller sample size calculator (two-proportion z-test)
```

## Randomization

- **Unit**: User-level (new signups only)
- **Method**: Hash-based assignment on user ID (deterministic)
- **Stickiness**: User ID hash persists across sessions; variant stored in `experiments.assignments` table
- **Exclusions**: Users on Enterprise plans (they receive white-glove onboarding)

## Runtime Estimation

```
Daily eligible signups:     ~180 users
Sample needed:              3,060 users
Estimated runtime:          17 days (to reach sample size)
Recommended minimum:        21 days (3 full weeks for day-of-week coverage)
Maximum runtime:            35 days (cap to avoid novelty decay)
```

## Stopping Rules

- **No peeking**: Fixed-horizon design. Do not evaluate primary metric significance until day 21.
- **Stop for harm**: If support ticket rate exceeds 5% (rolling 3-day average) in the treatment group, halt the experiment and revert all users to control.
- **No early stopping for success**: Even if results look significant at day 10, run to the planned horizon.

## Holdout Group

- **Size**: 5% of eligible traffic withheld from the winning variant after rollout
- **Duration**: 6 weeks post-rollout
- **Purpose**: Confirm the activation lift is durable and not a novelty effect

## Analysis Plan

1. **Primary analysis**: Two-proportion z-test on 14-day activation rate. Report point estimate, 95% CI, and p-value.
2. **Guardrail checks**: One-sided tests confirming no degradation beyond thresholds.
3. **Pre-registered segments**:
   - Free vs. Pro plan signups
   - Mobile vs. desktop first session
4. **SRM check**: Chi-square test on variant assignment ratio. Threshold: p < 0.001 indicates pipeline issue — invalidate results.
5. **Post-hoc** (labeled exploratory): Funnel analysis on which guided tour steps have the highest drop-off.

## Decision Framework

| Outcome | Action |
|---------|--------|
| Primary wins, guardrails pass | Ship to 100%, maintain holdout |
| Primary wins, guardrail fails | Investigate the degraded guardrail, iterate on treatment |
| Primary neutral | Kill the experiment, extract learnings from funnel analysis |
| Primary loses | Kill the experiment, post-mortem on hypothesis |
