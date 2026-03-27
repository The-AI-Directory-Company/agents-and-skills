---
name: technical-sgeo
description: Set up a site's technical foundation for visibility in both traditional search engines and AI platforms — covering crawlability, indexation, Core Web Vitals, structured data, mobile-first design, AI crawler access, and measurement infrastructure.
metadata:
  displayName: "Technical SGEO Setup"
  categories: ["engineering", "business"]
  tags: ["SEO", "GEO", "SGEO", "technical-SEO", "crawlability", "Core-Web-Vitals", "AI-visibility", "structured-data", "robots.txt"]
  worksWellWithAgents: ["seo-specialist", "frontend-engineer", "performance-engineer", "devops-engineer"]
  worksWellWithSkills: ["technical-seo-audit", "performance-audit", "on-page-sgeo", "content-sgeo", "off-page-sgeo"]
---

# Technical SGEO Setup

## Tool discovery

Before gathering project details, confirm which tools are available.
Ask the user directly — do not assume access to any external service.

**Free tools (no API key required):**
- [ ] WebFetch (fetch any public URL — robots.txt, sitemaps, pages)
- [ ] WebSearch (search engine queries for competitive analysis)
- [ ] Google PageSpeed Insights API (CWV data, no key needed for basic usage)
- [ ] Google Rich Results Test (structured data validation)
- [ ] Playwright MCP or Chrome DevTools MCP (browser automation)

**Paid tools (API key or MCP required):**
- [ ] Google Search Console API (requires OAuth)
- [ ] DataForSEO MCP (SERP data, keyword metrics, backlinks)
- [ ] Ahrefs API (backlink profiles, keyword research)
- [ ] Semrush API (competitive analysis, keyword data)

**The agent must:**
1. Present this checklist to the user
2. Record which tools are available
3. Pass the inventory to scripts as context
4. Fall back gracefully — every check has a free-tier path using WebFetch/WebSearch

Run `scripts/inventory-tools.py` to auto-detect available tools and generate a `tools.json` inventory for other scripts.

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What is the site URL?** (Production domain, including whether www or non-www is canonical)
2. **What platform/framework is the site built on?** (Next.js, WordPress, Shopify, custom SPA — determines rendering model, common pitfalls, and available tooling)
3. **What is the hosting/CDN provider?** (Vercel, Cloudflare, AWS CloudFront, Netlify — CDN configuration directly affects both search and AI crawler access)
4. **What is the current robots.txt status?** (Existing file contents, or confirmation that none exists)
5. **Do you have Google Search Console access?** (Required for crawl stats, index coverage, and Core Web Vitals field data)
6. **Does AI visibility matter for this site?** (If the site sells products, services, or publishes information that users ask AI assistants about, the answer is almost certainly yes)
7. **Are there known technical issues?** (Recent migration, traffic drop, indexation problems, CWV failures, rendering issues)
8. **What CMS or deployment workflow do you use?** (Determines how changes to robots.txt, sitemaps, meta tags, and structured data get deployed)

## Technical SGEO implementation template

### 1. Measurement Infrastructure

> **Scripts:** Run `scripts/inventory-tools.py` to detect available tools.
> **References:** See `references/measurement-setup.md` for detailed GSC/GA4/Bing setup walkthrough and AI referrer tracking configuration.

Set up tracking before making changes. Without measurement, you cannot verify that implementations work or detect regressions.

```
| Check                        | Status | Action                                                   | Priority |
|------------------------------|--------|----------------------------------------------------------|----------|
| Google Search Console (GSC)  | [ ]    | Verify ownership, submit XML sitemap, review index report | High     |
| Google Analytics 4 (GA4)     | [ ]    | Install tracking, configure key events, link to GSC       | High     |
| Bing Webmaster Tools         | [ ]    | Verify site — Bing data feeds into Microsoft Copilot,     | Medium   |
|                              |        | ChatGPT (via Bing API), and other AI systems              |          |
| Server log access            | [ ]    | Confirm ability to query logs for bot user-agents:        | Medium   |
|                              |        | Googlebot, Bingbot, GPTBot, ClaudeBot, PerplexityBot     |
| CrUX / PageSpeed Insights   | [ ]    | Verify field data availability for Core Web Vitals        | Medium   |
```

