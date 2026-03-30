-- monthly-retention-rate.sql
--
-- Calculates monthly customer retention rate.
--
-- Retention rate = customers active in both month N-1 and month N
--                  divided by customers active in month N-1.
--
-- Assumptions:
--   - A customer is "active" in a month if they have at least one
--     qualifying event (order, login, subscription payment, etc.)
--     during that month.
--   - Adjust the source table and activity definition to match your
--     data model.
--
-- Parameters to customize:
--   - Source table: Replace `events.customer_activity` with your table
--   - Activity filter: Adjust the WHERE clause for what counts as "active"
--   - Date range: Modify the WHERE clause to limit the analysis window
--   - Customer ID: Replace `customer_id` with your unique identifier

WITH monthly_active AS (
    -- Step 1: Identify distinct active customers per month
    SELECT
        DATE_TRUNC('month', activity_date)::date AS activity_month,
        customer_id
    FROM events.customer_activity
    WHERE activity_type IN ('purchase', 'subscription_payment')  -- Define what "active" means
      AND activity_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '13 months')  -- Last 13 months for 12 months of retention
    GROUP BY 1, 2
),

retention_pairs AS (
    -- Step 2: Join each month with the previous month to find retained customers
    SELECT
        curr.activity_month AS current_month,
        COUNT(DISTINCT prev.customer_id) AS retained_customers,
        COUNT(DISTINCT curr.customer_id) AS current_customers
    FROM monthly_active curr
    LEFT JOIN monthly_active prev
        ON curr.customer_id = prev.customer_id
        AND curr.activity_month = prev.activity_month + INTERVAL '1 month'
    GROUP BY 1
),

previous_month_counts AS (
    -- Step 3: Get the customer count for each month (to use as the denominator)
    SELECT
        activity_month,
        COUNT(DISTINCT customer_id) AS total_customers
    FROM monthly_active
    GROUP BY 1
)

-- Step 4: Calculate retention rate
SELECT
    rp.current_month,
    pmc.total_customers AS previous_month_customers,
    rp.retained_customers,
    rp.current_customers,
    rp.current_customers - rp.retained_customers AS new_customers,
    CASE
        WHEN pmc.total_customers = 0 THEN NULL  -- Avoid division by zero
        ELSE ROUND(
            (rp.retained_customers::numeric / pmc.total_customers) * 100,
            1
        )
    END AS retention_rate_pct,
    CASE
        WHEN pmc.total_customers = 0 THEN NULL
        ELSE ROUND(
            ((pmc.total_customers - rp.retained_customers)::numeric / pmc.total_customers) * 100,
            1
        )
    END AS churn_rate_pct
FROM retention_pairs rp
JOIN previous_month_counts pmc
    ON rp.current_month = pmc.activity_month + INTERVAL '1 month'
WHERE rp.current_month > (SELECT MIN(activity_month) FROM monthly_active)  -- Skip first month (no prior month to compare)
ORDER BY rp.current_month;

-- Expected output columns:
--   current_month           | The month being measured
--   previous_month_customers| Customers active in the prior month (denominator)
--   retained_customers      | Customers active in both months
--   current_customers       | Total customers active in the current month
--   new_customers           | Customers active in current month but not prior
--   retention_rate_pct      | (retained / previous) * 100
--   churn_rate_pct          | ((previous - retained) / previous) * 100
--
-- Notes:
--   - retention_rate_pct + churn_rate_pct = 100% (for the prior month's cohort)
--   - NULL values appear when the previous month had zero customers
--   - This measures logo retention (customer count), not revenue retention
--   - For net revenue retention (NRR), replace customer counts with revenue sums
