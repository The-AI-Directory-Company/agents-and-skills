# Discovery GSEO Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the `discovery-gseo` skill — the upstream discovery and prioritization layer for the SGEO skill series, with 12 browser-first Python scripts, 6 reference documents, and a comprehensive SKILL.md covering a 10-phase GEO-aware keyword discovery process.

**Architecture:** Single self-contained skill folder following the Agent Skills spec. Browser automation (Playwright MCP / Chrome DevTools MCP) is the primary tool tier. Scripts are designed as both standalone CLI tools and instructional code that AI agents read to understand how to use browser tools for live SERP data extraction.

**Tech Stack:** Python 3.9+ (scripts), Markdown (SKILL.md + references), Playwright MCP / Chrome DevTools MCP (primary), WebFetch/WebSearch (fallback), DataForSEO/Ahrefs/Semrush APIs (optional paid)

**Spec:** `docs/superpowers/specs/2026-03-27-discovery-gseo-design.md`
**Source guide:** `docs/seo-opportunity-discovery.md`
**Existing SGEO skills for reference:** `skills/technical-sgeo/`, `skills/on-page-sgeo/`, `skills/content-sgeo/`, `skills/off-page-sgeo/`

---

## Task 1: discovery-gseo — SKILL.md, References, and Scripts

**Files:**
- Create: `skills/discovery-gseo/SKILL.md`
- Create: `skills/discovery-gseo/references/seed-generation.md`
- Create: `skills/discovery-gseo/references/keyword-expansion.md`
- Create: `skills/discovery-gseo/references/competitor-intelligence.md`
- Create: `skills/discovery-gseo/references/community-listening.md`
- Create: `skills/discovery-gseo/references/evaluation-and-scoring.md`
- Create: `skills/discovery-gseo/references/browser-automation-guide.md`
- Create: `skills/discovery-gseo/scripts/harvest-autocomplete.py`
- Create: `skills/discovery-gseo/scripts/extract-paa.py`
- Create: `skills/discovery-gseo/scripts/scrape-related-searches.py`
- Create: `skills/discovery-gseo/scripts/analyze-serp-live.py`
- Create: `skills/discovery-gseo/scripts/competitor-gap-analysis.py`
- Create: `skills/discovery-gseo/scripts/scrape-community-keywords.py`
- Create: `skills/discovery-gseo/scripts/probe-ai-discovery.py`
- Create: `skills/discovery-gseo/scripts/evaluate-keywords.py`
- Create: `skills/discovery-gseo/scripts/classify-intent-live.py`
- Create: `skills/discovery-gseo/scripts/build-topic-clusters.py`
- Create: `skills/discovery-gseo/scripts/prioritize-opportunities.py`
- Create: `skills/discovery-gseo/scripts/find-quick-wins.py`

All paths relative to `/Users/raul/projects/ai-directory-company/apps/web/content/community/`.

