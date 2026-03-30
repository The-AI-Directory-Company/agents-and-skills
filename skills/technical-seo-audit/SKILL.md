---
name: technical-seo-audit
description: Conduct technical SEO audits — evaluating site crawlability, indexation, Core Web Vitals, structured data, mobile usability, and internal linking to produce a prioritized fix list.
metadata:
  displayName: "Technical SEO Audit"
  categories: ["business", "engineering"]
  tags: ["SEO", "technical-SEO", "Core-Web-Vitals", "crawlability", "audit"]
  worksWellWithAgents: ["frontend-engineer", "performance-engineer", "seo-specialist"]
  worksWellWithSkills: ["content-sgeo", "discovery-gseo", "off-page-sgeo", "on-page-sgeo", "performance-audit"]
---

# Technical SEO Audit

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What is the site URL?** (Production domain, canonical www vs. non-www)
2. **What platform/framework?** (Next.js, WordPress, Shopify, custom — determines common issues)
3. **What are the business-critical pages?** (Homepage, product pages, pricing, docs)
4. **Do you have Google Search Console access?** (Crawl stats, index coverage, performance data)
5. **Do you have a crawl tool?** (Screaming Frog, Sitebulb, Ahrefs Site Audit, or similar)
6. **Current organic traffic trend?** (Growing, flat, declining — over what timeframe)
7. **Known issues?** (Recent migration, traffic drop, indexation problems, CWV failures)

## Technical SEO audit template

### 1. Crawlability Assessment

Verify that search engines can discover and access all important pages.

```
| Check                    | Status | Finding                                  | Priority |
|--------------------------|--------|------------------------------------------|----------|
| robots.txt               | [P/F]  | [What is blocked, what should be]        | [H/M/L]  |
| XML sitemap              | [P/F]  | [URL, page count, last modified dates]   | [H/M/L]  |
| Crawl budget waste       | [P/F]  | [Faceted URLs, parameters, duplicates]   | [H/M/L]  |
| Orphan pages             | [P/F]  | [Pages in sitemap but no internal links] | [H/M/L]  |
| Redirect chains          | [P/F]  | [Chains > 2 hops, count affected URLs]  | [H/M/L]  |
| Server errors (5xx)      | [P/F]  | [Count and affected URL patterns]        | [H/M/L]  |
| Soft 404s                | [P/F]  | [Pages returning 200 but showing errors] | [H/M/L]  |
```

For JS-rendered sites, verify Googlebot sees the same content as a browser using URL Inspection or `site:` search.

### 2. Indexation Analysis

Check what Google has indexed versus what you want indexed.

```
| Check                     | Status | Finding                                 | Priority |
|---------------------------|--------|-----------------------------------------|----------|
| Index coverage (GSC)      | [P/F]  | [Indexed vs. submitted pages]           | [H/M/L]  |
| Accidental noindex        | [P/F]  | [Important pages blocked from index]    | [H/M/L]  |
| Canonical tags            | [P/F]  | [Self-referencing, cross-domain, errors]| [H/M/L]  |
| Duplicate content         | [P/F]  | [URL variations, parameterized pages]   | [H/M/L]  |
| Thin content pages        | [P/F]  | [Pages with < 200 words, no value]      | [H/M/L]  |
```

Compare `site:domain.com` result count against your sitemap count. Too few means indexation issues; too many means duplicates in the index.

### 3. Core Web Vitals

Evaluate performance using field data (CrUX) and lab data (Lighthouse, WebPageTest).

```
| Metric | Threshold (Good) | Field Data (p75) | Lab Data | Status | Priority |
|--------|-------------------|-------------------|----------|--------|----------|
| LCP    | < 2.5s            | [value]           | [value]  | [P/F]  | [H/M/L] |
| INP    | < 200ms           | [value]           | [value]  | [P/F]  | [H/M/L] |
| CLS    | < 0.1             | [value]           | [value]  | [P/F]  | [H/M/L] |
```

