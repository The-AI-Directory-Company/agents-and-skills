# Example: Product Ops Dashboard -- Incident & Uptime Monitoring

This example demonstrates the dashboard design template applied to a non-sales context: an engineering/product operations dashboard focused on system reliability and incident management.

## Inputs

1. **Audience:** Engineering managers and on-call leads
2. **Decisions supported:** Whether to allocate more engineering time to reliability, whether to change on-call staffing, whether to escalate recurring incident patterns
3. **Key questions:**
   - Are we meeting our SLA targets this month?
   - How has incident frequency changed over time?
   - Which services cause the most incidents?
   - How fast are we resolving incidents?
   - Are there recurring patterns in incident timing?
4. **Data source:** PagerDuty API + internal uptime monitoring, hourly refresh
5. **Viewed on:** Desktop monitors (1920x1080), occasional laptop (1440x900)

---

## Dashboard Design

### KPI Bar (Top Row)

```
[ Uptime: 99.94%       [ Incidents (MTD): 12    [ MTTR: 38 min         [ P1 Incidents: 2
  Target: 99.95%         vs last month: -3        vs last month: -12m    vs last month: +1
  Status: At Risk ]      Trend: Improving ]       Trend: Improving ]     Status: Watch ]
```

4 KPI cards, left to right by priority:

| Position | Metric | Format | Comparison | Trend |
|----------|--------|--------|-----------|-------|
| 1 (leftmost) | Monthly uptime % | 2 decimal places (99.94%) | vs SLA target (99.95%) | Sparkline, 30 days |
| 2 | Incident count MTD | Integer | vs same period last month | Arrow + delta |
| 3 | Mean Time to Resolve (MTTR) | Minutes | vs last month average | Arrow + delta |
| 4 | P1 (critical) incidents MTD | Integer | vs last month | Arrow + delta |

Color rules:
- Uptime >= target: green. Uptime < target but > target - 0.05%: yellow. Below that: red.
- MTTR improving (lower): green arrow. Worsening: red arrow.
- P1 count: red if higher than last month, green if lower.

### Middle Section: Primary Charts

**Chart 1: "How has incident frequency changed over the past 12 weeks?"**

- Type: Vertical bar chart, grouped by severity (P1, P2, P3)
- X-axis: Week (e.g., "Week of Jan 6")
- Y-axis: Incident count (start at 0)
- Colors: P1 = `#EE6677` (red), P2 = `#CCBB44` (yellow), P3 = `#4477AA` (blue)
- Interaction: Click a bar to filter the detail table below

**Chart 2: "Which services cause the most incidents?"**

- Type: Horizontal bar chart, sorted descending by total incidents (past 90 days)
- Y-axis: Service name
- X-axis: Incident count (start at 0)
- Color: Single color (`#4477AA`), highlight the selected service if cross-filtering is active
- Limit: Top 10 services. Group remainder into "Other (N services)"

**Chart 3: "When do incidents happen?"**

- Type: Heat map (day-of-week x hour-of-day)
- Y-axis: Monday through Sunday
- X-axis: 00:00 through 23:00
- Color: Sequential palette (`#EFF3FF` to `#08519C`), darker = more incidents
- Data: Past 90 days, count of incidents per cell
- Interaction: Hover shows exact count and top service for that time slot

### Bottom Section: Detail Table

**Incident Log**

| Column | Format | Sortable |
|--------|--------|----------|
| Date/Time | MMM DD, HH:MM | Yes (default: newest first) |
| Service | Text | Yes |
| Severity | P1 / P2 / P3 badge | Yes |
| Summary | Text, truncated to 80 chars | No |
| MTTR | Minutes (e.g., "38 min") | Yes |
| Status | Resolved / Investigating / Monitoring | Yes |
| Responder | Name | Yes |

- Paginated: 20 rows per page
- Cross-filtered by: severity bars (Chart 1), service bars (Chart 2), heat map cells (Chart 3)

### Filters

**Global filters (top bar):**
- Date range: Preset buttons (7d, 30d, 90d, Custom). Default: 30 days.
- Service: Multi-select dropdown. Default: All.
- Severity: Checkbox group (P1, P2, P3). Default: All selected.

**Filter state display:** Active filters shown as pills below the filter bar: "Last 30 days | All services | P1, P2, P3". When a filter reduces the data set, show: "Showing 12 of 47 incidents."

### Data Formatting Applied

| Metric | Format Rule |
|--------|-------------|
| Uptime percentage | 2 decimal places (99.94%) |
| Incident count | Integer, no abbreviation (range is 0-200) |
| MTTR | Minutes with no decimals under 60 min; "Xh Ym" above 60 min |
| Timestamps | MMM DD, HH:MM (timezone note in footer: "All times in UTC") |
| Missing MTTR (unresolved) | "--" (not 0 min) |
| Week with no incidents | Show bar at 0 height, do not skip the week |

---

## Why This Example Works

1. **Starts with questions, not data.** The five questions drive every chart choice.
2. **KPI bar tells the top-level story.** An engineering manager can glance at four numbers and know if reliability is on track.
3. **Chart types match questions.** Bar chart for comparison over time, horizontal bar for ranking, heat map for two-dimensional pattern detection.
4. **Cross-filtering connects views.** Clicking a service in Chart 2 filters Chart 1 and the detail table, enabling drill-down without a separate page.
5. **No decorative charts.** Every element ties to a decision: allocate reliability time, adjust on-call staffing, or escalate recurring patterns.
6. **Formatting is explicit.** MTTR for an unresolved incident is "--", not 0. The dashboard distinguishes between "resolved quickly" and "still open."