### Directory Setup

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p skills/discovery-gseo/references skills/discovery-gseo/scripts
```

### SKILL.md

- [ ] **Step 2: Write `skills/discovery-gseo/SKILL.md` (~450-500 lines)**

This is the most important file. It must cover the complete 10-phase discovery process with GEO integration throughout. Follow the pattern of the other 4 SGEO skills (read `skills/technical-sgeo/SKILL.md` for format reference) but this SKILL.md is larger due to the 10-phase scope.

**Frontmatter:**
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

**Body structure (12 sections):**

**## Tool discovery**

Extended version with browser automation as PRIMARY tier. Must include:
- Browser automation tier: Playwright MCP, Chrome DevTools MCP (marked as "primary for this skill")
- Free tools: WebFetch, WebSearch, Google PageSpeed Insights API, Google Rich Results Test
- Paid tools: GSC API, DataForSEO MCP, Ahrefs API, Semrush API
- Agent instructions: check for browser first, fall back to WebSearch/WebFetch if unavailable, present checklist to user

**## Before you start**

Gather 8 inputs:
1. Business/product description
2. Site URL (or "new site")
3. Known competitors (3-5 domains)
4. Current SEO status (new / some content / established)
5. Google Search Console access
6. Target country/region
7. Tool budget (none / small / moderate / significant)
8. AI visibility importance (determines GEO weight in scoring)

If the user says "I just want to find keywords," push back: "Keywords without intent classification, competitor validation, and prioritization scoring produce a random list, not a strategy. Which phase do you want to start from?"

**## Phase 1: Generate seed keywords**

From source guide Section 4. Must include:
- 5 seed generation questions (What do you sell? What problem? How would a stranger describe it? Competitors? Technologies?)
- Target: 15-30 seeds, 1-4 words each
- **GEO seed layer:** Probe AI platforms (ChatGPT, Perplexity, Gemini) with broad questions about the space. Record which brands/topics they mention — these are GEO-validated opportunities.
- Example seed list (use the invoicing SaaS example from the guide)
- Script pointer: "Run `scripts/probe-ai-discovery.py --queries 'What are the best [category] tools?'` to validate seeds against AI visibility."

**## Phase 2: Expand keyword universe**

From source guide Section 5. Must include:
- Google Keyword Planner walkthrough (free, volume ranges)
- Paid tool walkthrough (Ahrefs, Semrush, Ubersuggest — brief, point to reference for details)
- **Browser-automated expansion:** "Run `scripts/harvest-autocomplete.py --seeds 'seed1,seed2,seed3'` to harvest Google Autocomplete suggestions via live browser. Run `scripts/extract-paa.py` to expand People Also Ask boxes."
- Target output: 200-1000+ raw keyword ideas
- Reference pointer: `references/keyword-expansion.md`

**## Phase 3: Spy on competitors**

From source guide Section 6. Must include:
- Step 1: Identify SEO competitors (search 5-10 seeds, note recurring domains)
- Step 2: Keyword gap analysis (Ahrefs Content Gap, Semrush Keyword Gap, or free approximation via WebSearch)
- Step 3: Analyze why competitors rank (page type, depth, angle, weaknesses)
- Step 4: Top pages analysis (what drives their traffic)
- **GEO competitor analysis:** "Run `scripts/probe-ai-discovery.py` with competitor-relevant queries. Which competitors get cited by AI? What do their cited pages have that yours don't?"
- Script pointer: `scripts/competitor-gap-analysis.py`, `scripts/probe-ai-discovery.py`
- Reference pointer: `references/competitor-intelligence.md`

**## Phase 4: Mine Google for free ideas**

From source guide Section 7. Must include:
- Technique 1: Autocomplete (seed + a-z, question prefixes) — "Run `scripts/harvest-autocomplete.py`"
- Technique 2: PAA expansion — "Run `scripts/extract-paa.py --seeds 'seed1,seed2'`"
- Technique 3: Related Searches chaining — "Run `scripts/scrape-related-searches.py`"
- Technique 4: AnswerThePublic (3 free searches/day)
- Technique 5: GSC mining for existing sites (Queries tab, impressions sort, striking distance)
- Reference pointer: `references/browser-automation-guide.md` for Playwright technique details

**## Phase 5: Listen to communities**

From source guide Section 8. Must include:
- Where to look: Reddit, HN, Twitter/X, Quora, Product Hunt, industry forums/Discord/Slack
- What to capture: language patterns, pain points, question formats, comparison language
- Community observation → keyword candidate mapping (with examples from the guide)
- **GEO dimension:** "Community language maps to AI query language. The questions people ask on Reddit are the same questions they ask ChatGPT."
- Script pointer: "Run `scripts/scrape-community-keywords.py --topic 'your category' --platforms reddit,hn`"
- Reference pointer: `references/community-listening.md`

**## Phase 6: Evaluate and filter keywords**

From source guide Section 9. Must include:
- The 3 SEO metrics: Volume, Keyword Difficulty, Search Intent (with how-to-read scales from the guide)
- **GEO score (new):** AI citation potential assessment:
  - Does an AI platform answer this query?
  - How many sources does it cite?
  - Are cited sources weak (= replacement opportunity)?
  - Is this a topic where AI gives direct answers vs defers to search?
- Filtering rules: remove irrelevant, branded navigational, KD > threshold, duplicates/near-duplicates
- Spreadsheet structure: `| Keyword | Volume | KD | Intent | GEO Score | Source | Priority | Target URL | Status |`
- Script pointer: "Run `scripts/evaluate-keywords.py` to enrich your keyword list with volume/KD estimates and GEO scores. Run `scripts/probe-ai-discovery.py` to assess AI citation potential."
- Reference pointer: `references/evaluation-and-scoring.md`

**## Phase 7: Classify search intent**

From source guide Section 10. Must include:
- 4 intent types with signals, content types, and examples (Informational, Navigational, Commercial, Transactional — from the source guide)
- **The SERP test:** Search the keyword, look at what ranks, Google has already figured out the intent
- **AI-answerable flag (GEO):** Does Google show an AI Overview? Does Perplexity give a direct answer? If yes → GEO optimization is critical for this keyword
- Script pointer: "Run `scripts/classify-intent-live.py` — searches each keyword via Playwright, analyzes SERP composition, classifies intent, flags AI-answerable queries."

**## Phase 8: Group into topic clusters**

From source guide Section 11. Must include:
- Cluster structure: Pillar page (comprehensive, broad) + Supporting pages (specific, deep) + Internal links
- How to group: identify themes, find head keyword per group (= pillar target), remaining keywords = supports or H2 sections
- When a keyword deserves its own page vs H2 section (from the guide's rules)
- **GEO citation mapping:** Within each cluster, identify which supporting topics have highest AI citation potential — prioritize those for early creation
- Example cluster structure (use the invoicing example from the guide, enhanced with GEO scores)
- Script pointer: "Run `scripts/build-topic-clusters.py` with your evaluated keyword list."

**## Phase 9: Prioritize and build content plan**

From source guide Section 12 + GEO dimension. Must include:
- **4-dimension scoring framework (max 12 points):**
  - Business Value (1-3): Direct product relevance → 3, indirect → 2, tangential → 1
  - Ranking Feasibility (1-3): KD <20 + expertise → 3, KD 20-40 → 2, KD 40+ → 1
  - Traffic Potential (1-3): Volume >1000 → 3, 200-1000 → 2, <200 → 1
  - **GEO Opportunity (1-3):** AI cites weak sources you can replace → 3, AI answers but cites strong sources → 2, AI doesn't answer this query → 1
- Tiers: 10-12 = golden (first), 7-9 = strong (second), 4-6 = moderate (eventually), 1-3 = skip
- Content calendar template: `| Priority | Keyword | Volume | KD | Intent | GEO Score | Page Type | Target URL | Cluster | Publish By |`
- Monthly publishing cadence (Month 1: 3-5 highest priority, Month 2: supporting pages + internal links, Month 3: optimize Month 1 content with GSC data)
- Script pointer: "Run `scripts/prioritize-opportunities.py` to apply the 4-dimension scoring and generate your tiered content plan."

**## Phase 10: Find quick wins in existing data**

From source guide Section 13. Must include:
- Prerequisite: site must have existing traffic (skip if brand new, come back in 2-3 months)
- Quick win type 1: Striking distance (positions 8-20) — how to find in GSC, what to do
- Quick win type 2: High impressions, low CTR — title/description improvement
- Quick win type 3: Variant keywords — ranking for unintended keywords with higher value
- **GEO quick wins:** Keywords where you rank in search but aren't cited by AI. Optimize content structure using on-page-sgeo and content-sgeo skills.
- Script pointer: "Run `scripts/find-quick-wins.py --domain yourdomain.com`"

**## Available scripts**

Table listing all 12 scripts with descriptions and when to run them.
Highlight the browser-automated scripts: "Scripts marked with 🌐 use Playwright MCP for live browser data. If Playwright is unavailable, they fall back to WebSearch/WebFetch with reduced output quality."

**## Quality checklist**

8-10 items:
- All 10 phases completed (or consciously skipped with documented reason)
- Seed keywords validated against both search data AND AI platform probing
- Competitor gap analysis includes both SEO gaps and GEO citation gaps
- Every keyword has volume, KD, intent classification, and GEO score
- Intent classification verified via live SERP test (not just heuristic)
- Keywords grouped into topic clusters with pillar/support assignments
- Content plan uses 4-dimension scoring with GEO as a dimension
- Quick wins identified (if existing site)
- Output is a prioritized content plan, not a raw keyword list
- Plan feeds clearly into content-sgeo (what to write) and on-page-sgeo (how to optimize)

**## Common mistakes to avoid**

From source guide Section 17 + GEO mistakes:
1. Targeting keywords that are too broad
2. Ignoring search intent
3. Obsessing over search volume (intent matters more)
4. Never checking the actual SERP (tools provide data, SERP provides truth)
5. Targeting same keyword with multiple pages (cannibalization)
6. Skipping competitor analysis (single highest-ROI activity)
7. Creating content without a target keyword
8. Giving up too early (3-6 months for results)
9. Only looking at your own data (biggest opportunities are gaps)
10. Doing keyword research once and never again
11. **Ignoring GEO opportunity in prioritization** (a keyword where AI cites weak sources is a faster win than one where AI cites authoritative sources you can't displace)
12. **Not validating seeds against AI platforms** (what AI recommends in your space is a leading indicator of search trends)

### References

- [ ] **Step 3: Write `references/seed-generation.md` (120-150 lines)**

Must cover:
- Mental model: 5 sources of keyword ideas (brain, competitors, Google, communities, tools) — from source guide Section 2
- Seed generation methodology: the 5 questions, how to think like your customer, avoiding internal jargon
- Seed format: 1-4 words, 15-30 total, don't worry about volume yet
- **GEO seed validation:** How to probe AI platforms for topic ideas
  - Ask ChatGPT: "What are the best tools for [category]?", "How do I [problem]?"
  - Ask Perplexity: same queries (different citation sources)
  - Record: which brands mentioned, which topics covered, what language used
  - These AI-mentioned topics are GEO-validated seeds — AI already discusses them, so your content can be cited
- Example seed list with GEO validation annotations
- Tone: Practitioner. "Your seeds don't need to be clever. They need to be obvious. If you sell invoicing software, 'invoicing software' is a perfect seed. Start obvious, let the tools find the clever stuff."

Source: `docs/seo-opportunity-discovery.md` Sections 1-4.

- [ ] **Step 4: Write `references/keyword-expansion.md` (200-250 lines)**

Must cover:
- **Tool-by-tool expansion guides:**
  - Google Keyword Planner: step-by-step (from source guide Section 5), limitations (ranges not exact, ad competition not organic)
  - Ahrefs Keywords Explorer: Matching terms, Related terms, Questions, Also rank for
  - Semrush Keyword Magic Tool: largest database (20B+ keywords), long-tail discovery
  - Ubersuggest: keyword ideas, questions, related terms, lifetime deal value
  - AnswerThePublic: questions, prepositions, comparisons, alphabetical (3 free/day)
- **Browser automation expansion:**
  - Autocomplete technique: type seed + a-z suffix in Google, capture suggestions. Why this beats WebSearch: you get real-time, localized, personalized suggestions that tools miss.
  - PAA technique: search seed, expand all PAA boxes by clicking each question. Each click reveals 2-3 more questions. Can capture 20-50+ questions per seed.
  - Related Searches: scroll to bottom of SERP, extract related terms, click each for 2nd-level chaining.
  - Rate limiting: wait 2-5 seconds between searches to avoid captchas
- **Volume/KD interpretation across tools:**
  - Ahrefs KD vs Semrush KD: different scales, don't compare cross-tool
  - Google Keyword Planner ranges vs exact data from paid tools
  - Free proxy for difficulty: count high-DA domains in top 10
  - Ahrefs "Clicks" metric (unique to Ahrefs): some high-volume keywords have low clicks due to zero-click features
- **Zero-volume keywords:** Tools show 0 but real people search these. Valuable when intent is strong. Don't ignore them.
- Tone: "Google Keyword Planner gives you ranges. Ubersuggest gives you estimates. Ahrefs gives you data. Use whichever you can afford — the process works with any of them."

Source: `docs/seo-opportunity-discovery.md` Sections 5, 7, 14.

- [ ] **Step 5: Write `references/competitor-intelligence.md` (180-220 lines)**

Must cover:
- **SEO competitor identification:**
  - Search 5-10 seeds, note which domains appear repeatedly
  - SEO competitors ≠ business competitors (editorial sites, review sites, and aggregators compete for your keywords too)
  - Pick 3-5: mix of direct product competitors and content competitors
- **Keyword gap analysis methodology:**
  - Ahrefs Content Gap: target vs competitors → missing keywords
  - Semrush Keyword Gap: up to 5 competitors, Missing tab + Weak tab
  - SE Ranking: Competitive Research → organic keywords → gap analysis
  - **Free alternative:** WebSearch `site:competitor.com` to catalog their pages, compare against your sitemap
- **Top pages analysis:**
  - Ahrefs Site Explorer → Top Pages: which pages drive most traffic
  - What to learn: content format, depth, angle, keyword targeting, structured data
- **Analyzing why competitors rank:**
  - Page type (blog, landing page, comparison, tool, tutorial)
  - Content depth (word count, coverage breadth, visual aids)
  - Angle (beginner guide, expert deep-dive, comparison, review)
  - Weaknesses (outdated info, poor structure, thin content, no examples)
- **GEO competitor analysis:**
  - For target queries: which competitors get cited by AI platforms?
  - What do their cited pages look like? (Structure, data density, author attribution)
  - Where are AI citation gaps? (Queries where AI cites weak or outdated sources)
  - How to probe: use `probe-ai-discovery.py` with competitor-branded queries
- Tone: "Competitor analysis is the single highest-ROI activity in the entire discovery process. Other websites have done the research for you. Use their work as a shortcut."

Source: `docs/seo-opportunity-discovery.md` Section 6.

- [ ] **Step 6: Write `references/community-listening.md` (150-180 lines)**

Must cover:
- **Platform-by-platform guide:**
  - Reddit: search for category/industry, relevant subreddits, what to watch (repeated questions, complaints, comparisons, language patterns)
  - Hacker News: hn.algolia.com search, "Ask HN" threads for tool recommendations
  - Twitter/X: search for category, competitor names, problem descriptions
  - Quora: topic search, read questions (mirror Google searches directly)
  - Product Hunt: similar products, read comments (needs, comparisons)
  - Industry forums/Slack/Discord: niche-specific communities, lurk before engaging
- **Language pattern extraction:**
  - How real people describe problems vs how tools see keywords
  - Pain point → keyword candidate mapping (with examples):
    - "I need a way to automatically send payment reminders" → "automatic payment reminder software"
    - "Is there a Stripe alternative that handles invoicing too?" → "Stripe alternative with invoicing"
    - "How do I set up recurring billing without a developer?" → "recurring billing no code"
  - These community-sourced keywords often show zero volume in tools but have perfect intent
- **Browser automation for community scraping:**
  - Playwright technique: navigate to Reddit/HN, search for topic, extract post titles and popular comments
  - Why browser > simple fetch: Reddit's dynamic loading, HN's pagination, forum JS rendering
  - Rate limiting: respectful scraping, 3-5 second delays
- **GEO dimension:**
  - Community language maps directly to AI query language
  - Questions on Reddit = questions people ask ChatGPT
  - Pain points described in forums = problems people describe to AI
  - This makes community-sourced keywords doubly valuable: organic search AND AI citation opportunity
- Tone: "Keyword tools rely on historical data. Communities show you what people are asking right now. The language they use maps directly to both search queries and AI prompts."

Source: `docs/seo-opportunity-discovery.md` Section 8.

- [ ] **Step 7: Write `references/evaluation-and-scoring.md` (250-300 lines)**

This is the most important reference — it covers evaluation, intent classification, prioritization, and quick wins. Must cover:

**Volume interpretation:**
- 10,000+ = High volume, very competitive
- 1,000-10,000 = Medium, good for mid-authority sites
- 100-1,000 = Sweet spot for new sites
- <100 = Still valuable with strong intent
- 0 = Tools can't measure it, but real people search it

**Keyword Difficulty interpretation:**
- 0-20 = Easy, new sites can rank in weeks/months
- 21-40 = Medium, needs content + some backlinks
- 41-60 = Hard, needs excellent content + strong backlinks
- 61-80 = Very hard, dominated by major brands
- 81-100 = Avoid unless you have very high authority
- Nuance: KD is an estimate. Always manually check the SERP.

**Search Intent classification:**
- 4 types with signals, content types, examples, and business value:
  - Informational: "how to", "what is", "guide" → guides, tutorials
  - Navigational: brand names, "login" → your own brand pages
  - Commercial: "best", "vs", "review", "alternative" → comparisons, reviews
  - Transactional: "buy", "pricing", "free trial" → product/pricing pages
- **The SERP test:** Search the keyword, look at top 5-10 results, match the format that ranks
- **AI-answerable flag:** Check if Google shows AI Overview, check Perplexity. If AI answers this query → GEO optimization is critical

**GEO score methodology:**
- For each keyword, assess AI citation potential on a 1-3 scale:
  - 3 = AI answers this query and cites weak/few sources (replacement opportunity)
  - 2 = AI answers and cites strong sources (hard to displace but still worth targeting)
  - 1 = AI doesn't answer this query / defers to search (SEO-only value)
- How to assess: run `probe-ai-discovery.py` with target queries

**Filtering rules:**
- Remove irrelevant keywords (honest assessment: would this searcher ever become a customer?)
- Remove branded competitor navigational (keep "alternative" and "vs" variants)
- Remove KD above threshold (KD >40-50 for new sites, adjust based on domain authority)
- Remove duplicates and near-duplicates (keep higher-volume version)

**Spreadsheet structure:**
```
| Keyword | Volume | KD | Intent | GEO Score | Source | Priority | Target URL | Status |
```

**4-dimension prioritization framework (max 12 points):**
- Business Value (1-3): 3 = direct product relevance, 2 = indirect, 1 = tangential
- Ranking Feasibility (1-3): 3 = KD <20 + expertise, 2 = KD 20-40, 1 = KD 40+
- Traffic Potential (1-3): 3 = >1000/mo, 2 = 200-1000/mo, 1 = <200/mo
- GEO Opportunity (1-3): 3 = AI cites weak sources (replaceable), 2 = AI cites strong sources, 1 = AI doesn't answer
- Tiers: 10-12 golden, 7-9 strong, 4-6 moderate, 1-3 skip
- Include the worked scoring example from the source guide Section 15 (form builder), enhanced with GEO scores

**Quick win identification:**
- Striking distance (positions 8-20): already ranking, small improvements push to page 1
- High impressions, low CTR: title/description needs work
- Variant keywords: ranking for unintended terms with higher value
- GEO quick wins: keywords where you rank in search but aren't cited by AI

Source: `docs/seo-opportunity-discovery.md` Sections 9, 10, 12, 13.

- [ ] **Step 8: Write `references/browser-automation-guide.md` (300-350 lines)**

THE key reference for this skill. Detailed guide on using Playwright MCP and Chrome DevTools MCP for live SERP data extraction. Must cover:

**Why browser automation matters for discovery:**
- Google's SERP is dynamic — Autocomplete, PAA, AI Overviews are JS-rendered and require a real browser
- WebSearch returns structured results but misses SERP features, visual layout, and dynamic content
- Browser automation gives you the same data a human researcher sees, at scale

**Google navigation patterns:**
- Use incognito/private mode (no search history influence)
- Set location via URL parameters (`&gl=us` for US, `&hl=en` for English)
- Realistic viewport: 1280x800 or 1920x1080
- Wait for page load completion before extraction

**Avoiding captchas and rate limiting:**
- Wait 3-8 seconds between searches (randomized)
- Don't exceed 20-30 searches per session
- If captcha appears: pause 5 minutes, clear cookies, restart session
- Consider using different search entry points: google.com vs google.com/search?q=
- User-Agent: use a standard Chrome UA string

**Autocomplete extraction technique:**
- Navigate to google.com
- Focus search input
- Type seed keyword character by character (with 100-200ms delays between characters)
- After typing full seed: wait 500ms, capture suggestion dropdown
- Append each letter a-z to seed: type 'a', wait, capture, clear last character, type 'b', etc.
- Append question prefixes: clear input, type "how to [seed]", "what is [seed]", "best [seed]", "why [seed]"
- Exact Playwright MCP tool calls: `browser_navigate` → `browser_click` (search input) → `browser_type` → `browser_snapshot` or `browser_evaluate` (extract suggestion text)

**PAA expansion technique:**
- Search for keyword (press Enter)
- Wait for results page to load
- Find PAA box (CSS selector for PAA container)
- Click each question to expand it (reveals answer + 2-3 new questions)
- After each click: wait 1-2 seconds, new questions appear
- Keep clicking newly revealed questions until no new questions appear or you've captured 50+
- Extract: question text, answer snippet, source URL
- Exact Playwright MCP tool calls: `browser_navigate` → `browser_click` (PAA question) → `browser_snapshot` → repeat

**Related Searches extraction:**
- After a search, scroll to bottom of SERP
- Extract Related Searches links
- Click each related search for 2nd-level expansion
- Extract those Related Searches too (2 levels deep)
- Exact tool calls: `browser_evaluate` (scroll to bottom) → `browser_snapshot` → `browser_click` (related search) → repeat

**SERP feature detection:**
- After searching, analyze the SERP for features:
  - AI Overview: check for AI-generated answer box at top
  - Featured Snippet: check for highlighted answer box (paragraph, list, or table)
  - People Also Ask: check for PAA expandable box
  - Knowledge Panel: check for right-side panel
  - Video carousel: check for video results
  - Local pack: check for map + business listings
  - Sitelinks: check for expanded site links under top result
- Record which features appear and their position (above/below organic results)
- This data feeds into intent classification and GEO scoring

**Screenshot capture:**
- Use `browser_take_screenshot` to capture the full SERP
- Useful for: visual analysis, documentation, comparing SERP changes over time
- Save with descriptive names: `serp-[keyword]-[date].png`

**Chrome DevTools MCP alternative:**
- Same capabilities as Playwright MCP but different tool names
- `navigate_page` instead of `browser_navigate`
- `click` instead of `browser_click`
- `take_screenshot` instead of `browser_take_screenshot`
- `evaluate_script` instead of `browser_evaluate`
- Include mapping table between Playwright MCP and Chrome DevTools MCP tool names

**Fallback patterns when browser is unavailable:**
- Autocomplete: not replicable via WebSearch (no equivalent). Skip or use AnswerThePublic.
- PAA: WebSearch may return some PAA data in results. Quality is lower.
- Related Searches: WebSearch may include some. Quality is lower.
- SERP features: not available without browser. Classify intent from result titles/URLs only.
- Community scraping: use `site:reddit.com [topic]` via WebSearch as fallback

Tone: "Browser automation is the superpower that turns this skill from keyword research into live market intelligence. WebSearch gives you results. Playwright gives you the SERP."

### Scripts

All scripts follow the same conventions as the other 4 SGEO skills (Python 3.9+, shebang, argparse, JSON output, `--tools` flag, error handling) PLUS:
- Browser-first scripts include `--no-browser` flag for fallback mode
- Browser scripts document exact Playwright MCP / Chrome DevTools MCP tool calls in comments
- Anti-detection patterns: realistic delays (randomized 2-8s), standard viewport, no rapid-fire requests
- Each browser script checks for Playwright MCP availability before attempting browser operations

- [ ] **Step 9: Write `scripts/harvest-autocomplete.py`**

Takes seed keywords (via `--seeds` comma-separated):
- **Browser path (primary):**
  1. Open Google via Playwright (`browser_navigate` to `https://www.google.com`)
  2. For each seed: click search input, type seed, wait 500ms, capture autocomplete suggestions from dropdown
  3. For each seed: append letters a-z, capture suggestions for each
  4. For each seed: prepend "how to", "what is", "best", "why" — capture suggestions
  5. Deduplicate all suggestions
  6. Wait 3-8 seconds (randomized) between searches
