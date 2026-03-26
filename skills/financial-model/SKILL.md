---
name: financial-model
description: Build financial models for business cases — with revenue projections, cost structures, unit economics, DCF analysis, and scenario modeling that make assumptions explicit and outcomes testable.
metadata:
  displayName: "Financial Model"
  categories: ["business"]
  tags: ["finance", "modeling", "DCF", "unit-economics", "projections", "business-case"]
  worksWellWithAgents: ["cto-advisor", "financial-analyst", "pricing-strategist"]
  worksWellWithSkills: ["metrics-framework", "prd-writing"]
---

# Financial Model

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What is the business case?** (New product launch, expansion, investment decision, fundraising)
2. **What is the time horizon?** (12 months, 3 years, 5 years)
3. **What is the revenue model?** (Subscription, transactional, marketplace, usage-based, hybrid)
4. **What are the key cost drivers?** (Headcount, infrastructure, CAC, COGS)
5. **What assumptions exist?** (Growth rates, conversion rates, churn, pricing, market size)
6. **Who is the audience?** (Board, investors, internal leadership, lending institution)

If the user says "just give me a spreadsheet," push back: a model without documented assumptions is a fiction generator. Every number must trace to an assumption the reader can challenge.

## Financial model template

### 1. Assumptions Table

List every assumption explicitly. Each must have a source and confidence level.

```
| Assumption               | Value     | Source                      | Confidence |
|--------------------------|-----------|------------------------------|------------|
| Monthly growth rate      | 8%        | Last 6 months average        | High       |
| Gross margin             | 72%       | Current P&L                  | High       |
| CAC (blended)            | $340      | Marketing spend / new custs  | Medium     |
| Monthly churn rate       | 3.2%      | Cohort analysis (Q3-Q4)      | High       |
| Average contract value   | $1,200/yr | Sales data                   | High       |
```

Rules: assumptions with "Low" confidence must appear in sensitivity analysis. Never bury assumptions inside formulas.

### 2. Revenue Projections

Build revenue bottom-up from unit economics, not top-down from market share.

```
| Metric              | Month 1  | Month 6  | Month 12 | Month 24 | Month 36 |
|---------------------|----------|----------|----------|----------|----------|
| New customers       | 50       | 85       | 145      | 310      | 525      |
| Churned customers   | 8        | 22       | 48       | 95       | 155      |
| Active customers    | 200      | 420      | 780      | 1,650    | 2,850    |
| ARPU (monthly)      | $100     | $105     | $112     | $120     | $128     |
| MRR                 | $20,000  | $44,100  | $87,360  | $198,000 | $364,800 |
```

Show the formula for each row. MRR = Active customers x ARPU. Active customers = prior active + new - churned.

### 3. Cost Structure

Break costs into fixed and variable. Variable costs must link to a driver.

```
| Cost Category      | Type     | Driver             | Month 1  | Month 12 | Month 36 |
|--------------------|----------|--------------------|----------|----------|----------|
| Engineering team   | Fixed    | Headcount plan     | $85,000  | $120,000 | $200,000 |
| Cloud infra        | Variable | Per active customer| $4,000   | $15,600  | $57,000  |
| Sales & marketing  | Variable | CAC x new custs    | $17,000  | $49,300  | $178,500 |
| G&A                | Fixed    | Baseline ops       | $15,000  | $22,000  | $35,000  |
```

### 4. Unit Economics

```
| Metric                         | Current | Month 12 | Healthy Benchmark |
|--------------------------------|---------|----------|-------------------|
| CAC                            | $340    | $340     | < LTV/3           |
| LTV (gross margin / churn)     | $2,250  | $2,625   | > 3x CAC          |
| LTV:CAC ratio                  | 6.6x   | 7.7x     | > 3x              |
| CAC payback (months)           | 3.4    | 3.2      | < 12 months       |
| Gross margin                   | 72%    | 74%      | > 65% (SaaS)      |
```

Flag any metric outside healthy benchmarks. If LTV:CAC is below 3x, the business case is weak regardless of revenue projections.

### 5. Scenario Analysis

Model three scenarios minimum. Vary the assumptions with lowest confidence.

```
| Metric (Month 36)  | Bear Case  | Base Case  | Bull Case  |
|---------------------|------------|------------|------------|
| Growth rate         | 5%/mo      | 8%/mo      | 12%/mo     |
| Churn rate          | 4.5%       | 3.2%       | 2.0%       |
| Active customers    | 1,400      | 2,850      | 5,200      |
| ARR                 | $2.15M     | $4.38M     | $7.98M     |
| Cash position       | -$800K     | $1.2M      | $4.5M      |
```

Name what changes between scenarios. "Bear case" is not useful — "bear case: growth drops to 5% and churn increases to 4.5%" tells the reader what to watch for.

### 6. Cash Flow and Runway

Highlight the month cash reaches zero under bear case. If runway is under 6 months in any scenario, flag it as a critical risk. Include quarterly revenue, costs, net cash flow, cumulative cash balance, and remaining runway in months.

## Quality checklist

Before delivering a financial model, verify:

- [ ] Every number traces to a named assumption with a source
- [ ] Revenue is built bottom-up from unit economics, not top-down from TAM
- [ ] Cost structure separates fixed from variable with explicit drivers
- [ ] Unit economics include LTV, CAC, LTV:CAC ratio, and payback period
- [ ] At least 3 scenarios are modeled with named assumption changes
- [ ] Cash flow projection includes runway calculation
- [ ] The model audience (investors, board, internal) is reflected in the level of detail

## Common mistakes

- **Top-down revenue.** "We will capture 1% of a $10B market" is not a model. Build from units: customers x price x retention.
- **Static assumptions.** Growth rates, churn, and costs change over time. A model with constant 10% monthly growth for 5 years is fantasy.
- **Ignoring cash timing.** Revenue recognized is not cash received. Annual contracts paid monthly and net-60 invoices create cash gaps the P&L hides.
- **Single scenario.** One projection is a guess. Three scenarios with named variables show you understand the risk space.
- **Vanity unit economics.** Calculating LTV with gross revenue instead of gross margin inflates the numbers. Use gross-margin-based LTV.
- **Missing the "so what."** A model without a recommendation is a data dump. State the decision it supports.
