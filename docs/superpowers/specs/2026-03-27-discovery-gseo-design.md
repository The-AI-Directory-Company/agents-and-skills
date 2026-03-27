# Discovery GSEO Skill Design

**Date:** 2026-03-27
**Status:** Draft
**Scope:** Create a new skill `discovery-gseo` — the upstream discovery and prioritization layer for the SGEO skill series

---

## Context

Four SGEO skills exist covering execution:
- `technical-sgeo` — Making a site crawlable
- `on-page-sgeo` — Making each page relevant
- `content-sgeo` — Creating pages worth ranking and quoting
- `off-page-sgeo` — Building authority

Missing: the **discovery** layer that determines *what* to build before the execution skills take over. Without good discovery, all downstream execution effort is wasted — targeting the wrong keywords, creating content for topics nobody searches for, missing opportunities competitors are already winning.

`discovery-gseo` fills this gap. It is the first skill in the SGEO pipeline and the most critical.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| GEO integration | GEO-aware throughout every phase | Every discovery step evaluates both SEO and GEO potential. Not a bolt-on — GEO is a dimension of every keyword evaluation, competitor analysis, and prioritization score. |
| Automation model | Browser-first for live data | Playwright MCP and Chrome DevTools MCP are PRIMARY tools for SERP analysis, Autocomplete harvesting, PAA extraction, and competitor page analysis. WebFetch/WebSearch as fallback when browser unavailable. |
| SEO/GEO framing | Equal weight, unified | Consistent with the other 4 SGEO skills. |
| Tone | Practitioner — direct, opinionated | Same as the other 4 SGEO skills. |
| Tool availability | Upfront inventory (extended for browser) | Browser automation is listed as PRIMARY in Tool Discovery. Agent must check for Playwright MCP / Chrome DevTools MCP first. |
| Free/paid model | Free baseline + optional paid extensions | Browser + WebSearch covers 80% of the discovery process. Paid tools (DataForSEO, Ahrefs, Semrush) add volume/KD precision and competitor gap analysis. |
| Prioritization | 4-dimension scoring (max 12) | Business Value (1-3) + Feasibility (1-3) + Traffic (1-3) + GEO Opportunity (1-3). Extends the source guide's 3-dimension/9-point model with a GEO dimension. |

## Frontmatter

```yaml
---
name: discovery-gseo
description: >
  Find, evaluate, and prioritize keyword and content opportunities for both
  search engine ranking and AI platform citation — using live browser automation,
  SERP analysis, competitor intelligence, community listening, and GEO-aware
  scoring to produce a prioritized content plan that drives traffic and AI visibility.
metadata:
  displayName: "Discovery GSEO"
  categories: ["business", "communication"]
  tags: ["SEO", "GEO", "GSEO", "keyword-research", "discovery", "competitor-analysis",
         "SERP-analysis", "content-planning", "Playwright", "browser-automation"]
  worksWellWithAgents: ["seo-specialist", "marketing-strategist", "content-strategist",
                        "growth-engineer", "product-marketing-manager"]
  worksWellWithSkills: ["technical-sgeo", "on-page-sgeo", "content-sgeo", "off-page-sgeo",
                        "technical-seo-audit", "content-calendar", "go-to-market-plan"]
---
```

## SKILL.md Structure

### Tool Discovery (extended for browser automation)

Same pattern as other 4 SGEO skills, but with browser automation as PRIMARY tier:

```markdown
## Tool discovery

Before gathering project details, confirm which tools are available.
Ask the user directly — do not assume access to any external service.

**Browser automation (primary for this skill):**
- [ ] Playwright MCP (live SERP interaction, Autocomplete, PAA expansion, screenshots)
- [ ] Chrome DevTools MCP (alternative browser control, performance analysis)

**Free tools (no API key required):**
- [ ] WebFetch (fetch any public URL)
- [ ] WebSearch (search engine queries)
- [ ] Google PageSpeed Insights API
- [ ] Google Rich Results Test

**Paid tools (API key or MCP required):**
- [ ] Google Search Console API (requires OAuth — critical for Phase 10 quick wins)
- [ ] DataForSEO MCP (SERP data, keyword metrics, backlinks, AI visibility)
- [ ] Ahrefs API (keyword research, competitor gap analysis, backlink data)
- [ ] Semrush API (largest keyword database, keyword gap, magic tool)

**The agent must:**
1. Check for Playwright MCP or Chrome DevTools MCP FIRST — many scripts in this skill depend on browser automation for live SERP data
2. If no browser automation available: all scripts fall back to WebSearch + WebFetch, but output quality is reduced (no live Autocomplete, no PAA expansion, no visual SERP analysis)
3. Present the full checklist to the user and record what is available
4. Pass the inventory to scripts as context
```

