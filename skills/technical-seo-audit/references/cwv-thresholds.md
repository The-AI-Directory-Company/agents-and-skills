# Core Web Vitals Thresholds

Current thresholds for Core Web Vitals metrics as used by Google for page experience ranking signals. Use these when evaluating CWV in Section 3 of the audit template.

---

## Metric Thresholds

### Largest Contentful Paint (LCP)

Measures loading performance — how quickly the largest visible content element renders.

| Rating | Threshold (75th percentile) | Description |
|--------|---------------------------|-------------|
| **Good** | <= 2.5 seconds | Users perceive the page as loading quickly |
| **Needs Improvement** | > 2.5s and <= 4.0 seconds | Noticeable delay; users may lose patience |
| **Poor** | > 4.0 seconds | Users likely abandon; significant ranking impact |

**Common LCP elements:** Hero images, heading text blocks, video poster images, background images with text overlay.

**Common causes of poor LCP:**
- Unoptimized images (no compression, no responsive sizing, wrong format)
- Render-blocking CSS/JS delaying first paint
- Slow server response time (TTFB > 800ms)
- Client-side rendering where LCP content depends on JavaScript execution
- Web font loading blocking text render (FOIT)

---

### Interaction to Next Paint (INP)

Measures responsiveness — the latency of user interactions throughout the page lifecycle. Replaced FID (First Input Delay) as a Core Web Vital in March 2024.

| Rating | Threshold (75th percentile) | Description |
|--------|---------------------------|-------------|
| **Good** | <= 200 milliseconds | Interactions feel instant |
| **Needs Improvement** | > 200ms and <= 500 milliseconds | Noticeable lag; feels sluggish |
| **Poor** | > 500 milliseconds | Interactions feel broken; users may click repeatedly |

**Key difference from FID:** FID only measured the first interaction. INP measures all interactions throughout the page session and reports the worst (or near-worst) latency. A page can have good FID but poor INP.

**Common causes of poor INP:**
- Long JavaScript tasks blocking the main thread during interaction
- Excessive DOM size (> 1,500 elements) causing slow style/layout recalculation
- Large synchronous state updates in JavaScript frameworks
- Third-party scripts competing for main thread time
- Event handlers that trigger expensive reflows or repaints

---

### Cumulative Layout Shift (CLS)

Measures visual stability — how much the page content shifts unexpectedly during loading.

| Rating | Threshold (75th percentile) | Description |
|--------|---------------------------|-------------|
| **Good** | <= 0.1 | Minimal or no unexpected layout shifts |
| **Needs Improvement** | > 0.1 and <= 0.25 | Visible shifts that may cause misclicks |
| **Poor** | > 0.25 | Significant shifts; users click wrong elements or lose reading position |

**CLS is unitless.** It is calculated as: impact fraction x distance fraction. A large element shifting a small distance can produce the same score as a small element shifting a large distance.

**Common causes of poor CLS:**
- Images/videos without explicit width and height attributes
- Ads, embeds, or iframes without reserved space
- Dynamically injected content above existing content
- Web fonts causing text size changes (FOUT with size difference)
- Lazy-loaded content that pushes down existing elements

---

## Field Data vs. Lab Data

| Aspect | Field Data (CrUX) | Lab Data (Lighthouse, WebPageTest) |
|--------|-------------------|-----------------------------------|
| **What it measures** | Real user experiences on real devices and networks | Simulated experience on a controlled device and network |
| **Reported percentile** | 75th percentile across all page loads | Single test run (or averaged across runs) |
| **Availability** | Requires sufficient traffic (origin or URL level) | Always available — run on demand |
| **Covers INP** | Yes — captures all interactions across sessions | Limited — lab tools simulate specific interactions |
| **Update frequency** | Rolling 28-day window in CrUX; daily in Search Console | Instant (per test run) |
| **Best for** | Determining actual ranking impact; monitoring trends | Diagnosing specific issues; testing fixes before deploy |

### Which to Use

- **Always start with field data** if the site has enough traffic for CrUX data. This is what Google uses for ranking signals.
- **Use lab data to diagnose** specific issues identified in field data.
- **If field data is unavailable** (low-traffic site), lab data is the only option. Note this limitation in the audit — lab scores may not reflect real user experience.
- **Do not conflate them.** A Lighthouse score of 95 does not mean field CWV passes. Lab tests run on fast hardware with clean network conditions.

### Where to Find Field Data

| Source | Access | Granularity |
|--------|--------|-------------|
| Google Search Console | Requires site verification | URL groups by status |
| Chrome UX Report (CrUX) | Public BigQuery dataset or CrUX API | Origin-level and URL-level (if sufficient traffic) |
| PageSpeed Insights | No auth needed | Shows both field (CrUX) and lab (Lighthouse) data |
| `web-vitals` JavaScript library | Add to your site | Per-page, per-user real-time measurement |

---

## Threshold History

| Metric | Current Threshold | Previous | Change Date |
|--------|------------------|----------|-------------|
| LCP | 2.5s | — | May 2020 (launch) |
| INP | 200ms | N/A (replaced FID) | March 2024 |
| FID (retired) | 100ms | — | Retired March 2024 |
| CLS | 0.1 | — | May 2020 (calculation updated June 2021 to windowed approach) |

**Note on CLS calculation change:** Before June 2021, CLS accumulated all shifts over the entire page lifecycle. After the update, CLS uses a "session windows" approach — grouping shifts into windows with gaps, and reporting the maximum session window. This made CLS fairer for long-lived pages (e.g., SPAs, infinite scroll).
