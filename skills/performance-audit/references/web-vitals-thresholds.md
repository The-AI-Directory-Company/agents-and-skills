# Core Web Vitals Thresholds

Reference for current Google Core Web Vitals targets and the broader Web Vitals metrics suite.

## Core Web Vitals (CWV)

These three metrics are used by Google as ranking signals.

| Metric | Full Name | What It Measures | Good | Needs Improvement | Poor |
|--------|-----------|------------------|------|-------------------|------|
| LCP | Largest Contentful Paint | Time until the largest visible element (image, heading, video) finishes rendering | < 2,500 ms | 2,500 - 4,000 ms | > 4,000 ms |
| INP | Interaction to Next Paint | Worst-case latency between a user interaction (click, tap, keypress) and the next visual update | < 200 ms | 200 - 500 ms | > 500 ms |
| CLS | Cumulative Layout Shift | Total unexpected layout movement during the page lifespan (unitless score based on distance and impact fractions) | < 0.1 | 0.1 - 0.25 | > 0.25 |

**Note:** FID (First Input Delay) was retired as a Core Web Vital in March 2024, replaced by INP. Legacy reports may still reference FID < 100 ms.

## Other Web Vitals

These are not ranking signals but are critical for diagnosing performance issues.

| Metric | Full Name | What It Measures | Good Target |
|--------|-----------|------------------|-------------|
| TTFB | Time to First Byte | Time from navigation start until the first byte of the HTML response arrives | < 800 ms |
| FCP | First Contentful Paint | Time until the first text or image element is painted | < 1,800 ms |
| TBT | Total Blocking Time | Sum of all long-task blocking time (task duration minus 50 ms) between FCP and TTI | < 200 ms |
| TTI | Time to Interactive | Time until the page is fully interactive (no long tasks for 5 seconds) | < 3,800 ms |

## Measurement Percentile

Google evaluates CWV at the **75th percentile** of real user data. A page passes if the 75th percentile value is in the "Good" range. Do not optimize for the median -- target p75.

## Tools That Report These Metrics

### Lab Tools (synthetic, controlled environment)

| Tool | Metrics Reported | Notes |
|------|-----------------|-------|
| Lighthouse (Chrome DevTools) | LCP, CLS, TBT, FCP, TTI, TTFB | Simulated throttling; TBT is a lab proxy for INP |
| WebPageTest | LCP, CLS, TBT, FCP, TTFB, TTI | Real browser, configurable connection/location |
| PageSpeed Insights | LCP, INP, CLS + lab data | Combines field data (CrUX) with lab audit |

### Field Tools (real user monitoring)

| Tool | Metrics Reported | Notes |
|------|-----------------|-------|
| Chrome UX Report (CrUX) | LCP, INP, CLS, FCP, TTFB | 28-day rolling average from real Chrome users |
| Google Search Console | LCP, INP, CLS | Per-URL group status (Good / Needs Improvement / Poor) |
| `web-vitals` JS library | LCP, INP, CLS, FCP, TTFB, TBT | Drop-in script; send to any analytics endpoint |

### APM / RUM Platforms

Datadog RUM, New Relic Browser, Sentry Performance, and Vercel Analytics all report Core Web Vitals from real users with percentile breakdowns.

## Quick Reference: The Numbers to Remember

```
LCP   < 2.5 s     (largest paint)
INP   < 200 ms    (interaction responsiveness)
CLS   < 0.1       (layout stability)
TTFB  < 800 ms    (server response)
TBT   < 200 ms    (main-thread blocking)
```
