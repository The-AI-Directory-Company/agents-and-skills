# SGEO Skills Suite: Internal Usage Guide

*How to use the five SGEO skills together as a unified pipeline for search and AI visibility. Internal distribution only.*

---

## What This Is

The SGEO (Search Generative Engine Optimization) suite is five skills that cover the entire lifecycle of getting found — in both traditional search engines and AI platforms. Each skill is self-contained but designed to feed into the next.

**The core insight:** SEO gets you ranked. GEO gets you cited. You need both. These skills treat them as one discipline, not two.

## The Pipeline

```
┌─────────────────┐
│  discovery-gseo  │  Find WHAT to target
│  12 scripts      │  Output: prioritized content plan with GEO scores
│  6 references    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  technical-sgeo  │  Ensure the site CAN be found
│  10 scripts      │  Output: verified technical foundation
│  5 references    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  content-sgeo    │  Create pages worth ranking AND quoting
│  7 scripts       │  Output: content calendar, published articles
│  5 references    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  on-page-sgeo    │  Optimize each page for ranking AND citation
│  8 scripts       │  Output: page-level audit, optimized elements
│  5 references    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  off-page-sgeo   │  Build authority across search AND AI
│  7 scripts       │  Output: backlinks, brand presence, AI citations
│  5 references    │
└────────┬────────┘
         │
         ▼
    ┌────────┐
    │ REPEAT │  Re-run discovery quarterly.
    │        │  Refresh content every 3-6 months.
    │        │  Track AI visibility monthly.
    └────────┘
```

## When to Use Which Skill

| Situation | Start here | Then |
|-----------|-----------|------|
| Brand new site, no content | discovery-gseo → technical-sgeo → content-sgeo → on-page-sgeo | off-page-sgeo once content exists |
| Existing site, never done SEO | technical-sgeo (fix foundations) → discovery-gseo (find opportunities) → content-sgeo | on-page-sgeo + off-page-sgeo in parallel |
| Have content, not ranking | discovery-gseo Phase 10 (quick wins) → on-page-sgeo (optimize existing) → content-sgeo (fill gaps) | off-page-sgeo for authority |
| Ranking but not cited by AI | on-page-sgeo (GEO formatting) → content-sgeo (GEO framework) → off-page-sgeo (multi-platform presence) | discovery-gseo to find GEO-specific gaps |
| Quarterly refresh | discovery-gseo Phases 3+5+10 → content-sgeo Step 7 (refresh) → on-page-sgeo (re-audit) | off-page-sgeo measurement |
| Single page optimization | on-page-sgeo only — run `audit-page.py` | content-sgeo `score-content-geo.py` for GEO scoring |

## Skill-by-Skill Usage

### 1. discovery-gseo — Find What to Target

**When:** Before creating any content. Quarterly for refreshes.

**What it does:** Takes your business context and produces a prioritized content plan — keywords mapped to pages, scored on 4 dimensions (Business Value, Ranking Feasibility, Traffic Potential, GEO Opportunity), organized into topic clusters.

**Key tool requirement:** Playwright MCP or Chrome DevTools MCP. This skill is browser-first — live SERP data extraction (Autocomplete, People Also Ask, Related Searches, SERP feature detection) requires a real browser. Falls back to WebSearch if unavailable, but output quality drops.

**The 10 phases in brief:**

