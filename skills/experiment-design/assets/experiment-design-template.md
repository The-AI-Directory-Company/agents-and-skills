# Experiment Design: [Experiment Name]

**Author:** [Name]
**Date:** [YYYY-MM-DD]
**Status:** Draft | In Review | Approved | Running | Complete

---

## 1. Hypothesis

> If we [change],
> then [metric] will [direction] by at least [MDE],
> because [reasoning based on user behavior or data].

**Change description:** [1-2 sentences describing the treatment]

**Causal mechanism:** [Why you believe this change will produce the expected effect]

---

## 2. Metrics

| Role | Metric | Current Baseline | MDE | Direction |
|------|--------|-----------------|-----|-----------|
| Primary | | | | Increase / Decrease |
| Guardrail | | | | Must not degrade |
| Guardrail | | | | Must not degrade |
| Guardrail | | | | Must not degrade |

**Primary metric rationale:** [Why this metric, and not another, decides the experiment]

---

## 3. Sample Size

```
Baseline rate:              [e.g., 3.2%]
Minimum detectable effect:  [e.g., +0.5pp absolute, 15.6% relative]
Significance level (alpha): [e.g., 0.05, two-sided]
Power (1 - beta):           [e.g., 0.80]
Test type:                  [e.g., two-proportion z-test]
Tool used:                  [e.g., statsmodels, Evan Miller calculator]

Sample size per variant:    [N]
Total sample:               [N x variants]
```

---

## 4. Randomization

- **Unit:** [User / Session / Device / Cluster]
- **Method:** [Hash-based (deterministic) / Random draw]
- **Stickiness:** [How users stay in the same variant across sessions]
- **Split ratio:** [e.g., 50/50, 80/10/10]
- **Exclusions:** [Any users excluded from the experiment and why]

**Interaction risks:** [Does this experiment share traffic with other running experiments? If so, how is interaction handled?]

---

## 5. Runtime

```
Daily eligible traffic:     [N users/day]
Sample needed:              [Total N]
Raw runtime:                [N days]
Recommended runtime:        [N days, rounded to full weeks]
Maximum runtime:            [N days, to avoid novelty decay]
```

**Start date:** [YYYY-MM-DD]
**Planned end date:** [YYYY-MM-DD]

---

## 6. Stopping Rules

- [ ] **Do not peek** before planned sample size is reached (unless using sequential testing)
- [ ] **Stop for harm** if: [guardrail metric] degrades beyond [threshold]
- [ ] **No early stopping for success** under fixed-horizon design

**Sequential testing (if applicable):**
- Spending function: [e.g., O'Brien-Fleming]
- Interim analysis points: [e.g., 25%, 50%, 75% of sample]

---

## 7. Analysis Plan

*Written before the experiment starts. Do not modify after launch.*

1. **Primary analysis:** Compare treatment vs. control on [primary metric] using [test type]. Report point estimate, 95% CI, and p-value.
2. **Guardrail checks:** For each guardrail, confirm no degradation beyond threshold. Use one-sided tests.
3. **Pre-registered segments:**
   - Segment 1: [e.g., new vs. returning users]
   - Segment 2: [e.g., mobile vs. desktop]
   - Segment 3: [e.g., high-value vs. low-value]
4. **Multiple comparisons:** [Correction method if >2 variants, e.g., Bonferroni]
5. **SRM check:** Verify actual split matches intended ratio (chi-square, p < 0.001 threshold).

---

## 8. Holdout Plan

- **Holdout size:** [e.g., 5% of eligible traffic]
- **Duration:** [e.g., 4 weeks post-rollout]
- **Purpose:** Validate long-term impact, detect novelty effect decay

If no holdout: [Reason]

---

## 9. Results

*Fill in after the experiment concludes.*

```
Experiment:     [Name]
Dates:          [Start] - [End]
Variants:       [Control (X%) vs. Treatment (X%)]
Total users:    [N]

Primary metric: [Metric name]
  Control:      [Value] (n = [N])
  Treatment:    [Value] (n = [N])
  Difference:   [Absolute] ([Relative]%)
  95% CI:       [Lower, Upper]
  p-value:      [Value]

Guardrails:     [All passed / Details]
SRM check:      [p = X, pass/fail]
```

**Decision:** SHIP / ITERATE / KILL

**Rationale:** [1-2 sentences explaining the decision]

**Follow-up actions:** [Next steps based on the result]
