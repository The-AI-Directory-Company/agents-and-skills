# SGEO Skills Enrichment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enrich four SGEO skills with `references/` and `scripts/` directories, turning procedural guides into tool-augmented workflows with 32 executable Python scripts and 20 reference documents.

**Architecture:** Each skill folder is self-contained per the Agent Skills spec. References are topic-scoped markdown files loaded on-demand. Scripts are executable Python files that use WebFetch/WebSearch as free baseline with optional paid tool extensions. All 4 skills get a Tool Discovery section prepended to their SKILL.md. Tasks are organized so all 4 skills can be built in parallel.

**Tech Stack:** Python 3.9+ (scripts), Markdown (references), WebFetch/WebSearch/PageSpeed Insights API (free tier), DataForSEO/Ahrefs/Semrush APIs (optional paid tier)

**Spec:** `docs/superpowers/specs/2026-03-27-sgeo-skills-enrichment-design.md`
**Source guide:** `docs/seo-geo-marketing-guide.md`

**Parallelization:** Tasks 1-4 are fully independent (one per skill). Dispatch all 4 simultaneously. Task 5 depends on Tasks 1-4 completing.

---

## Task 1: technical-sgeo — References, Scripts, and SKILL.md Update

**Files:**
- Create: `skills/technical-sgeo/references/crawlability.md`
- Create: `skills/technical-sgeo/references/core-web-vitals.md`
- Create: `skills/technical-sgeo/references/structured-data.md`
- Create: `skills/technical-sgeo/references/ai-crawler-access.md`
- Create: `skills/technical-sgeo/references/measurement-setup.md`
- Create: `skills/technical-sgeo/scripts/inventory-tools.py`
- Create: `skills/technical-sgeo/scripts/check-robots-txt.py`
- Create: `skills/technical-sgeo/scripts/validate-sitemap.py`
- Create: `skills/technical-sgeo/scripts/check-cwv.py`
- Create: `skills/technical-sgeo/scripts/check-structured-data.py`
- Create: `skills/technical-sgeo/scripts/check-https-security.py`
- Create: `skills/technical-sgeo/scripts/check-ai-crawler-access.py`
- Create: `skills/technical-sgeo/scripts/check-mobile.py`
- Create: `skills/technical-sgeo/scripts/check-indexation.py`
- Create: `skills/technical-sgeo/scripts/check-redirect-chains.py`
- Modify: `skills/technical-sgeo/SKILL.md`

All paths relative to `/Users/raul/projects/ai-directory-company/apps/web/content/community/`.

### References

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p skills/technical-sgeo/references skills/technical-sgeo/scripts
```

- [ ] **Step 2: Write `references/crawlability.md` (150-200 lines)**

Deep reference on crawl mechanics for both search engines and AI bots. Must cover:
- How Googlebot and AI crawlers discover pages (crawl queue, URL discovery, link following)
- robots.txt directive syntax with complete examples (User-agent, Allow, Disallow, Crawl-delay)
- XML sitemap protocol spec (format, limits, lastmod, sitemap index for large sites)
- Crawl budget theory — what it is, why it matters, how to avoid wasting it (faceted URLs, parameters, duplicates)
- CDN bot-management gotchas: Cloudflare Bot Fight Mode (default blocks AI bots), AWS WAF bot control rules, Akamai bot manager, Fastly signal sciences
- Common misconfigurations with fix examples
- Tone: Practitioner. Opinionated. Example: "If you're on Cloudflare, check Bot Fight Mode first — it's the #1 cause of accidental AI blocking."
- SEO and GEO perspectives integrated throughout, not separated

Source material: `docs/seo-geo-marketing-guide.md` Section 2 Pillar 1 + Section 7 GEO Technical Checklist.

- [ ] **Step 3: Write `references/core-web-vitals.md` (150-200 lines)**

CWV optimization playbook. Must cover:
- LCP/INP/CLS definitions, thresholds (Good: LCP <2.5s, INP <200ms, CLS <0.1), and what each measures
- Root causes per metric:
  - LCP: slow TTFB, render-blocking resources, large hero images, slow font loading
  - INP: long main-thread tasks, heavy JS bundles, unoptimized event handlers
  - CLS: images without dimensions, dynamically injected content, late-loading ads
- Fix patterns by framework:
  - Next.js: next/image, next/font, server components, streaming SSR
  - WordPress: image optimization plugins, caching (WP Rocket, W3TC), lazy loading
  - Shopify: theme optimization, app script management, image CDN
- Field data vs lab data interpretation — when they disagree and why field data wins
- PageSpeed Insights API usage (free, no key for basic requests) — exact endpoint and response parsing
- Chrome DevTools Performance panel workflow for debugging INP
- Tone: "Lighthouse 100 on your MacBook means nothing. Field data is the only truth."

Source material: `docs/seo-geo-marketing-guide.md` Section 2 Pillar 1 (Page Speed) + Section 7.

- [ ] **Step 4: Write `references/structured-data.md` (200-250 lines)**

Schema.org implementation guide. Must cover:
- JSON-LD as the preferred format (Google's recommendation), placed in `<script type="application/ld+json">`
- Complete templates for every page type:
  - Organization (homepage): name, url, logo, sameAs, contactPoint
  - Product: name, description, image, offers (price, currency, availability), aggregateRating, review
  - Article: headline, datePublished, dateModified, author (Person with jobTitle, url), publisher, image
  - FAQPage: mainEntity array of Question + acceptedAnswer
  - HowTo: name, step array of HowToStep with text + image
  - LocalBusiness: name, address, telephone, openingHoursSpecification, geo
  - Service: name, description, provider, areaServed, serviceType
  - BreadcrumbList: itemListElement array
- Nesting patterns (Organization inside Article publisher, Person inside Article author)
- Validation workflow: Rich Results Test URL, GSC Enhancements report, Schema.org validator
- FAQ Schema as GEO accelerator — why Q&A structure maps directly to AI query patterns
- Common mistakes: schema not matching visible content (manual action risk), using Microdata instead of JSON-LD, missing required properties
- Tone: Practitioner. "FAQ Schema is your single best GEO investment for structured data. Pre-package Q&A pairs and AI engines extract them directly."

Source material: `docs/seo-geo-marketing-guide.md` Section 2 Pillar 1 (Structured data) + Section 7.

- [ ] **Step 5: Write `references/ai-crawler-access.md` (150-200 lines)**

Complete guide to AI bot management. Must cover:
- User-agent string table for every known AI crawler:
  - GPTBot (OpenAI, training + browsing)
  - ChatGPT-User (OpenAI, live browsing)
  - OAI-SearchBot (OpenAI, search results)
  - ClaudeBot (Anthropic, training + retrieval)
  - PerplexityBot (Perplexity, search answers)
  - Google-Extended (Google, Gemini training)
  - Bytespider (ByteDance, TikTok AI)
- robots.txt examples: allow all AI bots, allow specific bots, block specific bots
- CDN configuration per provider:
  - Cloudflare: Bot Fight Mode settings, Super Bot Fight Mode, WAF custom rules for AI bots
  - AWS: WAF bot control rule groups, CloudFront custom headers
  - Akamai: Bot Manager configuration
  - Fastly: Signal Sciences bot management
- Server log queries to verify bot access (grep/awk examples for common log formats)
- Content accessibility requirements for AI consumption: SSR vs CSR, no auth gates, no cookie walls, no iframe-isolated content
- llms.txt: specification, research findings (SE Ranking 300K domains, OtterlyAI 90-day study, ALLMO 94K+ URLs — all found no measurable impact), verdict (low effort, no harm, don't prioritize over fundamentals)
- Tone: "Many robots.txt files inherited AI blocks from 2023 panic. Review yours — those blocks are now costing you AI visibility."

Source material: `docs/seo-geo-marketing-guide.md` Section 3 + Section 7 GEO Technical Checklist.

- [ ] **Step 6: Write `references/measurement-setup.md` (100-150 lines)**

GSC/GA4/Bing Webmaster Tools setup walkthrough. Must cover:
- Google Search Console: domain verification methods, sitemap submission, index coverage report walkthrough, performance report (queries, pages, countries, devices), Core Web Vitals report
- Google Analytics 4: installation, key event configuration, traffic source tracking, conversion setup
- Bing Webmaster Tools: site verification, why it matters for AI (Bing index feeds Microsoft Copilot, ChatGPT browsing), URL submission, SEO reports
- AI referrer tracking in GA4: custom channel group for chat.openai.com, perplexity.ai, gemini.google.com, claude.ai — exact configuration steps
- Server log monitoring: setting up queries for AI bot user-agents, dashboard recommendations, frequency (weekly minimum)
- The "527% year-over-year" AI traffic growth stat as motivation for early tracking setup
- Tone: Practitioner. "Set up Bing Webmaster Tools. It takes 10 minutes and gives you a structural advantage in AI citation because Bing's index powers Copilot and ChatGPT."

Source material: `docs/seo-geo-marketing-guide.md` Section 4 Phase 1 + Section 5 + Section 8.

### Scripts

Each script must:
- Accept command-line arguments (URL, domain, etc.) via argparse
- Accept `--tools` flag or read `tools.json` for available tool inventory
- Output structured JSON to stdout (parseable by the agent)
- Include `--help` documentation
- Have a `#!/usr/bin/env python3` shebang and be executable
- Work with free tools (WebFetch/WebSearch) as baseline
- Include clear comments explaining what each section does
- Handle errors gracefully with fallback instructions
- Include rate limiting for external API calls

Scripts in this skill are meant to be READ by AI agents using the skill — agents understand the script's logic and execute equivalent operations using their available tools (WebFetch, WebSearch, Playwright MCP, etc.). Scripts also work as standalone CLI tools when run directly.

- [ ] **Step 7: Write `scripts/inventory-tools.py`**

Utility script that probes which tools/APIs are reachable. Checks:
- WebFetch availability (try fetching a known URL)
- WebSearch availability
- PageSpeed Insights API (fetch `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com`)
- DataForSEO API (if credentials provided, try auth endpoint)
- Ahrefs API (if key provided, try auth)
- Semrush API (if key provided, try auth)
- Playwright MCP / Chrome DevTools MCP availability

Outputs JSON: `{"webfetch": true, "websearch": true, "psi_api": true, "dataforseo": false, "ahrefs": false, ...}`

Other scripts consume this inventory to decide which code paths to take.

- [ ] **Step 8: Write `scripts/check-robots-txt.py`**

