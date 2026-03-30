---
name: discovery-gseo
description: >
  Find, evaluate, and prioritize keyword and content opportunities for both
  search engine ranking and AI platform citation — using live browser automation,
  SERP analysis, competitor intelligence, community listening, and GEO-aware
  scoring to produce a prioritized content plan that drives traffic and AI visibility.
metadata:
  displayName: "Discovery GSEO"
  categories: ["business", "operations"]
  tags: ["SEO", "GEO", "GSEO", "keyword-research", "discovery", "competitor-analysis",
         "SERP-analysis", "content-planning", "Playwright", "browser-automation"]
  worksWellWithAgents: ["content-strategist", "growth-engineer", "marketing-strategist", "product-marketing-manager", "seo-specialist"]
  worksWellWithSkills: ["content-sgeo", "off-page-sgeo", "on-page-sgeo", "technical-sgeo"]
---

# Discovery GSEO

Discovery GSEO is the upstream layer that determines *what* to build before the execution skills take over. Without good discovery, all downstream SEO and GEO effort is wasted — targeting the wrong keywords, creating content for topics nobody searches for, missing opportunities competitors are already winning.

This is skill 0 of 5 in the SGEO series: **discovery-gseo** > technical-sgeo > on-page-sgeo > content-sgeo > off-page-sgeo.

The output of this skill is a **prioritized content plan** — keywords mapped to pages, scored on 4 dimensions (including GEO opportunity), ordered by impact. Everything else in the SGEO pipeline flows from this plan.

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What is your business/product?** (Product category, target market, value proposition)
2. **What is your site URL?** (Existing site for quick win analysis, or "new site" if starting from scratch)
3. **Who are your known competitors?** (3-5 domains — business competitors AND SEO competitors)
4. **What is your current SEO status?** (Brand new / some content / established — determines whether Phase 10 is applicable)
5. **Do you have Google Search Console access?** (Critical for Phase 10 quick wins)
6. **What is the target country/region?** (For localized SERP analysis and volume data)
7. **What is your budget for tools?** (None / small / moderate / significant — determines which paid tool paths are available)
8. **How important is AI visibility?** (Determines weight of GEO scoring in prioritization — low / medium / high)

If the user says "I just want to find keywords," push back: "Keywords without intent classification, competitor validation, and prioritization scoring produce a random list, not a strategy. Which phase do you want to start from?"

## Tool discovery

Before gathering project details, confirm which tools are available. Ask the user directly — do not assume access to any external service.

**Browser automation (primary for this skill):**
- [ ] Playwright MCP (live SERP interaction, Autocomplete harvesting, PAA expansion, screenshots)
- [ ] Chrome DevTools MCP (alternative browser control, performance analysis)

**Free tools (no API key required):**
- [ ] WebFetch (fetch any public URL)
- [ ] WebSearch (search engine queries)
- [ ] Google PageSpeed Insights API (CWV data, no key needed for basic usage)
- [ ] Google Rich Results Test (structured data validation)

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

## Phase 1: Generate seed keywords

> **Scripts:** Run `scripts/probe-ai-discovery.py --queries queries.txt` to validate seeds against AI visibility. Add your seed queries (e.g., "What are the best [category] tools?") to `queries.txt`, one per line.
> **References:** See `references/seed-generation.md` for the 5-source mental model and GEO seed validation methodology.

Seed keywords are your starting points. They are the obvious, broad terms that describe your product, service, or topic. You do not need tools for this — just structured thinking.

**Ask yourself these 5 questions and write down every answer:**

1. **"What do I sell or offer?"** — Product category, service type, problem solved. If you sell invoicing software: "invoicing software", "invoice generator", "billing software."
2. **"What problem does my product solve?"** — Pain points. "How to manage invoices", "track payments", "send payment reminders."
3. **"How would a stranger describe what I do?"** — Plain language, no jargon. A CI/CD platform user might search "automate code deployment", not your product name.
4. **"What alternatives or competitors exist?"** — "[Competitor] alternative", "[Competitor A] vs [Competitor B]", "[category] comparison."
5. **"What technologies, methods, or concepts are relevant?"** — Integrations, workflows, adjacent technologies.

**Target:** 15-30 seeds, 1-4 words each. Do not worry about volume or competition yet.

