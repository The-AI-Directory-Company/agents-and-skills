# SGEO Skills Enrichment: References & Scripts Design

**Date:** 2026-03-27
**Status:** Draft
**Scope:** Enrich 4 existing SGEO skills with `references/` and `scripts/` directories

---

## Context

Four SGEO (Search Generative Engine Optimization) skills exist in `skills/`:
- `technical-sgeo` — Making a site crawlable for search engines and AI
- `on-page-sgeo` — Making each page relevant for ranking and citation
- `content-sgeo` — Creating pages worth ranking and quoting
- `off-page-sgeo` — Building authority across search and AI ecosystems

Each currently has only a `SKILL.md`. This design adds `references/` (topic-specific deep-dive markdown files) and `scripts/` (executable Python scripts for automatable checks) to each skill, turning them from procedural guides into tool-augmented workflows.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| SEO/GEO framing | Equal weight, unified | Every check, script, and reference covers both dimensions simultaneously. No hierarchy. |
| Tone | Practitioner — direct, opinionated | Recommends specific tools, calls out what's overrated. Matches the source guide's style. |
| Tool availability | Upfront inventory per skill | Agent asks the user once what tools are available. Scripts branch based on the inventory. |
| Script scope | Comprehensive toolkit | 32 scripts total across 4 skills covering all automatable checks. |
| Reference organization | By topic area | Each file covers one domain topic with all tool methods relevant to that topic. |
| Architecture | Self-contained per skill | Each skill folder has its own scripts and references. No cross-skill dependencies. Matches the repo's Agent Skills spec convention. |
| Script language | Python | Portable, readable, rich HTTP/parsing libraries. Agents can run via Bash tool. |
| Free/paid model | Free baseline + optional paid extensions | Every script works with WebFetch/WebSearch/public APIs. Paid tools (DataForSEO, Ahrefs, Semrush) enhance output when available. |

## Shared Pattern: Tool Discovery Section

Every SKILL.md gets a new section inserted before "Before you start":

```markdown
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
```

## Skill 1: technical-sgeo

### Scripts (10)

| Script | Purpose | Free Path | Paid Extension |
|--------|---------|-----------|----------------|
| `inventory-tools.py` | Probe which tools/MCPs/APIs are reachable. Output JSON inventory for other scripts. | Always runs | — |
| `check-robots-txt.py` | Fetch robots.txt, parse rules for Googlebot, Bingbot, GPTBot, ClaudeBot, PerplexityBot, Google-Extended. Report blocks, allows, missing entries. | WebFetch | — |
| `validate-sitemap.py` | Fetch XML sitemap/index, validate structure, check URL count, verify lastmod dates, sample 10 URLs for 200 status. | WebFetch | DataForSEO on-page API for bulk URL status |
| `check-cwv.py` | Call PageSpeed Insights API, return LCP/INP/CLS with field vs lab data, identify LCP element and CLS sources. | PSI API (free) | Chrome DevTools MCP for live tracing |
| `check-structured-data.py` | Extract JSON-LD blocks from a page, validate against schema.org types, flag mismatches. | WebFetch + parsing | DataForSEO on-page analysis |
| `check-https-security.py` | Verify HTTPS, check HTTP redirect chain, validate HSTS header, flag mixed content. | WebFetch | — |
| `check-ai-crawler-access.py` | Fetch page with AI bot user-agent strings, compare response codes/content against standard browser fetch. Detect CDN/WAF blocking. | WebFetch with custom headers | Playwright MCP for rendering comparison |
| `check-mobile.py` | Fetch at mobile viewport, check viewport meta tag, extract tap target sizes, verify content parity. | WebFetch + Playwright MCP | Chrome DevTools MCP |
| `check-indexation.py` | Use `site:domain.com` via WebSearch to estimate indexed pages, compare against sitemap count. | WebSearch | DataForSEO SERP API |
| `check-redirect-chains.py` | Follow redirect chains for URL list, report chain length, final destination, status codes per hop. | WebFetch | DataForSEO for bulk checking |

### References (5)

| File | Content | ~Lines |
|------|---------|--------|
| `crawlability.md` | Crawl mechanics for search + AI bots, robots.txt directive syntax, sitemap protocol, CDN bot-management gotchas (Cloudflare Bot Fight Mode, AWS WAF). | 150-200 |
| `core-web-vitals.md` | LCP/INP/CLS root causes, fix patterns by framework (Next.js, WordPress, Shopify), field vs lab data interpretation. | 150-200 |
| `structured-data.md` | Schema.org JSON-LD templates per page type, nesting patterns, validation workflow, FAQ Schema as GEO accelerator. | 200-250 |
| `ai-crawler-access.md` | AI crawler user-agent strings, CDN config per provider, server log queries, llms.txt spec and research findings. | 150-200 |
| `measurement-setup.md` | GSC/GA4/Bing Webmaster Tools setup, AI referrer tracking in GA4, server log monitoring. | 100-150 |