Fetches `{domain}/robots.txt`, parses all User-agent/Allow/Disallow directives. Specifically checks:
- Googlebot rules (allowed paths, blocked paths)
- Bingbot rules
- AI crawler rules: GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended
- Wildcard (*) rules that affect all bots
- Sitemap declarations in robots.txt
- Missing bot entries (no rule = allowed, but flag as "not explicitly managed")

Output JSON with per-bot status: `{"bots": {"Googlebot": {"status": "allowed", "blocked_paths": ["/admin"]}, "GPTBot": {"status": "not_mentioned", "recommendation": "Add explicit Allow rule"}, ...}, "sitemaps": ["https://example.com/sitemap.xml"]}`

Free path: WebFetch to `{domain}/robots.txt`. No paid extension needed.

- [ ] **Step 9: Write `scripts/validate-sitemap.py`**

Fetches XML sitemap (or sitemap index), validates:
- Valid XML structure
- URL count (warn if >50,000 per file)
- File size (warn if >50MB uncompressed)
- `<lastmod>` dates: present, ISO 8601 format, not all identical (flag fake dates), not future dates
- Samples 10 random URLs and checks for 200 status via HEAD requests
- If sitemap index, recursively validates child sitemaps
- Checks for sitemap declaration in robots.txt

Output JSON: `{"valid": true, "url_count": 847, "urls_with_lastmod": 800, "sampled_urls": [{"url": "...", "status": 200}, ...], "issues": [...]}`

Free path: WebFetch. Paid extension: DataForSEO on-page API for bulk URL status checking (faster for large sitemaps).

- [ ] **Step 10: Write `scripts/check-cwv.py`**

Calls Google PageSpeed Insights API for a URL. Extracts:
- LCP value (field + lab), LCP element identification
- INP value (field if available), interaction diagnostics
- CLS value (field + lab), CLS-causing elements
- TTFB (field + lab)
- Overall performance score
- Field data availability flag (some sites lack CrUX data)

API endpoint: `https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy={mobile|desktop}&category=performance`

Parse `lighthouseResult.audits` for specific metrics and `loadingExperience.metrics` for field data.

Output JSON: `{"url": "...", "strategy": "mobile", "field_data_available": true, "metrics": {"lcp": {"field_p75": 2.1, "lab": 1.8, "status": "good", "element": "img.hero"}, ...}, "score": 85}`

Free path: PSI API (no key needed for basic usage, rate limit ~25 req/100s). Paid extension: Chrome DevTools MCP for live Performance panel tracing.

- [ ] **Step 11: Write `scripts/check-structured-data.py`**

Fetches a page, extracts all `<script type="application/ld+json">` blocks, parses JSON-LD:
- Identifies schema types present (Organization, Product, Article, FAQPage, etc.)
- Validates required properties per type (reference `references/structured-data.md` property lists)
- Flags missing recommended properties
- Checks for common errors: invalid JSON, wrong @context, missing @type
- Validates nesting (author inside Article, offers inside Product)

Output JSON: `{"url": "...", "schemas_found": [{"type": "Article", "valid": true, "properties": {...}, "missing_recommended": ["dateModified"], "errors": []}], "rich_result_eligible": true}`

Free path: WebFetch + JSON parsing. Paid extension: DataForSEO on-page analysis for cross-referencing with visible content.

- [ ] **Step 12: Write `scripts/check-https-security.py`**