**Why Bing Webmaster Tools matters for AI visibility:** Bing's index is the retrieval layer for multiple AI systems including Microsoft Copilot and ChatGPT's browsing feature. A site that is well-indexed in Bing has a structural advantage in AI citation. Set it up — it takes 10 minutes.

**Server log monitoring for AI crawlers:** Traditional analytics (GA4) does not capture bot traffic. Server logs are the only way to see how often AI crawlers visit, which pages they request, and whether they receive 200 responses. Set up a log query or dashboard filtered to known AI bot user-agents.

### 2. Crawlability for Search Engines

> **Scripts:** Run `scripts/check-robots-txt.py` to audit robots.txt rules. Run `scripts/validate-sitemap.py` to validate your XML sitemap. Run `scripts/check-redirect-chains.py` to find redirect chains.
> **References:** See `references/crawlability.md` for deep context on crawl mechanics, robots.txt syntax, and CDN bot-management gotchas.

Search engines must discover, access, and render every page you want indexed. Crawlability failures are silent — pages simply do not appear in results.

```
| Check                    | Status | Action                                                      | Priority |
|--------------------------|--------|-------------------------------------------------------------|----------|
| robots.txt               | [ ]    | Allow Googlebot and Bingbot access to all indexable content. | High     |
|                          |        | Block: /admin, /api, /internal, faceted navigation paths    |          |
| XML sitemap              | [ ]    | Create/validate sitemap. Include only 200-status canonical   | High     |
|                          |        | URLs. Submit to GSC and Bing Webmaster Tools                |          |
| Crawl budget waste       | [ ]    | Eliminate faceted URLs, parameter variations, and duplicate  | High     |
|                          |        | paths from crawlable pages. Use robots.txt or noindex.      |          |
| Redirect chains          | [ ]    | Audit all redirects. Maximum 2 hops. Update internal links  | Medium   |
|                          |        | to point to final destinations directly                     |          |
| Server errors (5xx)      | [ ]    | Check GSC Coverage report for server errors. Aim for zero   | High     |
|                          |        | 5xx on any crawled URL                                      |          |
| Soft 404s                | [ ]    | Identify pages returning 200 status but displaying error    | Medium   |
|                          |        | content. Configure proper 404 responses                     |          |
| JavaScript rendering     | [ ]    | Verify rendered HTML matches intended content. Use GSC URL  | High     |
|                          |        | Inspection "View Tested Page" to see what Google renders    |          |
```

**XML sitemap requirements:**
- Only include URLs that return 200 and have a self-referencing canonical tag
- Keep sitemap under 50,000 URLs or 50MB uncompressed per file (use sitemap index for larger sites)
- Set `<lastmod>` dates to actual content modification dates, not the current date
- Validate with a sitemap validator before submission

**JavaScript rendering verification:** If the site uses client-side rendering (React SPA, Angular, Vue without SSR), Google's crawler may not see the content. Test by comparing the raw HTML source with the rendered DOM in GSC URL Inspection. If critical content is missing from the raw source and only appears after JavaScript execution, implement server-side rendering (SSR) or static site generation (SSG) for indexable pages.

### 3. Crawlability for AI Engines

> **Scripts:** Run `scripts/check-ai-crawler-access.py` to test whether AI crawlers can reach your pages.
> **References:** See `references/ai-crawler-access.md` for the complete AI bot user-agent table and CDN configuration guides per provider.

AI crawlers follow similar mechanics to search crawlers — they request pages via HTTP and read the response. But they have different user-agents, different CDN treatment, and different content consumption patterns. This section covers what to verify beyond standard search engine crawlability.

**robots.txt for AI crawlers:**

Check your robots.txt for rules affecting these user-agents:

```
| Bot              | Operator     | What it feeds              | Recommended |
|------------------|--------------|----------------------------|-------------|
| GPTBot           | OpenAI       | ChatGPT training + browse  | Allow       |
| ChatGPT-User     | OpenAI       | ChatGPT live browsing      | Allow       |
| OAI-SearchBot    | OpenAI       | ChatGPT search results     | Allow       |
| ClaudeBot        | Anthropic    | Claude training + retrieval | Allow       |
| PerplexityBot    | Perplexity   | Perplexity search answers  | Allow       |
| Google-Extended  | Google       | Gemini training            | Allow       |
| Bytespider       | ByteDance    | TikTok AI features         | Evaluate    |
```