### SKILL.md Updates
- Insert Tool Discovery section before "Before you start"
- Add script pointers in each implementation section
- Add reference pointers for deep context
- Add "Scripts" section after quality checklist documenting each script

---

## Skill 2: on-page-sgeo

### Scripts (8)

| Script | Purpose | Free Path | Paid Extension |
|--------|---------|-----------|----------------|
| `extract-meta-tags.py` | Extract title, meta description, OG tags, canonical, robots meta. Validate lengths, flag keyword stuffing. | WebFetch | — |
| `analyze-headings.py` | Extract heading hierarchy, validate structure, identify question-format H2s, score GEO heading quality. | WebFetch | — |
| `check-direct-answer.py` | Extract first 200 words after H1, analyze for direct answer vs meandering intro, check for anaphoric references, output GEO-readiness score. | WebFetch + parsing | — |
| `check-internal-links.py` | Extract all internal links from a page, evaluate anchor text quality, count links per 1000 words, check orphan status. | WebFetch | DataForSEO on-page |
| `check-images.py` | Extract `<img>` tags, check alt text, file format, lazy loading, width/height, estimate file sizes via HEAD requests. | WebFetch | Playwright MCP for rendered analysis |
| `extract-structured-data.py` | Pull JSON-LD from page, identify schema type, validate properties against page-type mapping. | WebFetch | DataForSEO on-page |
| `check-freshness.py` | Check visible dates, extract datePublished/dateModified from schema, verify author byline and author page link. | WebFetch | — |
| `audit-page.py` | Orchestrator — runs all 7 scripts above against a URL, aggregates into the On-Page SGEO Audit Table format. | Calls other scripts | Uses paid tools if available |

### References (5)