Checks HTTPS implementation:
- Verify URL is served over HTTPS (follow redirects from HTTP, record chain)
- Check redirect chain from `http://domain.com` → final HTTPS destination
- Validate HSTS header: `Strict-Transport-Security` present, `max-age` ≥ 31536000, `includeSubDomains` flag
- Check for mixed content indicators in HTML (http:// resource URLs in `<script>`, `<link>`, `<img>` tags)
- SSL certificate basic info (not expired, matches domain)

Output JSON: `{"https": true, "redirect_chain": ["http://example.com → 301 → https://example.com"], "hsts": {"present": true, "max_age": 31536000, "include_subdomains": true}, "mixed_content": [], "certificate_valid": true}`

Free path: WebFetch with redirect following. No paid extension.

- [ ] **Step 13: Write `scripts/check-ai-crawler-access.py`**

Tests whether AI crawlers can access a page by fetching with different User-Agent strings:
- Standard browser UA (baseline)
- GPTBot UA
- ClaudeBot UA
- PerplexityBot UA

For each: record HTTP status code, response size, whether content matches baseline. A significantly different response (403, 503, empty body, captcha page) indicates blocking.

Output JSON: `{"url": "...", "baseline": {"status": 200, "size": 45000, "has_content": true}, "bots": {"GPTBot": {"status": 200, "size": 45000, "content_match": true}, "ClaudeBot": {"status": 403, "size": 1200, "content_match": false, "likely_blocked": true}}, "recommendation": "ClaudeBot is blocked — check CDN bot management settings"}`

Free path: WebFetch with custom headers. Paid extension: Playwright MCP for full rendering comparison (detects JS-based bot detection).

- [ ] **Step 14: Write `scripts/check-mobile.py`**

Checks mobile-friendliness:
- Fetch page HTML, check for `<meta name="viewport" content="width=device-width, initial-scale=1">`
- Parse for mobile-unfriendly patterns: fixed-width containers, horizontal overflow indicators, tiny font sizes in CSS
- If Playwright MCP available: render at 375px width, take screenshot, check for horizontal scrollbar, measure tap target sizes

Output JSON: `{"url": "...", "viewport_meta": true, "viewport_content": "width=device-width, initial-scale=1", "potential_issues": ["Fixed width container found: .main-content { width: 1200px }"], "playwright_available": false, "recommendation": "..."}`

Free path: WebFetch + HTML parsing. Paid extension: Playwright MCP or Chrome DevTools MCP for visual rendering analysis.

- [ ] **Step 15: Write `scripts/check-indexation.py`**

Estimates indexation status:
- Run `site:domain.com` via WebSearch, extract approximate result count
- Compare against sitemap URL count (if `validate-sitemap.py` output available)
- Run `site:domain.com/important-path` for key sections to check partial indexation
- Flag large discrepancies (indexed >> sitemap = duplicate content; indexed << sitemap = indexation issues)

Output JSON: `{"domain": "...", "estimated_indexed": 1250, "sitemap_count": 847, "ratio": 1.48, "status": "over_indexed", "recommendation": "More pages indexed than in sitemap — likely duplicate content or parameter URLs being indexed. Check canonical tags.", "section_checks": [{"path": "/blog", "estimated": 450}, ...]}`

Free path: WebSearch. Paid extension: DataForSEO SERP API for precise indexed page counts.

- [ ] **Step 16: Write `scripts/check-redirect-chains.py`**

Follows redirect chains for a list of URLs:
- For each URL, follow all redirects (301, 302, 307, 308, meta refresh) up to 10 hops
- Record each hop: URL, status code, redirect type
- Flag chains >2 hops
- Flag redirect loops
- Flag mixed protocol redirects (HTTPS → HTTP)

Input: list of URLs (stdin, one per line, or `--url` flag for single URL)
Output JSON: `{"results": [{"original_url": "...", "chain_length": 3, "hops": [{"url": "...", "status": 301, "location": "..."}, ...], "final_url": "...", "final_status": 200, "issues": ["Chain exceeds 2 hops"]}]}`

Free path: WebFetch with redirect following disabled (manual hop tracking). No paid extension.

### SKILL.md Update

- [ ] **Step 17: Update `skills/technical-sgeo/SKILL.md`**

Insert the Tool Discovery section immediately after the frontmatter closing `---` and before the `# Technical SGEO Setup` heading. Use the exact template from the spec's "Shared Pattern: Tool Discovery Section."

Then add script and reference pointers throughout the existing sections:

- Section 1 (Measurement Infrastructure): Add → "See `references/measurement-setup.md` for detailed setup walkthrough. Run `scripts/inventory-tools.py` to detect available tools."
- Section 2 (Crawlability for Search Engines): Add → "Run `scripts/check-robots-txt.py` to audit robots.txt rules. Run `scripts/validate-sitemap.py` to validate your XML sitemap. Run `scripts/check-redirect-chains.py` to find redirect chains. See `references/crawlability.md` for deep context on crawl mechanics."
- Section 3 (Crawlability for AI Engines): Add → "Run `scripts/check-ai-crawler-access.py` to test whether AI crawlers can reach your pages. See `references/ai-crawler-access.md` for the complete AI bot user-agent table and CDN configuration guides."
- Section 4 (Indexation Control): Add → "Run `scripts/check-indexation.py` to estimate indexed vs submitted page counts."
- Section 5 (Core Web Vitals): Add → "Run `scripts/check-cwv.py` to pull PageSpeed Insights data. See `references/core-web-vitals.md` for fix patterns by framework."
- Section 6 (Mobile-First and HTTPS): Add → "Run `scripts/check-mobile.py` for mobile-friendliness checks. Run `scripts/check-https-security.py` to verify HTTPS and HSTS."
- Section 7 (Structured Data Foundation): Add → "Run `scripts/check-structured-data.py` to extract and validate JSON-LD. See `references/structured-data.md` for templates per page type."

After the "Common mistakes to avoid" section, add a new section:

```markdown
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
```

- [ ] **Step 18: Commit**

```bash
git add skills/technical-sgeo/
git commit -m "feat(technical-sgeo): add references and scripts for tool-augmented workflow

Add 5 reference files covering crawlability, Core Web Vitals, structured data,
AI crawler access, and measurement setup. Add 10 Python scripts for automated
checks including robots.txt, sitemap validation, CWV, structured data, HTTPS,
AI crawler access, mobile, indexation, and redirect chains. Update SKILL.md
with Tool Discovery section and script/reference pointers."
```

---

## Task 2: on-page-sgeo — References, Scripts, and SKILL.md Update

**Files:**
- Create: `skills/on-page-sgeo/references/meta-optimization.md`
- Create: `skills/on-page-sgeo/references/heading-and-structure.md`
- Create: `skills/on-page-sgeo/references/geo-formatting.md`
- Create: `skills/on-page-sgeo/references/internal-linking.md`
- Create: `skills/on-page-sgeo/references/image-and-media.md`
- Create: `skills/on-page-sgeo/scripts/extract-meta-tags.py`
- Create: `skills/on-page-sgeo/scripts/analyze-headings.py`
- Create: `skills/on-page-sgeo/scripts/check-direct-answer.py`
- Create: `skills/on-page-sgeo/scripts/check-internal-links.py`
- Create: `skills/on-page-sgeo/scripts/check-images.py`
- Create: `skills/on-page-sgeo/scripts/extract-structured-data.py`
- Create: `skills/on-page-sgeo/scripts/check-freshness.py`
- Create: `skills/on-page-sgeo/scripts/audit-page.py`
- Modify: `skills/on-page-sgeo/SKILL.md`

All paths relative to `/Users/raul/projects/ai-directory-company/apps/web/content/community/`.

### References

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p skills/on-page-sgeo/references skills/on-page-sgeo/scripts
```

- [ ] **Step 2: Write `references/meta-optimization.md` (120-150 lines)**

Title tag and meta description craft. Must cover:
- Title tag: character limit (60 chars / ~580px), keyword placement (front-load), specificity rules, pipe-separated keyword stuffing as anti-pattern
- Meta description: 155 character limit, value proposition framing, active voice, complete-sentence rule for GEO (AI engines pull meta as summary)
- OG tags: og:title, og:description, og:image, og:type — requirements for social sharing and AI card rendering
- Canonical tag: self-referencing rules, absolute URLs, placement in `<head>`
- Good vs bad examples by industry:
  - SaaS: "Invoice Automation Software: Cut Processing Time 80% | Acme" vs "Acme | Invoice | Automation | Software | Best"
  - E-commerce: "Women's Running Shoes — Free Shipping Over $50 | BrandName" vs "Buy Shoes Online — Best Shoes — Running Shoes Sale"
  - Content: "What Is Technical SEO? A 15-Point Checklist for 2026" vs "SEO Guide | Best SEO Tips | SEO Company"
- Tone: "If your title starts with your brand name, you're wasting the most valuable real estate on the page — unless you're Nike."

Source: `docs/seo-geo-marketing-guide.md` Section 2 Pillar 2 (Title tags, Meta descriptions).

- [ ] **Step 3: Write `references/heading-and-structure.md` (150-180 lines)**

Heading hierarchy rules + GEO question-format patterns. Must cover:
- One H1 per page rule, alignment with title tag
- H2 for major sections, H3 for subsections, never skip levels
- GEO question-format pattern: why questions match AI queries, when to use questions vs declarative headings
- H2 templates by intent type:
  - Informational: "What Is [X]?", "How Does [X] Work?", "Why Is [X] Important?"
  - Commercial: "How Much Does [X] Cost?", "[X] vs [Y]: Which Is Better?", "Is [X] Worth It?"
  - Transactional: "How to Get Started with [X]", "Where to Buy [X]"
  - Procedural: "Step 1: [Action]" (declarative is fine for procedures)
- 10+ before/after heading rewrites across industries:
  - "Pricing" → "How Much Does [Product] Cost in 2026?"
  - "Features" → "What Can [Product] Do?"
  - "Getting Started" → "How to Set Up [Product] in 5 Minutes"
  - "Benefits" → "Why Do Teams Switch to [Product]?"
  - "FAQ" → keep as "Frequently Asked Questions" (already a recognized pattern)
  - Plus 5+ more across e-commerce, content, SaaS
- When NOT to use question format: reference tables, changelogs, legal pages, API docs
- Tone: Practitioner. "Not every heading should be a question. Use questions for informational and commercial sections. Procedures and reference material read better with declarative headings."

Source: `docs/seo-geo-marketing-guide.md` Section 2 Pillar 2 (Heading hierarchy) + Section 3 (Question-format headers).

- [ ] **Step 4: Write `references/geo-formatting.md` (180-220 lines)**

Core GEO on-page reference. Must cover:
- Direct-answer-first pattern: first 200 words must directly answer the primary question, no meandering intros
  - 3 before/after rewrite examples across different content types (blog post, product page, documentation)
- Self-contained knowledge blocks: 50-150 words, extractable by AI, no anaphoric references
  - Anaphoric reference checklist: "As mentioned above", "This approach", "It" (at section start), "The above", "See previous section"
  - 3 before/after rewrite examples showing dependent → self-contained conversion
- Citation-worthy passage construction: specific data, named sources, dates, named entities
  - Formula: [Topic sentence with key claim] + [Specific data point with source] + [Implication or context]
  - 3 examples of weak vs strong passages
- Per-section scoring rubric (0-8 scale, used by `check-direct-answer.py`):
  - 0-2: Not citable (vague, dependent on context, no data)
  - 3-5: Partially citable (has some specific data but structure is weak)
  - 6-8: Citation-ready (self-contained, data-rich, source-cited, clear topic sentence)
- Scoring criteria: Direct answer present (0-2), Self-contained (0-2), Specific data (0-2), Source attribution (0-2)
- Tone: "AI engines don't cite entire pages. They extract passages. If your best content is buried in paragraph 5 after a lengthy intro, it's invisible to every AI platform."

Source: `docs/seo-geo-marketing-guide.md` Section 3 (GEO techniques) + Section 6 (Content creation framework).

- [ ] **Step 5: Write `references/internal-linking.md` (120-150 lines)**

Link strategy reference. Must cover:
- Link equity theory (simplified): links pass authority, internal links distribute it across your site, more links to a page = more authority signal
- Anchor text taxonomy with risk level:
  - Branded ("Acme Corp"): Safe, always appropriate
  - Natural/descriptive ("technical SEO audit guide"): Safe, most valuable for both SEO and GEO
  - Exact match keyword ("technical SEO"): Moderate risk if overused, fine in moderation
  - Generic ("click here", "learn more", "read this"): Waste of signal, avoid
  - Over-optimized ("best technical SEO audit checklist tool 2026"): High risk, spam signal
- Contextual linking (within body content) vs navigational (sidebar, footer, breadcrumbs) — contextual carries more weight
- Click depth optimization: important pages within 3 clicks of homepage, use breadcrumbs + in-content links
- Link audit workflow: crawl site, map click depth, identify orphan pages, identify pages with zero internal links pointing to them, identify over-linked pages
- GEO consideration: "A well-linked site signals topical authority. AI engines follow internal links to build context about your expertise — making any individual page more likely to be cited."
- Target: 3-5 internal links per 1,000 words, descriptive anchors

Source: `docs/seo-geo-marketing-guide.md` Section 2 Pillar 2 (Internal linking).

- [ ] **Step 6: Write `references/image-and-media.md` (100-130 lines)**

Image optimization reference. Must cover:
- Format decision tree:
  - Photographs/complex images → WebP (95% browser support), AVIF for cutting-edge (85% support)
  - Icons/illustrations/logos → SVG (scalable, tiny file size)
  - Screenshots with text → PNG or WebP (avoid JPEG artifacts on text)
  - Animated content → consider video over GIF (90% smaller)
- Compression targets by image role:
  - Hero/above-fold: <150KB (critical for LCP)
  - In-content: <100KB
  - Thumbnails: <30KB
  - Icons: <5KB
- Responsive images: `srcset` and `sizes` attributes, art direction with `<picture>`
- Lazy loading rules: `loading="lazy"` on all below-fold images, NEVER on the LCP image, never on first viewport content
- CLS prevention: always set `width` and `height` attributes OR use CSS `aspect-ratio`, reserve space for lazy-loaded images
- Alt text guide:
  - Descriptive, concise, under 125 characters
  - Include keyword ONLY if the image genuinely relates to it
  - Describe what the image shows, not what you want to rank for
  - Decorative images: `alt=""` (empty, not omitted)
  - Good: `alt="Screaming Frog crawl report showing 47 pages with redirect chains"`
  - Bad: `alt="SEO audit tool best technical SEO"` (keyword stuffing)
- File naming: descriptive, hyphenated (`technical-seo-audit-results.webp` not `IMG_4827.jpg`)
- Tools: Squoosh (manual), Sharp (Node.js pipeline), next/image (Next.js), Imagify/ShortPixel (WordPress)

Source: `docs/seo-geo-marketing-guide.md` Section 2 Pillar 2 (Image optimization).

### Scripts

Same conventions as Task 1 scripts (argparse, JSON output, `--tools` flag, shebang, error handling).

- [ ] **Step 7: Write `scripts/extract-meta-tags.py`**

Fetch URL, extract from HTML:
- `<title>` tag content and character count
- `<meta name="description">` content and character count
- `<meta name="robots">` content
- `<link rel="canonical">` href
- All OG tags (`og:title`, `og:description`, `og:image`, `og:type`, `og:url`)
- Twitter card tags (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`)

Validate: title <60 chars, description <155 chars, canonical is absolute URL, canonical matches current URL (self-referencing check).

Flag: keyword repetition in title (>2x same word = stuffing), missing OG image, meta robots noindex on a page that should be indexed.

Output JSON: `{"url": "...", "title": {"content": "...", "length": 52, "valid": true}, "meta_description": {"content": "...", "length": 140, "valid": true}, "canonical": {"href": "...", "self_referencing": true}, "og_tags": {...}, "issues": [...]}`

- [ ] **Step 8: Write `scripts/analyze-headings.py`**

Fetch URL, extract all headings (H1-H6) in document order:
- Count H1 tags (should be exactly 1)
- Build hierarchy tree, check for skipped levels (H1→H3 without H2)
- For each H2: classify as question-format ("What/How/Why/When/Where/Is/Can/Does") or declarative
- Calculate GEO heading score: % of H2s that are question-format (higher = better for GEO, target 40-60% for content pages)
- Check H1 alignment with title tag (semantic similarity, not exact match)

Output JSON: `{"url": "...", "h1_count": 1, "h1_text": "...", "headings": [{"level": 2, "text": "...", "is_question": true}, ...], "hierarchy_valid": true, "skipped_levels": [], "question_heading_ratio": 0.6, "geo_heading_score": "good"}`

- [ ] **Step 9: Write `scripts/check-direct-answer.py`**

Fetch URL, extract text content after the first H1 heading:
- Get first 200 words (excluding navigation, header, sidebar content — target the `<main>` or `<article>` element)
- Analyze opening for direct-answer patterns:
  - Starts with a definition or clear statement (good)
  - Starts with "In today's...", "As we all know...", "When it comes to..." (bad — meandering intro)
  - Contains specific data points in first 200 words (good for GEO)
  - Contains anaphoric references (bad — "As mentioned above", "This approach")
- Score on the 0-8 GEO per-section rubric from `references/geo-formatting.md`:
  - Direct answer present (0-2)
  - Self-contained (0-2)
  - Specific data (0-2)
  - Source attribution (0-2)

Output JSON: `{"url": "...", "first_200_words": "...", "score": 6, "breakdown": {"direct_answer": 2, "self_contained": 2, "specific_data": 1, "source_attribution": 1}, "issues": ["No source citations in opening"], "meandering_patterns": [], "anaphoric_references": []}`