If your goal is AI visibility, do not block these bots. Many robots.txt files inherited blocks from a period when site owners were uncertain about AI crawling. Review and remove blocks that conflict with your visibility goals.

**CDN and WAF configuration:**

This is a common source of accidental AI bot blocking:

- **Cloudflare:** Bot Fight Mode and Super Bot Fight Mode may block AI crawlers by default. Check Security > Bots settings. Verified bots (Googlebot) are typically allowed, but AI crawlers may not be on the verified list. Create explicit Allow rules for AI bot user-agents if using aggressive bot management.
- **AWS CloudFront + WAF:** AWS WAF bot control rules may categorize AI crawlers as "unauthorized." Review your WAF rule groups.
- **Other CDNs/WAFs:** Akamai, Fastly, Sucuri, and similar services each have bot management features. Verify AI crawlers are not caught in blanket bot-blocking rules.

**Action:** After configuring, verify by checking server logs for successful 200 responses to AI crawler requests. If you see no AI crawler traffic at all, the CDN/WAF is likely blocking before requests reach your origin server.

**Content accessibility for AI consumption:**

AI crawlers generally cannot:
- Execute JavaScript (they read raw HTML responses)
- Authenticate or log in
- Bypass paywalls or cookie consent walls that hide content
- Process content inside iframes from different origins

For pages you want AI systems to cite, ensure the substantive content is present in the initial HTML response, not loaded via client-side JavaScript, and not gated behind interactions.

**llms.txt consideration:**

The llms.txt proposal (a plain-text file at `/llms.txt` summarizing site content for LLMs) has gained discussion but limited measurable impact. Research findings:

- SE Ranking analysis of 300K domains: no correlation between llms.txt presence and AI visibility
- OtterlyAI 90-day study: no measurable impact on AI citation rates
- ALLMO analysis of 94K+ URLs: no statistically significant benefit detected

Adding an llms.txt file is low effort and does no harm. But it should not take priority over the fundamentals in this guide — crawlability, rendering, structured data, and content quality drive AI visibility far more than a summary file.

### 4. Indexation Control

> **Scripts:** Run `scripts/check-indexation.py` to estimate indexed vs submitted page counts.

Control which pages appear in search results. Every indexed page competes for crawl budget and can dilute topical authority if it is low-quality or duplicated.

```
| Check                     | Status | Action                                                    | Priority |
|---------------------------|--------|-----------------------------------------------------------|----------|
| Canonical tags            | [ ]    | Every indexable page has a self-referencing canonical.      | High     |
|                           |        | Cross-domain canonicals point to the authoritative version |          |
| noindex for low-value     | [ ]    | Apply noindex to: tag/archive pages, internal search       | Medium   |
| pages                     |        | results, paginated listing pages beyond page 1, thank-you  |          |
|                           |        | pages, utility pages with no search value                  |          |
| Duplicate content         | [ ]    | Identify URL variations (trailing slash, parameters, www   | High     |
|                           |        | vs non-www, HTTP vs HTTPS) that serve identical content.   |          |
|                           |        | Resolve with canonical tags and 301 redirects              |          |
| Index coverage (GSC)      | [ ]    | Compare submitted pages (sitemap) vs indexed pages in GSC. | High     |
|                           |        | Investigate gaps — "Discovered - currently not indexed"     |          |
|                           |        | and "Crawled - currently not indexed" require action        |          |
```

**Canonical tag implementation rules:**
1. Every indexable page gets a self-referencing canonical: `<link rel="canonical" href="https://example.com/page/" />`
2. Use absolute URLs, not relative paths
3. Include the canonical in the `<head>`, not the `<body>`
4. Canonical URLs must return 200 status (not redirect)
5. Canonical must match the protocol (HTTPS) and domain (www vs non-www) you want indexed

**Indexation gap analysis:** In GSC, navigate to Pages > Indexing. The "Why pages aren't indexed" section lists specific reasons. The most actionable categories are:
- "Discovered - currently not indexed" — Google found the URL but chose not to index it. Usually a quality or crawl budget signal. Improve the content or consolidate with a stronger page.
- "Crawled - currently not indexed" — Google fetched the page but decided not to index it. Content may be thin, duplicative, or low-value.
- "Blocked by robots.txt" — Unintentional blocks. Fix immediately if the page should be indexed.

