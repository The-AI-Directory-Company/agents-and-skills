# Dashboard Formatting Standards

Consistent formatting rules for numbers, dates, null values, and color across all dashboard elements.

## Number Formatting

### Abbreviation Thresholds

| Raw Value Range | Display Format | Example |
|-----------------|---------------|---------|
| 0 -- 999 | Full number | 842 |
| 1,000 -- 99,999 | Full with separator | 12,345 |
| 100,000 -- 999,999 | Abbreviated with one decimal | 342.5K |
| 1,000,000 -- 999,999,999 | Abbreviated with one decimal | 1.2M |
| 1,000,000,000+ | Abbreviated with one decimal | 3.4B |

Rules:
- Drop the decimal if it is `.0` (show `12M` not `12.0M`).
- KPI cards use abbreviated format. Detail tables use full numbers.
- Currency always shows the symbol: `$1.2M`, `EUR 342.5K`.
- Percentages: one decimal place unless whole number (`12.3%`, `50%`). Never show more than one decimal in a dashboard context.
- Negative values: use a minus sign, not parentheses (`-$42K` not `($42K)`), unless the audience is finance professionals who expect accounting notation.

### Decimal Places by Metric Type

| Metric Type | Decimal Places | Example |
|-------------|---------------|---------|
| Currency (KPI card) | 0-1 | $1.2M |
| Currency (table row) | 2 | $1,234.56 |
| Percentage | 1 | 12.3% |
| Count / Integer | 0 | 45,231 |
| Rate / Ratio | 2 | 0.87 |
| Duration (seconds) | 1 | 2.4s |
| Duration (minutes+) | 0 | 14m, 2h 30m |

## Date Formats

Use a single date format consistently across the entire dashboard.

| Granularity | Format | Example |
|-------------|--------|---------|
| Year | YYYY | 2025 |
| Quarter | QN YYYY | Q1 2025 |
| Month | MMM YYYY | Jan 2025 |
| Week | Week of MMM DD | Week of Jan 6 |
| Day | MMM DD, YYYY | Jan 15, 2025 |
| Hour | MMM DD HH:00 | Jan 15 14:00 |
| Relative (recent) | "2h ago", "Yesterday" | Acceptable in real-time dashboards only |

Rules:
- Never mix formats on one dashboard (e.g., "January 2025" in one chart and "2025-01" in another).
- X-axis date labels: use the shortest unambiguous format for the granularity. Monthly chart: "Jan", "Feb". Yearly chart: "2023", "2024".
- Time zones: always display the timezone if the data spans multiple zones. Default to the viewer's local timezone with a note.

## Null and Missing Data Handling

| Context | How to Handle | Never Do |
|---------|---------------|----------|
| KPI card with no data | Display "No data" in muted text | Show $0 or 0% |
| Line chart with gap | Break the line (show gap) | Interpolate or connect across missing points |
| Bar chart with missing period | Show empty space with "No data" label | Skip the period (distorts timeline) |
| Table cell with no value | Display "--" or "N/A" | Leave blank (ambiguous: is it 0 or missing?) |
| Percentage change with no prior period | Display "N/A" | Show +100% or "New" |
| Division by zero | Display "N/A" | Show Infinity, NaN, or crash |

Rule: missing data and zero are different things. Zero means "we measured and the value is zero." Missing means "we have no measurement." Never conflate them.

## Colorblind-Safe Palette

Primary categorical palette (8 colors). Tested for deuteranopia, protanopia, and tritanopia using Coblis color blindness simulator.

| Index | Name | Hex | Use Case |
|-------|------|-----|----------|
| 1 | Blue | `#4477AA` | Primary series, default |
| 2 | Cyan | `#66CCEE` | Secondary series |
| 3 | Green | `#228833` | Positive / success |
| 4 | Yellow | `#CCBB44` | Warning / caution |
| 5 | Red | `#EE6677` | Negative / error |
| 6 | Purple | `#AA3377` | Tertiary series |
| 7 | Grey | `#BBBBBB` | Inactive / baseline |
| 8 | Dark teal | `#44AA99` | Quaternary series |

Source: Paul Tol's color schemes (personal.sron.nl/~pault/), widely used in scientific visualization and verified for color vision deficiency accessibility.

### Sequential Palette (for heat maps, choropleths)

Light to dark, single hue:

```
#EFF3FF → #BDD7E7 → #6BAED6 → #3182BD → #08519C
```

### Diverging Palette (for above/below target)

```
Red ← #D73027 → #FC8D59 → #FEE08B → #D9EF8B → #91CF60 → #1A9850 → Green
```

### Color Rules

1. **Never use color as the sole encoding.** Pair with labels, patterns, or position.
2. **Red/green only for unambiguous good/bad.** Revenue up = green is fine. "Tickets closed" up could be good (resolving) or bad (more issues). Use neutral colors when direction is ambiguous.
3. **Maximum 5-6 colors per chart.** Beyond that, use small multiples or group into "Other."
4. **Consistent color assignment.** If "Revenue" is blue on one chart, it must be blue on every chart on the same dashboard.
5. **Background-aware contrast.** All palette colors must have at least 3:1 contrast against the chart background (white or dark mode).