- [ ] **Step 10: Write `scripts/check-internal-links.py`**

Fetch URL, extract all `<a>` tags with internal hrefs (same domain):
- Count total internal links
- Calculate links per ~1000 words (extract word count from body content)
- Evaluate each anchor text: classify as descriptive, generic ("click here", "learn more", "read more", "here"), branded, or over-optimized
- Check each linked URL responds with 200 (sample first 20 if many links)
- Identify links in body content vs navigation/sidebar/footer

Output JSON: `{"url": "...", "total_internal_links": 24, "body_links": 12, "nav_links": 12, "word_count": 3200, "links_per_1000_words": 3.75, "anchor_analysis": {"descriptive": 8, "generic": 3, "branded": 1, "over_optimized": 0}, "broken_links": [], "generic_anchors": [{"text": "click here", "href": "/guide"}], "issues": [...]}`

Free path: WebFetch. Paid extension: DataForSEO on-page for deeper site-wide link graph.

- [ ] **Step 11: Write `scripts/check-images.py`**

Fetch URL, extract all `<img>` tags:
- For each image: src, alt text (present? descriptive? keyword-stuffed?), width/height attributes (present?), loading attribute (lazy?), file format (from URL extension or Content-Type header)
- For first 10 images: HEAD request to get Content-Length (file size estimate)
- Flag: missing alt text, empty alt on non-decorative images, alt text >125 chars, missing width/height (CLS risk), legacy formats (JPEG/PNG where WebP would work), files >200KB, lazy loading on likely-above-fold images (first 2 images)
- Check for `<picture>` elements with `<source>` tags (responsive image implementation)

Output JSON: `{"url": "...", "total_images": 15, "images": [{"src": "...", "alt": "...", "alt_quality": "good|missing|keyword_stuffed", "dimensions_set": true, "lazy_loading": true, "format": "webp", "estimated_size_kb": 85}], "issues": [{"type": "missing_alt", "src": "..."}, {"type": "large_file", "src": "...", "size_kb": 450}]}`

Free path: WebFetch + HEAD requests. Paid extension: Playwright MCP for rendered image analysis (actual rendered dimensions, viewport position).

- [ ] **Step 12: Write `scripts/extract-structured-data.py`**

Fetch URL, extract all `<script type="application/ld+json">` blocks:
- Parse each JSON-LD block
- Identify @type for each
- Validate against the page-type mapping from SKILL.md Section 8:
  - Article: requires headline, author, datePublished, dateModified
  - Product: requires name, offers (with price, currency, availability)
  - FAQPage: requires mainEntity with Question/acceptedAnswer pairs
  - Organization: requires name, url
  - HowTo: requires name, step array
- Flag: invalid JSON, missing @context, missing @type, missing required properties, dateModified absent from Article schema

Output JSON: `{"url": "...", "schemas": [{"type": "Article", "valid": true, "properties": {"headline": "...", "datePublished": "2025-06-15", "dateModified": "2026-03-20"}, "missing_required": [], "missing_recommended": []}], "total_schemas": 1, "issues": []}`

- [ ] **Step 13: Write `scripts/check-freshness.py`**

Fetch URL, check for freshness signals:
- Search HTML for visible date patterns: "Last updated", "Published on", "Updated:", common date formats (YYYY-MM-DD, Month DD YYYY, etc.) in `<time>`, `<span>`, `<p>` elements
- Extract datePublished and dateModified from JSON-LD Article/BlogPosting schema
- Check for author byline: look for `<a>` or text near "by", "author", `rel="author"`, schema Person
- If author found: check if it links to an author page (href to /author/, /team/, /about/)
- Calculate days since last visible update

Output JSON: `{"url": "...", "visible_date": {"found": true, "text": "Last updated March 20, 2026", "parsed_date": "2026-03-20", "days_ago": 7}, "schema_dates": {"datePublished": "2025-06-15", "dateModified": "2026-03-20"}, "dates_match": true, "author": {"found": true, "name": "Jane Smith", "has_author_page_link": true, "author_page_url": "/team/jane-smith"}, "freshness_score": "good", "issues": []}`

- [ ] **Step 14: Write `scripts/audit-page.py`**

Orchestrator script — runs all 7 other scripts against a single URL and aggregates results into the On-Page SGEO Audit Table format from SKILL.md Section 10.

- Accept `--url` and `--tools` arguments
- Run each script (by importing or subprocess), collect JSON outputs
- Map results to the audit table columns: Element, SEO Impact, GEO Impact, What to Check, Status (pass/fail/warn)
- Calculate overall page score: count of pass/fail/warn across all elements
- Output both JSON (for programmatic use) and a formatted markdown table (for human reading, via `--format md` flag)

The markdown table output should match the exact format from SKILL.md Section 10:

```
| Element                    | SEO Impact | GEO Impact | Status | Finding                           |
|----------------------------|------------|------------|--------|-----------------------------------|
| Title tag                  | High       | Medium     | PASS   | 52 chars, keyword present         |
| ...                        |            |            |        |                                   |
```

- [ ] **Step 15: Update `skills/on-page-sgeo/SKILL.md`**

Same pattern as Task 1 Step 17. Insert Tool Discovery section after frontmatter. Add script and reference pointers per section:

- Section 1 (Title Tag & Meta Description): → "Run `scripts/extract-meta-tags.py`. See `references/meta-optimization.md`."
- Section 2 (URL Structure): No script (manual check), no reference needed.
- Section 3 (Heading Hierarchy): → "Run `scripts/analyze-headings.py`. See `references/heading-and-structure.md`."
- Section 4 (Direct-Answer-First): → "Run `scripts/check-direct-answer.py`. See `references/geo-formatting.md`."
- Section 5 (Knowledge Blocks): → "See `references/geo-formatting.md` for the scoring rubric."
- Section 6 (Internal Linking): → "Run `scripts/check-internal-links.py`. See `references/internal-linking.md`."
- Section 7 (Image Optimization): → "Run `scripts/check-images.py`. See `references/image-and-media.md`."
- Section 8 (Structured Data): → "Run `scripts/extract-structured-data.py`."
- Section 9 (Freshness Signals): → "Run `scripts/check-freshness.py`."
- Section 10 (Audit Table): → "Run `scripts/audit-page.py --format md` to generate this table automatically."

Add "Available scripts" section after Common Mistakes, with `audit-page.py` highlighted as the entry point:

```markdown
## Available scripts

For a complete page audit, run `scripts/audit-page.py --url <URL>` — it runs all other scripts and aggregates results into the audit table from Section 10.

| Script | What it checks | Run it when |
...
```

- [ ] **Step 16: Commit**

```bash
git add skills/on-page-sgeo/
git commit -m "feat(on-page-sgeo): add references and scripts for tool-augmented workflow

Add 5 reference files covering meta optimization, heading structure, GEO formatting,
internal linking, and image optimization. Add 8 Python scripts including audit-page.py
orchestrator. Update SKILL.md with Tool Discovery section and script/reference pointers."
```

---

## Task 3: content-sgeo — References, Scripts, and SKILL.md Update

**Files:**
- Create: `skills/content-sgeo/references/keyword-research.md`
- Create: `skills/content-sgeo/references/topic-clusters.md`
- Create: `skills/content-sgeo/references/geo-content-framework.md`
- Create: `skills/content-sgeo/references/eeat-signals.md`
- Create: `skills/content-sgeo/references/content-refresh.md`
- Create: `skills/content-sgeo/scripts/research-keywords.py`
- Create: `skills/content-sgeo/scripts/classify-intent.py`
- Create: `skills/content-sgeo/scripts/analyze-serp-competitors.py`
- Create: `skills/content-sgeo/scripts/score-content-geo.py`
- Create: `skills/content-sgeo/scripts/check-eeat-signals.py`
- Create: `skills/content-sgeo/scripts/audit-content-freshness.py`
- Create: `skills/content-sgeo/scripts/plan-topic-cluster.py`
- Modify: `skills/content-sgeo/SKILL.md`

All paths relative to `/Users/raul/projects/ai-directory-company/apps/web/content/community/`.

