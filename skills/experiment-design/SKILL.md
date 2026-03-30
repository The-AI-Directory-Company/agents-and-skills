---
name: experiment-design
description: Design rigorous A/B tests and product experiments — defining hypotheses, choosing metrics, calculating sample sizes, setting stopping rules, and writing analysis plans that avoid common statistical pitfalls.
metadata:
  displayName: "Experiment Design"
  categories: ["data", "product-management"]
  tags: ["a-b-testing", "experiments", "hypothesis", "sample-size", "statistics", "product-analytics"]
  worksWellWithAgents: ["data-scientist", "growth-engineer", "pricing-strategist", "product-analyst", "product-operations"]
  worksWellWithSkills: ["metrics-framework", "ml-model-evaluation", "prd-writing", "pricing-analysis", "prompt-engineering-guide"]
---

# Experiment Design

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What change are you testing?** (UI change, algorithm tweak, pricing model, new feature rollout)
2. **What outcome do you expect?** (Increase conversion, reduce churn, improve engagement — be specific)
3. **Who is the target population?** (All users, a segment, new users only, specific market)
4. **What is the current baseline?** (Current conversion rate, average revenue, retention rate — with approximate numbers)
5. **What is the minimum detectable effect (MDE)?** (Smallest improvement worth detecting — e.g., +2pp conversion, +5% revenue)
6. **What is the timeline?** (How long can the experiment run before a decision is needed?)
7. **Are there any constraints?** (Traffic volume, seasonality, regulatory requirements, shared infrastructure)

## Experiment design template

### 1. Hypothesis

State a falsifiable hypothesis in this format:

```
If we [change], then [metric] will [direction] by at least [MDE],
because [reasoning based on user behavior or data].
```

A hypothesis without a mechanism ("because") is a guess. The mechanism forces you to articulate why the change should work, which informs metric selection and interpretation.

### 2. Primary Metric + Guardrail Metrics

**Primary metric:** One metric that decides the experiment. Exactly one — not two, not "primary and secondary." If you cannot pick one, you do not understand the goal yet.

**Guardrail metrics:** 2-4 metrics that must not degrade. These protect against winning on the primary metric at the cost of something else.

| Role | Metric | Current Baseline | MDE | Direction |
|------|--------|-----------------|-----|-----------|
| Primary | Checkout conversion rate | 3.2% | +0.5pp | Increase |
| Guardrail | Revenue per user | $12.40 | -$0.50 | Must not decrease |
| Guardrail | Page load time (p95) | 1.8s | +200ms | Must not increase |
| Guardrail | Support ticket rate | 0.4% | +0.1pp | Must not increase |

### 3. Sample Size Calculation

Specify the inputs and the result:

```
Baseline rate:        3.2%
Minimum detectable effect: +0.5pp (absolute) → 3.7%
Significance level (alpha): 0.05 (two-sided)
Power (1 - beta):    0.80
Sample size per variant: ~14,750 users
Total sample:        ~29,500 users
```