- **Fallback path (`--no-browser`):**
  - Use WebSearch for `[seed] a`, `[seed] b`, etc. — quality is much lower
  - Note in output that autocomplete data is approximated

Output JSON:
```json
{"seeds_processed": 15, "total_suggestions": 847, "suggestions": [{"keyword": "invoicing software free", "source_seed": "invoicing software", "expansion_type": "autocomplete_base"}, {"keyword": "invoicing software for freelancers", "source_seed": "invoicing software", "expansion_type": "autocomplete_f"}, ...], "method": "playwright|fallback"}
```

- [ ] **Step 10: Write `scripts/extract-paa.py`**

Takes seed keywords (via `--seeds` comma-separated):
- **Browser path (primary):**
  1. For each seed: navigate to Google, search for the keyword
  2. Locate PAA box on the results page
  3. Click each PAA question to expand it (reveals answer + new questions)
  4. After each click: wait 1-2 seconds, capture new questions that appear
  5. Keep clicking new questions until no new ones appear or 50+ captured
  6. Extract: question text, answer snippet, source URL for each
  7. Wait 5-8 seconds between seed searches
- **Fallback path (`--no-browser`):**
  - Use WebSearch, parse any PAA data from results (limited)

Output JSON:
```json
{"seeds_processed": 10, "total_questions": 234, "questions": [{"question": "How do I create an invoice?", "answer_snippet": "To create an invoice...", "source_url": "https://...", "source_seed": "invoicing software"}, ...], "method": "playwright|fallback"}
```