### References

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p skills/content-sgeo/references skills/content-sgeo/scripts
```

- [ ] **Step 2: Write `references/keyword-research.md` (180-220 lines)**

Complete keyword research methodology. Must cover:
- Seed keyword generation: product/service terms, customer language vs internal jargon, competitor homepage/nav inspection
- Expansion techniques:
  - Google Autocomplete (type seed + each letter a-z)
  - "People Also Ask" extraction (search seed, expand PAA boxes)
  - Related searches (bottom of SERP)
  - Google Keyword Planner (designed for ads but useful for volume data)
  - AnswerThePublic (visualizes questions, prepositions, comparisons)
  - Search operators: `[topic] vs`, `[topic] alternative`, `best [topic]`, `how to [topic]`
- Tool-specific guidance:
  - Free: Google Keyword Planner (volume ranges, not exact), GSC query report (keywords you already rank for), Google Trends (seasonal patterns)
  - Paid: Ahrefs Keyword Explorer (exact volume, KD, clicks), Semrush Keyword Magic Tool, DataForSEO keyword data API
- Difficulty score interpretation: Ahrefs KD vs Semrush KD (different scales, don't compare across tools), free proxy (count of SERP results with DA >50)
- CPC as commercial intent proxy: high CPC = advertisers pay for this keyword = commercial value, low CPC ≠ low value (informational keywords drive awareness)
- Competitor gap analysis workflow: export your keywords, export competitor keywords, find keywords they rank for that you don't — these are immediate opportunities
- Quick win identification: GSC queries at positions 4-15 are your cheapest wins (already visible, small improvements push into top 3)
- Tone: "Start with your GSC query report. The keywords you already rank 10-20 for are your cheapest wins — don't go hunting before you harvest."

Source: `docs/seo-geo-marketing-guide.md` Section 4 Phase 2 Step 4 + Section 5 Tools.

- [ ] **Step 3: Write `references/topic-clusters.md` (150-180 lines)**

Cluster architecture deep dive. Must cover:
- What a topic cluster is: pillar page (comprehensive, 2000-4000 words) + 5-10 supporting articles (focused, 800-2000 words) + internal links connecting them
- Why clusters work: signal topical depth to search engines, create internal link equity flows, provide AI engines with a coherent knowledge graph on a topic
- Pillar vs supporting page sizing: pillar covers breadth (overview of entire topic), supports cover depth (one subtopic thoroughly)
- Internal link topology: every support → pillar, pillar → every support, support ↔ support where relevant
- Publishing sequence: pillar first (establishes the hub), then supports one at a time, then interlink pass after 3-4 supports are live
- When to merge vs keep separate: if two supporting articles have <500 words each and cover nearly identical subtopics, merge them into one stronger piece
- Cluster completion metrics: all planned supports published, all interlinks in place, pillar ranking for head term, supports ranking for long-tail variants
- 3 worked examples:
  - SaaS: "Invoice Automation" cluster (pillar + 7 supports as in SKILL.md Step 3)
  - E-commerce: "Running Shoes" cluster (buying guide pillar + supports for trail, road, beginner, injury prevention, brand comparisons)
  - Professional services: "Estate Planning" cluster (comprehensive guide pillar + supports for wills, trusts, power of attorney, tax implications, state-specific guides)
- Tone: "Build one cluster at a time. Depth beats breadth. One complete cluster of 8 interlinked articles outperforms 20 disconnected posts."

Source: `docs/seo-geo-marketing-guide.md` Section 2 Pillar 3 (Topic clusters) + Section 6.

- [ ] **Step 4: Write `references/geo-content-framework.md` (250-300 lines)**

The 8-element GEO content creation method expanded. This is the definitive reference for making content citation-worthy. Must cover each element with:

For each of the 8 elements (TLDR first, question headers, data-rich body, self-contained sections, expert quotations, source citations, original value, author attribution):
- Why it matters for AI citation (mechanism, not just assertion)
- Concrete before/after rewrite example (at least 1 per element, 2 for TLDR and self-contained sections)
- Common failure pattern
- Quick test: "How to tell if you've done this well"

Scoring rubric (used by `scripts/score-content-geo.py`):
- 8 elements × 0-5 points each = 0-40 total score
- Per-element criteria:
  - 0: Not present
  - 1: Present but weak (vague data, generic quotes, no sources)
  - 2-3: Adequate (some specifics, partial sourcing)
  - 4-5: Strong (specific sourced data, named experts, original insights)
- Score interpretation: 0-10 (not citable), 11-20 (partially citable, needs work), 21-30 (good, citation-ready for some queries), 31-40 (excellent, high citation potential)

Passage extraction simulation: "Read each H2 section as if you're an AI that needs to quote exactly 2-3 sentences from it. Can you? If not, the section needs restructuring."

Tone: "Original data is the only unfakeable GEO advantage. If you can run a survey, scrape a dataset, or benchmark something — do it. Everything else can be commoditized."

Source: `docs/seo-geo-marketing-guide.md` Section 3 (GEO techniques) + Section 6 (Content creation framework).

- [ ] **Step 5: Write `references/eeat-signals.md` (180-220 lines)**

E-E-A-T implementation guide. Must cover:
- What Google's quality raters actually look for (distilled from the Search Quality Evaluator Guidelines):
  - Experience: first-hand involvement, original photos/screenshots, specific results ("we tested on 3 sites and saw 40% improvement")
  - Expertise: depth of coverage, addressing edge cases and counterarguments, technical accuracy, credentials
  - Authoritativeness: citations from other sites, author reputation, site reputation in the topic area
  - Trustworthiness: source citing, transparency about limitations, contact information, editorial policies, secure site (HTTPS)
- December 2025 update impact: E-E-A-T evaluation now applies to ALL competitive queries, not just YMYL. Every topic where multiple sites compete for rankings gets E-E-A-T scrutiny.
- How AI engines assess author credibility: author entity recognition, cross-referencing author across publications, credential verification against visible signals
- Author page template:
  - Name, photo, job title, company
  - Bio (2-3 paragraphs of relevant expertise)
  - Links to social profiles (LinkedIn, Twitter, GitHub)
  - Links to other published work
  - Credentials/certifications relevant to topics covered
- Editorial policy template:
  - How content is researched
  - Fact-checking process
  - Update policy and cadence
  - Corrections policy
  - Author qualifications
- Per-article E-E-A-T implementation checklist (the one from SKILL.md Step 6, expanded):
  - Author byline with link to author page
  - Author page has bio, photo, credentials, social links
  - At least one first-hand experience or case study
  - All statistics cite primary sources with dates
  - Article acknowledges limitations
  - "Last updated" date is visible and accurate
  - Contact information accessible from the page
- Tone: "E-E-A-T is not a checklist you bolt on after writing. It's a content philosophy. If you don't have genuine expertise on a topic, find someone who does and put their name on it."

Source: `docs/seo-geo-marketing-guide.md` Section 2 Pillar 3 (E-E-A-T).

- [ ] **Step 6: Write `references/content-refresh.md` (120-150 lines)**

Content maintenance playbook. Must cover:
- Why content decays: statistics become outdated, competitors publish newer content, search intent shifts, freshness signals degrade
- 3-tier refresh model:
  - Optimizations (<15% changes): meta title/description tweaks, add internal links to newer content, improve CTAs, fix broken links. Do continuously.
  - Upgrades (15-70% changes): refresh statistics, add new sections, improve visuals, add expert quotes, update examples. Schedule every 3-6 months for important pages.
  - Rewrites (70%+ changes): complete overhaul when angle no longer works or topic has fundamentally changed. Treat as new content in production workflow.
- How to identify refresh candidates from GSC data:
  - Position decay: pages that dropped from positions 1-10 to 11-20 in last 3 months
  - CTR decay: pages with stable impressions but declining CTR (title/description fatigue)
  - Impression growth without clicks: topic gaining search volume but your page isn't compelling enough
  - High impressions, low position: pages at positions 4-15 (cheapest wins — small improvements push into top 3)
- Update workflow that preserves existing rankings:
  - Don't change the URL
  - Keep the core topic and primary keyword the same
  - Add to the content, don't remove sections that may be ranking for long-tail queries
  - Update dateModified in schema and visible date
  - Resubmit URL to GSC for re-crawling
- Freshness signals that matter vs cosmetic changes: search engines detect superficial updates (changing only the date). Substantive changes = new sections, updated data, fresh examples.
- Tone: "Updating the date without changing substance is worse than doing nothing — Google can detect it and it erodes trust."

Source: `docs/seo-geo-marketing-guide.md` Section 6 (Content refresh strategy).

### Scripts

Same conventions as Task 1 scripts.

- [ ] **Step 7: Write `scripts/research-keywords.py`**

Takes seed keywords (via `--seeds` comma-separated or stdin), expands using WebSearch:
- For each seed: search Google, extract "People Also Ask" questions from results, extract related searches, extract autocomplete suggestions (search `{seed} a`, `{seed} b`, ... `{seed} z` patterns)
- Deduplicate results
- For each expanded keyword: estimate search volume (if DataForSEO available, use keyword data API; otherwise mark as "estimated" based on SERP result counts)
- Classify intent per keyword using simple heuristics: "how to"/"what is"/"guide" = informational, "best"/"vs"/"review" = commercial, "buy"/"pricing"/"free trial" = transactional, brand terms = navigational
- Calculate a difficulty proxy: count high-authority domains (known high-DA sites) in top 10 results

Output JSON matching the keyword table from SKILL.md Step 1:
```json
{"keywords": [{"keyword": "...", "volume_estimate": "1200", "difficulty_proxy": "low", "cpc_estimate": null, "intent": "informational", "source": "people_also_ask", "priority": "high"}], "total_found": 47}
```

Free path: WebSearch. Paid extension: DataForSEO keyword data API for exact volume, difficulty, and CPC.

- [ ] **Step 8: Write `scripts/classify-intent.py`**

Takes a keyword list (via `--keywords` file or stdin, one per line):
- For each keyword: run a WebSearch query
- Analyze top 5 organic results: extract page type (blog post, product page, comparison, tool, docs) from URL patterns and title patterns
- Classify intent based on majority result type:
  - All guides/tutorials = informational
  - All product/pricing pages = transactional
  - Mix of comparison/review posts = commercial
  - Brand-specific results = navigational
- Assign confidence score (0.0-1.0) based on result type unanimity

Output JSON:
```json
{"classifications": [{"keyword": "...", "intent": "informational", "confidence": 0.9, "top_results": [{"url": "...", "type": "guide"}, ...], "recommended_content_type": "comprehensive guide"}]}
```

Free path: WebSearch. Paid extension: DataForSEO SERP API for richer SERP feature data.

- [ ] **Step 9: Write `scripts/analyze-serp-competitors.py`**

Takes a target keyword (via `--keyword`):
- WebSearch for the keyword, extract top 10 organic results
- For each result: fetch the page via WebFetch and extract:
  - Title tag and character count
  - Word count of main content
  - Heading structure (H1, H2 count, H3 count)
  - Structured data types present
  - Content format (guide, listicle, comparison, tool, FAQ, glossary)
  - Visible publish/update dates
- Aggregate: average word count, common schema types, dominant content format
- Identify gaps: what do top results have that user's content doesn't?

Output JSON:
```json
{"keyword": "...", "results": [{"position": 1, "url": "...", "title": "...", "word_count": 3200, "h2_count": 12, "schema_types": ["Article", "FAQPage"], "format": "comprehensive_guide", "last_updated": "2026-02-15"}], "averages": {"word_count": 2800, "h2_count": 10}, "dominant_format": "comprehensive_guide", "common_schemas": ["Article"], "gaps": [...]}
```

Free path: WebSearch + WebFetch. Paid extension: DataForSEO + Ahrefs for backlink counts per result.

- [ ] **Step 10: Write `scripts/score-content-geo.py`**

Takes a URL (via `--url`), scores against the 8-element GEO Content Creation Framework:

1. **TLDR first (0-5):** Extract first 200 words, check for direct answer vs meandering intro. Use heuristics: starts with definition/clear statement = higher score, starts with "In today's..." / "When it comes to..." = lower score, contains specific data in opening = bonus.

2. **Question-format headers (0-5):** Extract H2s, calculate % that are question-format. >50% = 4-5, 30-50% = 2-3, <30% = 0-1.

3. **Data density (0-5):** Count statistics/numbers per 500 words of content. >3 per 500 words = 4-5, 1-3 = 2-3, 0 = 0-1.

4. **Self-contained sections (0-5):** Check H2 sections for anaphoric references ("As mentioned above", "This approach", "See previous"). Fewer = higher score.

5. **Expert quotations (0-5):** Search for quotation patterns (blockquotes, "According to [Name]", attribution patterns). Present with named source = 4-5, present but vague = 2-3, absent = 0.

6. **Source citations (0-5):** Count outbound links to external sources (studies, official docs, data). >5 = 4-5, 3-5 = 2-3, 0-2 = 0-1.

7. **Original value (0-5):** Check for patterns indicating original data: "our data shows", "we tested", "we surveyed", proprietary framework mentions, case study indicators. Present = 3-5, absent = 0-2. (This is the hardest to automate — flag for human review if uncertain.)

8. **Author attribution (0-5):** Check for author byline, link to author page, credentials visible. All present = 4-5, partial = 2-3, absent = 0.

Output JSON:
```json
{"url": "...", "total_score": 28, "max_score": 40, "rating": "good", "breakdown": {"tldr_first": 4, "question_headers": 3, "data_density": 4, "self_contained": 3, "expert_quotations": 5, "source_citations": 4, "original_value": 3, "author_attribution": 2}, "recommendations": ["Add dateModified to Article schema", "First section lacks specific data — add a statistic"], "interpretation": "Citation-ready for most queries. Improve author attribution for higher scores."}
```

Free path: WebFetch + parsing. No paid extension needed.

- [ ] **Step 11: Write `scripts/check-eeat-signals.py`**

Takes a URL (via `--url`), checks E-E-A-T signal presence:
- Author byline: search for "by [Name]", `rel="author"`, schema Person, `.author` class elements
- Author page link: if author found, check if name links to another page on the same domain
- Author page quality: if author page found, fetch it and check for bio text (>50 words), photo (`<img>` near author name), credentials, social links (LinkedIn, Twitter, GitHub URLs)
- External citations: count outbound links to external domains (exclude navigation, social, tracking links)
- Visible dates: search for date patterns as in `check-freshness.py`
- Editorial policy: check for links to /editorial-policy, /about/editorial, etc.
- Contact information: check for /contact page link or visible email/phone

Output JSON with per-signal pass/fail:
```json
{"url": "...", "signals": {"author_byline": {"present": true, "name": "Jane Smith"}, "author_page": {"present": true, "url": "/team/jane-smith", "has_bio": true, "has_photo": true, "has_credentials": true, "has_social_links": true}, "external_citations": {"count": 7, "domains": ["arxiv.org", "semrush.com", ...]}, "visible_dates": {"published": "2025-06-15", "modified": "2026-03-20"}, "editorial_policy": {"found": false}, "contact_page": {"found": true}}, "eeat_score": "strong", "missing": ["editorial_policy"]}
```

- [ ] **Step 12: Write `scripts/audit-content-freshness.py`**

Takes a sitemap URL or list of URLs (via `--sitemap` or `--urls` file):
- For each URL: extract dateModified from JSON-LD schema, visible "last updated" text, and lastmod from sitemap
- Calculate days since last update
- Flag pages by freshness tier: <6 months (fresh), 6-12 months (aging), 12-18 months (stale), >18 months (needs rewrite)
- If WebSearch available: spot-check ranking positions for a sample of URLs (search `site:domain.com/path`) to identify position 4-15 refresh candidates
- Prioritize: position 4-15 pages first, then declining traffic pages, then stale pages

Output JSON matching the refresh tracking template from SKILL.md Step 7:
```json
{"pages": [{"url": "...", "last_updated": "2025-08-14", "days_ago": 225, "freshness": "aging", "estimated_position": 6, "refresh_priority": "high", "recommended_action": "upgrade"}], "summary": {"total": 50, "fresh": 20, "aging": 15, "stale": 10, "needs_rewrite": 5}}
```

Free path: WebFetch + WebSearch. Paid extension: DataForSEO for bulk ranking position data.

- [ ] **Step 13: Write `scripts/plan-topic-cluster.py`**

Takes a pillar topic (via `--topic`):
- WebSearch for the topic, extract:
  - "People Also Ask" questions (these become supporting article ideas)
  - Related searches (more supporting article ideas)
  - Top 10 organic results (analyze their heading structures for subtopic discovery)
- For each top result: fetch and extract H2 headings to discover subtopics
- Deduplicate and group subtopics into potential supporting articles (5-10)
- Generate cluster structure:
  - Pillar page title suggestion
  - Supporting article titles with target keywords
  - Internal link map (which supports link to which)
- If DataForSEO available: get volume estimates per subtopic keyword

Output JSON matching the cluster diagram from SKILL.md Step 3:
```json
{"pillar": {"title": "Complete Guide to [Topic]", "target_keyword": "[topic]", "estimated_volume": "high"}, "supports": [{"title": "How to [Subtopic]", "target_keyword": "...", "intent": "informational", "source": "people_also_ask"}, ...], "link_map": {"pillar_to_supports": true, "supports_to_pillar": true, "support_to_support": [["support_1", "support_3"], ["support_2", "support_5"]]}}
```

Free path: WebSearch + WebFetch. Paid extension: DataForSEO for volume per subtopic.

### SKILL.md Update

- [ ] **Step 14: Update `skills/content-sgeo/SKILL.md`**

Insert Tool Discovery section after frontmatter. Add script and reference pointers per step:

- Step 1 (Keyword Research): → "Run `scripts/research-keywords.py --seeds 'term1,term2,term3'`. See `references/keyword-research.md` for methodology details."
- Step 2 (Search Intent Classification): → "Run `scripts/classify-intent.py` with your keyword list."
- Step 3 (Topic Cluster Architecture): → "Run `scripts/plan-topic-cluster.py --topic 'your pillar topic'`. See `references/topic-clusters.md` for worked examples."
- Step 4 (GEO Content Creation Framework): → "Run `scripts/score-content-geo.py --url <URL>` to score existing content. See `references/geo-content-framework.md` for the full scoring rubric and before/after examples."
- Step 5 (Content Types): No script or reference needed (table is self-contained in SKILL.md).
- Step 6 (E-E-A-T Integration): → "Run `scripts/check-eeat-signals.py --url <URL>`. See `references/eeat-signals.md` for the full implementation guide and templates."
- Step 7 (Content Refresh Strategy): → "Run `scripts/audit-content-freshness.py --sitemap <URL>`. See `references/content-refresh.md` for refresh prioritization framework."
- Step 8 (Content Calendar): No script needed (template is in SKILL.md).

Add "Available scripts" section. Highlight `score-content-geo.py` as the key feedback loop:

```markdown
## Available scripts

