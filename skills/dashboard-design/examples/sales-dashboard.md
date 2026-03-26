# Dashboard Design: Sales Team Dashboard

## Key Questions This Dashboard Answers

1. Are we on track to hit this quarter's revenue target?
2. Which reps are ahead or behind their individual quotas?
3. Where are deals stalling in the pipeline?
4. How has win rate trended over the past 6 months?
5. Which lead sources produce the highest-value closed deals?

## 1. KPI Bar (Top Row)

```
[ Closed Revenue     ]  [ Pipeline Value      ]  [ Win Rate          ]  [ Avg Deal Cycle    ]  [ Quota Attainment  ]
[ $2.4M              ]  [ $8.1M               ]  [ 34%               ]  [ 42 days           ]  [ 78%               ]
[ +18% vs last Q     ]  [ -5% vs last month   ]  [ +3pts vs last Q   ]  [ -4 days vs last Q ]  [ Target: 100%      ]
[ [sparkline up]     ]  [ [sparkline flat]    ]  [ [sparkline up]    ]  [ [sparkline down]  ]  [ [progress bar]    ]
```

- Ordered left-to-right by importance: revenue first, attainment last (it is derived from revenue vs target).
- Each card shows: metric name, current value, comparison, and a sparkline or progress bar.
- "Pipeline Value" turning red when it drops below 3x the remaining quota gap.

## 2. Chart Selection

| Question | Chart Type | Title (phrased as question) |
|----------|-----------|----------------------------|
| Are we on track this quarter? | Area chart with target line overlay | "How is closed revenue tracking against our quarterly target?" |
| Which reps are ahead or behind? | Horizontal bar chart, sorted by attainment % | "Where does each rep stand against their quota?" |
| Where are deals stalling? | Funnel chart with stage-to-stage conversion rates | "Where are deals dropping out of the pipeline?" |
| How has win rate changed? | Line chart, 6-month trend, monthly granularity | "How has our win rate trended over the past 6 months?" |
| Which sources produce the best deals? | Horizontal bar chart, sorted by avg deal size | "Which lead sources generate the highest-value closed deals?" |

## 3. Visual Hierarchy

**Top row**: KPI bar (5 cards). Answers "are we on track?" in 5 seconds.

**Middle section (2 columns)**:
- Left (60% width): Revenue vs target area chart (primary question)
- Right (40% width): Rep attainment horizontal bar chart

**Bottom section (2 columns)**:
- Left (50% width): Pipeline funnel with conversion rates between stages
- Right (50% width): Win rate trend line chart

**Detail panel (expandable)**: Lead source performance table with sortable columns (source, deal count, avg deal size, win rate, total revenue). Accessible via "View details" link below the funnel chart.

## 4. Filters and Interactivity

**Global filters (top bar, affects all charts)**:
- Date range: Preset options (This quarter, Last quarter, Last 6 months, Custom). Default: current quarter.
- Team: All teams, or filter to a specific sales team. Default: all.
- Region: North America, EMEA, APAC, All. Default: all.

**Cross-filtering**:
- Clicking a rep's bar in the attainment chart filters all other charts to that rep's deals.
- Clicking a funnel stage shows a deal list panel with deal name, value, days in stage, and next action.

**Drill-down paths**:
- KPI card click: Opens a detail modal with the metric's weekly breakdown for the period.
- Rep bar click: Navigates to that rep's individual pipeline view.
- Funnel stage click: Shows filterable deal table for that stage.

**Filter rules**:
- Active filters display as removable chips below the filter bar.
- When filters reduce a chart to zero data, display "No deals match these filters" with a "Clear filters" link.

## 5. Data Formatting Standards

| Metric | Format | Null Handling |
|--------|--------|---------------|
| Revenue / deal value | `$X.XM` above $1M, `$XXX.XK` above $1K, exact below | "No data" (not $0) |
| Percentages (win rate, attainment) | Whole number + `%` (e.g., 34%) | "N/A" |
| Deal cycle days | Whole number + "days" (e.g., 42 days) | "--" |
| Dates | "MMM d, yyyy" (e.g., Mar 19, 2026) | -- |

**Color rules**:
- Green: at or above target. Red: below target. Applied only to KPI comparison indicators and the target line.
- Pipeline funnel uses sequential blue shades (darkest at top), not traffic-light colors.
- All color-coded information also has a text label or icon — never color alone.
- Palette is colorblind-safe (tested with deuteranopia and protanopia simulators).

**Data refresh**: Pipeline data updates every 15 minutes from the CRM sync. KPIs recalculate on each page load. Last-refreshed timestamp shown in the dashboard footer.