Field data trumps lab data — it reflects real user experience. If field data is unavailable (low traffic sites), note this limitation. For failing metrics, identify the specific element or resource causing the issue (e.g., LCP element is an unoptimized hero image, CLS is caused by late-loading ad slots).

### 4. Structured Data

Audit JSON-LD/microdata for correctness and coverage.

```
| Page Type     | Schema Type     | Present | Valid | Rich Result Eligible | Priority |
|---------------|-----------------|---------|-------|----------------------|----------|
| Homepage      | Organization    | [Y/N]   | [Y/N] | [Y/N]               | [H/M/L]  |
| Product pages | Product         | [Y/N]   | [Y/N] | [Y/N]               | [H/M/L]  |
| Blog posts    | Article         | [Y/N]   | [Y/N] | [Y/N]               | [H/M/L]  |
| FAQ pages     | FAQPage         | [Y/N]   | [Y/N] | [Y/N]               | [H/M/L]  |
```

Validate with Google's Rich Results Test. Structured data that does not match visible page content risks manual action.

### 5. Mobile Usability

Google uses mobile-first indexing — the mobile experience is the indexed experience. Check: mobile-friendly test result, viewport meta tag, text size and tap targets, content parity between mobile and desktop, and intrusive interstitials. Use the same `[P/F] | Finding | Priority` table format.

### 6. Internal Linking

Evaluate click depth to key pages (should be within 3 clicks of homepage), broken internal links, anchor text relevance, and navigation structure. Pages buried 5+ clicks deep receive less crawl attention and link equity.

### 7. Prioritized Fix List

Consolidate all findings into a single ranked list. Order by impact and effort.

```
| # | Issue                              | Impact | Effort | Priority | Owner    |
|---|-------------------------------------|--------|--------|----------|----------|
| 1 | Fix 47 broken internal links        | High   | Low    | P0       | @dev     |
| 2 | Add canonical tags to parameterized | High   | Low    | P0       | @dev     |
|   | product URLs                        |        |        |          |          |
| 3 | Optimize LCP (compress hero images) | High   | Medium | P0       | @frontend|
| 4 | Add Product schema to product pages | Medium | Low    | P1       | @dev     |
| 5 | Reduce redirect chains (23 URLs)    | Medium | Low    | P1       | @dev     |
| 6 | Consolidate thin content pages      | Medium | High   | P2       | @content |
```

## Quality checklist

Before delivering an audit, verify:

- [ ] All six audit areas covered — crawlability, indexation, CWV, structured data, mobile, linking
- [ ] Findings reference specific URLs or page patterns, not generic advice
- [ ] Core Web Vitals use field data where available, lab data as supplement
- [ ] Structured data validated with Rich Results Test
- [ ] Every finding has priority rating (H/M/L) based on impact
- [ ] Prioritized fix list orders by impact and effort, not audit section
- [ ] Each fix has an owner assigned

## Common mistakes to avoid

- **Auditing without Search Console data.** Crawl tools show what is on the site. Search Console shows what Google actually sees, crawls, and indexes. Without it, you are guessing at half the picture.
- **Treating all pages equally.** A canonical tag issue on 10 high-traffic product pages matters more than the same issue on 500 old blog posts. Weight findings by the business value of affected pages.
- **Lab data only for Core Web Vitals.** Lighthouse scores in a dev environment on a fast machine do not reflect real user experience. Use CrUX field data as the source of truth.
- **Listing issues without prioritization.** A 200-item audit report with no ranking paralyzes the team. Rank by impact times effort — quick wins first, then high-impact projects.
- **Ignoring JavaScript rendering.** If the site is a SPA or uses client-side rendering, search engines may not see the content you think they see. Always verify rendered HTML against source HTML for JS-heavy sites.
- **Fixing technical SEO without content strategy.** A perfectly crawlable site with thin, undifferentiated content will not rank. Technical SEO removes barriers — content and authority drive rankings.