| Phase | What you do | Key script | Time |
|-------|-------------|-----------|------|
| 1. Seeds | Brainstorm 15-30 starting keywords + validate against AI platforms | `probe-ai-discovery.py` | 30-60 min |
| 2. Expand | Feed seeds into tools, harvest Autocomplete + PAA | `harvest-autocomplete.py`, `extract-paa.py` | 1-3 hrs |
| 3. Competitors | Keyword gap analysis + check who AI cites | `competitor-gap-analysis.py`, `probe-ai-discovery.py` | 1-2 hrs |
| 4. Google mining | Autocomplete, PAA expansion, Related Searches chaining | `scrape-related-searches.py` | 30-60 min |
| 5. Communities | Extract keyword candidates from Reddit, HN, forums | `scrape-community-keywords.py` | 1-2 hrs |
| 6. Evaluate | Add volume, KD, GEO score; filter noise | `evaluate-keywords.py` | 2-3 hrs |
| 7. Classify intent | Live SERP test for each keyword, flag AI-answerable queries | `classify-intent-live.py`, `analyze-serp-live.py` | 1-2 hrs |
| 8. Cluster | Group keywords into pillar + support structure | `build-topic-clusters.py` | 1-2 hrs |
| 9. Prioritize | 4D scoring (max 12), tier into golden/strong/moderate/skip | `prioritize-opportunities.py` | 1-2 hrs |
| 10. Quick wins | GSC striking distance + GEO citation gaps | `find-quick-wins.py` | 1-2 hrs |

**What it produces:** A prioritized content plan that feeds directly into content-sgeo (what to write) and on-page-sgeo (how to optimize each page).

**The 4-dimension scoring system:**

| Dimension | 3 points | 2 points | 1 point |
|-----------|----------|----------|---------|
| Business Value | Direct product relevance | Indirect relevance | Tangential |
| Ranking Feasibility | KD <20 + expertise | KD 20-40 | KD 40+ |
| Traffic Potential | Volume >1,000/mo | 200-1,000/mo | <200/mo |
| GEO Opportunity | AI cites weak sources (replaceable) | AI cites strong sources | AI doesn't answer this query |

Scores 10-12 = golden opportunities (do first). 7-9 = strong. 4-6 = moderate. 1-3 = skip for now.

---

### 2. technical-sgeo — Ensure the Site Can Be Found

**When:** Before publishing content on a new site. After any migration or infrastructure change. Annually as a health check.

**What it does:** Verifies and fixes the technical foundation so that both search engine crawlers (Googlebot, Bingbot) and AI crawlers (GPTBot, ClaudeBot, PerplexityBot) can access, crawl, and index your pages.

**8 implementation areas:**

| Area | What to check | Key script |
|------|--------------|-----------|
| 1. Measurement | GSC, GA4, Bing Webmaster Tools, server logs | `inventory-tools.py` |
| 2. Search crawlability | robots.txt, XML sitemap, crawl budget, redirects, errors | `check-robots-txt.py`, `validate-sitemap.py`, `check-redirect-chains.py` |
| 3. AI crawlability | AI bot access in robots.txt, CDN/WAF blocking, SSR, content gating | `check-ai-crawler-access.py` |
| 4. Indexation | Canonicals, noindex, duplicates, GSC coverage | `check-indexation.py` |
| 5. Core Web Vitals | LCP <2.5s, INP <200ms, CLS <0.1 | `check-cwv.py` |
| 6. Mobile + HTTPS | Responsive design, viewport, tap targets, HSTS | `check-mobile.py`, `check-https-security.py` |
| 7. Structured data | JSON-LD per page type, Rich Results validation | `check-structured-data.py` |
| 8. Verification | Unified SEO + GEO checklist — all items must pass | — |

**The #1 thing people miss:** CDN bot-blocking. Cloudflare Bot Fight Mode and AWS WAF block AI crawlers by default. Run `check-ai-crawler-access.py` — if AI bots get 403s or empty responses, your content is invisible to every AI platform regardless of quality.

**What it produces:** A verified technical foundation. All crawlability barriers removed, Core Web Vitals passing, structured data validated, AI crawlers confirmed accessible. This is the prerequisite for everything else.

---

### 3. content-sgeo — Create Pages Worth Ranking and Quoting

**When:** After discovery (you know what to write) and technical (your site is crawlable). Ongoing as you publish.

**What it does:** Guides the creation of content that performs in both search engines and AI platforms. Covers keyword research refinement, intent matching, topic cluster architecture, the GEO Content Creation Framework, E-E-A-T signals, and content refresh strategy.

**The 8-element GEO Content Creation Framework:**

This is the core differentiator. For every piece of content:

| Element | What it means | Scoring (0-5) |
|---------|--------------|---------------|
| 1. TLDR first | First 150-200 words directly answer the primary question | 5 = complete answer, 0 = meandering intro |
| 2. Question-format headers | H2s mirror how people ask AI | 5 = >50% question H2s, 0 = generic headings |
| 3. Data-rich body | Specific statistics, percentages, dates with sources | 5 = >3 stats per 500 words, 0 = vague claims |
| 4. Self-contained sections | Each H2 is extractable on its own (50-150 words) | 5 = fully independent, 0 = depends on context |
| 5. Expert quotations | Named authority quotes with attribution | 5 = multiple named experts, 0 = none |
| 6. Source citations | Outbound links to studies, data, official sources | 5 = >5 citations, 0 = no sources |
| 7. Original value | Your own data, framework, case study, unique angle | 5 = proprietary data/framework, 0 = nothing original |
| 8. Author attribution | Byline, credentials, author page with bio | 5 = full author page, 0 = no author |

**Total: 0-40 points.** Run `score-content-geo.py --url <URL>` to score any page. This is the key feedback loop — score before and after optimization to measure improvement.

| Score | Rating | Meaning |
|-------|--------|---------|
| 0-10 | Not citable | AI will not cite this content |
| 11-20 | Partially citable | Some queries might trigger citation |
| 21-30 | Citation-ready | Good for most queries in your space |
| 31-40 | Excellent | High citation potential, competitive advantage |

**Content types ranked by SEO + GEO value:**

| Type | SEO | GEO | Priority |
|------|-----|-----|----------|
| Glossaries/definitions | Medium | Very High | Quick GEO wins |
| How-to tutorials | High | High | Core content |
| Comprehensive guides | High | High | Pillar content |
| Data-driven studies | Medium | Very High | Citation magnets |
| FAQ pages | Medium | High | GEO-structured |
| Comparison posts (X vs Y) | High | Medium | Commercial traffic |
| Case studies | Medium | High | E-E-A-T + citations |

**What it produces:** A content calendar with articles mapped to keywords, intent, and clusters. Published content scored on the GEO framework. Existing content flagged for refresh.

---

### 4. on-page-sgeo — Optimize Each Page for Ranking and Citation

**When:** After writing content (apply to each page). For existing pages that need optimization.

**What it does:** Optimizes 10 individual page elements so the page ranks in search AND gets cited by AI platforms. Every element is evaluated for both SEO impact and GEO impact.

**The quick audit:** Run `audit-page.py --url <URL> --format md` to get a complete on-page SGEO audit in one command. It runs all 7 other scripts and produces a table:

```
| Element                  | SEO Impact | GEO Impact | Status | Finding                        |
|--------------------------|------------|------------|--------|--------------------------------|
| Title tag                | High       | Medium     | PASS   | 52 chars, keyword present      |
| Meta description         | Medium     | Medium     | WARN   | 168 chars — over 155 limit     |
| Heading hierarchy        | Medium     | High       | PASS   | 1 H1, 8 H2s, 5 question-format|
| Direct-answer opening    | Low        | High       | FAIL   | Meandering intro, no answer    |
| Knowledge blocks         | Low        | High       | WARN   | 3 of 8 sections not standalone |
| Internal links           | High       | Medium     | PASS   | 4.2 per 1000 words            |
| Images                   | Medium     | Low        | WARN   | 2 images missing alt text      |
| Structured data          | Medium     | High       | FAIL   | No Article schema found        |
| Freshness signals        | Low        | High       | PASS   | Updated 2026-03-15, author set |
```

**The two GEO-specific techniques that matter most:**

**Direct-Answer-First (Section 4):** The first 200 words of any page must directly answer the primary question. No meandering introductions, no "In today's digital landscape..." openers. AI engines extract opening content — if your answer is in paragraph 5, you won't be cited. Run `check-direct-answer.py` to score this on a 0-8 rubric.

**Self-Contained Knowledge Blocks (Section 5):** Each H2 section should make sense if extracted on its own. AI engines pull individual passages, not whole pages. If a section starts with "As mentioned above..." it's useless when extracted. Make every section a standalone knowledge snippet.