### 5. Core Web Vitals

> **Scripts:** Run `scripts/check-cwv.py` to pull PageSpeed Insights data (field + lab, LCP element identification).
> **References:** See `references/core-web-vitals.md` for fix patterns by framework (Next.js, WordPress, Shopify) and debugging workflows.

Core Web Vitals are a confirmed Google ranking factor. They also affect user experience, which affects engagement metrics that influence both search ranking and AI citation (AI systems learn from pages with higher engagement and authority signals).

```
| Metric | What It Measures          | Good     | Needs Work | Poor     |
|--------|---------------------------|----------|------------|----------|
| LCP    | Largest Contentful Paint  | < 2.5s   | 2.5-4.0s   | > 4.0s   |
| INP    | Interaction to Next Paint | < 200ms  | 200-500ms  | > 500ms  |
| CLS    | Cumulative Layout Shift   | < 0.1    | 0.1-0.25   | > 0.25   |
```

**Field data vs lab data:** Field data (Chrome User Experience Report / CrUX, accessible via PageSpeed Insights or GSC) reflects real users on real devices and networks. Lab data (Lighthouse, WebPageTest) reflects a simulated environment. Google uses field data for ranking decisions. If field and lab data disagree, field data is the source of truth. Sites with low traffic may not have field data — note this limitation and use lab data as a proxy.

**LCP optimization actions:**
1. Identify the LCP element (usually hero image, heading, or video poster). Use PageSpeed Insights — it identifies the element.
2. If image: serve in WebP/AVIF, properly sized, with `fetchpriority="high"` and no lazy loading on the LCP image
3. If text: ensure fonts load quickly — use `font-display: swap`, preload critical fonts
4. Reduce server response time (TTFB) — target under 800ms. TTFB directly delays LCP.
5. Remove render-blocking CSS and JS from the critical path

**INP optimization actions:**
1. Identify slow interactions using Chrome DevTools Performance panel or Web Vitals extension
2. Break up long tasks (>50ms) on the main thread — use `requestIdleCallback`, Web Workers, or `scheduler.yield()`
3. Reduce JavaScript bundle size — every KB of JS must be parsed and compiled
4. Defer non-critical third-party scripts (analytics, chat widgets, A/B testing)

**CLS optimization actions:**
1. Set explicit `width` and `height` attributes on images and videos
2. Reserve space for ads and dynamically injected content with CSS `min-height`
3. Avoid inserting content above existing visible content after page load
4. Use CSS `contain` on elements that resize independently

### 6. Mobile-First and HTTPS

> **Scripts:** Run `scripts/check-mobile.py` for mobile-friendliness checks. Run `scripts/check-https-security.py` to verify HTTPS and HSTS.

Google uses mobile-first indexing — the mobile version of your site is the version Google crawls and indexes. As of 2024, 62.73% of global web traffic comes from mobile devices. AI systems also primarily consume the same content Google indexes.

**Mobile verification checklist:**

```
| Check                   | Status | Action                                                     | Priority |
|-------------------------|--------|------------------------------------------------------------|----------|
| Responsive design       | [ ]    | Site renders correctly across viewport widths 320px-1440px  | High     |
| Viewport meta tag       | [ ]    | <meta name="viewport" content="width=device-width,         | High     |
|                         |        | initial-scale=1"> present in <head>                        |          |
| Tap targets             | [ ]    | Interactive elements are at least 48x48px with 8px spacing  | Medium   |
| Text sizing             | [ ]    | Base font size >= 16px. No text requires zooming to read    | Medium   |
| Content parity          | [ ]    | Mobile version has the same content as desktop — no hidden  | High     |
|                         |        | sections, collapsed accordions with critical content, or    |          |
|                         |        | mobile-only reduced content                                 |          |
| No intrusive interstitials | [ ] | No full-screen popups that block content on mobile. Google  | Medium   |
|                         |        | demotes pages with intrusive interstitials                  |          |
```

**HTTPS implementation:**

HTTPS is a non-negotiable baseline. Google has used HTTPS as a ranking signal since 2014. AI crawlers also prefer HTTPS endpoints.