| File | Content | ~Lines |
|------|---------|--------|
| `meta-optimization.md` | Title/description craft, pixel-width truncation, keyword placement, OG tags, AI engine meta usage. Good/bad examples by industry. | 120-150 |
| `heading-and-structure.md` | Hierarchy rules, GEO question-format patterns, H2 templates by intent type. 10+ before/after heading rewrites. | 150-180 |
| `geo-formatting.md` | Direct-answer-first pattern, self-contained knowledge blocks, citation-worthy passage construction. Per-section scoring rubric (0-8 scale for individual page sections — distinct from content-sgeo's `score-content-geo.py` which scores full articles on a 0-40 scale across 8 elements at 0-5 each). | 180-220 |
| `internal-linking.md` | Link equity theory, anchor text taxonomy with risk levels, contextual vs navigational linking, click depth optimization. | 120-150 |
| `image-and-media.md` | Format decision tree, compression targets by type, responsive images, lazy loading rules, CLS prevention, alt text guide. | 100-130 |

### SKILL.md Updates
- Insert Tool Discovery section
- Script pointers per optimization section
- Reference pointers for deep context
- Highlight `audit-page.py` as the "run everything" entry point

---

## Skill 3: content-sgeo

### Scripts (7)

| Script | Purpose | Free Path | Paid Extension |
|--------|---------|-----------|----------------|
| `research-keywords.py` | Expand seed keywords via WebSearch (Autocomplete, PAA, related searches). Output keyword table with volume estimates, difficulty proxy, intent. | WebSearch + WebFetch | DataForSEO keyword API |
| `classify-intent.py` | Search each keyword, analyze top 5 results to determine intent. Output classification with confidence score. | WebSearch | DataForSEO SERP API |
| `analyze-serp-competitors.py` | Fetch top 10 SERP for a keyword, extract title patterns, word counts, heading structures, schema types, content formats. Identify gaps. | WebSearch + WebFetch | DataForSEO + Ahrefs |
| `score-content-geo.py` | Score a URL against the 8-element GEO framework: TLDR, question headers, data density, self-contained sections, expert quotes, citations, original value, author attribution. Output 0-40 score with breakdown. | WebFetch + parsing | — |
| `check-eeat-signals.py` | Check author byline, author page, bio/credentials, external citations, visible dates, editorial policy. Output E-E-A-T checklist. | WebFetch | — |
| `audit-content-freshness.py` | Extract dates from sitemap/URL list, flag pages >6/12/18 months without updates, identify position 4-15 refresh candidates. | WebFetch + WebSearch | DataForSEO for bulk ranking data |
| `plan-topic-cluster.py` | Take pillar topic, discover subtopics via WebSearch (PAA, related searches, competitor analysis), generate cluster structure with pillar + 5-10 supporting articles. | WebSearch | DataForSEO for volume per subtopic |

### References (5)

| File | Content | ~Lines |
|------|---------|--------|
| `keyword-research.md` | Seed expansion, search operator tricks, difficulty score interpretation, CPC as intent proxy, competitor gap workflow. | 180-220 |
| `topic-clusters.md` | Cluster architecture, pillar/support sizing, publishing sequence, cluster completion metrics. 3 worked examples. | 150-180 |
| `geo-content-framework.md` | 8-element GEO method expanded with before/after rewrites, scoring rubric, passage extraction simulation. | 250-300 |
| `eeat-signals.md` | Quality rater guidelines distilled, AI credibility assessment, author page template, December 2025 update impact. | 180-220 |
| `content-refresh.md` | 3-tier refresh model, GSC-based candidate identification, update workflows, freshness signal mechanics. | 120-150 |

### SKILL.md Updates
- Insert Tool Discovery section
- Script pointers per step
- Reference pointers for deep context
- Highlight `score-content-geo.py` as the key feedback loop (run before and after optimization)

---

## Skill 4: off-page-sgeo

### Scripts (7)

| Script | Purpose | Free Path | Paid Extension |
|--------|---------|-----------|----------------|
| `check-backlink-profile.py` | Estimate backlink profile via WebSearch (`"domain.com" -site:domain.com`), count referring domains, identify top sources. | WebSearch | DataForSEO backlink API / Ahrefs API |
| `monitor-brand-mentions.py` | Search brand name across web, Reddit, HN, LinkedIn. Classify mentions as linked/unlinked, sentiment. Output mention report with conversion candidates. | WebSearch | DataForSEO content analysis API |
| `audit-platform-presence.py` | Check brand presence on 7 AI-cited platforms (Reddit, YouTube, LinkedIn, Wikipedia, GitHub, Stack Overflow, industry forums). Output platform audit template. | WebSearch + WebFetch | — |
| `probe-ai-visibility.py` | Test 10-20 queries against accessible AI platforms (Perplexity via WebFetch, others via WebSearch). Record brand citations, competitor citations. | WebFetch + WebSearch | DataForSEO AI visibility endpoints |
| `analyze-competitor-authority.py` | Compare 3-5 competitor domains on backlinks, platform presence, mention volume, content volume. Output competitive authority matrix. | WebSearch | DataForSEO domain analytics |
| `find-link-opportunities.py` | Find resource pages, broken link candidates, guest post targets, journalist queries for a topic. Output prioritized outreach list. | WebSearch | Ahrefs for broken links, DataForSEO for DR/DA |
| `track-ai-referrers.py` | Generate GA4 custom channel group config for AI referrers (chat.openai.com, perplexity.ai, gemini.google.com, claude.ai). Output setup guide. | Generates config | GSC API if available |

### References (5)

| File | Content | ~Lines |
|------|---------|--------|
| `backlink-strategy.md` | Link acquisition playbook, outreach templates, response rate benchmarks, anchor text distribution, toxic link identification. | 200-250 |
| `brand-mentions.md` | Monitoring setup, mention-to-link conversion workflow, building mentionable authority, AI entity signal processing. | 130-160 |
| `ai-citation-platforms.md` | Platform-by-platform guide for 7 AI-cited sources. Do's, don'ts, and high-citation patterns per platform. | 300-350 |
| `digital-pr.md` | Journalist identification, pitch construction, podcast guesting, awards/lists, conference speaking. 3 pitch examples. | 150-180 |
| `ai-visibility-measurement.md` | Manual testing protocol, tool comparison (Cairrot vs AIclicks vs Peec vs Semrush), GA4 setup, Share of Model metric. | 180-220 |

### SKILL.md Updates
- Insert Tool Discovery section
- Script pointers per step
- Reference pointers for deep context
- Highlight `probe-ai-visibility.py` as the key measurement script (baseline + monthly)

---

## Totals

| | Scripts | References | SKILL.md Updates |
|-|---------|------------|-----------------|
| technical-sgeo | 10 | 5 | Tool Discovery + pointers |
| on-page-sgeo | 8 | 5 | Tool Discovery + pointers + orchestrator |
| content-sgeo | 7 | 5 | Tool Discovery + pointers + feedback loop |
| off-page-sgeo | 7 | 5 | Tool Discovery + pointers + measurement |
| **Total** | **32** | **20** | **4 rewrites** |

## Implementation Notes

- All scripts accept a `--tools` flag or read a `tools.json` inventory file produced by `inventory-tools.py`
- Scripts output structured data (JSON) that the agent can parse and present in the SKILL.md table formats
- References are loaded on-demand — the agent reads only the reference relevant to its current step
- Each script has a `--help` flag documenting usage, required inputs, and expected outputs
- Scripts that call external APIs include rate limiting and error handling with clear fallback instructions