- [ ] **Step 11: Write `scripts/scrape-related-searches.py`**

Takes seed keywords (via `--seeds` comma-separated):
- **Browser path (primary):**
  1. For each seed: search Google, scroll to bottom of SERP
  2. Extract all Related Searches from the bottom section
  3. Click each related search (level 2): scroll to bottom, extract its related searches
  4. Deduplicate across levels
  5. Wait 3-5 seconds between navigations
- **Fallback path (`--no-browser`):**
  - Use WebSearch, extract any related search data from results

Output JSON:
```json
{"seeds_processed": 10, "total_related": 180, "related": [{"keyword": "billing software small business", "level": 1, "source_seed": "invoicing software"}, {"keyword": "free billing software no subscription", "level": 2, "source_seed": "invoicing software", "parent": "billing software small business"}, ...], "method": "playwright|fallback"}
```

- [ ] **Step 12: Write `scripts/analyze-serp-live.py`**

The flagship script. Takes a keyword (via `--keyword`) or keyword list (via `--keywords` file):
- **Browser path (primary):**
  1. Search keyword on Google via Playwright
  2. Wait for full SERP load
  3. Extract organic results: position, title, URL, description, displayed URL
  4. Detect SERP features: AI Overview (present/absent, source count), Featured Snippet (type: paragraph/list/table), PAA (present/absent, question count), Knowledge Panel, Video carousel, Local pack, Sitelinks, Image pack, Shopping results
  5. Record feature positions relative to organic results
  6. Take screenshot of full SERP
  7. For each organic result: classify content type (blog, product page, comparison, tool, docs) from URL/title patterns
  8. Determine search intent from SERP composition
  9. Flag as AI-answerable if AI Overview is present
