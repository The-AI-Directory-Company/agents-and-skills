# Pricing Analysis: Gridline Developer API Platform

## Context

Gridline provides a geocoding and routing API for logistics companies. Currently on a single pay-as-you-go plan ($0.005/request). Evaluating a move to tiered pricing to improve revenue predictability and capture more value from high-volume customers.

## 1. Value Metric Assessment

| Candidate Metric  | Aligns with Value? | Predictable Cost? | Recommendation              |
|-------------------|--------------------|--------------------|------------------------------|
| Per API request   | High               | Low (spiky usage)  | Good base, but add volume tiers |
| Per seat/API key  | Low                | Yes                | Poor fit — one key can serve millions of calls |
| Per successful geocode | High          | Moderate           | Penalizes retries; avoid      |
| Monthly commit    | Moderate           | Yes                | Strong for mid-market + enterprise |
| Per vehicle tracked | High             | Yes                | Strong for routing product    |

**Selected:** Hybrid — monthly request commitment tiers with overage pricing. Aligns cost with value, gives customers predictable bills, and creates natural upgrade triggers.

## 2. Competitive Pricing Landscape

| Competitor       | Model            | Entry Price        | Mid-Tier          | Differentiator              |
|------------------|------------------|--------------------|--------------------|-----------------------------|
| MapStack         | Pay-as-you-go    | $0.007/request     | $0.004 at 1M/mo   | Market leader, broadest coverage |
| RouteWise        | Tiered monthly   | $49/mo (10K req)   | $299/mo (250K)     | Logistics-focused, fast routing  |
| OpenGeo          | Free / hosted    | $0 (self-host)     | $199/mo (managed)  | Free but ops-heavy              |
| Google Maps      | Pay-as-you-go    | $0.005/request     | $0.004 at 100K/mo  | Trusted brand, broad but generic |
| Status quo       | Internal tooling | Engineering time   | Engineering time   | "Free" but 2-3 FTE to maintain  |

**Opportunity:** RouteWise proves tiered pricing works in this market. Google and MapStack cluster at $0.004-0.007 PAYG. Gap exists for a mid-price tier with logistics-specific features (ETA, fleet constraints).

## 3. Willingness-to-Pay Analysis

| Data Source          | Method                                 | Finding                              |
|----------------------|----------------------------------------|--------------------------------------|
| Win/loss analysis    | CRM data, last 6 months (n=124)       | Price cited in 12% of losses; feature gaps in 48% |
| Customer interviews  | 8 interviews across segments           | Teams spending $200-800/mo consider switching at >$1,000 |
| Usage distribution   | Product analytics                      | Median customer: 85K req/mo; P90: 1.2M req/mo |
| Churn exit surveys   | Last 12 months (n=31)                  | 19% left for price; 42% for missing features |

**Key insight:** Price is not the primary churn driver. Customers are more sensitive to feature gaps than cost. This supports a packaging strategy that gates features by tier, not just volume.

## 4. Packaging and Tier Design

| Tier        | Target Segment          | Price            | Includes                             | Upgrade Trigger                   |
|-------------|------------------------|------------------|--------------------------------------|-----------------------------------|
| Starter     | Solo devs, prototyping | $0 (5K req/mo)  | Geocoding, basic routing             | Need >5K requests or batch API    |
| Growth      | Small logistics teams  | $79/mo (100K)   | + batch geocoding, webhooks, 48h support | Need >100K req or fleet routing |
| Business    | Mid-market fleets      | $349/mo (500K)  | + fleet routing, ETA, SLA, 4h support | Need >500K req or custom SLA     |
| Enterprise  | Large logistics cos    | Custom (2M+)    | + dedicated infra, 1h support, CSM   | Inbound only                     |

Overage: $0.004/request (Growth), $0.003/request (Business). No overage surprise — usage alerts at 80% and 100%.

## 5. Revenue Impact Model

| Scenario             | Avg Revenue/Customer | Conv. Rate | Customers (Y1) | ARR (Y1)  | vs. Current |
|----------------------|---------------------|------------|-----------------|-----------|-------------|
| Current (PAYG only)  | $4,080              | 6.2%       | 380             | $1.55M    | Baseline    |
| Proposed tiers       | $4,920              | 5.8%       | 355             | $1.75M    | +12.6%      |
| Aggressive (higher)  | $5,640              | 4.5%       | 275             | $1.55M    | +0% (volume drop offsets) |

**Assumptions:** Proposed tiers assume 15% of free users convert to Growth, 8% of Growth upgrade to Business within 12 months. Existing PAYG customers migrated with 6-month price lock at current effective rate.

**Existing customer impact:** 78% of current customers map to Growth tier at equal or lower effective cost. 14% see a 10-20% increase. 8% (enterprise-volume) see decreases via committed pricing.

## 6. Recommendation

```
Recommended pricing:  $79/mo (Growth), $349/mo (Business), custom Enterprise
Value metric:         Monthly request commitment with per-request overage
Rationale:            +12.6% ARR, within WTP range, 20-40% below MapStack at equivalent volume
Risk:                 Conversion rate on free-to-Growth is unvalidated
Migration risk:       14% of existing customers face increase — offer 6-month grace period
Next step:            A/B test new pricing page on 20% of new signups for 6 weeks
                      Measure: signup-to-paid conversion, 30-day retention, ARPU
```
