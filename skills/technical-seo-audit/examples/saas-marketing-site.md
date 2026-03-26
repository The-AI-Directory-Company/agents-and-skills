# Technical SEO Audit — Planwise.io Marketing Site

## Context

**Site:** https://www.planwise.io (SaaS project management tool)
**Platform:** Next.js 14 (App Router), deployed on Vercel, Contentful CMS for blog
**Critical pages:** Homepage, /features, /pricing, /integrations, /blog (142 posts)
**Organic traffic trend:** Flat for 6 months despite content investment. 18,400 monthly organic sessions.
**Known issue:** Redesign launched 4 months ago; traffic has not recovered to pre-redesign levels (was 24,000/mo).

Audit conducted with Screaming Frog (full crawl, 1,847 URLs), Google Search Console (90 days), and PageSpeed Insights (field data).

## 1. Crawlability

| Check | Status | Finding | Priority |
|-------|--------|---------|----------|
| robots.txt | PASS | Correct, allows all crawlers, points to sitemap | — |
| XML sitemap | FAIL | Sitemap at /sitemap.xml lists 1,204 URLs but site has 1,847 crawlable pages. 643 blog pages missing — Contentful webhook not triggering sitemap rebuild. | High |
| Crawl budget waste | FAIL | 312 faceted /integrations URLs (`?category=X&sort=Y`) are crawlable. No canonical tags, no `noindex`. Googlebot spent 18% of crawl budget on these parameter variations. | High |
| Orphan pages | FAIL | 47 blog posts have no internal links pointing to them. They appear in the old sitemap but were dropped from category pages during redesign. | Medium |
| Redirect chains | FAIL | 23 URLs have 3-hop redirect chains (old blog slug -> redesign slug -> canonical). Avg chain: old.planwise.io/blog/X -> planwise.io/blog/X -> www.planwise.io/blog/X. | Medium |
| Server errors | PASS | 0 5xx errors in crawl and GSC | — |
| Soft 404s | FAIL | 8 integration partner pages return 200 but display "Coming soon" placeholder with no content. GSC reports these as "Crawled - currently not indexed." | Low |

## 2. Indexation

| Check | Status | Finding | Priority |
|-------|--------|---------|----------|
| Index coverage | FAIL | GSC shows 1,031 indexed pages vs. 1,847 crawlable. 312 parameter pages inflating crawlable count, but 643 blog posts genuinely missing from index. | High |
| Accidental noindex | FAIL | `/pricing` page has `<meta name="robots" content="noindex">` — left from A/B test 3 months ago. Pricing page receives 0 organic impressions. | High |
| Canonical tags | FAIL | 312 integration filter pages lack canonical tags. Self-referencing canonicals present on other pages. | High |
| Duplicate content | FAIL | Blog posts accessible at both `/blog/post-slug` and `/blog/posts/post-slug` (legacy route still active). 142 duplicate pairs. | High |
| Thin content | PASS | Blog posts average 1,400 words. Feature pages have adequate content. | — |

**Critical finding:** The `/pricing` noindex tag is the single highest-impact issue. This page had 2,100 monthly organic sessions before it was noindexed.

## 3. Core Web Vitals

Field data from CrUX (28-day, mobile):

| Metric | Good Threshold | Field (p75) | Lab | Status | Priority |
|--------|---------------|------------|-----|--------|----------|
| LCP | < 2.5s | 3,800 ms | 3,200 ms | FAIL | High |
| INP | < 200ms | 120 ms | 95 ms | PASS | — |
| CLS | < 0.1 | 0.24 | 0.18 | FAIL | High |

**LCP cause:** Hero image on homepage and feature pages served as unoptimized 2.4 MB PNG. LCP element identified as `.hero-image` across 5 high-traffic pages. Next.js `<Image>` component not used — raw `<img>` tags bypass automatic optimization.

**CLS cause:** Pricing toggle (monthly/annual) causes layout shift of 0.19 when switching. Cookie consent banner pushes content down by 0.05. Combined CLS: 0.24.

## 4. Structured Data

| Page Type | Schema | Present | Valid | Rich Result | Priority |
|-----------|--------|---------|-------|-------------|----------|
| Homepage | Organization | Yes | Yes | Yes (logo) | — |
| Blog posts | Article | No | — | No | Medium |
| Pricing | — | No | — | — | Low |
| FAQ (/faq) | FAQPage | No | — | No | Medium |
| Integrations | SoftwareApplication | No | — | No | Low |

Blog posts lack Article schema — missing opportunity for rich results on 142 pages with 8,200 combined monthly impressions. FAQ page has 34 Q&A pairs but no FAQPage schema.

## 5. Mobile Usability

| Check | Status | Finding | Priority |
|-------|--------|---------|----------|
| Mobile-friendly test | PASS | All tested pages pass | — |
| Viewport meta tag | PASS | Present on all pages | — |
| Tap targets | FAIL | Footer links have 6px spacing (minimum: 8px). Integration card buttons 36x28px (minimum: 48x48px). | Low |
| Content parity | PASS | No content hidden on mobile | — |
| Interstitials | PASS | Cookie banner is non-intrusive (bottom bar) | — |

## 6. Internal Linking

| Check | Status | Finding | Priority |
|-------|--------|---------|----------|
| Click depth | FAIL | 47 orphaned blog posts are 5+ clicks from homepage (only reachable via pagination of /blog page 4+). | Medium |
| Broken links | FAIL | 31 broken internal links found. 28 point to old integration partner pages that were removed during redesign. 3 point to renamed blog slugs. | Medium |
| Anchor text | PASS | Blog cross-links use descriptive anchor text, not "click here" | — |
| Navigation | FAIL | Blog category pages removed during redesign. Previously linked to 8 category hubs, now only a flat /blog list. Lost topical clustering. | Medium |

## 7. Prioritized Fix List

| # | Issue | Impact | Effort | Priority | Owner |
|---|-------|--------|--------|----------|-------|
| 1 | Remove `noindex` from /pricing | High | 5 min | P0 | @frontend |
| 2 | Add canonical tags to 312 integration filter URLs | High | 2 hours | P0 | @frontend |
| 3 | Fix sitemap generation to include all blog posts | High | 4 hours | P0 | @frontend |
| 4 | Remove legacy `/blog/posts/` route, redirect to `/blog/` | High | 2 hours | P0 | @frontend |
| 5 | Switch hero images to Next.js `<Image>`, serve WebP | High | 1 day | P0 | @frontend |
| 6 | Fix CLS: reserve space for pricing toggle, resize consent banner | High | 4 hours | P0 | @frontend |
| 7 | Flatten redirect chains to single 301 | Medium | 3 hours | P1 | @frontend |
| 8 | Fix 31 broken internal links | Medium | 2 hours | P1 | @content |
| 9 | Re-link 47 orphaned blog posts from category hubs | Medium | 1 day | P1 | @content |
| 10 | Add Article schema to blog posts | Medium | 4 hours | P1 | @frontend |
| 11 | Add FAQPage schema to /faq | Medium | 2 hours | P1 | @frontend |
| 12 | Restore blog category pages for topical clustering | Medium | 1 week | P2 | @content |
| 13 | Fix tap target sizes on mobile | Low | 2 hours | P2 | @frontend |
| 14 | Add content or noindex to 8 "Coming soon" pages | Low | 1 hour | P2 | @content |

**Estimated recovery:** Fixing items 1-6 (P0, achievable within 1 sprint) should recover the ~5,600 lost monthly sessions — primarily from re-indexing /pricing and resolving the 643 missing blog pages.
