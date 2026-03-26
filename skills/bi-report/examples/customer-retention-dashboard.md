# BI Report: Customer Retention Dashboard

## Report Purpose

This report answers: "Are we retaining customers, and where are we losing them?" It supports the VP of Customer Success and Growth Product team in their weekly retention review. The primary use case is identifying cohorts with declining retention so the team can intervene before churn materializes.

## Metric Definitions

| Metric | Definition | Formula | Unit | Grain |
|--------|-----------|---------|------|-------|
| Monthly Retention Rate | Percentage of customers active at month start who remain active at month end | `(start_customers - churned_customers) / start_customers * 100` | % | Monthly |
| Net Revenue Retention | Revenue from existing customers this month vs. same cohort last month, including expansion and contraction | `(current_month_revenue - contraction + expansion) / prior_month_revenue * 100` | % | Monthly |
| Churn Rate | Percentage of customers who cancelled or did not renew | `churned_customers / start_of_month_customers * 100` | % | Monthly |
| Time to Churn | Median days from signup to cancellation for churned customers | `MEDIAN(cancelled_at - created_at) WHERE status = 'cancelled'` | Days | Rolling 90d |
| Reactivation Rate | Percentage of churned customers who return within 90 days | `reactivated_90d / churned_total * 100` | % | Monthly |

**Includes/excludes**: Churn excludes customers on seasonal pause. Trial users who never converted are excluded from all metrics. Downgrades count as contraction in NRR but not as churn.

## Data Source Mapping

| Metric | Source Table(s) | Key Columns | Join Logic | Known Issues |
|--------|----------------|-------------|------------|-------------|
| Retention Rate | `analytics.customer_monthly_snapshot` | `customer_id`, `is_active`, `snapshot_month` | None | Snapshot runs at 02:00 UTC; customers cancelling after midnight appear in next month |
| NRR | `billing.invoices`, `billing.subscriptions` | `customer_id`, `amount`, `period_start` | Join on `customer_id` + `period_start` month | Refunds posted mid-month reduce NRR retroactively |
| Churn Rate | `crm.customers`, `billing.cancellations` | `customer_id`, `cancelled_at`, `reason` | Join on `customer_id` | "Reason" field is free-text; ~15% are blank |

## Filters and Parameters

| Filter | Type | Default | Options | Behavior |
|--------|------|---------|---------|----------|
| Date Range | Date picker | Last 12 months | Any range, max 24 months | Applies to all metrics |
| Plan Tier | Multi-select | All | Free, Starter, Pro, Enterprise | Filters underlying data |
| Signup Cohort | Month picker | None | Any month | Overlays cohort curve on retention chart |
| Region | Multi-select | All | NA, EMEA, APAC | Filters all panels |

## Layout

1. **KPI cards** — Retention Rate, NRR, Churn Rate, Reactivation Rate. Current month value, month-over-month delta, 3-month trend sparkline.
2. **Retention curve** — Line chart showing month-N retention by signup cohort. X-axis: months since signup (0-12). Y-axis: % retained. One line per cohort, highlight selected cohort.
3. **NRR waterfall** — Stacked bar showing starting revenue, expansion, contraction, churn, and ending revenue for the selected period.
4. **Churn reason breakdown** — Horizontal bar chart of top 10 cancellation reasons. Clicking a reason filters the detail table.
5. **Customer detail table** — Filterable table: customer name, plan, MRR, tenure, health score, last login. Sortable. Export to CSV.

## Drill-Down Paths

```
Retention KPI Card → Retention by Plan Tier (bar) → Cohort Curve for Selected Tier → Customer List → Individual Customer Record
Churn Rate Card → Churn by Reason (bar) → Customers with That Reason (table) → Customer Detail Page in CRM
```

## SQL Example — Monthly Retention Rate

```sql
WITH monthly AS (
  SELECT snapshot_month,
         COUNT(*) FILTER (WHERE is_active) AS active_end,
         COUNT(*) AS active_start
  FROM analytics.customer_monthly_snapshot
  WHERE snapshot_month BETWEEN :start_date AND :end_date
  GROUP BY snapshot_month
)
SELECT snapshot_month,
       ROUND(active_end::numeric / active_start * 100, 2) AS retention_rate
FROM monthly
ORDER BY snapshot_month;
```

## Refresh Schedule

| Data Source | Refresh Frequency | Method | SLA | Failure Handling |
|------------|-------------------|--------|-----|-----------------|
| `analytics.customer_monthly_snapshot` | Daily at 03:00 UTC | Incremental | Available by 03:30 UTC | Retry 3x, alert #data-ops on failure; stale-data badge on dashboard |
| `billing.invoices` | Every 4 hours | CDC stream | 15-minute lag | Lag counter shown in footer |
| `crm.customers` | Daily at 02:00 UTC | Full sync | Available by 02:45 UTC | Previous day's snapshot used; warning banner displayed |