- **Fallback path (`--no-browser`):**
  - Use WebSearch for organic results. Cannot detect SERP features, AI Overview, or take screenshots. Note limitations in output.

Output JSON:
```json
{"keyword": "invoicing software", "method": "playwright|fallback", "organic_results": [{"position": 1, "title": "...", "url": "...", "description": "...", "content_type": "product_page"}, ...], "serp_features": {"ai_overview": {"present": true, "source_count": 3}, "featured_snippet": {"present": false}, "paa": {"present": true, "question_count": 4}, "knowledge_panel": {"present": false}, "video_carousel": {"present": true}, "local_pack": {"present": false}}, "intent_classification": "commercial", "ai_answerable": true, "screenshot_path": "serp-invoicing-software-2026-03-27.png"}
```

- [ ] **Step 13: Write `scripts/competitor-gap-analysis.py`**

Takes user domain (via `--domain`) and competitor domains (via `--competitors` comma-separated):
- **Free path:**
  1. For each competitor: WebSearch `site:competitor.com` to estimate total indexed pages
  2. For each competitor: WebSearch `site:competitor.com [seed keyword]` to find their relevant pages
  3. Catalog competitor pages by topic/keyword
  4. Compare against user's pages (WebSearch `site:userdomain.com`)
  5. Identify gaps: topics competitors cover that user doesn't
