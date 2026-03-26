# Financial Model: SaaS Expansion into APAC Market

## Business Case

NovaCRM (Series B, $18M ARR) is evaluating expansion of its sales-automation platform into the APAC market, starting with Australia and Singapore. The model covers a 36-month horizon and targets internal leadership for a go/no-go decision.

## 1. Assumptions Table

| Assumption                | Value       | Source                            | Confidence |
|---------------------------|-------------|-----------------------------------|------------|
| Monthly growth rate (APAC)| 6%          | Comparable competitor APAC launch | Medium     |
| Gross margin              | 68%         | Current P&L adjusted for support  | High       |
| CAC (APAC blended)        | $520        | US CAC x 1.3 (partner channel)   | Low        |
| Monthly churn rate        | 4.0%        | US churn + market maturity adj.   | Low        |
| Average contract value    | $960/yr     | US ACV discounted 20% for entry   | Medium     |
| Localization cost         | $340K       | Engineering estimate              | High       |
| Regional team cost        | $45K/mo     | 3 FTEs (sales, CS, marketing)     | High       |

## 2. Revenue Projections

| Metric              | Month 1 | Month 6  | Month 12 | Month 24  | Month 36  |
|---------------------|---------|----------|----------|-----------|-----------|
| New customers       | 20      | 35       | 60       | 105       | 180       |
| Churned customers   | 0       | 8        | 22       | 52        | 88        |
| Active customers    | 20      | 145      | 310      | 720       | 1,380     |
| ARPU (monthly)      | $80     | $80      | $84      | $88       | $92       |
| MRR                 | $1,600  | $11,600  | $26,040  | $63,360   | $126,960  |

Formulas: Active = prior active + new - churned. MRR = Active x ARPU. ARPU grows 5% annually via upsell.

## 3. Cost Structure

| Cost Category         | Type     | Driver                | Month 1   | Month 12  | Month 36  |
|-----------------------|----------|-----------------------|-----------|-----------|-----------|
| Regional team         | Fixed    | Headcount plan        | $45,000   | $55,000   | $85,000   |
| Cloud infrastructure  | Variable | $18/active customer   | $360      | $5,580    | $24,840   |
| Sales & marketing     | Variable | CAC x new customers   | $10,400   | $31,200   | $93,600   |
| Localization (amort.) | Fixed    | One-time / 24 months  | $14,167   | $14,167   | $0        |
| G&A allocation        | Fixed    | 8% of HQ G&A         | $6,000    | $7,200    | $9,600    |

## 4. Unit Economics

| Metric                       | Launch  | Month 12 | Healthy Benchmark |
|------------------------------|---------|----------|-------------------|
| CAC                          | $520    | $520     | < LTV/3           |
| LTV (gross margin / churn)   | $1,360  | $1,428   | > 3x CAC          |
| LTV:CAC ratio                | 2.6x   | 2.7x     | > 3x              |
| CAC payback (months)         | 6.5    | 6.2      | < 12 months       |
| Gross margin                 | 68%    | 70%      | > 65% (SaaS)      |

**Flag:** LTV:CAC ratio is below the 3x benchmark at launch. The model depends on churn improving from 4.0% to 3.0% by Month 18 to reach 3.2x. If churn stays at 4.0%, the expansion is marginally viable.

## 5. Scenario Analysis

| Metric (Month 36)     | Bear Case                        | Base Case                     | Bull Case                       |
|------------------------|----------------------------------|-------------------------------|---------------------------------|
| Assumption changes     | Growth 4%/mo, churn stays 4.0%  | Growth 6%/mo, churn drops 3%  | Growth 9%/mo, churn drops 2.5% |
| Active customers       | 680                              | 1,380                         | 2,450                           |
| ARR                    | $750K                            | $1.52M                        | $2.71M                          |
| Cumulative cash flow   | -$620K                           | +$380K                        | +$1.9M                          |
| Cash-flow positive     | Never (within 36 months)         | Month 22                      | Month 14                        |

## 6. Cash Flow and Runway

| Quarter | Revenue   | Costs     | Net Cash Flow | Cumulative Cash | Runway (months) |
|---------|-----------|-----------|---------------|-----------------|-----------------|
| Q1      | $18K      | $214K     | -$196K        | -$196K          | 15              |
| Q4      | $72K      | $268K     | -$196K        | -$680K          | 10              |
| Q8      | $198K     | $276K     | -$78K         | -$840K          | 8               |
| Q10     | $312K     | $298K     | +$14K         | -$780K          | Positive        |
| Q12     | $456K     | $348K     | +$108K        | +$380K          | Positive        |

Initial investment required: $900K. Bear-case runway hits zero at Month 28 without additional funding. Base case breaks even at Month 22.

## Recommendation

Proceed with APAC expansion contingent on two conditions: (1) secure $900K earmarked budget with board approval for bear-case loss of $620K, and (2) define a Month 12 checkpoint where churn must be at or below 3.5% to continue. If Month 12 churn exceeds 3.5%, trigger a wind-down plan to limit losses to $680K.