**Example seed list (invoicing SaaS):**
```
invoicing software, invoice generator, online invoicing, billing software,
send invoices online, freelancer invoice tool, invoice template, recurring billing,
payment reminder, invoice tracking, accounting software, [CompetitorA] alternative,
[CompetitorB] vs [CompetitorC], small business invoicing, automated invoicing
```

**GEO seed layer — the discovery step that separates this from traditional keyword research:**

Probe AI platforms with broad questions about your space before relying solely on search data:

- Ask ChatGPT: "What are the best tools for [category]?", "How do I [problem]?"
- Ask Perplexity: same queries — different citation sources reveal different market landscape
- Ask Gemini: same queries — yet another AI perspective

Record which brands AI mentions, which topics it covers, and what language it uses. These are GEO-validated seeds — AI already discusses them, so content targeting these topics has citation potential from day one.

Run `scripts/probe-ai-discovery.py --queries queries.txt` to automate this GEO validation. Keywords that appear in AI responses get a GEO-validated flag in your seed list.

**Output:** Seed keyword list with GEO validation flags (15-30 seeds).

## Phase 2: Expand keyword universe

> **Scripts:** Run `scripts/harvest-autocomplete.py --seeds 'seed1,seed2,seed3'` to harvest Google Autocomplete suggestions via live browser. Run `scripts/extract-paa.py --seeds 'seed1,seed2'` to expand People Also Ask boxes.
> **References:** See `references/keyword-expansion.md` for tool-by-tool guides and browser automation expansion techniques.

Take each seed and expand it using keyword research tools. The goal is to go from 15-30 seeds to 200-1000+ raw keyword ideas.

**Google Keyword Planner (free, volume ranges):**
1. Google Ads > Tools > Keyword Planner > "Discover new keywords."
2. Enter one seed at a time. Set target country.
3. Download results as CSV. Repeat for each seed.
4. Limitation: shows volume ranges (1K-10K), not exact numbers. Ad competition metric, not organic KD.

**Paid tools (brief — see reference for full walkthrough):**
- Ahrefs Keywords Explorer: Matching terms, Related terms, Questions, Also rank for.
- Semrush Keyword Magic Tool: 20B+ keyword database, long-tail discovery, auto-grouping.
- Ubersuggest: keyword ideas, questions, related terms. Lifetime deal (~$120) is strong value.

**Browser-automated expansion (primary for this skill):**

Run `scripts/harvest-autocomplete.py --seeds 'invoicing software,billing software,invoice generator'` — this types each seed into Google with a-z letter suffixes and question prefixes (how/what/why/best), capturing every Autocomplete suggestion. This is data that WebSearch cannot replicate — real-time, localized, intent-rich suggestions.

Run `scripts/extract-paa.py --seeds 'invoicing software,billing software'` — searches Google for each seed, then click-expands every People Also Ask question, capturing 20-50+ questions per seed with answer snippets and source URLs.

**GEO expansion step:** Review your expanded list. Flag any keywords that match topics mentioned by AI platforms in Phase 1. These keywords have dual value — organic search traffic plus AI citation potential.

**Output:** Raw spreadsheet with 200-1000+ keyword ideas, each with at least a volume estimate.

## Phase 3: Spy on competitors

> **Scripts:** Run `scripts/competitor-gap-analysis.py --domain yourdomain.com --competitors comp1.com,comp2.com`. Run `scripts/probe-ai-discovery.py` with competitor-relevant queries for GEO gap analysis.
> **References:** See `references/competitor-intelligence.md` for gap analysis methodology and GEO competitor analysis.

Competitor analysis is the single highest-ROI activity in the discovery process. Other websites have done the research for you.

**Step 1: Identify SEO competitors.**
Search Google for 5-10 of your seed keywords. Note which domains appear repeatedly in the top 10. These are your SEO competitors — even if they sell different products. Pick 3-5, mixing direct product competitors and content competitors (blogs, review sites, aggregators).

**Step 2: Keyword gap analysis.**
Find keywords competitors rank for that you do not.
- Ahrefs: Competitive Analysis > Content Gap. Enter your domain + 3-5 competitors. Export "Missing" keywords.
- Semrush: Keyword Gap tool. Compare up to 5 domains. "Missing" tab + "Weak" tab.
- Free approximation: `scripts/competitor-gap-analysis.py` uses WebSearch `site:competitor.com` to catalog their pages and compares against your sitemap.