- **Paid path (DataForSEO/Ahrefs):**
  - Call keyword gap API for comprehensive data
  - Get exact keywords, volumes, positions per domain
  - "Missing" and "Weak" keyword lists

Output JSON:
```json
{"user_domain": "...", "competitors": ["...", "..."], "method": "websearch|dataforseo|ahrefs", "gaps": [{"keyword": "NPS survey template", "competitor_ranking": "jotform.com", "competitor_position": 3, "user_position": null, "volume_estimate": "medium", "opportunity": "high"}], "total_gaps": 47, "top_opportunities": [...]}
```

- [ ] **Step 14: Write `scripts/scrape-community-keywords.py`**

Takes topic (via `--topic`) and platforms (via `--platforms` comma-separated, default: reddit,hn):
- **Browser path (primary):**
  1. For Reddit: navigate to reddit.com/search, search for topic, extract post titles and popular comments (top 50 results)
  2. For HN: navigate to hn.algolia.com, search for topic, extract story titles and top comments
  3. For each platform: extract unique phrases, questions, pain point language
  4. NLP-light keyword extraction: identify 2-4 word phrases that appear repeatedly, extract question patterns
- **Fallback path (`--no-browser`):**
  - WebSearch `site:reddit.com [topic]`, `site:news.ycombinator.com [topic]`
  - Parse titles and snippets from search results

Output JSON:
```json
{"topic": "invoicing software", "platforms_scraped": ["reddit", "hn"], "method": "playwright|fallback", "keywords": [{"phrase": "automatic payment reminder", "frequency": 8, "source": "reddit", "context": "I need a way to automatically send payment reminders", "suggested_keyword": "automatic payment reminder software"}, ...], "total_extracted": 67, "question_patterns": ["How do I [verb] [topic]?", "Is there a [tool] that [feature]?", "What's the best [category] for [use case]?"]}
```

