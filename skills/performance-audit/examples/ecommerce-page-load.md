# Performance Audit — Product Listing Page, Greenleaf Commerce

## Context

**What is slow:** `/collections/*` product listing pages (PLPs) across all categories.
**How slow:** LCP 5.8s (p75 field data), TTFB 1.9s, page weight 4.2 MB.
**Target:** LCP under 2.5s, TTFB under 600ms. Pass Core Web Vitals.
**Architecture:** Next.js 14 (Pages Router), PostgreSQL via Prisma, Redis cache, Cloudflare CDN, Vercel hosting.
**Traffic:** 12,000 daily sessions, 85% mobile, peak 2x during promotions.

## Baselines (measured Jan 8, 2026, production traffic)

| Metric | Field (p75) | Lab (Lighthouse mobile) | Target | Status |
|--------|------------|-------------------------|--------|--------|
| LCP | 5,800 ms | 4,200 ms | < 2,500 ms | FAIL |
| INP | 310 ms | 280 ms | < 200 ms | FAIL |
| CLS | 0.08 | 0.04 | < 0.1 | PASS |
| TTFB | 1,900 ms | 1,400 ms | < 600 ms | FAIL |
| TBT | — | 1,100 ms | < 200 ms | FAIL |
| Page weight | — | 4.2 MB | < 1.5 MB | FAIL |

Page weight breakdown: JS 2.1 MB (50%), images 1.6 MB (38%), CSS 320 KB (8%), fonts 180 KB (4%).

## Frontend Findings

**F1. Unoptimized product images (1.6 MB).** All product thumbnails served as full-resolution PNGs (1200x1200) regardless of viewport. No `srcset`, no lazy loading below the fold. LCP element is the first product image.

**F2. JavaScript bundle bloat (2.1 MB).** Bundle analysis: `moment.js` (290 KB) used only for relative timestamps, `lodash` full import (72 KB) for 3 functions, analytics SDK loaded synchronously (180 KB), product zoom library loaded on every PLP (340 KB, only needed on PDP).

**F3. Render-blocking CSS.** Single 320 KB stylesheet blocks first paint. No critical CSS extraction. Includes PDP, checkout, and admin styles on every page.

**F4. No code splitting on filter interactions.** Selecting a filter re-renders the entire product grid client-side, triggering 310ms INP. Filter state managed in a single top-level component, causing 48 product cards to re-render.

## Backend Findings

**B1. Missing page-level cache.** Every PLP request executes a fresh database query. Redis is deployed but only caches user sessions. PLP data changes at most hourly but is queried ~200 times/minute during peaks.

**B2. Slow product query (1,200ms avg).** The PLP query joins `products`, `variants`, `inventory`, and `categories` in a single query. EXPLAIN shows a sequential scan on `variants` (280K rows, no index on `product_id + is_active`).

**B3. Sequential API calls.** Breadcrumb data, filter facet counts, and product results fetched sequentially in `getServerSideProps`. Combined: 1,200ms (products) + 380ms (facets) + 210ms (breadcrumbs) = 1,790ms server time.

## Database Findings

**D1. Missing composite index.** `variants` table lacks index on `(product_id, is_active)`. The PLP query filters on both columns across 280K rows. Adding the index reduces query time from 1,200ms to 85ms in staging.

**D2. N+1 on inventory checks.** After fetching 48 products, inventory availability is checked per-SKU in a loop (48 individual queries, 6ms each = 288ms). Should be a single `WHERE sku IN (...)` query.

**D3. Untuned connection pool.** Prisma default pool size of 2 connections. Under load, queries queue behind each other. Server has capacity for 20 connections; pool should be 10-15.

## Optimization Roadmap

| Priority | Finding | Action | Expected Gain | Effort |
|----------|---------|--------|---------------|--------|
| P0 | D1 | Add composite index on `variants(product_id, is_active)` | TTFB -1,100ms | 1 hour |
| P0 | B3 | Parallelize `getServerSideProps` calls with `Promise.all` | TTFB -400ms | 2 hours |
| P0 | D2 | Batch inventory check into single IN query | TTFB -250ms | 3 hours |
| P0 | F1 | Convert images to WebP, add `srcset` and `loading="lazy"` | LCP -2,000ms, weight -1.2 MB | 1 day |
| P1 | B1 | Cache PLP responses in Redis (60s TTL, invalidate on publish) | TTFB to <100ms for cache hits | 2 days |
| P1 | F2 | Replace moment with dayjs, tree-shake lodash, lazy-load zoom lib | JS bundle -700 KB | 1 day |
| P1 | F3 | Extract critical CSS, async-load remainder | First paint -800ms | 1 day |
| P2 | F4 | Memoize product cards, virtualize grid for >48 items | INP from 310ms to <150ms | 3 days |
| P2 | D3 | Increase Prisma pool to 12 connections | p99 latency -40% under load | 1 hour |

## Projected Results

After P0 fixes (achievable in 1-2 days):

| Metric | Current (p75) | Projected | Target |
|--------|--------------|-----------|--------|
| LCP | 5,800 ms | ~2,400 ms | < 2,500 ms |
| TTFB | 1,900 ms | ~450 ms | < 600 ms |
| Page weight | 4.2 MB | ~2.8 MB | < 1.5 MB |

After P0+P1 fixes (achievable in 1 sprint):

| Metric | Projected | Target |
|--------|-----------|--------|
| LCP | ~1,600 ms | < 2,500 ms |
| INP | ~240 ms | < 200 ms |
| TTFB | ~100 ms (cached) | < 600 ms |
| Page weight | ~1.9 MB | < 1.5 MB |

## Monitoring

- **Vercel Web Analytics:** Track LCP, INP, CLS on `/collections/*` pages daily.
- **Application alert:** TTFB p95 > 800ms on PLP routes triggers PagerDuty warning.
- **Redis cache hit rate:** Alert if hit rate drops below 80% (indicates invalidation bug or cold cache).
- **Verification date:** Re-measure field data 7 days after each deployment.