**Step 3: Analyze why competitors rank.**
For the most interesting gap keywords, visit the ranking pages. Ask: what type of page is it? How deep is the content? What angle do they take? What is weak or outdated? Your goal is to understand the format Google rewards, then create something better.

**Step 4: Top pages analysis.**
Use Ahrefs Site Explorer > Top Pages or Semrush > Organic Research > Pages to find which competitor pages drive the most traffic. Export and add the most relevant keywords.

**GEO competitor analysis:**
For your target queries, check which competitors get cited by AI platforms. Run `scripts/probe-ai-discovery.py --queries target-queries.txt --brand YourBrand`. Compare: who does AI cite? What do their cited pages look like — structure, data density, author attribution? Where are the gaps — queries where AI cites weak or outdated sources you can replace?

**Output:** Gap keywords added to master spreadsheet + GEO citation gap analysis.

## Phase 4: Mine Google for free ideas

> **Scripts:** Run `scripts/harvest-autocomplete.py`, `scripts/extract-paa.py --seeds 'seed1,seed2'`, and `scripts/scrape-related-searches.py --seeds 'seed1,seed2'`.
> **References:** See `references/browser-automation-guide.md` for Playwright technique details — the exact tool calls for Autocomplete extraction, PAA expansion, and Related Searches chaining.

Google reveals what people search for through dynamic SERP features. Browser automation extracts this data systematically.

**Technique 1: Autocomplete harvesting.**
Type seeds + a-z suffixes, question prefixes (how/what/why/best). Run `scripts/harvest-autocomplete.py` — this uses Playwright to interact with live Google Autocomplete, capturing real-time localized suggestions.

**Technique 2: PAA expansion.**
Search each seed, click-expand all PAA boxes. Each click reveals 2-3 new questions. Run `scripts/extract-paa.py` to capture 20-50+ questions per seed with answer snippets and source URLs. Each question is a potential H2 heading or standalone article.

**Technique 3: Related Searches chaining.**
Scroll to the bottom of Google SERPs, extract Related Searches, click each for 2nd-level expansion. Run `scripts/scrape-related-searches.py` for 2-level deep chaining. This uncovers lateral keyword ideas that tools miss.

**Technique 4: AnswerThePublic.**
3 free searches per day at answerthepublic.com. Enter your broadest seed keywords. Export the questions, prepositions, and comparisons data.

**Technique 5: GSC mining (existing sites only).**
GSC > Performance > Queries tab. Sort by impressions descending. Find keywords with high impressions but low CTR (title/description needs improvement) and keywords at positions 8-20 (striking distance to page 1).

**Output:** Question-based and long-tail keywords added to master spreadsheet.

## Phase 5: Listen to communities

> **Scripts:** Run `scripts/scrape-community-keywords.py --topic 'your category' --platforms reddit,hn` to extract keyword candidates from community discussions.
> **References:** See `references/community-listening.md` for platform-by-platform guide and language pattern extraction methodology.

Keyword tools rely on historical search data. Communities show you what people are asking right now, in their own language, before tools catch up.

**Where to look:**
- **Reddit:** Search for your category in relevant subreddits. Read titles and comments of popular posts. Watch for repeated questions, complaints about tools, comparison language.
- **Hacker News:** Search hn.algolia.com for your category. Read "Ask HN" threads for tool recommendations.
- **Twitter/X:** Search for your category, competitor names, problem descriptions.
- **Quora:** Questions mirror Google searches directly. Search your topic.
- **Product Hunt:** Similar products — read comments for needs, comparisons, frustrations.
- **Industry forums/Discord/Slack:** Niche communities where your customers congregate.

**What to capture — language patterns, not keyword data:**
Turn observations into keyword candidates:
- "I need a way to automatically send payment reminders" → "automatic payment reminder software"
- "Is there a Stripe alternative that handles invoicing too?" → "Stripe alternative with invoicing"
- "How do I set up recurring billing without a developer?" → "recurring billing no code"

Community-sourced keywords often show zero volume in tools because the volume is too low to register. Do not ignore them — low volume with perfect intent can be more valuable than high volume with vague intent.