The key feedback loop: run `scripts/score-content-geo.py` on existing content to get a GEO score (0-40), then optimize based on the element-by-element breakdown. Run it again after changes to measure improvement.

| Script | What it does | Run it when |
...
```

- [ ] **Step 15: Commit**

```bash
git add skills/content-sgeo/
git commit -m "feat(content-sgeo): add references and scripts for tool-augmented workflow

Add 5 reference files covering keyword research, topic clusters, GEO content framework,
E-E-A-T signals, and content refresh strategy. Add 7 Python scripts including
score-content-geo.py (0-40 GEO scoring) and plan-topic-cluster.py (generative cluster
planning). Update SKILL.md with Tool Discovery section and script/reference pointers."
```

---

## Task 4: off-page-sgeo — References, Scripts, and SKILL.md Update

**Files:**
- Create: `skills/off-page-sgeo/references/backlink-strategy.md`
- Create: `skills/off-page-sgeo/references/brand-mentions.md`
- Create: `skills/off-page-sgeo/references/ai-citation-platforms.md`
- Create: `skills/off-page-sgeo/references/digital-pr.md`
- Create: `skills/off-page-sgeo/references/ai-visibility-measurement.md`
- Create: `skills/off-page-sgeo/scripts/check-backlink-profile.py`
- Create: `skills/off-page-sgeo/scripts/monitor-brand-mentions.py`
- Create: `skills/off-page-sgeo/scripts/audit-platform-presence.py`
- Create: `skills/off-page-sgeo/scripts/probe-ai-visibility.py`
- Create: `skills/off-page-sgeo/scripts/analyze-competitor-authority.py`
- Create: `skills/off-page-sgeo/scripts/find-link-opportunities.py`
- Create: `skills/off-page-sgeo/scripts/track-ai-referrers.py`
- Modify: `skills/off-page-sgeo/SKILL.md`

All paths relative to `/Users/raul/projects/ai-directory-company/apps/web/content/community/`.

### References

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p skills/off-page-sgeo/references skills/off-page-sgeo/scripts
```

- [ ] **Step 2: Write `references/backlink-strategy.md` (200-250 lines)**

Link acquisition playbook. Must cover:
- The 5 linkable asset types with effort/reward matrix:
  - Original research: High effort, very high reward. Takes weeks. Best ROI long-term.
  - Free tools: High effort, high reward. Requires development resources. Passive links forever.
  - Comprehensive guides: Medium effort, high reward. Writing-intensive. Needs regular updates.
  - Data visualizations: Medium effort, medium reward. Embeddable = viral potential.
  - Frameworks/templates: Low-medium effort, medium reward. Quick to create, easy to share.
- Outreach email templates (3 templates):
  - Initial pitch (guest post): Subject line with angle, personalized opening referencing their content, what you offer, credentials, soft ask
  - Broken link replacement: Identify the broken link, explain you noticed it, offer your content as replacement, brief description of why it fits
  - Follow-up (5 business days later): Brief, not pushy, offer additional value
- Response rate benchmarks: guest post outreach 5-8%, resource page outreach 8-12%, broken link building 10-15%, HARO/Connectively 15-25% (if responded within 2 hours with data)
- Anchor text distribution guidelines for a natural link profile:
  - Branded anchors (your company/product name): 40-50%
  - Natural/descriptive (topic-relevant phrases): 30-40%
  - Exact match keyword: <10% (higher triggers spam signals)
  - Generic ("click here"): <5%
  - URL as anchor: 5-10%
- Toxic link identification: signs of a link you should disavow (PBN patterns, irrelevant foreign-language sites, link farms, sites with >80% outbound links, sites penalized by Google)
- Tone: "If you're sending more than 30 outreach emails a day, you're spamming. Quality outreach is 5-10 highly personalized pitches per day."

Source: `docs/seo-geo-marketing-guide.md` Section 2 Pillar 4 + Section 4 Phase 4 Step 9.

- [ ] **Step 3: Write `references/brand-mentions.md` (130-160 lines)**

Brand monitoring and mention conversion. Must cover:
- Monitoring setup:
  - Google Alerts: exact brand name in quotes, product names, founder/CEO names, set to "All results" not just "Best results"
  - Ahrefs Alerts (paid): web mentions, backlink alerts (new and lost)
  - Social listening: Mention.com (paid), Brand24 (paid), or free alternatives (Twitter search, Reddit search, Google search with `"brand name" -site:yourdomain.com`)
  - Frequency: weekly review minimum, daily for high-velocity brands
