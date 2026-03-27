# Measurement Setup: GSC, GA4, Bing, and AI Tracking

Set up measurement before making any changes. Without measurement, you cannot verify implementations or detect regressions. AI-referred sessions jumped 527% year-over-year in the first five months of 2025 — if you are not tracking AI referrers, you are blind to a rapidly growing traffic channel.

## Google Search Console (GSC)

GSC is the single most important free tool. It shows you exactly what Google sees.

### Setup

1. **Verify ownership** using one of: DNS TXT record (recommended for domain-level verification), HTML file upload, HTML meta tag, or Google Analytics/Tag Manager verification.
2. **Domain property vs URL prefix:** Use domain property (`sc-domain:example.com`) when possible — it covers all subdomains and protocols in one property. URL prefix (`https://www.example.com/`) is limited to that exact prefix.
3. **Submit XML sitemap:** Indexing > Sitemaps > enter sitemap URL > Submit.

### Key reports

| Report | Location | What It Shows | Check Frequency |
|--------|----------|---------------|-----------------|
| Performance | Performance > Search results | Queries, clicks, impressions, CTR, position | Weekly |
| Index coverage | Pages > Indexing | Indexed, not indexed, reasons for exclusion | Weekly |
| Core Web Vitals | Experience > Core Web Vitals | Field CWV data (mobile + desktop) | Monthly |
| Enhancements | Various under Enhancements | Structured data errors/warnings per type | Monthly |
| URL Inspection | Top bar URL input | Per-URL crawl, index, and rendering status | As needed |

### Critical workflow: index coverage

Navigate to Pages > Indexing. The "Why pages aren't indexed" section is your action list:
- **"Discovered - currently not indexed"**: Google found the URL but chose not to crawl it. Quality or crawl budget signal. Improve content or consolidate.
- **"Crawled - currently not indexed"**: Google fetched but chose not to index. Content may be thin, duplicative, or low-value.
- **"Blocked by robots.txt"**: Unintentional blocks. Fix immediately if page should be indexed.
- **"Excluded by noindex tag"**: Intentional if you set it. If not, remove the noindex.

## Google Analytics 4 (GA4)

### Installation

1. Create a GA4 property at analytics.google.com
2. Install the tracking snippet (gtag.js) or use Google Tag Manager
3. Link GA4 to GSC: GA4 Admin > Product Links > Search Console

### Key event configuration

Configure these events as key events (formerly "conversions"):
- Form submissions (contact, demo request, signup)
- Purchases or checkout completions
- Key page views (pricing page, feature page)
- File downloads
- Outbound link clicks to important destinations

### Traffic source tracking

GA4 tracks traffic sources automatically via UTM parameters and referrer headers. Key channels to monitor:
- **Organic Search**: Traffic from Google, Bing, and other search engines
- **Referral**: Traffic from other websites linking to you
- **Direct**: Traffic with no referrer (bookmarks, typed URLs, some app traffic)
- **AI Referrers**: See the dedicated section below

## Bing Webmaster Tools

Set up Bing Webmaster Tools. It takes 10 minutes and gives you a structural advantage in AI citation because Bing's index powers Microsoft Copilot and ChatGPT's browsing feature.

### Setup

1. Go to bing.com/webmasters
2. Import directly from GSC (fastest method) or verify manually
3. Submit your XML sitemap
4. Review the SEO reports section for issues

### Why Bing matters for AI visibility

Bing's search index is the retrieval layer for multiple AI systems:
- **Microsoft Copilot**: Uses Bing search results directly
- **ChatGPT browsing**: Uses Bing's API for web search when users enable browsing
- **Other AI systems**: Several AI assistants license Bing's search API

A site well-indexed in Bing has a structural advantage in AI citation from these platforms. Bing has over 100 million daily active users independently, plus its indirect reach through AI systems.

## AI referrer tracking in GA4

AI platforms that link to your site generate referral traffic. Track it with a custom channel group.

### Custom channel group setup

1. GA4 Admin > Data display > Channel groups
2. Create a new custom channel group or modify Default
3. Add a new channel called "AI Platforms" with these rules:

| Condition | Operator | Value |
|-----------|----------|-------|
| Source | matches regex | `chat\.openai\.com|chatgpt\.com` |
| Source | matches regex | `perplexity\.ai` |
| Source | matches regex | `gemini\.google\.com` |
| Source | matches regex | `claude\.ai` |
| Source | matches regex | `copilot\.microsoft\.com` |
| Source | matches regex | `you\.com` |

4. Place this channel rule above "Referral" in the priority list so AI traffic is not lumped into generic referral

### What to track

- **Volume trend**: Is AI referral traffic growing? (The 527% YoY growth suggests it should be)
- **Landing pages**: Which pages are AI systems linking to? These are your most AI-cited content.
- **Engagement**: Do AI-referred visitors behave differently? (They often have higher intent — they specifically followed a citation)
- **Conversion rate**: Compare AI referral conversion rates against organic search

## Server log monitoring

GA4 does not capture bot traffic. Server logs are the only way to see AI crawler visits.

### Setup recommendations

1. **Ensure access to raw server logs** (Apache access.log, Nginx access.log, or CDN logs)
2. **Create a filtered view or dashboard** showing only requests from known AI bot user-agents
3. **Track weekly**: total requests per bot, response code distribution, top requested pages
4. **Alert on anomalies**: sudden drops in AI bot traffic (may indicate new CDN blocking), new bot user-agents, spikes in non-200 responses

### Bot user-agents to monitor

Filter logs for these strings: `GPTBot`, `ChatGPT-User`, `OAI-SearchBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, `Bytespider`, `Googlebot`, `Bingbot`.

Track search engine bots alongside AI bots — they share crawlability infrastructure, and a regression in one often indicates a regression in the other.

### Dashboard metrics

| Metric | What It Tells You |
|--------|-------------------|
| Requests per bot per week | Whether each bot is actively crawling your site |
| Response code distribution | Whether bots are getting 200s or being blocked |
| Top requested pages | Which content bots prioritize |
| New/changed pages crawled | Whether fresh content is being discovered |
| Crawl frequency trend | Whether bot interest is increasing or decreasing |