**GEO dimension:** Community language maps directly to AI query language. The questions people ask on Reddit are the same questions they ask ChatGPT. Pain points described in forums are the same problems people describe to AI assistants. Community-sourced keywords have dual value: organic search traffic AND AI citation opportunity.

**Output:** Community-sourced keyword candidates added to master spreadsheet.

## Phase 6: Evaluate and filter keywords

> **Scripts:** Run `scripts/evaluate-keywords.py --keywords raw-keywords.txt --max-kd 50` to enrich your keyword list with volume/KD estimates and GEO scores. Run `scripts/probe-ai-discovery.py` to assess AI citation potential for your keywords.
> **References:** See `references/evaluation-and-scoring.md` for volume/KD interpretation scales, GEO score methodology, and filtering rules.

You now have a large, messy spreadsheet with hundreds or thousands of keywords from all five sources. Time to evaluate and filter.

**The 3 SEO metrics for every keyword:**

- **Volume:** Monthly searches. 10,000+ = high/competitive. 1,000-10,000 = medium/sweet spot for mid-authority. 100-1,000 = low-medium/sweet spot for new sites. <100 = still valuable with strong intent. 0 = tools cannot measure but real people search it.
- **Keyword Difficulty (KD):** 0-100 scale. 0-20 = easy (new sites rank in weeks). 21-40 = medium (needs content + some backlinks). 41-60 = hard (needs strong authority). 61+ = very hard (dominated by major brands). Always verify by manually checking the SERP — KD is an estimate.
- **Search Intent:** Covered in depth in Phase 7.

**GEO score — the 4th metric unique to this skill:**
For each keyword, assess AI citation potential on a 1-3 scale:
- **3 = High opportunity:** AI answers this query and cites weak or few sources. You can create content that replaces those citations. This is the discovery equivalent of finding an easy-KD keyword.
- **2 = Moderate opportunity:** AI answers and cites strong, authoritative sources. Hard to displace existing citations but still worth targeting for AI visibility.
- **1 = Low opportunity:** AI does not answer this query or defers entirely to search. SEO-only value — still worth targeting for organic traffic.

Run `scripts/probe-ai-discovery.py --queries keywords-to-check.txt` to assess GEO scores. This is the backbone of GEO-aware discovery.

**Filtering rules:**
- Remove irrelevant keywords — if the searcher would never become your customer, cut it
- Remove branded competitor navigational terms (keep "alternative" and "vs" variants)
- Remove keywords above your KD threshold (KD >40-50 for new sites, adjust based on authority)
- Remove duplicates and near-duplicates (keep higher-volume version — Google understands synonyms)

**Spreadsheet structure after filtering:**

```
| Keyword | Volume | KD | Intent | GEO Score | Source | Priority | Target URL | Status |
```

**Output:** Filtered, enriched keyword spreadsheet with volume, KD, and GEO scores.

## Phase 7: Classify search intent

> **Scripts:** Run `scripts/classify-intent-live.py --keywords keywords.txt` to search each keyword via Playwright, analyze SERP composition, classify intent, and flag AI-answerable queries.
> **References:** See `references/evaluation-and-scoring.md` for the 4 intent types with signals, content types, and business value.

Search intent is the most important and most overlooked step. If you create the wrong content type for a keyword, you will not rank — regardless of content quality.

**The 4 intent types:**

- **Informational — "I want to learn."** Signals: "how to", "what is", "guide", "tutorial." Content: blog posts, guides, tutorials. Business value: top-of-funnel, builds authority.
- **Navigational — "I want a specific site."** Signals: brand names, "login", "pricing." Content: your own brand pages. Not worth targeting for other brands.
- **Commercial — "I'm comparing options."** Signals: "best", "vs", "review", "alternative." Content: comparison pages, reviews, "best of" lists. Business value: high — close to purchase decision.
- **Transactional — "I'm ready to act."** Signals: "buy", "free trial", "download", "pricing." Content: product pages, pricing pages, free tools. Business value: highest — direct conversion.

**The SERP test — how to determine intent with certainty:**
1. Open an incognito browser window.
2. Search for the keyword.
3. Look at the top 5-10 results.
4. Match the format: blog posts = informational. Product pages = transactional. Comparison articles = commercial.

Google has already figured out the intent. If every result for "invoice generator" is a free online tool, the intent is transactional. A blog post targeting that keyword will never rank.