- Mention-to-link conversion workflow:
  1. Export unlinked mentions (search: `"brand name" -site:yourdomain.com -link:yourdomain.com`)
  2. Prioritize by site authority (target DA/DR >40 first)
  3. Find author contact (check article byline → LinkedIn/Twitter, or site contact page)
  4. Send brief, friendly request (template provided)
  5. Conversion rate: 5-15% of attempts result in added links
  - Email template: "Hi [Name], thanks for mentioning [Brand] in [Article Title]. Would you mind linking to [specific URL] so readers can find us easily? Happy to reciprocate — our audience would love your [piece they'd benefit from]."
- Building mentionable authority:
  - Publish quotable statistics with branded attribution ("According to [Brand]'s 2025 report...")
  - Create named methodologies/frameworks/scores ("[Brand] Readiness Score", "[Brand] Framework")
  - Participate in industry surveys where your brand appears alongside competitors
  - Contribute expert commentary with named attribution
- How AI engines process brand entity signals: entity recognition across diverse sources, mention frequency as authority signal, co-occurrence with topic entities (your brand + "invoice automation" appearing together across many sources)
- Tone: "Create a named methodology. '[Brand] Score' or '[Brand] Framework' gets cited by name. Generic advice gets attributed to nobody."

Source: `docs/seo-geo-marketing-guide.md` Section 2 Pillar 4 (Brand mentions).

- [ ] **Step 4: Write `references/ai-citation-platforms.md` (300-350 lines)**

Platform-by-platform guide for the 7 AI-cited sources. This is the longest reference because each platform needs specific tactical guidance. Must cover each platform with: why AI cites it, how to build presence, do's, don'ts, and example high-citation content patterns.

**Reddit (60-70 lines):**
- Why AI cites it: AI engines treat Reddit threads as authentic opinions. Perplexity and ChatGPT both heavily index Reddit.
- Subreddit selection: find 3-5 where your audience asks questions. Use Reddit search, check subscriber count, post frequency, moderator rules.
- Building presence: answer questions thoroughly (200+ word answers with specific details), build karma over 2-4 weeks before any brand mentions, use your real identity or a clearly professional username
- Do's: be genuinely helpful, share expertise, provide specific numbers and experiences, link to relevant resources (including yours) only when directly answering a question
- Don'ts: never create promotional posts, never use multiple accounts, never have employees brigade threads, never post "I'm the founder of X and..."
- High-citation patterns: detailed experience reports, specific comparisons between tools, data-backed recommendations

**YouTube (40-50 lines):**
- Why: transcripts indexed by AI, video answers increasingly cited
- Content: tutorial/explainer videos with clear keyword-rich spoken content
- Optimization: detailed descriptions (500+ words, AI reads these), chapters with descriptive titles, keyword-rich spoken content (not just text overlays)
- Transcript quality: speak clearly, use topic terminology, AI extracts from auto-transcripts

**LinkedIn (40-50 lines):**
- Why: professional content cited for business/industry topics
- Articles vs posts: articles have permanent URLs (citable), posts are ephemeral
- Strategy: publish long-form articles with original data/analysis, comment substantively on industry discussions, build connections with industry voices

**Wikipedia (40-50 lines):**
- Why: extremely high authority for AI citation
- Rules: NEVER edit your own brand's article (COI violation, reverted), contribute genuine expertise to RELATED topic articles, ensure brand is cited in reliable secondary sources first (Wikipedia requires these)
- Strategy: build notability through media coverage and publications, then let Wikipedia editors create/update naturally

**GitHub (30-40 lines):**
- Why: critical for developer-focused products, READMEs directly cited
- Strategy: comprehensive READMEs (explain concepts, not just installation), quality documentation, participation in relevant open-source projects
- AI citation patterns: well-structured README sections get cited as definitions and how-to answers

**Stack Overflow / Industry Forums (30-40 lines):**
- Why: expert answers cited for technical questions
- Strategy: thorough, well-structured answers with code examples and explanations of WHY not just HOW, build reputation through consistent quality

**Industry Publications (30-40 lines):**
- Why: extends citation surface area, builds authority backlinks simultaneously
- Strategy: target publications ranking for your audience's queries, prioritize evergreen over news, include data and frameworks in guest articles

Source: `docs/seo-geo-marketing-guide.md` Section 4 Phase 4 Step 9 (platforms AI cite).

- [ ] **Step 5: Write `references/digital-pr.md` (150-180 lines)**

PR for authority building. Must cover:
- Journalist identification workflow:
  - Find reporters covering your niche (use Muck Rack, or manually: search "[topic] reporter" on Twitter/X, check bylines on relevant publications)
  - Build a list of 20-30 relevant journalists with their beat, publication, and contact
  - Follow and engage with their work before pitching (comment on articles, share their work, quote them)
- Pitch construction (the data-lead format):
  - Subject line: lead with the most surprising statistic or angle + publication name
  - Opening: one sentence connecting to something they specifically cover (reference a recent article)
  - Body: two sentences with the data/story, leading with a specific number
  - Credibility: one sentence on why you're qualified (role, years, dataset size)
  - Ask: offer to share full report/data. Don't attach unsolicited files.
- 3 pitch examples:
  - Data study pitch: "62% of SaaS companies block AI crawlers accidentally — [Publication]"
  - Expert commentary pitch: "Source: AI search impact on B2B buying — [Publication]"
  - Trend analysis pitch: "AI-referred traffic up 527% YoY — how brands are adapting — [Publication]"
- Timing and follow-up: Tuesday-Thursday mornings for cold pitches, follow up once after 3-5 business days, never follow up more than twice
- Response rate expectations: cold pitch 5-10%, warm contact 15-25%, HARO/Connectively 15-25% if responded within 2 hours
- Podcast guesting:
  - Find relevant shows: search "[niche] podcast" on Apple Podcasts/Spotify, check episode topics and guest quality
  - Pitch template: brief bio, 3 topic suggestions with why their audience would care, link to past appearances if any
  - Show notes optimization: ensure host links to your site, provide keyword-rich bio and topic description
- Award/list submissions: "Best of" lists, "Top 50" roundups, industry awards — each generates high-authority mentions and links
- Conference speaking: speaker pages link to your site, recorded talks become searchable content, slides get shared
- Tone: "If your pitch doesn't have a number in the subject line, it's going to the bottom of the inbox."

Source: `docs/seo-geo-marketing-guide.md` Section 4 Phase 4 Step 10.

- [ ] **Step 6: Write `references/ai-visibility-measurement.md` (180-220 lines)**

Complete measurement framework. Must cover:
- Manual testing protocol:
  - Query design: compile 10-20 queries your target audience would ask AI (mix of informational, commercial, and brand-adjacent)
  - Platform coverage: test on ChatGPT, Perplexity, Claude, Gemini (minimum 3 platforms)
  - Recording methodology: for each query × platform, record: brand cited (Y/N), competitors cited (list), source URL if available, citation context (direct quote vs mention)
  - Cadence: monthly minimum, weekly for high-priority tracking
  - Trend tracking: maintain a spreadsheet over time to identify patterns
- Tool comparison (honest, opinionated):
  - Cairrot (~$40/mo): Best value for small-to-mid sites. Tracks ChatGPT, Perplexity, Claude, Gemini. WordPress plugin for AI bot log tracking. Includes llms.txt generator. Limitation: citation data can lag 1-2 weeks.
  - AIclicks (~$39/mo): Good for prompt-level tracking and content recommendations. AI visibility score is useful for benchmarking. Limitation: fewer platforms than Cairrot.
  - Peec AI (varies): Competitive benchmarking focus. Good if you need to compare against specific competitors. Limitation: pricing is opaque.
  - Semrush AI add-on (included in Semrush): Fine if you already pay for Semrush. Don't buy Semrush just for AI tracking. Prompt research is useful but limited.
  - Profound (enterprise): Deep citation analytics for large brands. Share-of-voice tracking. Overkill for most sites.
- GA4 AI referrer setup (step-by-step):
  1. Go to Admin → Data Streams → Web → Configure tag settings → Define internal traffic (exclude AI referrers from bot filtering)
  2. Go to Admin → Custom Definitions → Custom Channel Groups
  3. Create "AI Assistants" channel group with referrer conditions: contains "chat.openai.com" OR "perplexity.ai" OR "gemini.google.com" OR "claude.ai" OR "copilot.microsoft.com"
  4. These appear in Acquisition → Traffic Acquisition report
  - Context: AI-referred sessions grew 527% YoY in early 2025. Track now even if volumes are small.
- Server log analysis for AI bot activity: grep patterns for GPTBot, ClaudeBot, PerplexityBot user-agents. Frequency: are they visiting weekly, daily, rarely? Which pages? Are they getting 200s?
- Share of Model metric: your brand's % of AI answers in your category. Calculate by running category queries and counting how often you appear vs competitors.
- Benchmarking against competitors: run the same queries for your brand and 3-5 competitors, compare citation rates
- Tone: "Cairrot is the best value right now for small-to-mid sites. Semrush's add-on is fine if you already pay for Semrush but don't buy Semrush just for AI tracking."

Source: `docs/seo-geo-marketing-guide.md` Section 5 (GEO tools) + Section 8 (Measuring success).

### Scripts

Same conventions as Task 1 scripts.

- [ ] **Step 7: Write `scripts/check-backlink-profile.py`**

Takes a domain (via `--domain`):
- Free path: WebSearch for `"domain.com" -site:domain.com` to find pages mentioning/linking to the domain. Extract unique referring domains from results. Count total mentions found. Identify top sources by apparent authority (known high-DA domains).
- Paid path (DataForSEO): call backlink API for full profile — total backlinks, referring domains, anchor text distribution, dofollow/nofollow ratio, top linking pages.
- Paid path (Ahrefs): call backlinks endpoint for comprehensive data.

Output JSON:
```json
{"domain": "...", "method": "websearch|dataforseo|ahrefs", "referring_domains_estimate": 145, "top_sources": [{"domain": "techcrunch.com", "context": "mentioned in article about..."}, ...], "anchor_text_sample": [...], "issues": [], "recommendation": "..."}
```

- [ ] **Step 8: Write `scripts/monitor-brand-mentions.py`**

Takes brand name (via `--brand`) and optional product names (via `--products`):
- WebSearch across multiple queries:
  - `"brand name" -site:yourdomain.com` (web mentions)
  - `site:reddit.com "brand name"` (Reddit mentions)
  - `site:news.ycombinator.com "brand name"` (HN mentions)
  - `site:linkedin.com "brand name"` (LinkedIn mentions)
