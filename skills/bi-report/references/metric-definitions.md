# Metric Definitions

Canonical definitions for common business metrics. Use these when defining metrics in Section 2 (Metric Definitions) of the BI report template. Every metric must have a precise definition before building a report.

---

## Monthly Recurring Revenue (MRR)

| Field | Definition |
|-------|-----------|
| **What it measures** | Predictable monthly revenue from active subscriptions |
| **Formula** | `SUM(monthly_subscription_amount) WHERE subscription_status = 'active' AND date = last_day_of_month` |
| **Unit** | Currency (USD, EUR, etc.) |
| **Grain** | Monthly snapshot (measured at month end) |
| **Includes** | Active subscriptions, upgraded amounts, prorated mid-month changes |
| **Excludes** | One-time fees, professional services, usage overages (unless contractually recurring), free/trial accounts, paused subscriptions |
| **Null handling** | Subscriptions with NULL amount are excluded and flagged as data quality issues. A customer with an active subscription and $0 amount (e.g., free tier) is excluded from MRR but tracked separately. |
| **Historical comparability** | If the definition changes (e.g., overages become recurring), document the change date and restate prior periods if possible. |

### MRR Components

| Component | Definition | Formula |
|-----------|-----------|---------|
| New MRR | Revenue from customers who subscribed this month | `SUM(amount) WHERE first_subscription_date IN current_month` |
| Expansion MRR | Revenue increase from existing customers (upgrades, add-ons) | `SUM(current_amount - previous_amount) WHERE current_amount > previous_amount AND customer existed in prior month` |
| Contraction MRR | Revenue decrease from existing customers (downgrades) | `SUM(previous_amount - current_amount) WHERE current_amount < previous_amount AND customer still active` |
| Churned MRR | Revenue lost from cancelled customers | `SUM(previous_amount) WHERE subscription_status changed to 'cancelled' in current month` |
| Net New MRR | Net change in MRR | `New MRR + Expansion MRR - Contraction MRR - Churned MRR` |

---

## Churn Rate

| Field | Definition |
|-------|-----------|
| **What it measures** | Percentage of customers lost during a period |
| **Formula** | `(customers_cancelled_in_period / customers_at_start_of_period) * 100` |
| **Unit** | Percentage (%) |
| **Grain** | Monthly |
| **Includes** | Customers whose subscriptions were cancelled or expired during the period (voluntary and involuntary) |
| **Excludes** | Customers who downgraded but remained active, customers who paused (if pause is a distinct status), trial users who never converted |
| **Null handling** | If `cancelled_at` is NULL for a customer whose status is 'cancelled', use the last activity date or flag as data quality issue. Never count NULL cancellation dates as non-churned. |
| **Historical comparability** | Involuntary churn (failed payment) vs. voluntary churn (customer-initiated) should be tracked separately when possible. Combining them masks different root causes. |

### Churn Variants

| Variant | Formula | When to Use |
|---------|---------|------------|
| Gross customer churn | `cancelled_customers / start_customers * 100` | Default; measures logo loss |
| Gross revenue churn | `churned_MRR / start_MRR * 100` | When customer value varies significantly |
| Net revenue churn | `(churned_MRR - expansion_MRR) / start_MRR * 100` | Shows whether expansion offsets losses (can be negative, which is good) |

---

## Net Revenue Retention (NRR)

| Field | Definition |
|-------|-----------|
| **What it measures** | Revenue retained and expanded from existing customers, expressed as a percentage of prior period revenue |
| **Formula** | `((start_MRR + expansion_MRR - contraction_MRR - churned_MRR) / start_MRR) * 100` |
| **Unit** | Percentage (%) |
| **Grain** | Monthly or annual (specify which) |
| **Includes** | All recurring revenue changes from customers who existed at the start of the period: upgrades, downgrades, and cancellations |
| **Excludes** | Revenue from new customers acquired during the period |
| **Null handling** | If start_MRR is zero (no existing customers), NRR is undefined — do not report as 0% or 100%. |
| **Historical comparability** | NRR is sensitive to the cohort definition. Ensure "existing customer" is defined consistently (e.g., subscribed before the first day of the period). |

### Benchmarks

| NRR Range | Interpretation |
|-----------|---------------|
| > 130% | Exceptional — strong expansion revenue from existing customers |
| 110-130% | Strong — expansion outpaces churn significantly |
| 100-110% | Healthy — expansion roughly offsets churn |
| 90-100% | Concerning — losing revenue from existing customers |
| < 90% | Critical — significant net revenue loss from existing base |

---

## Average Order Value (AOV)

| Field | Definition |
|-------|-----------|
| **What it measures** | Mean revenue per completed order |
| **Formula** | `SUM(order_revenue) / COUNT(DISTINCT order_id) WHERE order_status = 'completed'` |
| **Unit** | Currency (USD, EUR, etc.) |
| **Grain** | Daily, weekly, or monthly (specify which) |
| **Includes** | Completed orders with positive revenue, including discounted orders (at the discounted price) |
| **Excludes** | Cancelled orders, fully refunded orders, $0 orders (free samples, internal test orders), pending/processing orders |
| **Null handling** | Orders with NULL revenue are excluded and flagged. Orders with NULL status are excluded (do not assume "completed"). |
| **Historical comparability** | If the product mix changes significantly (e.g., launching a high-priced enterprise tier), segment AOV by product line to avoid misleading averages. |

### AOV Considerations

- **Partial refunds:** If an order is partially refunded, use the net revenue (original minus refund) in the AOV calculation.
- **Multi-currency:** Convert all orders to a base currency using the exchange rate at the time of the order, not the current rate.
- **Outliers:** Report both mean and median AOV. A few large enterprise orders can skew the mean significantly.
- **Segmentation:** AOV is most useful when segmented by channel, product line, or customer segment. A blended AOV across all segments often masks important patterns.

---

## General Metric Definition Checklist

When defining any metric for a BI report, ensure each of these fields is documented:

| Field | Question |
|-------|----------|
| **Name** | What is the metric called? (Use the same name everywhere — report, docs, meetings) |
| **Definition** | What does it measure in plain language? |
| **Formula** | Exactly how is it calculated? (SQL-level precision) |
| **Unit** | What unit is the result in? (%, USD, count, ratio) |
| **Grain** | At what time grain is it measured? (daily, weekly, monthly) |
| **Includes** | What is counted in the numerator/denominator? |
| **Excludes** | What is explicitly excluded? |
| **Null handling** | What happens when expected data is missing? |
| **Edge cases** | Division by zero, negative values, partial periods |
| **Source table(s)** | Where does the data come from? |
| **Historical comparability** | Has the definition changed? When? |
| **Owner** | Who is responsible for this metric's accuracy? |