### Before You Start

Gather from user:
1. **What is your business/product?** (Product category, target market, value proposition)
2. **What is your site URL?** (Existing site for quick win analysis, or "new site" if starting from scratch)
3. **Who are your known competitors?** (3-5 domains — business competitors AND SEO competitors)
4. **What is your current SEO status?** (Brand new / some content / established. Determines whether Phase 10 is applicable)
5. **Do you have Google Search Console access?** (Critical for Phase 10 quick wins)
6. **What is the target country/region?** (For localized SERP analysis and volume data)
7. **What is your budget for tools?** (None / small / moderate / significant — determines which paid tool paths are available)
8. **How important is AI visibility?** (Determines weight of GEO scoring in prioritization)

### Phase 1: Generate Seed Keywords

From the source guide's methodology + GEO seed layer:
- 5 questions to generate seeds (What do you sell? What problem do you solve? How would a stranger describe you? What competitors exist? What technologies are relevant?)
- Target 15-30 seeds, 1-4 words each
- **GEO seed layer:** Probe AI platforms with broad questions about your space ("What are the best tools for [your category]?", "How do I solve [your problem]?"). Record which brands/topics AI mentions — these are GEO-validated seed keywords.
- Script: `probe-ai-discovery.py` for GEO seed validation
- Output: seed keyword list with GEO validation flags

### Phase 2: Expand Keyword Universe

Tool-driven expansion from each seed:
- Google Keyword Planner (free, volume ranges)
- Paid tools: Ahrefs Keywords Explorer, Semrush Keyword Magic Tool, Ubersuggest
- **Browser automation:** `harvest-autocomplete.py` for live Google Autocomplete (seed + a-z variations)
- **Browser automation:** `extract-paa.py` for People Also Ask expansion
- Target: 200-1000+ raw keyword ideas per seed set
- Script: `harvest-autocomplete.py`, `extract-paa.py`
- Reference: `keyword-expansion.md`

### Phase 3: Spy on Competitors

Competitor intelligence:
- Identify SEO competitors (search 5-10 seeds, note which domains appear repeatedly)
- Keyword gap analysis: what competitors rank for that you don't
- Top pages analysis: which competitor pages drive the most traffic
- **GEO competitor analysis:** For target queries, check which competitors get cited by AI platforms. Who is winning in AI answers? What do their cited pages have that yours don't?
- Script: `competitor-gap-analysis.py`, `probe-ai-discovery.py` (for GEO competitor check)
- Reference: `competitor-intelligence.md`

### Phase 4: Mine Google for Free Ideas

Live browser-automated Google mining:
- **Autocomplete harvesting:** `harvest-autocomplete.py` — type seeds with a-z suffixes, question prefixes (how/what/why/best)
- **PAA expansion:** `extract-paa.py` — search each seed, click-expand all PAA boxes, capture 20-50+ questions
- **Related Searches chaining:** `scrape-related-searches.py` — scroll to bottom, extract related searches, click each for 2 levels deep
- **GSC mining (existing sites):** Queries tab, sort by impressions, find striking-distance keywords
- Script: `harvest-autocomplete.py`, `extract-paa.py`, `scrape-related-searches.py`
- Reference: `browser-automation-guide.md`

### Phase 5: Listen to Communities

Community keyword extraction:
- Reddit, HN, Twitter/X, Quora, Product Hunt, industry forums
- **Browser automation:** `scrape-community-keywords.py` — opens platforms via Playwright, searches topic, extracts question titles, popular comment phrases, pain point language
- Language pattern → keyword candidate mapping
- **GEO dimension:** Community language maps directly to AI query language. Questions people ask on Reddit are the same questions people ask ChatGPT.
- Script: `scrape-community-keywords.py`
- Reference: `community-listening.md`

### Phase 6: Evaluate and Filter Keywords

Data enrichment and filtering:
- For each keyword: get volume, KD, CPC (via paid tools if available, or estimates via SERP analysis)
- **GEO score:** For each keyword, assess AI citation potential:
  - Do AI platforms answer this query? (searched via `probe-ai-discovery.py`)
  - How many sources do they cite?
  - Are the cited sources weak (= opportunity to replace them)?
  - Is this a topic where AI engines give answers vs defer to search?