- For each result: extract URL, title, snippet, classify as linked (contains href to your domain) or unlinked
- Classify sentiment: positive (contains "recommend", "great", "love"), negative ("avoid", "disappointed", "issue"), neutral
- Prioritize unlinked mentions on high-authority sites as link conversion candidates

Output JSON:
```json
{"brand": "...", "total_mentions": 34, "linked": 12, "unlinked": 22, "sentiment": {"positive": 18, "neutral": 12, "negative": 4}, "conversion_candidates": [{"url": "...", "domain": "...", "estimated_authority": "high", "context": "..."}], "platforms": {"reddit": 8, "web": 20, "linkedin": 4, "hn": 2}}
```

- [ ] **Step 9: Write `scripts/audit-platform-presence.py`**

Takes brand name (via `--brand`):
- For each of the 7 AI-cited platforms, search for brand presence:
  - Reddit: `site:reddit.com "[brand]"` — count results, check if official account exists
  - YouTube: `site:youtube.com "[brand]"` — check for official channel, video count
  - LinkedIn: `site:linkedin.com/company "[brand]"` — check for company page
  - Wikipedia: `site:wikipedia.org "[brand]"` — check for article
  - GitHub: `site:github.com "[brand]"` — check for organization
  - Stack Overflow: `site:stackoverflow.com "[brand]"` — count mentions/answers
  - Industry forums: configurable via `--forums` flag

Output JSON matching the platform audit template:
```json
{"brand": "...", "platforms": [{"name": "Reddit", "presence": true, "estimated_activity": "active", "mention_count": 45, "ai_citation_potential": "high", "priority": "maintain"}, ...], "missing_platforms": ["Wikipedia", "YouTube"], "recommendation": "Create YouTube channel and build Reddit presence — these are the top AI citation sources you're missing."}
```

- [ ] **Step 10: Write `scripts/probe-ai-visibility.py`**

Takes a list of queries (via `--queries` file, one per line) and brand name (via `--brand`):
- For each query: attempt to get AI-generated answers:
  - Perplexity: WebFetch `https://www.perplexity.ai/search?q={query}` (extract citations from HTML if accessible)
  - General web search: WebSearch `{query} AI answer` or `{query} site:perplexity.ai` to find cached AI answers
  - Check if brand name appears in results
- Record: query, platform checked, brand cited (Y/N), competitors cited (names), source URLs

Output JSON matching the AI visibility tracking template:
```json
{"brand": "...", "queries_tested": 15, "citations_found": 4, "citation_rate": 0.27, "results": [{"query": "...", "platforms_checked": ["perplexity"], "brand_cited": false, "competitors_cited": ["competitor1", "competitor2"], "cited_sources": ["reddit.com", "competitor1.com"]}], "competitor_citation_rates": {"competitor1": 0.60, "competitor2": 0.40}, "recommendation": "..."}
```

Free path: WebFetch + WebSearch. Paid extension: DataForSEO AI visibility endpoints, ChatGPT scraper API.

- [ ] **Step 11: Write `scripts/analyze-competitor-authority.py`**

Takes user domain (via `--domain`) and competitor domains (via `--competitors` comma-separated):
- For each domain (including user's): estimate via WebSearch:
  - Backlink profile: `"domain.com" -site:domain.com` result count as proxy
  - Brand mentions: `"brand name"` result count
  - Content volume: `site:domain.com` result count
  - Platform presence: quick check across Reddit, YouTube, LinkedIn (reuse audit-platform-presence logic)
- Build competitive matrix comparing all domains

Output JSON:
```json
{"user_domain": "...", "competitors": [{"domain": "...", "backlink_estimate": 450, "mention_estimate": 1200, "content_volume": 230, "platform_score": 5}], "user_metrics": {...}, "gaps": ["competitor1 has 3x more backlinks", "competitor2 has active YouTube channel"], "strengths": ["user has more content volume than competitor3"]}
```

- [ ] **Step 12: Write `scripts/find-link-opportunities.py`**

Takes a topic/niche (via `--topic`) and optionally user domain (via `--domain`):
- Search for link opportunities using WebSearch:
  - Resource pages: `intitle:"resources" [topic]`, `intitle:"useful links" [topic]`
  - Guest post targets: `[topic] "write for us"`, `[topic] "guest post"`, `[topic] "contribute"`
  - Broken link candidates: `[topic] + common 404 indicators` (this is approximate without Ahrefs — flag as "verify manually")
  - HARO/Connectively: `site:connectively.us [topic]` for current journalist queries
  - Roundup/list posts: `[topic] "best tools"`, `[topic] "top resources"`, `[topic] roundup`
- For each opportunity: extract URL, title, type (resource page/guest post/roundup), estimated authority (based on domain recognition)

Output JSON:
```json
{"topic": "...", "opportunities": [{"type": "resource_page", "url": "...", "title": "...", "estimated_authority": "medium", "action": "Pitch your [asset] for inclusion"}, ...], "total_found": 23, "by_type": {"resource_pages": 8, "guest_post_targets": 6, "roundups": 5, "journalist_queries": 4}}
```

Free path: WebSearch. Paid extension: Ahrefs for broken link discovery and DR/DA scores, DataForSEO for bulk authority metrics.

- [ ] **Step 13: Write `scripts/track-ai-referrers.py`**

This is an instructional/config-generation script, not a data-fetching script:
- Generates GA4 custom channel group configuration for AI referrers
- Outputs the exact referrer conditions to set up:
  - chat.openai.com
  - perplexity.ai
  - gemini.google.com
  - claude.ai
  - copilot.microsoft.com
- Generates a step-by-step setup guide the user can follow in GA4
- If GSC API credentials available: query for referrer data showing AI traffic

Output JSON:
```json
{"ga4_config": {"channel_group_name": "AI Assistants", "conditions": [{"type": "referrer_contains", "value": "chat.openai.com"}, ...], "setup_steps": ["1. Go to GA4 Admin → Custom Definitions → Custom Channel Groups", "2. Click 'Create custom channel group'", ...]}, "known_ai_referrers": ["chat.openai.com", "perplexity.ai", "gemini.google.com", "claude.ai", "copilot.microsoft.com"], "note": "AI-referred sessions grew 527% YoY in early 2025. Track now even if volumes are small."}
```

### SKILL.md Update

- [ ] **Step 14: Update `skills/off-page-sgeo/SKILL.md`**

Insert Tool Discovery section after frontmatter. Add script and reference pointers per step:

- Step 1 (Backlink Strategy): → "Run `scripts/check-backlink-profile.py --domain yourdomain.com` for baseline. Run `scripts/find-link-opportunities.py --topic 'your niche'` for prospects. See `references/backlink-strategy.md` for outreach templates and anchor text guidelines."
- Step 2 (Brand Mention Development): → "Run `scripts/monitor-brand-mentions.py --brand 'Your Brand'`. See `references/brand-mentions.md` for monitoring setup and mention-to-link conversion workflow."
- Step 3 (Multi-Platform Presence): → "Run `scripts/audit-platform-presence.py --brand 'Your Brand'`. See `references/ai-citation-platforms.md` for platform-by-platform tactical guides."
- Step 4 (Digital PR): → "See `references/digital-pr.md` for pitch templates and journalist identification workflow."
- Step 5 (Community Engagement): → "See `references/ai-citation-platforms.md` (Reddit and forum sections) for community-specific tactics."
- Step 6 (AI Visibility Measurement): → "Run `scripts/probe-ai-visibility.py` for baseline measurement. Run `scripts/analyze-competitor-authority.py` for competitive comparison. Run `scripts/track-ai-referrers.py` for GA4 setup instructions. See `references/ai-visibility-measurement.md` for the complete measurement framework."
- Step 7 (Measurement Cadence): No script needed (schedule is in SKILL.md).

Add "Available scripts" section. Highlight `probe-ai-visibility.py` as the key measurement script:

```markdown
## Available scripts

Start with `scripts/probe-ai-visibility.py` to establish your AI citation baseline, then measure monthly to track the impact of your authority-building efforts.

| Script | What it does | Run it when |
...
```

- [ ] **Step 15: Commit**

```bash
git add skills/off-page-sgeo/
git commit -m "feat(off-page-sgeo): add references and scripts for tool-augmented workflow

Add 5 reference files covering backlink strategy, brand mentions, AI citation platforms,
digital PR, and AI visibility measurement. Add 7 Python scripts for backlink analysis,
brand monitoring, platform presence audit, AI visibility probing, competitor analysis,
link opportunity finding, and AI referrer tracking. Update SKILL.md with Tool Discovery
section and script/reference pointers."
```

---

## Task 5: Cross-Skill Validation

**Depends on:** Tasks 1-4 all complete.

- [ ] **Step 1: Verify all files exist**

```bash
# Count files per skill
echo "=== technical-sgeo ===" && find skills/technical-sgeo -type f | wc -l  # Expected: 16 (1 SKILL.md + 5 references + 10 scripts)
echo "=== on-page-sgeo ===" && find skills/on-page-sgeo -type f | wc -l     # Expected: 14 (1 SKILL.md + 5 references + 8 scripts)
echo "=== content-sgeo ===" && find skills/content-sgeo -type f | wc -l     # Expected: 13 (1 SKILL.md + 5 references + 7 scripts)
echo "=== off-page-sgeo ===" && find skills/off-page-sgeo -type f | wc -l   # Expected: 13 (1 SKILL.md + 5 references + 7 scripts)
```

- [ ] **Step 2: Verify SKILL.md frontmatter cross-references**

Check that `worksWellWithSkills` in each SKILL.md still lists the other 3 SGEO skills and existing skills (technical-seo-audit, performance-audit, content-calendar, go-to-market-plan). Check that `worksWellWithAgents` lists valid agent slugs.

- [ ] **Step 3: Verify Tool Discovery section is present in all 4 SKILL.md files**

```bash
grep -l "## Tool discovery" skills/*/SKILL.md
# Expected: 4 results
```

- [ ] **Step 4: Verify all Python scripts are executable and have shebangs**

```bash
head -1 skills/*/scripts/*.py | grep -c "#!/usr/bin/env python3"
# Expected: 32
```

- [ ] **Step 5: Verify all scripts have --help documentation**

```bash
grep -l "argparse" skills/*/scripts/*.py | wc -l
# Expected: 32
```

- [ ] **Step 6: Commit validation results**

If any issues found in Steps 1-5, fix them. Then:

```bash
git add -A skills/
git commit -m "chore: validate SGEO skill enrichment — all 56 files verified"
```