**What it produces:** Per-page audit with SEO Impact, GEO Impact, and status for each of 10 elements. Specific fix recommendations per element.

---

### 5. off-page-sgeo — Build Authority Across Search and AI

**When:** Once you have content worth linking to. Ongoing as a long-term investment.

**What it does:** Builds the authority signals that sustain search rankings and AI citations: backlinks, brand mentions, multi-platform presence, digital PR, and community engagement.

**The key GEO insight:** AI engines cite sources beyond your website. If your brand only exists on your domain, you limit citation potential. Building presence on platforms AI engines frequently cite expands your citation surface area.

**The 7 platforms AI engines cite most (in order):**

| Platform | Why AI cites it | What to do |
|----------|----------------|-----------|
| Reddit | Authentic opinions, recommendations | Answer questions genuinely in relevant subreddits |
| YouTube | Transcripts indexed by AI | Create tutorials with keyword-rich spoken content |
| LinkedIn | Professional/business topics | Publish long-form articles (permanent URLs) |
| Wikipedia | Extremely high authority | Contribute to related topics (never edit own article) |
| GitHub | Developer products | Quality READMEs and documentation |
| Stack Overflow | Technical Q&A | Thorough answers explaining WHY, not just HOW |
| Industry publications | Authority backlinks + citation surface | Guest articles, quoted as expert source |

**Measurement — the `probe-ai-visibility.py` loop:**

Run monthly. Test 10-20 queries your audience would ask AI platforms. Record:
- Is your brand cited? (Y/N per platform per query)
- Which competitors are cited instead?
- What do cited sources have that you don't?

Track over time. AI citation improves slower than search ranking (6-12 months for meaningful change), but compounds powerfully once it starts.

**What it produces:** Backlink tracking, brand mention monitoring, multi-platform presence established, AI visibility baseline measured and tracked monthly.

---

## How the Skills Connect — Data Flow

```
discovery-gseo
│
├─ Output: Prioritized keyword list
│  ├─ keyword, volume, KD, intent, GEO score, cluster, priority tier
│  └─ Content plan: what pages to create, in what order
│
├─ Feeds into: content-sgeo
│  ├─ Input: keyword clusters, intent classifications, GEO priority ordering
│  ├─ Uses: topic cluster architecture, content type selection, GEO framework
│  └─ Output: articles written per the 8-element GEO framework
│
├─ Feeds into: on-page-sgeo
│  ├─ Input: page URL + target keyword from discovery/content plan
│  ├─ Uses: per-page audit across 10 elements
│  └─ Output: optimized pages ready for indexing and AI citation
│
├─ Feeds into: off-page-sgeo
│  ├─ Input: published, optimized content (linkable assets)
│  ├─ Uses: backlink strategy, brand building, multi-platform presence
│  └─ Output: authority signals that sustain rankings and citations
│
└─ Feeds into: technical-sgeo (runs in parallel with above)
   ├─ Input: site URL
   ├─ Uses: crawlability, indexation, CWV, structured data, AI access
   └─ Output: verified technical foundation (prerequisite for all above)
```

## Tool Requirements Across the Suite

### Minimum viable (free)

Every skill works with just these:
- **WebFetch** — Fetch any public URL
- **WebSearch** — Search engine queries

This covers ~60% of the functionality. Scripts fall back to these when paid tools are unavailable.

### Recommended additions (free)

- **Playwright MCP** or **Chrome DevTools MCP** — Required for discovery-gseo to reach full potential. Live SERP data extraction, Autocomplete harvesting, PAA expansion. Without browser automation, discovery output quality drops significantly.
- **Google Search Console API** — Required for quick win identification (Phase 10 of discovery, content refresh in content-sgeo).
- **Google PageSpeed Insights API** — Free, no key needed. Required for CWV checks in technical-sgeo.

### Optional paid tools

