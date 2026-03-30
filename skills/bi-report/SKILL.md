---
name: bi-report
description: Design BI reports and analytics views — with metric definitions, data source mapping, filter logic, drill-down paths, and refresh schedules that enable self-service decision-making.
metadata:
  displayName: "BI Report"
  categories: ["data", "business"]
  tags: ["business-intelligence", "reports", "analytics", "SQL", "self-service"]
  worksWellWithAgents: ["bi-analyst", "data-analyst", "data-visualization-specialist", "product-analyst"]
  worksWellWithSkills: ["dashboard-design", "metrics-framework"]
---

# BI Report

## Before you start

Gather the following from the user before designing any report:

1. **What decision does this report support?** Name the specific business question. "How is revenue trending?" is a question. "Revenue dashboard" is not.
2. **Who is the audience?** Executives need summaries and trends. Analysts need drill-downs and raw data access. Operators need real-time alerts.
3. **What metrics matter?** List the 3-7 KPIs this report must answer. Every metric needs a precise definition before you build anything.
4. **What data sources exist?** Tables, schemas, APIs, or third-party systems. Confirm access and freshness.
5. **How often is the data needed?** Real-time, hourly, daily, weekly — this drives refresh strategy and cost.
6. **What filters and breakdowns are required?** Date range, region, product line, customer segment — define the dimensions.

If the user says "build me a sales report," push back: "What specific questions should this report answer? Who will use it and how often?"

## BI report design template

### 1. Report Purpose

Write 2-3 sentences:
- The business question this report answers
- The primary audience and how they will use it
- The cadence of use (daily standup, weekly review, monthly board meeting)

### 2. Metric Definitions

Define every metric precisely. Ambiguous metrics produce misleading reports.

| Metric | Definition | Formula | Unit | Grain |
|--------|-----------|---------|------|-------|
| Monthly Recurring Revenue | Sum of active subscription values at month end | `SUM(subscription_amount) WHERE status = 'active' AND date = last_day_of_month` | USD | Monthly |
| Churn Rate | Percentage of customers who cancelled in the period | `cancelled_customers / start_of_period_customers * 100` | % | Monthly |
| Average Order Value | Mean revenue per completed order | `SUM(revenue) / COUNT(DISTINCT order_id) WHERE status = 'completed'` | USD | Daily |

For each metric, specify:
- **Includes/excludes**: Does revenue include refunds? Does churn count downgrades?
- **Null handling**: What happens when a dimension value is missing?
- **Historical comparability**: Has the definition changed? Document when and how.

### 3. Data Source Mapping

| Metric | Source Table(s) | Key Columns | Join Logic | Known Issues |
|--------|----------------|-------------|------------|-------------|
| MRR | `billing.subscriptions` | `customer_id`, `amount`, `status`, `period_end` | None | Trial subscriptions have amount=0, exclude |
| Churn Rate | `billing.subscriptions`, `crm.customers` | `customer_id`, `cancelled_at` | Join on `customer_id` | Reactivated customers counted as new, not returning |

Document data freshness for each source — when was the last ETL run, what is the typical lag?

### 4. Filters and Parameters

| Filter | Type | Default | Options | Behavior |
|--------|------|---------|---------|----------|
| Date Range | Date picker | Last 30 days | Any range, max 1 year | Applies to all metrics |
| Region | Multi-select | All | NA, EMEA, APAC, LATAM | Filters underlying data, not just display |
| Product Line | Single-select | All Products | Product A, B, C | Changes all metrics to selected product |

Specify filter interactions: Does selecting a region also filter the product dropdown to products available in that region?

### 5. Layout and Visualizations

Describe each section of the report top-to-bottom:

1. **Summary bar** — KPI cards showing current value, period-over-period change (%), and trend arrow. Metrics: MRR, Churn Rate, New Customers, AOV.
2. **Trend chart** — Line chart of MRR over time with comparison period overlay. X-axis: date grain matching the filter. Y-axis: USD.
3. **Breakdown table** — Tabular view of all metrics broken down by the selected dimension (region, product, segment). Sortable on every column. Include sparklines for trend.
4. **Detail drill-down** — Clicking any row in the breakdown table opens a filtered view showing the individual records that compose that aggregate.

For each visualization, specify: chart type, axes, legend, color encoding, and what interaction (click, hover, filter) is supported.

### 6. Drill-Down Paths

Define how users navigate from summary to detail:

```
MRR Summary Card → MRR by Region (bar chart) → Region Detail Table → Individual Subscription Record
```

At each level, specify what filters carry forward and what new dimensions become available.

### 7. Refresh Schedule

| Data Source | Refresh Frequency | Method | SLA | Failure Handling |
|------------|-------------------|--------|-----|-----------------|
| `billing.subscriptions` | Every 6 hours | Incremental ETL | Data available by :30 past | Retry 3x, alert #data-ops after failure |
| `crm.customers` | Daily at 02:00 UTC | Full sync | Data available by 03:00 UTC | Stale data badge shown on report |

Specify what the user sees when data is stale — a timestamp, a warning banner, or a fallback to the last successful refresh.

## Quality checklist

Before delivering the report design, verify:

- [ ] Every metric has a precise written definition with includes/excludes
- [ ] Formulas are unambiguous — another analyst could reproduce the number from the formula alone
- [ ] Data sources are identified with table names, join logic, and known data quality issues
- [ ] Filters specify defaults, options, and cross-filter behavior
- [ ] Drill-down paths are defined from summary to the most granular level
- [ ] Refresh schedule includes SLA, failure handling, and staleness indicators
- [ ] The report answers the stated business question — not adjacent interesting questions
- [ ] Null and edge case handling is documented (zero-division, missing dimensions, partial periods)

## Common mistakes to avoid

- **Undefined metrics.** "Revenue" means different things to finance, sales, and product. Write the SQL-level definition. If two stakeholders disagree on the definition, that is a conversation to have before building the report, not after.
- **Too many metrics on one report.** A report with 20 KPIs answers no question well. Limit to 3-7 primary metrics that directly answer the stated business question. Link to secondary reports for everything else.
- **No drill-down path.** A summary number without the ability to investigate why it changed is useless. Every aggregate needs a path to the underlying records.
- **Ignoring data freshness.** Users will make decisions based on stale data if you do not make freshness visible. Always show the last-refreshed timestamp on the report.
- **Filters that mislead.** A date filter that only filters one chart but not another on the same report causes users to draw wrong conclusions. Document exactly what each filter affects.
