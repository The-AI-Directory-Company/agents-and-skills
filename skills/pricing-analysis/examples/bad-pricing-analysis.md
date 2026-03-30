# Bad Pricing Analysis Example

This is an example of a weak pricing analysis. Each section is annotated with what is wrong and why. Use this as a "what not to do" reference.

---

## The Analysis (as delivered)

### Pricing Recommendation for ProjectFlow

**Product:** ProjectFlow -- project management tool for teams
**Recommendation:** $29/user/month

#### How we got here

Our infrastructure costs are $8/user/month. We want a 70% margin, so:

$8 / (1 - 0.70) = $26.67, rounded up to $29/user/month.

We looked at competitors and this is in the same range:
- Asana: $10.99-24.99/user/month
- Monday.com: $9-19/user/month
- ClickUp: $7-12/user/month

Our product has more features than ClickUp so $29 seems fair.

#### Tiers

- Free: 3 users, 5 projects
- Pro: $29/user/month, unlimited everything
- Enterprise: Contact us

#### Expected Revenue

If we get 1% of the project management market ($7B TAM), that is $70M ARR.

---

## What Is Wrong

### Problem 1: Cost-plus pricing

**The mistake:** The entire pricing rationale is "our costs are $8, we want 70% margin, so we charge $29." This prices based on what it costs to deliver, not what customers are willing to pay.

**Why it matters:** Customers pay for outcomes (saving time, reducing errors, shipping faster), not for your server bill. A product that saves a team 10 hours/week could be worth $200/user/month regardless of whether infrastructure costs $2 or $20.

**What a good analysis does instead:** Starts with willingness-to-pay research (Van Westendorp survey, win/loss analysis, churn exit data) to find the price range customers will accept, then validates that the range is above the cost floor.

### Problem 2: No willingness-to-pay data

**The mistake:** There is zero customer data informing the price. No surveys, no win/loss analysis, no churn data, no sales feedback. The competitor comparison is the closest thing to market evidence, and it is superficial.

**Why it matters:** Without WTP data, the recommendation is a guess. The $29 price point could be leaving 50% of revenue on the table -- or it could be 40% above what the target segment will pay. There is no way to know.

**What a good analysis does instead:** Presents WTP findings from at least two data sources (survey + behavioral data), identifies the acceptable price range, and acknowledges uncertainty with scenario modeling.

### Problem 3: Superficial competitive comparison

**The mistake:** Lists three competitor prices without analyzing their positioning, target customer, packaging, or value metric. "Our product has more features than ClickUp so $29 seems fair" is not competitive analysis.

**Why it matters:** Asana at $24.99 targets enterprise teams with workflow automation. ClickUp at $7 targets budget-conscious small teams. These are different segments with different WTP. Listing their prices without segment context is meaningless.

**What a good analysis does instead:** Maps each competitor's target buyer, value proposition, pricing model, and positioning. Identifies where the pricing landscape has gaps and where it is crowded.

### Problem 4: Only two tiers (plus "contact us")

**The mistake:** Free and $29/user/month with nothing in between, and an enterprise tier with no pricing guidance. This forces a binary choice: free or $29.

**Why it matters:** A 5-person startup and a 200-person company have very different budgets and needs. A single paid tier at $29 either undercharges the 200-person company or overcharges the 5-person startup. The "contact us" enterprise tier with no pricing signals will deter mid-market buyers who want predictable costs.

**What a good analysis does instead:** Designs 3-4 tiers with distinct target segments and natural upgrade triggers. Each tier serves a different buyer, not just the same buyer with more features.

### Problem 5: Top-down revenue projection

**The mistake:** "1% of a $7B TAM = $70M ARR." This is not a revenue model -- it is a wish.

**Why it matters:** TAM-based revenue projections tell investors and leadership nothing about how you will actually acquire and retain customers. "1% market share" assumes penetration without explaining the mechanism.

**What a good analysis does instead:** Models revenue bottom-up: number of target customers in the segment x expected conversion rate x average deal size x retention rate. Then models 3 scenarios with different assumptions.

### Problem 6: No validation plan

**The mistake:** The analysis delivers a single price point with no plan to test whether it works. The implicit assumption is that $29 is the right answer, ship it to 100% of users.

**Why it matters:** Pricing is a hypothesis until validated. Launching a new price to all customers without testing is an all-or-nothing bet that risks churn (if too high) or leaves revenue on the table (if too low).

**What a good analysis does instead:** Proposes a pricing experiment: A/B test on 10-15% of new signups for 4-6 weeks, measuring conversion rate, activation rate, and 30-day retention. Defines success criteria before the test starts.

---

## Summary of Missing Elements

| Element | Present? | Impact |
|---|---|---|
| Willingness-to-pay data | No | Cannot validate any price point |
| Value metric analysis | No | Defaulted to per-seat without justification |
| Detailed competitive positioning | No | Surface-level price comparison only |
| Segment-specific tier design | No | Binary free/paid with no mid-market option |
| Bottom-up revenue model | No | TAM percentage is not a forecast |
| Scenario analysis | No | Single price point with no sensitivity |
| Validation plan | No | No way to test before full rollout |
| Retention impact analysis | No | No modeling of churn risk from price change |