Run `scripts/classify-intent-live.py` to automate this — it searches each keyword via Playwright, analyzes the SERP composition (content types, SERP features), and classifies intent programmatically.

**AI-answerable flag (GEO):**
Does Google show an AI Overview for this keyword? Does Perplexity give a direct answer? If yes, GEO optimization is critical for this keyword — optimizing for AI citation (via content-sgeo and on-page-sgeo) is not optional, it is required to capture visibility.

**Output:** Every keyword in your spreadsheet now has an intent classification and AI-answerable flag.

## Phase 8: Group into topic clusters

> **Scripts:** Run `scripts/build-topic-clusters.py --keywords evaluated-keywords.json` to group keywords by semantic similarity, identify pillars, and generate a cluster map.
> **References:** See `references/evaluation-and-scoring.md` for cluster architecture and the "own page" test.

Individual keywords are not a strategy. Group them into clusters that build topical authority.

**Cluster structure:**
- **Pillar page:** Comprehensive, long-form page covering a broad topic. Highest volume, broadest scope per cluster. Example: "The Complete Guide to Online Invoicing."
- **Supporting pages:** Shorter, specific pages covering subtopics in depth. Link back to the pillar. Examples: "How to Write a Professional Invoice", "Invoice Payment Terms Explained."
- **Internal links:** Every support links to the pillar. The pillar links to every support. This signals to Google that you are an authority on the topic.

**How to group:**
1. Identify natural themes in your keyword list.
2. Group keywords sharing the same root topic.
3. Per group: identify the head keyword (highest volume, broadest) — this is the pillar target.
4. Remaining keywords become supporting pages or H2 sections within the pillar.

**When does a keyword deserve its own page?**
- It has a distinct search intent from others in the group.
- The topic is deep enough for 800+ words of dedicated content.
- The SERP shows standalone pages ranking (not subsections of larger pages).
Otherwise, target it as an H2 section within a larger page.

**Example cluster (invoicing SaaS, with GEO scores):**

**Pillar: "Online Invoicing" (volume: 5,400, KD: 45, GEO: 2)**
- "How to Create a Professional Invoice" (vol: 6,600, KD: 35, GEO: 3) — guide [create first: highest GEO]
- "Invoice Payment Terms: Net 30, Net 60" (vol: 1,900, KD: 12, GEO: 2) — blog post
- "Recurring Invoice Software Comparison" (vol: 800, KD: 22, GEO: 3) — comparison [create second: high GEO]
- "Invoice Template Free Download" (vol: 3,200, KD: 28, GEO: 1) — free tool
- "FreshBooks vs Wave for Freelancers" (vol: 1,100, KD: 20, GEO: 2) — comparison

**GEO citation mapping:** Within each cluster, rank supporting topics by GEO score. Highest GEO-score topics are created first — they get cited by AI sooner, building AI visibility for the entire cluster.

**Output:** Keywords grouped into clusters with pillar/support assignments and GEO priority ordering.

## Phase 9: Prioritize and build content plan

> **Scripts:** Run `scripts/prioritize-opportunities.py --clusters clusters.json` to apply 4-dimension scoring and generate a tiered content plan with publishing schedule.
> **References:** See `references/evaluation-and-scoring.md` for the complete 4-dimension framework and tier definitions.

You have clusters, but you cannot create everything at once. Prioritize using 4 dimensions.

**4-dimension scoring framework (max 12 points):**

**Dimension 1 — Business Value (1-3):**
- 3 = Directly relates to your product. Searcher could become a paying customer. "[category] software", "[competitor] alternative."
- 2 = Indirectly related. Builds awareness with target audience. "How to [solve problem]."
- 1 = Tangentially related. Drives traffic but weak revenue connection.

**Dimension 2 — Ranking Feasibility (1-3):**
- 3 = KD under 20 AND you have relevant existing content or expertise.
- 2 = KD 20-40 OR requires building backlinks.
- 1 = KD 40+ OR dominated by major brands.

**Dimension 3 — Traffic Potential (1-3):**
- 3 = Volume over 1,000/month.
- 2 = Volume 200-1,000/month.
- 1 = Volume under 200/month.

**Dimension 4 — GEO Opportunity (1-3):**
- 3 = AI answers this query and cites weak/few sources you can replace. Fastest GEO win.
- 2 = AI answers but cites strong sources. Worth targeting for AI presence, harder to displace.
- 1 = AI does not answer this query. SEO-only value.