- [ ] **Step 15: Write `scripts/probe-ai-discovery.py`**

The GEO differentiator. Takes queries (via `--queries` file, one per line) and optionally brand name (via `--brand`):
- For each query: check what AI platforms say:
  1. Perplexity: WebFetch `https://www.perplexity.ai/search?q={query}` — extract citations, sources, brands mentioned
  2. WebSearch for cached AI answers: `{query} site:perplexity.ai`, `{query} AI answer`
  3. If brand provided: check if brand appears in any AI response
- Record per query: which brands cited, which sources used, what topics covered, quality of cited sources (strong/medium/weak)
- Identify **GEO gaps:** queries where AI answers but cites few/weak sources = opportunity
- Identify **GEO-validated topics:** topics that AI platforms actively discuss

Output JSON:
```json
{"queries_tested": 20, "brand": "AcmeInvoice", "results": [{"query": "best invoicing software for freelancers", "ai_answers": true, "brands_cited": ["FreshBooks", "Wave", "Zoho"], "user_brand_cited": false, "sources": [{"url": "...", "quality": "medium"}, ...], "gap_opportunity": "high", "topic": "invoicing for freelancers"}], "summary": {"brand_citation_rate": 0.05, "high_gap_queries": 8, "geo_validated_topics": ["freelancer invoicing", "recurring billing", "payment reminders"]}}
```

- [ ] **Step 16: Write `scripts/evaluate-keywords.py`**

Takes raw keyword list (via `--keywords` file, one per line):
- For each keyword:
  1. Estimate volume: if DataForSEO available, use keyword data API. Otherwise, use SERP result count as proxy (WebSearch, count total results).
  2. Estimate KD: if paid tool available, use it. Otherwise, WebSearch the keyword, count high-authority domains in top 10 as proxy.
  3. Add GEO score: if `probe-ai-discovery.py` output available (via `--geo-data` file), merge. Otherwise, mark as "unscored."
  4. Apply filters: remove KD > threshold (configurable via `--max-kd`), remove volume < threshold (via `--min-volume`), flag duplicates
- Output the filtered, enriched spreadsheet format

Output JSON:
```json
{"total_input": 500, "total_after_filter": 187, "keywords": [{"keyword": "invoice generator free", "volume_estimate": 2400, "kd_estimate": 18, "intent": "transactional", "geo_score": 3, "source": "tool_expansion", "priority_score": null}], "filters_applied": {"max_kd": 50, "min_volume": 0, "duplicates_removed": 34, "irrelevant_removed": 0}}
```

- [ ] **Step 17: Write `scripts/classify-intent-live.py`**

Takes keyword list (via `--keywords` file, one per line):
- **Browser path (primary):**
  1. For each keyword: search Google via Playwright
  2. Analyze SERP composition:
     - What content types rank? (blog, product, comparison, tool, docs)
     - What SERP features appear? (AI Overview, Featured Snippet, PAA, Knowledge Panel)
     - Are there Shopping results? (strong transactional signal)
     - Are there video results? (informational signal)
  3. Classify intent based on SERP majority: informational, navigational, commercial, transactional
  4. Flag AI-answerable if AI Overview present
  5. Wait 5-8 seconds between searches
- **Fallback path (`--no-browser`):**
  - Use WebSearch, analyze result titles/URLs for content type patterns
  - Cannot detect SERP features or AI Overview. Note limitation.

Output JSON:
```json
{"total_classified": 120, "method": "playwright|fallback", "classifications": [{"keyword": "best invoicing software", "intent": "commercial", "confidence": 0.9, "ai_answerable": true, "ai_overview_present": true, "serp_features": ["paa", "ai_overview"], "dominant_content_type": "comparison", "recommended_page_type": "comparison page"}, ...], "intent_distribution": {"informational": 45, "commercial": 38, "transactional": 28, "navigational": 9}}
```

- [ ] **Step 18: Write `scripts/build-topic-clusters.py`**