- Verify all pages are served over HTTPS
- HTTP requests 301 redirect to HTTPS equivalents
- No mixed content warnings (HTTP resources loaded on HTTPS pages)
- HSTS header is set: `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- SSL certificate is valid and auto-renews

### 7. Structured Data Foundation

> **Scripts:** Run `scripts/check-structured-data.py` to extract and validate JSON-LD from any page.
> **References:** See `references/structured-data.md` for complete JSON-LD templates per page type and validation workflow.

Structured data (Schema.org JSON-LD) helps search engines understand page content precisely and enables rich results. For AI systems, structured data provides machine-readable facts that are easier to extract and cite accurately than unstructured text.

**Implementation by page type:**

```
| Page Type      | Schema Type     | Key Properties                                     | Rich Result |
|----------------|-----------------|----------------------------------------------------|-------------|
| Homepage       | Organization    | name, url, logo, sameAs (social profiles),         | Knowledge   |
|                |                 | contactPoint                                       | Panel       |
| Product pages  | Product         | name, description, image, offers (price, currency, | Product     |
|                |                 | availability), aggregateRating, review             | snippet     |
| Blog/articles  | Article         | headline, datePublished, dateModified, author,     | Article     |
|                |                 | image, publisher                                   | snippet     |
| FAQ pages      | FAQPage         | mainEntity array of Question + acceptedAnswer      | FAQ rich    |
|                |                 |                                                    | result      |
| Service pages  | Service         | name, description, provider, areaServed,           | —           |
|                |                 | serviceType                                        |             |
| Local business | LocalBusiness   | name, address, telephone, openingHoursSpecification| Local pack  |
```

**JSON-LD implementation template (Organization — homepage):**

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Your Company Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/yourcompany",
    "https://linkedin.com/company/yourcompany"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-555-5555",
    "contactType": "customer service"
  }
}
</script>
```

**FAQ Schema for AI citation potential:** FAQ pages with properly implemented FAQPage schema serve dual purposes. Search engines may display FAQ rich results (though Google has reduced eligibility). AI systems frequently cite well-structured Q&A content because the question-answer format maps directly to how users query AI assistants. Implement FAQPage schema on any page with genuine Q&A content.

**Validation:**
1. Test every page type with Google's Rich Results Test (https://search.google.com/test/rich-results)
2. Verify in GSC under Enhancements — check for errors and warnings
3. Structured data must match visible page content. Marking up content that is not visible to users risks a manual action from Google.

### 8. Verification Checklist

After completing the implementation sections above, run through this unified SEO + GEO technical readiness checklist. Every item should pass before considering the technical foundation complete.

**Crawlability and Access:**
- [ ] robots.txt allows Googlebot, Bingbot, and target AI crawlers (GPTBot, ClaudeBot, PerplexityBot)
- [ ] robots.txt blocks only non-indexable paths (/admin, /api, /internal, faceted navigation)
- [ ] XML sitemap is valid, submitted to GSC and Bing, contains only 200-status canonical URLs
- [ ] CDN/WAF is not blocking AI crawlers — verified via server logs showing 200 responses
- [ ] No redirect chains exceed 2 hops
- [ ] Zero 5xx server errors on crawled URLs
- [ ] JavaScript-rendered content is verified accessible to Googlebot via URL Inspection

**Indexation:**
- [ ] Every indexable page has a self-referencing canonical tag with absolute URL
- [ ] Low-value pages have noindex applied
- [ ] Duplicate content resolved via canonicals and 301 redirects
- [ ] GSC index coverage reviewed — "not indexed" reasons investigated and addressed
- [ ] URL parameter handling configured to prevent duplicate indexation

**Performance:**
- [ ] LCP under 2.5s (field data, or lab data if field unavailable)
- [ ] INP under 200ms
- [ ] CLS under 0.1
- [ ] TTFB under 800ms

**Mobile and Security:**
- [ ] Responsive design verified across 320px-1440px viewports
- [ ] Viewport meta tag present
- [ ] All pages served over HTTPS with valid certificate
- [ ] HTTP to HTTPS redirects in place
- [ ] HSTS header configured

