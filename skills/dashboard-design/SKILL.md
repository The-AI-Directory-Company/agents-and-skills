---
name: dashboard-design
description: Design effective data dashboards — choosing the right chart types, establishing visual hierarchy, defining KPI layouts, and creating interactive filters that help users answer questions without analyst support.
metadata:
  displayName: "Dashboard Design"
  categories: ["data", "design"]
  tags: ["dashboards", "data-visualization", "charts", "KPIs", "analytics"]
  worksWellWithAgents: ["bi-analyst", "data-scientist", "data-visualization-specialist", "product-analyst"]
  worksWellWithSkills: ["bi-report", "metrics-framework"]
---

# Dashboard Design

## Before you start

Gather the following from the user before designing:

1. **Who is the primary audience?** (Executive, manager, analyst, operator — each needs different density and interactivity)
2. **What decisions will this dashboard support?** (Not "what data do you want to see" but "what will you do differently based on this data")
3. **What are the 3-5 key questions this dashboard must answer?** (Every element must tie back to a question)
4. **What is the data source and refresh cadence?** (Real-time stream, hourly batch, daily ETL — this constrains layout)
5. **Where will it be viewed?** (Desktop monitor, laptop, TV wall, mobile, embedded in another tool)

If the user says "I want a dashboard with all our metrics," push back: "A dashboard that shows everything answers nothing. Which 3-5 questions should someone be able to answer in under 10 seconds?"

## Dashboard design template

### 1. Define the KPI bar

Place 3-5 headline metrics at the top of the dashboard. Each KPI card must include:

- **Metric name** in plain language (not column names like `mrr_net_new`)
- **Current value** with appropriate formatting (currency, percentage, count)
- **Comparison value** — period-over-period change or target attainment
- **Trend indicator** — directional arrow or sparkline for context

Layout rule: KPIs read left to right in order of importance. The leftmost metric is the one the viewer checks first.

```
[ Revenue: $1.2M  +12% vs last month ]  [ Active Users: 45.2K  -3% ]  [ NPS: 72  +5pts ]
```

### 2. Select chart types by question

Match each question to the right chart type. Use this decision framework:

| Question type | Chart type | Avoid |
|---|---|---|
| How has X changed over time? | Line chart (continuous) or bar chart (discrete periods) | Pie chart |
| How does X compare across categories? | Horizontal bar chart (ranked) | 3D charts, radar charts |
| What is the distribution of X? | Histogram or box plot | Pie chart with 10+ slices |
| What is the relationship between X and Y? | Scatter plot | Dual-axis charts (misleading scales) |
| What is the composition of X? | Stacked bar (few categories) or treemap (many) | Pie chart with >5 slices |
| Where does X happen? | Choropleth map or heat map | Pin maps with overlapping markers |

Rule: if you cannot justify why a chart type is better than a simple table for your data, use the table.

### 3. Establish visual hierarchy

Arrange the dashboard in an inverted pyramid:

- **Top row**: KPI bar — answers "are we on track?" in 5 seconds
- **Middle section**: 2-3 primary charts that answer the core questions — each with a clear title stating the question it answers
- **Bottom section**: Detail tables, drill-down views, or secondary charts

Title every chart as a question: "How has revenue trended this quarter?" not "Revenue Chart." The viewer should know what to look for before reading the data.

### 4. Design filters and interactivity

Define filters that let users slice data without building new charts:

- **Global filters** (top of dashboard): Date range, business unit, region — affect all charts simultaneously
- **Chart-level filters**: Applied to individual visualizations only — use sparingly to avoid confusion
- **Cross-filtering**: Clicking a bar in one chart filters related charts — state this behavior explicitly in design notes

Filter rules:
- Default to the most common view (current month, all regions)
- Show the active filter state visibly so users know what they are looking at
- Never hide data silently — if a filter excludes records, display the count of excluded items

### 5. Specify data formatting standards

Document these for every metric on the dashboard:

- **Number formatting**: Thousands separator, decimal places, abbreviations ($1.2M vs $1,200,000)
- **Date formatting**: Consistent across all charts (Q1 2025, Jan 2025, 2025-01)
- **Color usage**: Green/red only for good/bad when the direction is unambiguous. Use a colorblind-safe palette. Never encode meaning in color alone
- **Null/missing data**: Show gaps in line charts (do not interpolate), display "No data" in cards (not $0)

## Quality checklist

Before delivering the dashboard design, verify:

- [ ] Every chart answers one of the stated key questions — no decorative visualizations
- [ ] KPI bar is limited to 3-5 metrics with comparison values and trend indicators
- [ ] Chart types match the question type from the selection framework above
- [ ] Chart titles are phrased as questions, not labels
- [ ] Filters default to the most common view and show active filter state
- [ ] Color use is consistent, colorblind-safe, and never the sole means of conveying information
- [ ] Null and missing data are handled explicitly, not silently dropped or shown as zero
- [ ] The dashboard answers its core questions within 10 seconds of viewing

## Common mistakes

- **Starting with data instead of questions.** "We have this table, let's chart it" produces dashboards nobody uses. Start with decisions, then find the data.
- **Too many charts.** More than 6-8 visualizations on a single view creates cognitive overload. Split into tabs or linked dashboards if needed.
- **Pie charts for comparison.** Humans are poor at comparing angles and areas. Use horizontal bar charts for categorical comparison — they are faster to read and rank.
- **Dual Y-axes.** Two scales on one chart let you imply false correlations by adjusting axis ranges. Use two separate charts side by side instead.
- **Missing context on KPIs.** A number without a comparison is meaningless. "$1.2M revenue" says nothing. "$1.2M revenue, +12% vs last month, 96% of target" tells a story.
- **Ignoring mobile or TV display.** A dashboard designed for a 27-inch monitor is unreadable on a laptop. Specify the target viewport and test at that size.