**Total = Business Value + Feasibility + Traffic + GEO Opportunity (max 12)**

**Tiers:**
- **10-12 = Golden.** Do these first. High business value, achievable difficulty, meaningful traffic, strong GEO opportunity.
- **7-9 = Strong.** Do these second. Solid opportunities requiring more effort.
- **4-6 = Moderate.** Do these eventually. Lower priority, still worth creating over time.
- **1-3 = Skip.** Not worth the effort right now.

**Example scoring (form builder SaaS):**

| Keyword | BV | RF | TP | GEO | Total | Tier |
|---------|----|----|----|----|-------|------|
| Typeform alternative | 3 | 2 | 3 | 3 | 11 | Golden |
| NPS survey template | 3 | 3 | 2 | 2 | 10 | Golden |
| form builder with payment | 3 | 3 | 1 | 3 | 10 | Golden |
| how to create online form | 2 | 2 | 3 | 3 | 10 | Golden |
| best online form builder | 3 | 1 | 2 | 2 | 8 | Strong |
| conditional logic form | 2 | 3 | 1 | 1 | 7 | Strong |

**Content calendar template:**

```
| Priority | Keyword | Volume | KD | Intent | GEO Score | Page Type | Target URL | Cluster | Publish By |
```

**Monthly cadence:**
- Month 1: 3-5 pages targeting golden-tier keywords. Pillar pages first, then highest-GEO supports.
- Month 2: 3-5 supporting pages. Internal linking between published pages.
- Month 3: Optimize Month 1 content with GSC data. Continue publishing supports.
- Ongoing: 2-4 new pages/month. Update existing content quarterly. Re-run discovery quarterly.

**Output:** Prioritized content plan with 4-dimension scores, tiers, page types, target URLs, clusters, and publishing schedule.

## Phase 10: Find quick wins in existing data

> **Scripts:** Run `scripts/find-quick-wins.py --domain yourdomain.com` to identify striking-distance keywords, low-CTR pages, variant keywords, and GEO citation gaps.
> **References:** See `references/evaluation-and-scoring.md` for quick win identification methodology.

This phase applies only to sites with existing traffic. If your site is brand new, skip this and return after 2-3 months of content publishing and GSC data collection.

Quick wins are the fastest path to more traffic — they optimize what is already partially working.

**Quick win type 1 — Striking distance (positions 8-20):**
GSC > Performance > Queries. Filter positions 8-20. Sort by impressions descending. These keywords are on the edge of page 1. You already rank — Google considers your content relevant. A small improvement pushes you onto page 1, where traffic increases dramatically.
Action: improve content depth for the ranking page, add internal links from other pages, optimize the title tag.

**Quick win type 2 — High impressions, low CTR:**
Filter for CTR below 2-3%, sort by impressions descending. Google shows your page, but people do not click. Your title or meta description is not compelling.
Action: rewrite title to be specific with a clear benefit. Rewrite meta description with active voice and value proposition. Check if a SERP feature pushes your result down.

**Quick win type 3 — Variant keywords:**
Check which keywords your pages rank for that you did not deliberately target. Sometimes a page ranks for a variant keyword with higher volume or better intent than the original target.
Action: shift primary target to the higher-value variant. At minimum, add a section covering the variant and include it in the title or an H2.

**GEO quick wins — keywords where you rank but AI does not cite you:**
For your top-ranking keywords, run `scripts/probe-ai-discovery.py` to check if AI platforms cite your pages. If you rank on page 1 but are not cited by AI, you have a GEO gap. Apply on-page-sgeo and content-sgeo to optimize content structure for AI citation — direct-answer formatting, data density, author attribution, structured data.

**Output:** Quick win list with specific actions per keyword, including GEO citation gaps.

## Available scripts

Run these scripts to automate discovery tasks. Each outputs JSON. Scripts marked with [browser] use Playwright MCP for live browser data. If Playwright is unavailable, they fall back to WebSearch/WebFetch with reduced output quality. All browser scripts accept `--no-browser` to force the fallback path.

