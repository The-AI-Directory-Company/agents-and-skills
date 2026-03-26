---
name: pricing-analysis
description: Conduct pricing analysis — evaluating competitive pricing, willingness-to-pay, packaging options, and revenue impact modeling to produce pricing recommendations with supporting data.
metadata:
  displayName: "Pricing Analysis"
  categories: ["business", "product-management"]
  tags: ["pricing", "analysis", "competitive", "willingness-to-pay", "revenue-modeling"]
  worksWellWithAgents: ["pricing-strategist", "vp-product"]
  worksWellWithSkills: ["experiment-design", "metrics-framework"]
---

# Pricing Analysis

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What are you pricing?** (New product, repricing, add-on feature, new tier)
2. **Who is the target customer?** (Persona, company size, budget authority)
3. **What is the current pricing?** (If repricing — model, tiers, average deal size)
4. **Who are the competitors?** (Direct competitors and public pricing, indirect alternatives)
5. **What is the value metric?** (What unit the customer pays for — seats, usage, projects)
6. **Do you have willingness-to-pay data?** (Surveys, win/loss data, sales feedback, churn reasons)
7. **What are the business constraints?** (Margin requirements, revenue targets, positioning)

If the user says "just tell me what to charge," push back: pricing without data on customer value perception, competitive landscape, and unit economics is guessing. This analysis produces a recommendation grounded in evidence.

## Pricing analysis template

### 1. Value Metric Assessment

Identify the unit of value that aligns price with customer outcomes. The right value metric scales with the value the customer receives.

```
| Candidate Metric | Aligns with Value? | Predictable Cost? | Recommendation     |
|------------------|--------------------|-------------------|--------------------|
| Per seat/user    | Moderate           | Yes               | Good default       |
| Per API call     | High               | Low (spiky)       | Consider caps      |
| Per project      | High               | Yes               | Strong for SMB     |
| Flat rate        | Low                | Yes               | Only if homogeneous|
| Per GB stored    | Moderate           | Moderate          | Common for infra   |
```

**Selection criteria:** The metric should scale with customer value (paying 10x = getting ~10x value). Customers must be able to predict their cost before committing. The metric must be explainable in one sentence — if sales cannot articulate it, deals stall.

### 2. Competitive Pricing Landscape

Map competitor pricing. Include direct competitors and the "do nothing" alternative.

```
| Competitor       | Model          | Entry Price | Mid-Tier    | Differentiator          |
|------------------|----------------|-------------|-------------|-------------------------|
| Competitor A     | Per seat/month | $29/seat    | $79/seat    | Market leader, full suite|
| Competitor B     | Usage-based    | Free tier   | $0.01/req   | Developer-focused        |
| Competitor C     | Flat rate      | $199/month  | $499/month  | All-inclusive, simple    |
| Open-source alt. | Self-hosted    | $0 (+ ops)  | $0 (+ ops)  | Free but costly to run   |
| Status quo       | Manual         | Staff time  | Staff time  | "Free" but slow          |
```

Note where competitors cluster and where gaps exist. Gaps can signal differentiation opportunities.

### 3. Willingness-to-Pay Analysis

Use available data to estimate price sensitivity.

```
| Data Source         | Method                              | Finding                          |
|---------------------|-------------------------------------|----------------------------------|
| Van Westendorp      | Survey: too cheap/cheap/expensive   | Acceptable range: $35-$75/user/mo|
| Win/loss analysis   | CRM data on deals won vs. lost      | Lost on price: 18% of losses    |
| Sales feedback      | AE interviews (n=8)                 | Price rarely an issue below $60  |
| Churn analysis      | Exit survey + cancellation data     | Price cited in 22% of churns     |
```

If WTP data is unavailable, flag this as a risk. Without it, any price recommendation is a hypothesis.

### 4. Packaging and Tier Design

Design tiers serving distinct segments with clear upgrade triggers.

```
| Tier       | Target Segment    | Price          | Upgrade Trigger                    |
|------------|-------------------|----------------|------------------------------------|
| Free       | Individual devs   | $0             | Need collaboration or >3 projects  |
| Team       | Small teams (5-20)| $49/user/month | Need SSO, audit logs, analytics    |
| Business   | Mid-market (20-100)| $89/user/month| Need SLAs, dedicated support       |
| Enterprise | Large orgs (100+) | Custom         | N/A — top tier                     |
```

**Rules:** Each tier needs a distinct target customer, not just more features at higher price. Upgrade triggers should be natural growth inflection points. Free tiers must demonstrate real value while creating conversion pressure. Limit to 4 tiers maximum.

### 5. Revenue Impact Model

Model the financial impact of the proposed pricing against alternatives.

```
| Scenario           | Avg Price | Conv. Rate | Customers (Y1) | ARR (Y1) | Notes                 |
|--------------------|-----------|------------|-----------------|----------|-----------------------|
| Current pricing    | $39/user  | 8%         | 400             | $780K    | Baseline              |
| Proposed pricing   | $49/user  | 7%         | 350             | $857K    | +10% ARR, -12% volume |
| Aggressive pricing | $69/user  | 5%         | 250             | $863K    | High churn risk       |
```

Model at least 3 scenarios. For each, estimate impact on acquisition, conversion, and churn. Highlight assumptions explicitly.

### 6. Recommendation

Synthesize findings into a clear recommendation with rationale, risks, and next steps.

```
Recommended pricing:  $49/user/month (Team), $89/user/month (Business)
Value metric:         Per seat, monthly billing with annual discount (20%)
Rationale:            Within WTP range, 25% below Competitor A, +10% ARR vs. current
Risk:                 Conversion rate assumption needs validation
Next step:            Pricing experiment on 10% of new signups for 4 weeks
```

## Quality checklist

Before delivering a pricing analysis, verify:

- [ ] Value metric is identified with rationale — not just defaulting to "per seat"
- [ ] Competitive landscape includes at least 3 competitors and the "do nothing" alternative
- [ ] Willingness-to-pay uses real data, or gaps in data are explicitly flagged as risks
- [ ] Tiers have distinct target segments and natural upgrade triggers
- [ ] Revenue impact model includes at least 3 scenarios with explicit assumptions
- [ ] Recommendation includes rationale, risks, and a validation plan
- [ ] Pricing aligns with positioning — premium pricing for a budget positioning is contradictory
- [ ] The analysis addresses both acquisition (new customer) and retention (existing customer) impact

## Common mistakes to avoid

- **Cost-plus pricing.** Customers pay for outcomes, not your infrastructure bill. Cost sets the floor — value sets the price.
- **Copying competitor pricing.** Matching a competitor assumes identical value proposition and cost structure. Price based on your value, positioned relative to competitors.
- **Too many tiers.** Three tiers plus enterprise custom is the proven pattern. More creates decision paralysis.
- **Artificial limitations on free tiers.** Crippling free tiers breeds resentment. Free should deliver real value — paid should deliver meaningfully more.
- **Ignoring existing customers during repricing.** A price increase that churns 20% of existing customers is a net loss. Model retention impact.
- **No validation plan.** Run pricing experiments on a subset first. Launching to 100% on day one is an all-or-nothing bet.
