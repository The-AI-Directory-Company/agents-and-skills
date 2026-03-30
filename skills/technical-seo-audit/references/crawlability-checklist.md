# Crawlability Checklist

Systematic checks for ensuring search engines can discover and access all important pages. Use this when evaluating Section 1 (Crawlability Assessment) of the technical SEO audit.

---

## robots.txt

| Check | How to Verify | Pass Criteria |
|-------|--------------|---------------|
| File exists and is accessible | Fetch `https://domain.com/robots.txt` — must return 200 | File returns 200 with valid directives |
| No accidental blocking of important paths | Review all `Disallow` directives | Business-critical pages/directories are not blocked |
| Sitemap reference present | Look for `Sitemap:` directive | At least one sitemap URL listed |
| No overly broad blocks | Check for `Disallow: /` or blanket directory blocks | No rules that block entire site sections unintentionally |
| User-agent specificity | Check for `User-agent: *` vs. specific bots | Specific bot rules do not contradict wildcard rules |
| Staging/dev environment check | Verify production robots.txt is not a copy of staging | No `Disallow: /` left over from pre-launch |

### Common robots.txt Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| `Disallow: /` on production | Entire site deindexed | Remove or scope to specific paths |
| Blocking CSS/JS files | Googlebot cannot render pages; sees blank content | Allow CSS/JS directories |
| Blocking search/filter URLs without noindex | Pages drop from index but are never recrawled to see the directive | Use noindex meta tag instead of robots.txt for pages already indexed |
| No `Sitemap:` directive | Crawlers rely on sitemap discovery via Search Console only | Add `Sitemap: https://domain.com/sitemap.xml` |

---

## XML Sitemap

| Check | How to Verify | Pass Criteria |
|-------|--------------|---------------|
| Sitemap exists | Fetch common paths: `/sitemap.xml`, `/sitemap_index.xml` | At least one sitemap accessible |
| Submitted to Search Console | Check GSC > Sitemaps | Sitemap submitted and status is "Success" |
| Only canonical URLs | Compare sitemap URLs against canonical tags | Every URL in the sitemap is its own canonical |
| No 4xx/5xx URLs | Crawl all sitemap URLs | All URLs return 200 |
| No noindex URLs | Check meta robots on sitemap URLs | No URL in the sitemap has `noindex` |
| lastmod dates accurate | Compare `<lastmod>` to actual page changes | Dates reflect real content changes, not automated timestamps |
| URL count reasonable | Compare sitemap count to `site:domain.com` | Counts are in the same order of magnitude |
| Sitemap is under limits | Check file size and URL count | Max 50,000 URLs per sitemap; max 50MB uncompressed |
| Sitemap index for large sites | Check for sitemap index structure | Sites with >50K URLs use a sitemap index |

### Sitemap Quality Signals

- **Good:** Sitemap contains only indexable, canonical, 200-status pages with accurate lastmod dates.
- **Bad:** Sitemap contains redirects, 404s, noindex pages, non-canonical URLs, or static lastmod dates that never change.

---

## JavaScript Rendering

| Check | How to Verify | Pass Criteria |
|-------|--------------|---------------|
| Content visible in rendered HTML | Google Search Console > URL Inspection > "View Tested Page" | Critical content (headings, body text, links) present in rendered HTML |
| `site:` search matches expectations | Search `site:domain.com "specific page content"` | Content appears in Google's cached version |
| No render-dependent internal links | View page source vs. rendered DOM | Internal links exist in initial HTML, not only in JS-rendered DOM |
| Meta tags in initial HTML | View page source (not DevTools Elements) | title, description, canonical, and robots tags are in the initial server response |
| Dynamic rendering (if applicable) | Check if the site serves different HTML to Googlebot | Googlebot receives pre-rendered or server-rendered HTML |

### JavaScript Rendering Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Client-side only rendering (CSR) | Googlebot may not index content; two-wave indexing delays | Use SSR, SSG, or dynamic rendering |
| JavaScript errors preventing render | Page appears blank to Googlebot | Monitor Google Search Console for rendering errors |
| Lazy-loaded content below fold | Content may not be indexed if Googlebot does not scroll | Use intersection observer with a generous rootMargin; ensure critical content is in initial viewport |
| Client-side routing without SSR | Internal links may not be discovered by crawlers | Ensure all routes are in the sitemap; use SSR or prerendering |

---

## Crawl Budget

Crawl budget matters primarily for large sites (100K+ pages). For smaller sites, focus on crawlability fundamentals instead.

| Check | How to Verify | Pass Criteria |
|-------|--------------|---------------|
| Crawl stats trending healthy | GSC > Settings > Crawl stats | No declining trends in crawl requests or crawl rate |
| No excessive parameterized URLs | Check GSC URL Parameters or crawl tool | Faceted/filtered URLs are either canonicalized, noindexed, or blocked |
| No infinite crawl spaces | Check for calendar pages, session IDs, or sort/filter URLs | Infinite URL patterns are handled with parameter handling or crawl directives |
| Server response time acceptable | Check GSC crawl stats for average response time | Average response time < 500ms |
| 5xx error rate low | Check GSC crawl stats for server error rate | Server errors < 1% of crawled URLs |

### Crawl Budget Optimization

| Action | When to Use | Impact |
|--------|------------|--------|
| Remove low-value pages from index | Thin content, duplicate parameter pages | Frees crawl budget for important pages |
| Fix redirect chains | Chains > 2 hops | Reduces wasted crawl requests on intermediate redirects |
| Improve server response time | TTFB > 500ms | Faster responses allow more pages to be crawled per session |
| Update sitemap to prioritize important pages | Large sites with mixed content quality | Signals which pages to crawl first |
| Set crawl rate in Search Console | Only if server is overloaded | Limits Googlebot's crawl rate (use sparingly — this slows indexing) |

---

## Redirect Audit

| Check | How to Verify | Pass Criteria |
|-------|--------------|---------------|
| No redirect chains > 2 hops | Crawl tool redirect report | All redirects resolve in 1-2 hops |
| No redirect loops | Crawl tool error report | Zero redirect loops |
| 301 (permanent) vs. 302 (temporary) | Check HTTP status codes | Permanent moves use 301; temporary content uses 302 |
| Old URLs redirect to equivalent content | Spot-check redirect destinations | Redirects go to the closest equivalent page, not the homepage |
| HTTPS redirects in place | Check HTTP > HTTPS redirect | All HTTP URLs redirect to HTTPS with 301 |
| www/non-www consistency | Check www and non-www variants | One version redirects to the other with 301 |

---

## Quick Pass/Fail Summary Template

Use this to record crawlability findings in the audit:

| Area | Status | Critical Issues | Action Items |
|------|--------|----------------|-------------|
| robots.txt | [Pass/Fail] | | |
| XML Sitemap | [Pass/Fail] | | |
| JS Rendering | [Pass/Fail] | | |
| Crawl Budget | [Pass/Fail/N/A] | | |
| Redirects | [Pass/Fail] | | |