- Filtering: remove irrelevant, remove branded navigational, remove KD > threshold, remove duplicates
- Script: `evaluate-keywords.py`, `probe-ai-discovery.py`
- Reference: `evaluation-and-scoring.md`

### Phase 7: Classify Search Intent

SERP-based intent classification:
- **Live SERP test via Playwright:** `classify-intent-live.py` — for each keyword, searches Google, analyzes what content types rank (blog/product/comparison/tool), what SERP features appear (AI Overview, PAA, Featured Snippet, Video), classifies intent
- 4 intent types: Informational, Navigational, Commercial, Transactional
- **AI-answerable flag:** Does Google show an AI Overview for this query? Does Perplexity give a direct answer? If yes, GEO optimization is especially important for this keyword.
- Script: `classify-intent-live.py`
- Reference: `evaluation-and-scoring.md`

### Phase 8: Group Into Topic Clusters

Keyword grouping and cluster architecture:
- Group by semantic similarity and parent/child relationships
- Identify pillar candidates (highest volume, broadest scope per cluster)
- Assign supporting keywords (depth topics, questions, long-tail variants)
- **GEO citation mapping:** For each cluster, identify which supporting topics have the highest AI citation potential — these become priority content within the cluster
- Script: `build-topic-clusters.py`
- Reference: `evaluation-and-scoring.md`

### Phase 9: Prioritize and Build Content Plan

4-dimension scoring (max 12 points):
- **Business Value (1-3):** Direct product relevance, conversion potential
- **Ranking Feasibility (1-3):** KD assessment, existing authority, competitive landscape
- **Traffic Potential (1-3):** Search volume, click-through potential
- **GEO Opportunity (1-3):** AI citation potential, weak existing sources, AI-answerable queries with few cited sources

Tiers: 10-12 = golden (do first), 7-9 = strong (do second), 4-6 = moderate (do eventually), 1-3 = skip for now

Output: prioritized content plan with keyword, volume, KD, intent, GEO score, page type, target URL, cluster, publish schedule
- Script: `prioritize-opportunities.py`
- Reference: `evaluation-and-scoring.md`

### Phase 10: Find Quick Wins in Existing Data

For sites with existing traffic only:
- **Striking distance (positions 8-20):** Already ranking, small improvements push to page 1
- **High impressions, low CTR:** Title/description needs improvement
- **Variant keywords:** Ranking for unintended keywords with higher value
- **GEO quick wins:** Keywords where you rank but aren't cited by AI — optimize content structure for GEO (apply on-page-sgeo skill)
- Script: `find-quick-wins.py`
- Reference: `evaluation-and-scoring.md`

## Scripts (12)

| # | Script | Purpose | Primary Tool | Fallback |
|---|--------|---------|-------------|----------|
| 1 | `harvest-autocomplete.py` | Type seeds + a-z in Google, capture all Autocomplete suggestions | Playwright MCP | WebSearch approximation |
| 2 | `extract-paa.py` | Search Google, expand all PAA boxes, capture 20-50+ questions per seed | Playwright MCP | WebSearch + HTML parsing |
| 3 | `scrape-related-searches.py` | Extract Related Searches from Google SERP bottom, chain 2 levels deep | Playwright MCP | WebSearch |
| 4 | `analyze-serp-live.py` | Flagship: search keyword, capture organic results + all SERP features + AI Overview presence + screenshot | Playwright MCP | WebSearch + WebFetch |
| 5 | `competitor-gap-analysis.py` | Compare user domain vs competitors for keyword gaps | WebSearch + WebFetch | DataForSEO/Ahrefs API |
| 6 | `scrape-community-keywords.py` | Search Reddit/HN/forums, extract question titles and pain point language | Playwright MCP | WebSearch `site:reddit.com` |
| 7 | `probe-ai-discovery.py` | GEO differentiator: test queries on AI platforms, record citations, find gaps | WebFetch + WebSearch | DataForSEO AI endpoints |
| 8 | `evaluate-keywords.py` | Enrich raw keyword list with volume/KD estimates + GEO score, filter noise | WebSearch | DataForSEO keyword API |
| 9 | `classify-intent-live.py` | Live SERP analysis: determine intent + AI-answerable flag per keyword | Playwright MCP | WebSearch |
| 10 | `build-topic-clusters.py` | Group keywords by semantic similarity, identify pillars, generate cluster map | Local processing | — |
| 11 | `prioritize-opportunities.py` | 4-dimension scoring (max 12), output tiered content plan with schedule | Local processing | — |
| 12 | `find-quick-wins.py` | GSC striking distance + high-impression/low-CTR + GEO citation gaps | GSC API | WebSearch `site:domain` |