- **DataForSEO MCP** — SERP data, keyword metrics, backlink profiles, AI visibility endpoints. Best all-in-one for agents.
- **Ahrefs API** — Strongest backlink data and competitor gap analysis. Best if budget allows one premium tool.
- **Semrush API** — Largest keyword database (20B+ keywords). Best for keyword expansion volume.

### Tool Discovery flow

Every skill starts with a Tool Discovery section. The agent asks the user once what's available, records the inventory, and passes it to scripts. You don't need to repeat this between skills — carry the inventory forward.

## Typical Timelines

| Scenario | Discovery | Technical | Content | On-Page | Off-Page | First Results |
|----------|-----------|-----------|---------|---------|----------|---------------|
| New site, full process | Week 1 | Week 1-2 | Week 2-8 (ongoing) | Per page as published | Week 4+ (ongoing) | 3-6 months (SEO), 1-3 months (GEO) |
| Existing site, first SGEO pass | Week 1 | Week 1 | Week 2-4 | Week 2-4 | Week 3+ | 1-3 months (quick wins), 3-6 months (full) |
| Quarterly refresh | Half day | — (unless issues found) | 1-2 days (refresh existing) | Per refreshed page | Review measurement | Cumulative improvement |

## Measurement Cadence (Across All Skills)

| Frequency | What to do | Which skill |
|-----------|-----------|-------------|
| Weekly | Check keyword rankings, GSC for crawl errors, new backlinks | technical-sgeo, off-page-sgeo |
| Monthly | AI visibility probe (10-20 queries), content performance review, community monitoring | off-page-sgeo, content-sgeo, discovery-gseo |
| Quarterly | Re-run competitor gap analysis, refresh top content, full backlink audit, update content plan | discovery-gseo, content-sgeo, off-page-sgeo |
| Biannually | Full discovery re-run, technical re-audit, tool stack assessment | discovery-gseo, technical-sgeo |

## The GEO Thread

GEO is not a separate activity — it's a dimension woven through every skill:

| Skill | How GEO appears |
|-------|----------------|
| discovery-gseo | GEO score per keyword (1-3), 4th dimension in prioritization, AI platform probing for seed validation |
| technical-sgeo | AI crawler access verification, CDN bot-blocking checks, SSR for AI consumption |
| content-sgeo | 8-element GEO Content Creation Framework (0-40 scoring), content types ranked by GEO value |
| on-page-sgeo | Direct-answer-first pattern, self-contained knowledge blocks, question-format headings, per-section 0-8 GEO rubric |
| off-page-sgeo | Multi-platform presence on AI-cited platforms, AI visibility measurement, brand mention as entity signal |

## Quick Start Cheat Sheet

**"I have a new site and need to start from zero"**
1. Run discovery-gseo (all 10 phases) → produces content plan
2. Run technical-sgeo → fix foundations
3. Start content-sgeo → write your first 3-5 pages (golden tier from discovery)
4. Run on-page-sgeo on each page before publishing
5. Start off-page-sgeo once you have 5+ pages live

**"I have an existing site but no AI visibility"**
1. Run technical-sgeo `check-ai-crawler-access.py` → are AI bots blocked?
2. Run on-page-sgeo `audit-page.py` on your top 5 pages → check GEO elements
3. Run content-sgeo `score-content-geo.py` on those pages → get GEO scores
4. Fix: add direct-answer openings, question-format H2s, self-contained sections, data, citations
5. Run off-page-sgeo `audit-platform-presence.py` → build presence where missing

**"I just need to optimize one page"**
1. Run on-page-sgeo `audit-page.py --url <URL> --format md`
2. Fix every FAIL and WARN item
3. Run content-sgeo `score-content-geo.py --url <URL>` for GEO score
4. Target score 25+ (citation-ready)

**"I need to find new content opportunities"**
1. Run discovery-gseo Phases 3 (competitors) + 5 (communities) + 10 (quick wins)
2. Run `prioritize-opportunities.py` on the new keywords
3. Feed golden-tier opportunities into content-sgeo

---

*This guide covers the SGEO skill suite as of March 2026. The skills evolve — always read the SKILL.md for the latest procedures.*
