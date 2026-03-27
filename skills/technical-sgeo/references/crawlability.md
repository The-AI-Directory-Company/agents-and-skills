# Crawlability: Search Engines and AI Bots

Crawlability is the foundation of all visibility. If a crawler cannot reach your page, that page does not exist in search results or AI answers. This reference covers the mechanics of crawling for both traditional search engines and AI platforms.

## How crawlers discover pages

Both Googlebot and AI crawlers (GPTBot, ClaudeBot, PerplexityBot) discover pages through two primary mechanisms:

1. **Link following.** Crawlers find a page, extract all links, add them to a crawl queue. Internal links are how crawlers map your site structure. Pages with zero inbound internal links (orphan pages) are effectively invisible unless submitted via sitemap.
2. **Sitemap parsing.** Crawlers read your XML sitemap to discover URLs directly. This supplements link following but does not replace it. A URL in a sitemap with no internal links pointing to it sends a weak signal.

Googlebot maintains a crawl queue with priority scoring. Pages with more inbound links, more frequent updates, and faster server responses get crawled more often. AI crawlers generally operate on simpler schedules and may not revisit as frequently.

## robots.txt directive syntax

The robots.txt file at your domain root (`/robots.txt`) controls crawler access. Every search engine and responsible AI crawler reads it.

### Basic structure

```
User-agent: Googlebot
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /internal/

User-agent: GPTBot
Allow: /

User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
```

### Key directives

| Directive | Meaning | Example |
|-----------|---------|---------|
| `User-agent` | Which bot the rules apply to | `User-agent: Googlebot` |
| `Allow` | Explicitly permit crawling a path | `Allow: /blog/` |
| `Disallow` | Block crawling a path | `Disallow: /admin/` |
| `Sitemap` | Declare sitemap location | `Sitemap: https://example.com/sitemap.xml` |
| `Crawl-delay` | Request delay between requests (not honored by Google) | `Crawl-delay: 10` |

**Matching rules:** More specific paths take precedence. `Allow: /blog/important-page` overrides `Disallow: /blog/` for that specific URL. Google matches by longest path prefix. Trailing wildcards (`*`) and end-of-URL markers (`$`) are supported.

**Critical detail:** `Disallow` prevents crawling, not indexing. If a blocked URL has inbound links, Google may still index it (with no snippet). Use `noindex` meta tags to prevent indexing. But a page cannot have both `Disallow` (blocks crawl) and `noindex` (requires crawl to read the tag). Pick one.

## XML sitemap protocol

The XML sitemap tells crawlers which URLs you consider important and when they were last updated.

### Format requirements

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page/</loc>
    <lastmod>2026-03-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

### Rules that matter

- **50,000 URL limit** per sitemap file, 50MB uncompressed. Use a sitemap index for larger sites.
- **Only include canonical, 200-status URLs.** Redirects, 404s, and non-canonical URLs waste crawl budget and send conflicting signals.
- **`<lastmod>` must be accurate.** Set it to the actual content modification date, not the build date or current date. Fake lastmod dates (all identical, or always "today") cause Google to ignore lastmod entirely for your domain.
- **`<changefreq>` and `<priority>` are ignored by Google.** They remain in the spec but have no practical effect. Include them if your CMS generates them, but do not manually tune them.
- **Submit to both GSC and Bing Webmaster Tools.** Also declare in robots.txt: `Sitemap: https://example.com/sitemap.xml`

### Sitemap index for large sites

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-pages.xml</loc>
    <lastmod>2026-03-15</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-blog.xml</loc>
    <lastmod>2026-03-20</lastmod>
  </sitemap>
</sitemapindex>
```

## Crawl budget: what it is and why it matters

Crawl budget is the number of pages Google will crawl on your site within a given timeframe. For sites under 10,000 pages, crawl budget is rarely a problem. For larger sites, it becomes critical.

**What wastes crawl budget:**
- Faceted navigation URLs (e.g., `/shoes?color=red&size=10&sort=price`) — these can generate millions of low-value URLs
- URL parameter variations (`?utm_source=...`, `?ref=...`, `?page=2`)
- Duplicate content served at different URLs (www vs non-www, HTTP vs HTTPS, trailing slash variants)
- Soft 404 pages (200 status but error/empty content)
- Infinite scroll pagination without proper `<link rel="next/prev">` or sitemap coverage

**How to protect crawl budget:**
1. Block faceted URLs in robots.txt or use `noindex`
2. Set canonical tags on all parameter variants
3. Consolidate protocol and domain variants with 301 redirects
4. Return proper 404 status for deleted pages
5. Keep internal links clean — point to final canonical URLs, not redirect sources

## CDN bot-management gotchas

This is the most common cause of accidental AI visibility loss. CDN providers ship bot management features that block AI crawlers by default.

### Cloudflare

If you are on Cloudflare, check Bot Fight Mode first — it is the number one cause of accidental AI blocking.

- **Bot Fight Mode** (free plan): Blocks bots it considers "definitely automated." AI crawlers often fall into this category. Check Security > Bots.
- **Super Bot Fight Mode** (Pro+): More aggressive. Can block verified bots that are not on Cloudflare's allow list. Many AI crawlers are not on the allow list.
- **Fix:** Create WAF custom rules that Allow traffic matching AI bot user-agent strings. Or switch Bot Fight Mode to "monitor" instead of "block."

### AWS CloudFront + WAF

- AWS WAF bot control rules categorize bots into "verified" and "unverified." AI crawlers may be classified as unverified.
- Review your WAF rule groups under Bot Control. Add exceptions for specific AI bot user-agents.

### Akamai

- Akamai Bot Manager has predefined bot categories. Check whether AI crawlers are categorized and allowed.
- Custom bot definitions may be needed for newer AI crawlers.

### Fastly

- Signal Sciences (Fastly's WAF) applies bot scoring. AI crawlers may trigger automated blocking thresholds.
- Review bot detection rules and add exceptions.

### Verification

After configuring CDN settings, verify with server logs. Look for 200 responses to requests from AI bot user-agents. If you see zero AI crawler traffic in logs but have not explicitly blocked them in robots.txt, your CDN is the culprit.

## Common misconfigurations

| Problem | Symptom | Fix |
|---------|---------|-----|
| `Disallow: /` for `User-agent: *` | All bots blocked including AI crawlers | Use specific Disallow paths, not root |
| AI bots blocked in robots.txt | Zero AI visibility despite good content | Remove or change to Allow for GPTBot, ClaudeBot, etc. |
| Sitemap contains redirected URLs | Crawl budget waste, conflicting signals | Only include 200-status canonical URLs |
| CDN blocks AI bots silently | Server logs show zero AI bot requests | Check CDN bot management, add exceptions |
| Sitemap not submitted | Crawlers rely only on link following | Submit to GSC and Bing Webmaster Tools |
| `lastmod` dates all identical | Google ignores lastmod for your domain | Use actual content modification dates |
| Faceted URLs crawlable | Millions of low-value pages in crawl queue | Block with robots.txt or noindex |
