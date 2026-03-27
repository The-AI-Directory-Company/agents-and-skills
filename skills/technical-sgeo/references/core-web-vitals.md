# Core Web Vitals: Optimization Playbook

Core Web Vitals are a confirmed Google ranking factor and a direct signal of user experience quality. Sites with good CWV have higher engagement, lower bounce rates, and stronger authority signals — all of which also influence AI citation likelihood. AI systems learn from pages that users actually engage with.

## Metrics and thresholds

| Metric | Full Name | What It Measures | Good | Needs Work | Poor |
|--------|-----------|------------------|------|------------|------|
| LCP | Largest Contentful Paint | How fast the main content loads | < 2.5s | 2.5-4.0s | > 4.0s |
| INP | Interaction to Next Paint | How responsive the page is to input | < 200ms | 200-500ms | > 500ms |
| CLS | Cumulative Layout Shift | How much the layout shifts during load | < 0.1 | 0.1-0.25 | > 0.25 |

Google evaluates CWV at the 75th percentile of field data. Your worst 25% of page loads determine your score.

## Field data vs lab data

This distinction matters more than most people realize. Lighthouse 100 on your MacBook means nothing. Field data is the only truth.

**Field data** (Chrome User Experience Report / CrUX): Collected from real Chrome users on real devices and networks. Accessed via PageSpeed Insights, GSC Core Web Vitals report, or CrUX API. Google uses field data for ranking decisions.

**Lab data** (Lighthouse, WebPageTest): Simulated on a specific device and network profile. Useful for debugging but does not represent your actual users.

**When they disagree:** Field data always wins for ranking purposes. Common reasons for disagreement:
- Lab tests run on fast hardware and fast networks — real users may be on 3G phones
- Lab tests do not capture third-party script behavior under real conditions
- Lab tests run without cookies/state — real users trigger consent popups, personalization scripts
- Low-traffic sites may not have field data — note this limitation and use lab data as a proxy

**PageSpeed Insights API** (free, no key for basic requests):
```
GET https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&category=performance
```

Key response paths:
- `loadingExperience.metrics` — field data (CrUX)
- `lighthouseResult.audits` — lab data
- `loadingExperience.overall_category` — "FAST", "AVERAGE", or "SLOW"

Rate limit: ~25 requests per 100 seconds without an API key. Register a free API key for higher limits.

## LCP: root causes and fixes

LCP measures when the largest visible element finishes rendering. This is usually a hero image, a heading, or a video poster frame.

### Root causes

1. **Slow server response (TTFB > 800ms).** Everything downstream is delayed. Target TTFB under 800ms.
2. **Render-blocking resources.** CSS and synchronous JS in `<head>` delay rendering. The browser cannot paint until these load.
3. **Large hero images.** An unoptimized 2MB hero image downloaded over a mobile connection destroys LCP.
4. **Slow font loading.** If the LCP element is text and the font has not loaded, LCP is delayed.
5. **Client-side rendering.** If content is JS-rendered, LCP waits for JS download + parse + execute + API call + render.

### Fix patterns by framework

**Next.js:**
- Use `next/image` with `priority` prop on the LCP image (sets `fetchpriority="high"`, disables lazy loading)
- Use `next/font` with `display: 'swap'` — fonts are self-hosted and preloaded automatically
- Use Server Components (default in App Router) to reduce client JS bundle
- Enable `streaming` for SSR to send initial HTML faster

**WordPress:**
- Install an image optimization plugin (ShortPixel, Imagify, or Smush) — converts to WebP, resizes
- Use a caching plugin (WP Rocket or W3 Total Cache) for server-side page caching — reduces TTFB
- Add `fetchpriority="high"` to the hero image manually if theme does not do it
- Defer non-critical plugins that inject render-blocking CSS/JS

**Shopify:**
- Optimize theme images — Shopify's CDN serves WebP automatically but source images still matter
- Audit installed apps — each app can inject its own JS/CSS. Remove unused apps.
- Use `loading="eager"` and `fetchpriority="high"` on hero/banner images in theme code
- Minimize Liquid template complexity to reduce server render time

## INP: root causes and fixes

INP measures the latency between a user interaction (click, tap, keypress) and the next visual update. It captures the full lifecycle: input delay + processing time + presentation delay.

### Root causes

1. **Long main-thread tasks (> 50ms).** The browser cannot process input while running a long JavaScript task.
2. **Heavy JavaScript bundles.** Every KB of JS must be downloaded, parsed, and compiled. Large bundles delay interactivity.
3. **Unoptimized event handlers.** Click/scroll handlers that trigger expensive computations or synchronous layout.
4. **Third-party scripts.** Analytics, chat widgets, A/B testing tools, and tag managers compete for main thread time.

### Fixes

- Break long tasks with `scheduler.yield()` (modern) or `setTimeout(fn, 0)` (fallback). Let the browser process pending input between task chunks.
- Code-split aggressively. Load only the JS needed for the current page.
- Move heavy computations to Web Workers (runs off main thread).
- Defer non-critical third-party scripts: add `async` or `defer` attributes, or load them after user interaction.
- Use `requestIdleCallback` for low-priority work (analytics, prefetching).

### Chrome DevTools debugging workflow

1. Open DevTools > Performance panel
2. Enable "Web Vitals" lane
3. Record a trace while clicking buttons and interacting with the page
4. Look for long tasks (marked with red triangles) that overlap with interactions
5. Drill into the call stack to find the expensive function
6. The "Interactions" lane shows each INP candidate with its duration breakdown

## CLS: root causes and fixes

CLS measures unexpected layout shifts — elements moving after they have been rendered. Users hate this. So does Google.

### Root causes

1. **Images without dimensions.** Browser does not know the image size until it loads, then content below shifts.
2. **Dynamically injected content.** Ads, cookie banners, notification bars pushed into the viewport after initial render.
3. **Late-loading fonts.** Text renders in a fallback font, then shifts when the web font loads (FOUT — Flash of Unstyled Text).
4. **Async content above the fold.** Client-fetched data that inserts elements above already-visible content.

### Fixes

- Always set `width` and `height` on `<img>` and `<video>` elements. The browser calculates aspect ratio and reserves space.
- Use CSS `aspect-ratio` for responsive containers: `aspect-ratio: 16 / 9;`
- Reserve space for ads with `min-height` on ad containers.
- Use `font-display: swap` and size-adjust fallback fonts to minimize layout shift from font loading.
- Never insert content above the current viewport without user action. If you must, use CSS `transform` animations instead of layout-changing properties.
- Use `contain: layout` on elements that resize independently (sidebars, widgets).

## TTFB: the silent LCP killer

Time to First Byte (TTFB) is not a Core Web Vital itself, but it directly constrains LCP. A TTFB of 2 seconds means LCP cannot possibly be under 2 seconds.

**Target:** Under 800ms for the 75th percentile.

**Common causes of high TTFB:**
- No CDN or CDN cache misses (every request hits origin)
- Slow database queries on dynamic pages
- No page-level caching (WordPress without a cache plugin)
- DNS resolution delays (use a fast DNS provider)
- SSL handshake overhead (enable TLS 1.3, OCSP stapling)

**Quick wins:**
- Enable CDN edge caching for static and semi-static pages
- Implement stale-while-revalidate caching strategies
- Use a fast DNS provider (Cloudflare DNS is free and fast)
- Enable HTTP/2 or HTTP/3 (most modern CDNs support this)
