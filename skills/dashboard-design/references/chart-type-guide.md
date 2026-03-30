# Chart Type Guide

Decision framework for matching data questions to the right visualization. Every chart on a dashboard must answer a specific question -- if it does not, remove it.

## Question-to-Chart Mapping

### How has X changed over time?

**Use:** Line chart (continuous data) or vertical bar chart (discrete periods).

- Line chart: best for trends over many time points (daily revenue over 90 days).
- Bar chart: best for comparing discrete periods (monthly revenue, Q1 vs Q2).
- Area chart: acceptable when showing cumulative or stacked composition over time.

**Avoid:** Pie chart. Time is sequential -- pie slices have no inherent order.

### How does X compare across categories?

**Use:** Horizontal bar chart, sorted by value (largest at top).

- Horizontal bars are faster to read than vertical because labels are left-aligned and legible.
- Sort by value, not alphabetically, unless there is a natural order (e.g., age ranges).
- Limit to 10-15 categories. Beyond that, group the long tail into "Other."

**Avoid:** Radar chart (distorts comparison), 3D bar chart (perspective hides values), vertical bars with rotated labels (unreadable).

### What is the distribution of X?

**Use:** Histogram (continuous data) or box plot (comparing distributions across groups).

- Histogram: show the shape of the data -- normal, skewed, bimodal.
- Box plot: compare medians and spreads across 3+ groups side by side.
- Violin plot: acceptable when you need more distribution detail than a box plot.

**Avoid:** Pie chart with bucketed ranges (hides the distribution shape).

### What is the relationship between X and Y?

**Use:** Scatter plot. Add a trend line only if the correlation is meaningful.

- Color-code by a third categorical variable (max 5 categories).
- Size-code by a fourth numeric variable (bubble chart) -- but label the sizes.
- Use log scales if the data spans multiple orders of magnitude.

**Avoid:** Dual Y-axis chart. Two different scales on one chart lets the creator imply false correlations by adjusting axis ranges. Use two separate charts side by side instead.

### What is the composition of X?

**Use:** Stacked bar chart (few categories, < 6) or treemap (many categories).

- Stacked bar: best for showing part-to-whole over time or across groups.
- 100% stacked bar: best for comparing proportions when totals differ.
- Treemap: best for hierarchical composition (e.g., spending by department > team > project).

**Avoid:** Pie chart with more than 5 slices. Donut chart (same problem plus a hole that wastes space). Humans cannot accurately compare angles -- bar lengths are faster.

### Where does X happen?

**Use:** Choropleth map (regional aggregates) or heat map (density on a grid).

- Choropleth: best for data aggregated by region (revenue by state, users by country).
- Heat map: best for showing concentration patterns (clicks on a page, incidents by hour/day).
- Dot map: acceptable for individual locations when count is small (< 500 points).

**Avoid:** Pin maps with overlapping markers. Choropleth with more than one variable (use side-by-side maps).

### What is the ranking of X?

**Use:** Horizontal bar chart or lollipop chart, sorted descending.

- Lollipop chart: a lighter visual alternative to bar charts when there are many items.
- Bump chart: acceptable for tracking rank changes over time.

**Avoid:** Word cloud (sizes are imprecise), bubble chart for rankings (hard to compare circle areas).

## Anti-Patterns with Rationale

### Pie charts for comparison

**Problem:** Humans are poor at comparing angles. A 28% slice vs. a 32% slice looks nearly identical.

**Fix:** Horizontal bar chart. The length difference is immediately visible.

**Exception:** Pie charts are acceptable only for showing a simple 2-3 part split where the proportions are obvious (e.g., 75% / 25%).

### Dual Y-axes

**Problem:** Two independent scales on one chart can be manipulated to suggest any correlation. Stretching one axis makes lines converge or diverge at will.

**Fix:** Two charts side by side, same X-axis, independent Y-axes. Or normalize both metrics to the same scale (e.g., % change from baseline).

### 3D charts

**Problem:** Perspective distortion makes values unreadable. Back bars are occluded by front bars. The third dimension adds no data -- it is decorative.

**Fix:** Use 2D charts. Always.

### Truncated Y-axes

**Problem:** Starting the Y-axis at a value other than zero (for bar charts) exaggerates differences. A 2% change looks like a 50% change.

**Fix:** Start bar charts at zero. For line charts, truncation is acceptable when the focus is on change rather than absolute values -- but label the axis clearly.

### Too many series on one chart

**Problem:** More than 5 series on a line chart creates a "spaghetti chart" where no trend is readable.

**Fix:** Highlight 1-2 key series and gray out the rest, or use small multiples (one chart per series, shared axes).

### Color as sole encoding

**Problem:** 8% of men have red-green color vision deficiency. A chart that relies only on color to distinguish categories is inaccessible.

**Fix:** Combine color with pattern, label, or position. Use a colorblind-safe palette.