**Structured Data:**
- [ ] Organization schema on homepage
- [ ] Relevant schema type implemented per page type (Product, Article, FAQPage, etc.)
- [ ] All structured data passes Rich Results Test without errors
- [ ] Structured data matches visible page content

**AI-Specific Access:**
- [ ] Server-side rendered content available in initial HTML for AI crawlers
- [ ] No critical content gated behind JavaScript-only rendering, authentication, or cookie walls
- [ ] Server logs confirm AI crawler visits are receiving 200 responses
- [ ] Bing Webmaster Tools verified (feeds Microsoft Copilot, ChatGPT browsing)

## Quality checklist

Before delivering this implementation, verify:

- [ ] All eight sections are completed with specific findings, not generic advice
- [ ] Measurement infrastructure is set up first — changes can be verified
- [ ] robots.txt addresses both search engine and AI crawler access
- [ ] Core Web Vitals use field data where available, with lab data noted as supplementary
- [ ] Structured data is validated with Rich Results Test, not just visually inspected
- [ ] CDN/WAF configuration has been explicitly checked for AI crawler blocking
- [ ] Mobile verification covers content parity, not just responsive layout
- [ ] The Section 8 unified checklist passes — all items checked off

## Common mistakes to avoid

- **Blocking AI crawlers accidentally.** CDN bot management features (Cloudflare Bot Fight Mode, AWS WAF bot control) often block AI crawlers by default. This is the most common cause of zero AI visibility for sites that should have it. Check CDN settings and verify with server logs.
- **Using lab data only for Core Web Vitals.** Lighthouse on a developer's MacBook Pro with fiber internet does not represent real users. Field data from CrUX is what Google uses for ranking. If your Lighthouse score is 95 but field LCP is 4.2s, you have a problem.
- **Fixing technical SEO without a content strategy.** A perfectly crawlable, fast, mobile-friendly site with thin content will not rank or get cited. Technical SGEO removes barriers — content quality and topical authority drive actual visibility. Pair this skill with content-sgeo and on-page-sgeo.
- **Ignoring JavaScript rendering.** 60% of Google searches result in zero clicks — users get answers directly from search results and AI systems. If your content is invisible without JavaScript execution, it is invisible to most of the discovery ecosystem. Verify rendered HTML.
- **Treating llms.txt as a priority over fundamentals.** Adding an llms.txt file before fixing crawlability, rendering, and structured data is optimizing the wrong layer. Current research shows no measurable impact from llms.txt. Implement the fundamentals first.
- **Setting up robots.txt once and never reviewing it.** New AI crawlers appear regularly. CDN providers update their bot management rules. Review robots.txt and CDN bot settings quarterly.
- **Implementing structured data that does not match visible content.** Marking up a product with a 4.5-star rating in schema when the page shows 3.2 stars is a manual action risk. Schema must reflect exactly what users see on the page.
- **Submitting sitemaps with non-canonical or non-200 URLs.** Every URL in the sitemap should return 200 and have a self-referencing canonical. Including redirects, 404s, or non-canonical URLs wastes crawl budget and sends conflicting signals.

## Available scripts

Run these scripts to automate technical checks. Each script outputs JSON. Use `scripts/inventory-tools.py` first to detect available tools — all scripts fall back to free methods (WebFetch/WebSearch) when paid tools are unavailable.

| Script | What it checks | Run it when |
|--------|---------------|-------------|
| `inventory-tools.py` | Available tools/APIs/MCPs | First — before any other script |
| `check-robots-txt.py` | robots.txt rules for search + AI bots | Starting any technical audit |
| `validate-sitemap.py` | XML sitemap structure and URL status | Starting any technical audit |
| `check-cwv.py` | Core Web Vitals via PageSpeed Insights | Evaluating page performance |
| `check-structured-data.py` | JSON-LD schema validation | Checking structured data implementation |
| `check-https-security.py` | HTTPS, redirects, HSTS, mixed content | Verifying security baseline |
| `check-ai-crawler-access.py` | AI bot accessibility (CDN/WAF blocking) | Diagnosing zero AI visibility |
| `check-mobile.py` | Mobile viewport, tap targets, content parity | Checking mobile-first readiness |
| `check-indexation.py` | Indexed pages vs sitemap count | Diagnosing indexation gaps |
| `check-redirect-chains.py` | Redirect chain length and status codes | Finding redirect issues |