Takes evaluated keyword list (via `--keywords` file, JSON format from `evaluate-keywords.py`):
- Pure local processing (no external tools needed):
  1. Group keywords by semantic similarity:
     - Extract root topic from each keyword (remove modifiers like "best", "free", "how to")
     - Group keywords sharing the same root topic
     - Merge near-duplicate groups
  2. For each group: identify pillar candidate (highest volume, broadest scope)
  3. Assign remaining keywords as supporting topics or H2 sections
  4. Apply the "own page" test: distinct intent? Deep enough for 800+ words? SERP shows standalone pages?
  5. Generate internal link topology: every support → pillar, pillar → every support, support ↔ related support
  6. **GEO citation mapping:** within each cluster, rank supporting topics by GEO score. Highest GEO-score topics should be created first (they'll be cited by AI sooner).

Output JSON:
```json
{"total_clusters": 8, "total_keywords_assigned": 187, "clusters": [{"name": "Online Invoicing", "pillar": {"keyword": "online invoicing", "volume": 5400, "kd": 45, "geo_score": 2}, "supports": [{"keyword": "how to create an invoice", "volume": 6600, "kd": 35, "geo_score": 3, "page_type": "guide", "geo_priority": 1}, ...], "internal_links": {"pillar_to_supports": true, "supports_to_pillar": true, "cross_links": [["support_1", "support_3"]]}}], "unassigned_keywords": 12}
```

- [ ] **Step 19: Write `scripts/prioritize-opportunities.py`**

Takes clustered keyword data (via `--clusters` file, JSON from `build-topic-clusters.py`):
- For each keyword/page in the plan:
  1. Score Business Value (1-3): direct product → 3, indirect → 2, tangential → 1 (user provides business context via `--business-keywords` or interactive prompt)
  2. Score Ranking Feasibility (1-3): KD <20 → 3, KD 20-40 → 2, KD 40+ → 1
  3. Score Traffic Potential (1-3): volume >1000 → 3, 200-1000 → 2, <200 → 1
  4. Score GEO Opportunity (1-3): from GEO score data
  5. Total = sum (max 12)
  6. Assign tier: 10-12 golden, 7-9 strong, 4-6 moderate, 1-3 skip
- Generate content calendar:
  - Month 1: top-tier keywords (golden), pillar pages first
  - Month 2: supporting pages + internal links
  - Month 3: optimize Month 1 content with GSC data
  - Ongoing: 2-4 pages/month

Output JSON:
```json
{"total_opportunities": 187, "content_plan": [{"priority": 1, "keyword": "Typeform alternative", "volume": 2200, "kd": 22, "intent": "commercial", "geo_score": 3, "total_score": 11, "tier": "golden", "page_type": "comparison", "target_url": "/compare/typeform-alternative", "cluster": "Alternatives", "publish_by": "Month 1 Week 1"}, ...], "tier_distribution": {"golden": 12, "strong": 34, "moderate": 67, "skip": 74}, "monthly_plan": {"month_1": [...], "month_2": [...], "month_3": [...]}}
```

- [ ] **Step 20: Write `scripts/find-quick-wins.py`**

Takes domain (via `--domain`):
- **If GSC API available:**
  1. Pull queries for last 3 months
  2. Striking distance: filter positions 8-20, sort by impressions descending. These are close to page 1.
  3. High impressions, low CTR: filter CTR <3%, sort by impressions descending. Title/description needs work.
  4. Variant keywords: find queries ranking for pages that weren't targeting them. Check if variant has higher volume.
  5. For each quick win: identify the ranking page, recommend action
- **Fallback (no GSC):**
  1. WebSearch `site:domain.com` for various seed keywords
  2. Identify which pages exist and roughly where they rank
  3. Note limitations: no impression/CTR data without GSC
- **GEO quick wins:** For top-ranking keywords, run `probe-ai-discovery.py` to check if the ranking page is also cited by AI. If not → opportunity to optimize for GEO using on-page-sgeo and content-sgeo.

Output JSON:
```json
{"domain": "...", "method": "gsc_api|websearch", "quick_wins": {"striking_distance": [{"keyword": "invoice payment terms", "position": 12, "impressions": 3400, "page": "/blog/payment-terms", "action": "Improve content depth, add internal links, optimize title"}], "low_ctr": [{"keyword": "free invoice generator", "position": 5, "impressions": 8900, "ctr": 0.018, "page": "/tools/generator", "action": "Rewrite title and meta description for higher CTR"}], "variant_keywords": [{"keyword": "recurring invoice template", "position": 9, "impressions": 2100, "current_target": "invoice templates", "action": "Consider dedicated page or optimize existing page for this variant"}], "geo_gaps": [{"keyword": "best invoicing software freelancers", "position": 4, "ai_cited": false, "action": "Apply on-page-sgeo optimization for AI citation"}]}, "total_quick_wins": 23}
```

### Commit

- [ ] **Step 21: Commit all files**

```bash
git add skills/discovery-gseo/
git commit -m "feat(discovery-gseo): add upstream discovery skill for SGEO pipeline

Create discovery-gseo — the most critical skill in the SGEO series. Covers the
complete 10-phase keyword discovery process with GEO-aware evaluation throughout.

Key features:
- Browser-first automation via Playwright MCP for live SERP data extraction
- 12 Python scripts: Autocomplete harvesting, PAA expansion, Related Searches
  chaining, live SERP analysis, competitor gap analysis, community scraping,
  AI visibility probing, keyword evaluation, intent classification, topic
  clustering, 4-dimension prioritization (max 12), and quick win identification
- 6 reference files: seed generation, keyword expansion, competitor intelligence,
  community listening, evaluation/scoring, and browser automation guide
- GEO integration throughout: AI citation potential as a discovery dimension,
  AI platform probing for seed validation, GEO opportunity in prioritization
- All scripts work with free tools (WebFetch/WebSearch) as fallback when
  browser automation is unavailable"
```

---

## Task 2: Validation

**Depends on:** Task 1 complete.

- [ ] **Step 1: Verify all files exist**

```bash
echo "=== discovery-gseo ===" && find skills/discovery-gseo -type f | wc -l
# Expected: 19 (1 SKILL.md + 6 references + 12 scripts)
```

- [ ] **Step 2: Verify Python script conventions**

```bash
head -1 skills/discovery-gseo/scripts/*.py | grep -c "#!/usr/bin/env python3"
# Expected: 12

grep -l "argparse" skills/discovery-gseo/scripts/*.py | wc -l
# Expected: 12

grep -l "\-\-no-browser\|no.browser" skills/discovery-gseo/scripts/*.py | wc -l
# Expected: at least 6 (browser-first scripts)
```

- [ ] **Step 3: Verify SKILL.md structure**

```bash
grep "## Tool discovery" skills/discovery-gseo/SKILL.md
grep "## Phase 1" skills/discovery-gseo/SKILL.md
grep "## Phase 10" skills/discovery-gseo/SKILL.md
grep "## Available scripts" skills/discovery-gseo/SKILL.md
grep "## Quality checklist" skills/discovery-gseo/SKILL.md
grep "## Common mistakes" skills/discovery-gseo/SKILL.md
# All 6 should match
```

- [ ] **Step 4: Verify cross-references**

Check that `worksWellWithSkills` includes all 4 existing SGEO skills.
Check that `worksWellWithAgents` points to valid agent slugs.

- [ ] **Step 5: Final commit if any fixes needed**

```bash
git add skills/discovery-gseo/
git commit -m "chore: validate discovery-gseo — all 19 files verified"
```