| Script | What it does | Run it when |
|--------|-------------|-------------|
| `harvest-autocomplete.py` [browser] | Types seeds + a-z in Google, captures all Autocomplete suggestions | Phase 2: expanding keyword universe |
| `extract-paa.py` [browser] | Searches Google, expands PAA boxes, captures 20-50+ questions per seed | Phase 2, 4: expanding and mining keywords |
| `scrape-related-searches.py` [browser] | Extracts Related Searches, chains 2 levels deep | Phase 4: mining Google for free ideas |
| `analyze-serp-live.py` [browser] | Flagship: full SERP analysis with organic results, features, AI Overview, screenshot | Phase 7: SERP-based intent classification |
| `competitor-gap-analysis.py` | Compares user domain vs competitors for keyword gaps | Phase 3: competitor analysis |
| `scrape-community-keywords.py` [browser] | Searches Reddit/HN/forums, extracts question titles and pain point language | Phase 5: community listening |
| `probe-ai-discovery.py` | GEO backbone: tests queries on AI platforms, records citations, finds gaps | Phase 1, 3, 6, 10: GEO validation throughout |
| `evaluate-keywords.py` | Enriches raw keywords with volume/KD/GEO scores, filters noise | Phase 6: evaluation and filtering |
| `classify-intent-live.py` [browser] | Live SERP analysis: determines intent + AI-answerable flag per keyword | Phase 7: intent classification |
| `build-topic-clusters.py` | Groups keywords by similarity, identifies pillars, generates cluster map | Phase 8: topic clustering |
| `prioritize-opportunities.py` | 4-dimension scoring (max 12), outputs tiered content plan with schedule | Phase 9: prioritization |
| `find-quick-wins.py` | GSC striking distance + high-impression/low-CTR + GEO citation gaps | Phase 10: quick wins |

## Quality checklist

Before delivering the content plan, verify:

- [ ] All 10 phases completed (or consciously skipped with documented reason)
- [ ] Seed keywords validated against both search data AND AI platform probing
- [ ] Competitor gap analysis includes both SEO gaps and GEO citation gaps
- [ ] Every keyword has volume estimate, KD estimate, intent classification, and GEO score
- [ ] Intent classification verified via live SERP test (not just heuristic guessing)
- [ ] Keywords grouped into topic clusters with pillar/support assignments
- [ ] Content plan uses 4-dimension scoring (max 12) with GEO as a real dimension, not a token checkbox
- [ ] Quick wins identified (if existing site with GSC data)
- [ ] Output is a prioritized content plan, not a raw keyword list
- [ ] Plan feeds clearly into content-sgeo (what to write) and on-page-sgeo (how to optimize)

## Common mistakes to avoid

1. **Targeting keywords that are too broad.** "Software" is not a keyword — it is a category. "Invoice software for freelancers" is a keyword.
2. **Ignoring search intent.** If every SERP result is a blog post and you create a product page, you will not rank. Match the content type Google rewards.
3. **Obsessing over search volume.** A keyword with 50 monthly searches and perfect buyer intent can be worth more than a keyword with 10,000 searches and vague informational intent.
4. **Never checking the actual SERP.** Tools provide data. The SERP provides truth. Always manually search your most important target keywords.
5. **Targeting the same keyword with multiple pages (cannibalization).** Each keyword or keyword cluster maps to exactly one page. If two pages compete, Google may rank neither.
6. **Skipping competitor analysis.** This is the single highest-ROI activity. Other sites have validated which keywords drive traffic. Use their work.
7. **Creating content without a target keyword.** Every page needs a clear primary keyword. If you cannot identify one, the page lacks strategic purpose.
8. **Giving up too early.** SEO results take 3-6 months. Publish in January, check rankings in July. Not February.
9. **Only looking at your own data.** GSC shows keywords you already rank for. The biggest opportunities are keywords you have zero presence for — only competitor analysis and expansion tools reveal those.
10. **Doing keyword research once and never again.** Search behavior evolves. Competitors publish new content. New questions emerge. Re-run discovery quarterly.
11. **Ignoring GEO opportunity in prioritization.** A keyword where AI cites weak sources is a faster win than one where AI cites authoritative sources you cannot displace. GEO opportunity is a real competitive dimension, not a nice-to-have.
12. **Not validating seeds against AI platforms.** What AI recommends in your space is a leading indicator of search trends. If AI platforms discuss a topic, searchers are asking about it too — often before traditional keyword tools register the volume.