### Script Conventions

Same as the other 4 SGEO skills:
- Python 3.9+, `#!/usr/bin/env python3` shebang
- argparse with `--help`
- JSON output to stdout
- `--tools` flag for tool inventory
- Error handling with fallback instructions
- Rate limiting for external calls

**Additional for browser-first scripts:**
- Scripts that use Playwright MCP include instructions for the agent on how to invoke browser tools (navigate, click, wait, extract text, take screenshot)
- Each browser script has a `--no-browser` flag that activates the WebSearch/WebFetch fallback path
- Browser scripts include anti-detection patterns: realistic delays between actions, standard viewport sizes, no rapid-fire requests
- Scripts document the exact Playwright MCP tool calls needed (e.g., `browser_navigate`, `browser_click`, `browser_snapshot`, `browser_evaluate`)

## References (6)

| File | Content | ~Lines |
|------|---------|--------|
| `seed-generation.md` | Mental model (5 keyword sources), seed methodology, customer language extraction, GEO seed validation (probing AI for topic ideas), seed-to-universe expansion strategy. | 120-150 |
| `keyword-expansion.md` | Tool-by-tool guides (Google Keyword Planner, Ahrefs, Semrush, Ubersuggest, AnswerThePublic), browser automation expansion (Autocomplete technique, PAA technique, Related Searches chaining), volume/KD interpretation across tools, zero-volume keywords as opportunities. | 200-250 |
| `competitor-intelligence.md` | SEO competitor identification, keyword gap methodology (Ahrefs Content Gap, Semrush Keyword Gap, free alternatives), top pages analysis, analyzing why competitors rank, GEO competitor analysis (who gets cited in AI answers, what their cited pages look like). | 180-220 |
| `community-listening.md` | Platform-by-platform guide (Reddit, HN, Twitter/X, Quora, Product Hunt, forums, Discord/Slack), language pattern extraction methodology, community observation → keyword candidate pipeline, GEO dimension (community language = AI query language), browser automation for community scraping. | 150-180 |
| `evaluation-and-scoring.md` | Volume/KD/intent metrics explained, GEO score methodology (AI citation potential assessment), filtering rules (irrelevant, branded, too-difficult, duplicates), spreadsheet structure, 4-dimension prioritization framework (max 12 points with GEO), quick win identification, the SERP test for intent classification, AI-answerable flag. | 250-300 |
| `browser-automation-guide.md` | THE key reference. How to use Playwright MCP and Chrome DevTools MCP for live SERP data extraction. Covers: Google navigation (incognito, avoiding captchas, realistic delays), Autocomplete extraction technique, PAA box expansion and capture, Related Searches extraction, SERP feature detection (AI Overview, Featured Snippet, Knowledge Panel, Video carousel, Local pack), screenshot capture, handling dynamic content, rate limiting, session management, fallback patterns when browser is unavailable. Tool call examples for both Playwright MCP and Chrome DevTools MCP. | 300-350 |

## SKILL.md Size Estimate

The SKILL.md for discovery-gseo will be larger than the other 4 skills because it covers a 10-phase process. Estimated ~450-500 lines. This is at the upper limit of the authoring guide's recommendation (<500 lines) but appropriate given the process complexity. The references absorb the deep detail, keeping SKILL.md procedural.

## How It Fits in the SGEO Pipeline

```
discovery-gseo → finds WHAT to target
    ↓
technical-sgeo → ensures the site CAN be found
    ↓
content-sgeo → creates content worth ranking/quoting
    ↓
on-page-sgeo → optimizes each page for ranking/citation
    ↓
off-page-sgeo → builds authority to sustain rankings/citations
```

discovery-gseo is the entry point. Its output (prioritized content plan with keywords, intent, clusters, GEO scores) feeds directly into content-sgeo (what to write) and on-page-sgeo (how to optimize each page).

## Totals

| Category | Count |
|----------|-------|
| Scripts | 12 |
| References | 6 |
| SKILL.md sections | 12 (Tool Discovery + Before You Start + 10 phases) |
| Total files | 19 (1 SKILL.md + 6 references + 12 scripts) |