State the formula or tool used (e.g., Evan Miller's calculator, statsmodels power analysis). If using a ratio metric or non-binomial outcome, note the test type (t-test, Mann-Whitney, etc.).

### 4. Randomization Unit

Define what gets randomized and how:

- **Unit:** User-level (most common), session-level, device-level, or cluster-level
- **Method:** Hash-based assignment (deterministic) vs. random draw (non-deterministic)
- **Stickiness:** Users must stay in the same variant across sessions. Specify how (user ID hash, cookie, backend assignment table)

Flag risks: if randomizing at user level but the feature affects shared resources (e.g., marketplace supply), consider cluster or switchback designs.

### 5. Runtime Estimation

```
Daily eligible traffic:    ~4,200 users
Sample needed:             29,500 users
Estimated runtime:         8 days (to reach sample size)
Recommended minimum:       14 days (to capture weekly seasonality)
Maximum runtime:           28 days (to avoid novelty effect decay)
```

Always round up to full weeks to account for day-of-week effects. If runtime exceeds 4 weeks, revisit the MDE — you may be trying to detect an effect too small to matter.

### 6. Stopping Rules

Define in advance when and how the experiment ends:

- **Do not peek** at results before the planned sample size unless using a sequential testing framework (e.g., group sequential design, always-valid p-values)
- **Stop early for harm:** If a guardrail metric degrades beyond a pre-defined threshold (e.g., revenue drops > 5%), stop the experiment regardless of primary metric
- **No early stopping for success** under fixed-horizon testing — a significant p-value at 40% of the sample does not mean the effect is real
- **If using sequential testing:** Specify the spending function (O'Brien-Fleming, Pocock) and planned interim analysis points

### 7. Holdout Groups

When the experiment will lead to a permanent rollout, reserve a holdout:

- **Size:** 5-10% of eligible traffic, withheld from the winning variant after rollout
- **Purpose:** Measure long-term impact, detect novelty effects wearing off, validate the experiment result in production
- **Duration:** Minimum 4 weeks post-rollout, ideally one full business cycle

If no holdout is planned, document why (e.g., regulatory requirement to treat all users equally).

### 8. Analysis Plan

Write this before the experiment starts — never after seeing results:

1. **Primary analysis:** Compare variant vs. control on the primary metric using [test type]. Report the point estimate, 95% confidence interval, and p-value.
2. **Guardrail checks:** For each guardrail, confirm the metric did not degrade beyond the threshold. Use one-sided tests where appropriate.
3. **Segmentation:** Pre-register 2-3 subgroup analyses (e.g., new vs. returning users, mobile vs. desktop). Segments chosen after seeing results are exploratory, not confirmatory.
4. **Multiple comparisons:** If running more than two variants, apply Bonferroni or Holm correction. State the adjusted alpha.
5. **Sample Ratio Mismatch (SRM) check:** Verify the actual split matches the intended ratio (chi-square test, p < 0.001 threshold). SRM invalidates the experiment.

### 9. Reporting Template

```
Experiment:    [Name]
Dates:         [Start] – [End]
Variants:      Control (50%) vs. Treatment (50%)
Total users:   [N]

Primary metric: Checkout conversion
  Control:     3.18% (n = 14,800)
  Treatment:   3.71% (n = 14,700)
  Difference:  +0.53pp (+16.7% relative)
  95% CI:      [+0.12pp, +0.94pp]
  p-value:     0.011

Guardrails:    All passed (see appendix)
SRM check:     p = 0.42 (no mismatch)
Decision:      SHIP / ITERATE / KILL
Rationale:     [1-2 sentences]
```

## Quality checklist

Before delivering an experiment design, verify:

- [ ] Hypothesis includes a falsifiable prediction and a causal mechanism
- [ ] Exactly one primary metric is defined — not a composite or a list
- [ ] Guardrail metrics cover revenue, performance, and user experience
- [ ] Sample size calculation includes all inputs (baseline, MDE, alpha, power)
- [ ] Randomization unit matches the unit of analysis (no user-level randomization with session-level metrics without correction)
- [ ] Runtime accounts for weekly seasonality (full-week increments)
- [ ] Stopping rules are defined before the experiment starts, not improvised mid-flight
- [ ] Analysis plan is pre-registered — subgroups and corrections specified in advance
- [ ] SRM check is included in the analysis plan

## Common mistakes to avoid

- **Peeking at results.** Checking significance daily and stopping when p < 0.05 inflates false positive rates to 20-30%. Use sequential testing if you need interim looks, or commit to a fixed horizon.
- **Underpowered tests.** Running an experiment "for a week" regardless of traffic. If you do not have enough sample to detect your MDE, the experiment will almost certainly show "no significant difference" — and you will learn nothing.
- **Multiple comparisons without correction.** Testing 5 variants against control at alpha = 0.05 gives a ~23% chance of at least one false positive. Apply Bonferroni (alpha / k) or use a hierarchical testing procedure.
- **Novelty effects.** New UI elements get extra attention simply for being new. If you measure a lift in week 1, it may vanish by week 3. Run experiments long enough and use holdout groups to validate durability.
- **Post-hoc segmentation as proof.** "It didn't win overall, but it won for mobile users in Germany" is not a valid conclusion — it is hypothesis generation. Pre-register segments or label post-hoc findings as exploratory.
- **Ignoring SRM.** If your 50/50 split is actually 51/49, something in the assignment or logging pipeline is broken. No amount of statistical analysis can fix corrupted randomization.
