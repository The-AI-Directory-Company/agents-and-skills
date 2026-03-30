---
name: content-sgeo
description: Plan and create content that ranks in traditional search and gets cited by AI platforms — covering keyword research, search intent mapping, topic cluster architecture, the GEO content creation framework, content types, E-E-A-T signals, and content refresh strategy.
metadata:
  displayName: "Content SGEO Strategy"
  categories: ["communication", "business"]
  tags: ["SEO", "GEO", "SGEO", "content-strategy", "keyword-research", "search-intent", "topic-clusters", "E-E-A-T", "AI-citation"]
  worksWellWithAgents: ["content-strategist", "copywriter", "marketing-strategist", "seo-specialist"]
  worksWellWithSkills: ["content-calendar", "discovery-gseo", "off-page-sgeo", "on-page-sgeo", "technical-sgeo"]
---

# Content SGEO Strategy

## Before you start

Gather the following from the user before planning or creating any content:

1. **What should content achieve?** (Lead generation, signups, brand awareness, topical authority, investor credibility — pick a primary goal)
2. **Who is the target audience?** (Job titles, experience levels, industries. "Everyone" is not an audience.)
3. **What content already exists?** (Number of published pages, topics covered, current traffic levels. An audit URL or sitemap helps.)
4. **Who are the competitors?** (3-5 sites that rank for the same topics. Needed for gap analysis in Step 1.)
5. **Is Google Search Console connected?** (Existing query data accelerates keyword research and reveals quick wins at positions 4-15.)
6. **What resources are available?** (Who writes? How many pieces per month? Budget for tools like Ahrefs, Semrush, or Clearscope?)
7. **How important is AI citation?** (Some businesses prioritize appearing in ChatGPT, Perplexity, or Gemini answers. Others only care about Google rankings. This changes content structure.)
8. **What is the timeline?** (SEO compounds over 3-6 months. GEO citation can be faster but fluctuates. Set expectations early.)

If the user says "we need more content," push back: "More content without keyword research, intent mapping, and a cluster strategy creates noise. What specific business outcome should content drive in the next quarter?"

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

## Content SGEO procedure

### Step 1: Keyword Research

Run `scripts/research-keywords.py --seeds 'term1,term2,term3'` to expand seed keywords automatically. See `references/keyword-research.md` for the full methodology, tool-specific guidance, and difficulty interpretation.

Start with data, not guesses. Follow this sequence:

1. **Seed keywords.** List 5-10 terms directly related to the product or service. Use the language customers use, not internal jargon.
2. **Expand the list.** Run seeds through Google Keyword Planner, Ahrefs/Semrush keyword explorer, AnswerThePublic, Google Autocomplete, and "People Also Ask" boxes. Target 50-200 keywords.
3. **Capture metrics for each keyword:**
   - Search volume (monthly)
   - Keyword difficulty (0-100 scale)
   - CPC (indicates commercial value — high CPC = high buyer intent)
   - Current ranking position (from GSC or rank tracker)
4. **Prioritize low-competition, high-intent keywords first.** These produce the quickest wins. A keyword with 200 monthly searches and difficulty 15 is more valuable than one with 10,000 searches and difficulty 85 — especially for newer sites.
5. **Run a competitor gap analysis.** What keywords do competitors rank for that you do not? Tools: Ahrefs Content Gap, Semrush Keyword Gap. These reveal topics your audience already searches for but you have not addressed.

Output this table for every keyword cluster:

```
| Keyword                        | Volume | Difficulty | CPC   | Intent        | Current Pos. | Priority |
|--------------------------------|--------|-----------|-------|---------------|-------------|----------|
| how to automate invoice processing | 1,200  | 22        | $4.50 | Informational | Not ranking | High     |
| invoice automation software    | 880    | 45        | $12.80| Commercial    | Position 18 | High     |
| best invoice automation tools  | 720    | 38        | $9.20 | Commercial    | Not ranking | Medium   |
| invoice automation vs manual   | 320    | 12        | $3.10 | Commercial    | Not ranking | High     |
| what is invoice automation     | 1,600  | 18        | $2.40 | Informational | Position 32 | Medium   |
```

### Step 2: Search Intent Classification

Run `scripts/classify-intent.py` with your keyword list to classify intent via SERP analysis.

For every keyword, classify the intent. This determines what type of content to create.

- **Informational** — User wants to learn. Queries start with "how to," "what is," "why does," "guide to." Create guides, tutorials, explainers, and FAQ pages.
- **Navigational** — User wants a specific site or page. Queries include brand names ("Stripe dashboard," "Notion templates"). Ensure brand pages and key landing pages are optimized.
- **Commercial** — User is comparing or researching before a purchase. Queries include "best," "vs," "review," "alternative to." Create comparison posts, reviews, and roundups.
- **Transactional** — User wants to act now. Queries include "buy," "pricing," "signup," "free trial," "download." Create product pages, pricing pages, and signup flows.

**Critical rule: Match content type to intent.** A blog post will not rank for a transactional keyword. A product page will not rank for "how to" queries. If you mismatch, Google will not rank you regardless of content quality, and AI engines will not cite you because the content does not answer the actual question.

Verify intent by searching the keyword in Google and checking what currently ranks in positions 1-5. If the top results are all comparison posts, write a comparison post — not a tutorial.

### Step 3: Topic Cluster Architecture

Run `scripts/plan-topic-cluster.py --topic 'your pillar topic'` to discover subtopics and generate cluster structure. See `references/topic-clusters.md` for worked examples across SaaS, e-commerce, and professional services.

Isolated articles do not build authority. Organize content into topic clusters to signal depth to both search engines and AI systems.

**Structure:**

- One **pillar page** per core topic (comprehensive guide, 2,000-4,000 words)
- 5-10 **supporting articles** per pillar (deep dives on subtopics, 800-2,000 words each)
- Every supporting article links back to the pillar page
- The pillar page links out to every supporting article
- Supporting articles interlink where relevant

```
[Pillar: Complete Guide to Invoice Automation]
  |-- [Support: How to Automate Invoice Data Extraction]
  |-- [Support: Invoice Automation vs Manual Processing: Cost Comparison]
  |-- [Support: 7 Common Invoice Automation Mistakes]
  |-- [Support: Invoice Automation for Small Businesses]
  |-- [Support: Advanced Invoice Matching Techniques]
  |-- [Support: How to Choose Invoice Automation Software]
  |-- [Support: Invoice Automation ROI Calculator Guide]
```

**Planning template:**

```
| Cluster Topic           | Pillar Page Title                        | Supporting Articles (count) | Target Keywords | Status   |
|-------------------------|------------------------------------------|-----------------------------|-----------------|----------|
| Invoice Automation      | Complete Guide to Invoice Automation     | 7                           | 12              | Planning |
| AP Workflow             | How to Streamline Accounts Payable       | 5                           | 8               | Draft    |
| Expense Management      | Expense Management Best Practices        | 6                           | 10              | Idea     |
```

Build one cluster at a time. Do not start a second cluster until the first has its pillar page and at least 3 supporting articles published and interlinked.

### Step 4: GEO Content Creation Framework

Run `scripts/score-content-geo.py --url <URL>` to score existing content against this framework (0-40 scale). See `references/geo-content-framework.md` for the full scoring rubric, before/after rewrite examples, and passage extraction simulation.

This is the core differentiator between content that only ranks and content that also gets cited by AI engines. For every piece of content, apply all eight elements:

**1. TLDR first.** Open with a direct, complete answer in the first 150-200 words. Do not bury the answer after a long introduction. This serves quick-answer users AND AI engines that extract opening content for citations. Start the page with the answer, then spend the rest of the article proving and expanding on it.

**2. Question-format headers.** Use H2s that mirror how people actually ask questions. Pull phrasing from GSC query data, AnswerThePublic, and "People Also Ask" boxes. "What Is Invoice Automation?" gets cited more than "Invoice Automation Overview" because it matches the query structure AI engines process.

**3. Data-rich body.** Include specific statistics, percentages, dollar amounts, and dates. Cite the source for every claim. "Companies using invoice automation reduce processing costs by 60-80% (Ardent Partners, 2025)" beats "Invoice automation significantly reduces costs." AI engines preferentially cite content with specific, sourced data.

**4. Self-contained sections.** Each H2 section should make complete sense if extracted on its own. Aim for 50-150 word knowledge blocks per section. AI engines pull individual sections, not entire articles. If a section requires reading the previous section to make sense, restructure it.

**5. Expert quotations.** Include quotes from recognized authorities, industry analysts, or internal subject matter experts with named attribution. "According to Mary Chen, VP of Finance at Acme Corp, 'Automation cut our invoice cycle from 14 days to 2 days.'" This signals authority to both Google and AI systems.

**6. Source citations.** Link to primary sources — studies, official documentation, data sets. Content that cites its own sources signals reliability. AI engines track source chains. Include at least 3-5 external citations per article.

**7. Original value.** Add something no competitor has: your own data, a proprietary framework, a case study from direct experience, a unique perspective. This differentiates from commodity content and gives AI engines a reason to cite you specifically over the dozens of similar articles.

**8. Clear author attribution.** Show who wrote the article, their credentials, and why they are qualified to write it. Link to an author page with bio and credentials. This feeds E-E-A-T signals that both Google and AI engines evaluate.

### Step 5: Content Types That Work

Not all content formats perform equally for SEO and GEO. Choose the right format for each keyword and intent.

```
| Content Type            | SEO Value  | GEO Value  | When to Use                                              |
|-------------------------|-----------|-----------|----------------------------------------------------------|
| Comprehensive guides    | High      | High      | Pillar content for topical authority                     |
| How-to tutorials        | High      | High      | Step-by-step procedures — frequently cited by AI         |
| Comparison posts (X vs Y)| High    | Medium    | Commercial intent keywords, decision support             |
| Data-driven studies     | Medium    | Very High | Original research is uniquely citable by AI engines      |
| Tool roundups           | High      | Low       | Drives search traffic but rarely cited by AI             |
| FAQ pages               | Medium    | High      | Pre-structured Q&A pairs ideal for AI extraction         |
| Glossaries/definitions  | Medium    | Very High | AI engines cite clear, authoritative definitions heavily |
| Case studies            | Medium    | High      | First-hand experience with specific results              |
| Templates/calculators   | High      | Low       | Drives traffic and backlinks, less AI citation value     |
```

**Priority order for a new site:** Glossary/definitions (quick GEO wins) then how-to tutorials (SEO + GEO) then pillar guides (authority building) then comparison posts (commercial traffic) then original research (citation magnets).

### Step 6: E-E-A-T Integration

Run `scripts/check-eeat-signals.py --url <URL>` to check E-E-A-T signal presence. See `references/eeat-signals.md` for the full implementation guide, author page template, and editorial policy template.

Google's December 2025 update extended E-E-A-T evaluation to all competitive queries, not just YMYL (Your Money or Your Life) topics. Every piece of content must demonstrate:

- **Experience.** Include first-hand accounts, screenshots of actual results, specific numbers from real projects. "We tested this on 3 client sites and saw a 40% increase" beats "Studies show increases are possible."
- **Expertise.** Demonstrate deep domain knowledge. Cover edge cases. Address counterarguments. Surface-level summaries do not signal expertise.
- **Authoritativeness.** Build author pages with bios, credentials, and links to other published work. Get cited by other sites. Publish on topics where you have demonstrable authority.
- **Trustworthiness.** Cite sources. Be transparent about limitations ("This approach works best for B2B SaaS — results may differ for e-commerce"). Keep content updated with current dates. Display clear contact information and editorial policies.

**Implementation checklist for every article:**

```
- [ ] Author byline with link to author page
- [ ] Author page has bio, photo, credentials, and links to social/professional profiles
- [ ] Article includes at least one first-hand experience or case study
- [ ] All statistics cite primary sources
- [ ] Article acknowledges limitations or cases where the advice does not apply
- [ ] "Last updated" date is visible and accurate
```

### Step 7: Content Refresh Strategy

Run `scripts/audit-content-freshness.py --sitemap <URL>` to identify stale pages and refresh candidates. See `references/content-refresh.md` for the refresh prioritization framework and update workflow.

Published content decays. A 2024 guide loses to a 2026 article on the same topic. Maintenance is as important as creation.

**Three tiers of content updates:**

- **Optimizations** (under 15% changes): Update meta titles and descriptions, add internal links to newer content, improve CTAs, fix broken links. Do continuously as new content is published.
- **Upgrades** (15-70% changes): Refresh statistics with current data, add new sections covering recent developments, improve visuals, add expert quotes. Schedule every 3-6 months for important pages.
- **Rewrites** (70%+ changes): Complete overhaul when the angle no longer works, the topic has fundamentally changed, or the content was never good enough. Treat as a new piece of content in the production workflow.

**Priority order for refreshes:**

1. Pages ranking at positions 4-15 (cheapest wins — small improvements can push into top 3)
2. Pages with declining traffic over the past 3 months (catch decay early)
3. Pages with high impressions but low CTR (title/description need work)
4. Pages older than 12 months that have never been updated

**Refresh tracking template:**

```
| URL                          | Current Pos. | Last Updated | Traffic Trend | Refresh Type  | Priority | Status  |
|------------------------------|-------------|-------------|---------------|---------------|----------|---------|
| /guide/invoice-automation    | 6           | 2025-08-14  | Declining     | Upgrade       | High     | Planned |
| /blog/ap-best-practices      | 14          | 2025-03-20  | Flat          | Optimization  | High     | Done    |
| /glossary/three-way-matching | 3           | 2025-11-01  | Growing       | None needed   | Low      | --      |
```

### Step 8: Content Calendar Template

Plan production at the weekly level. Every entry must map to a keyword, intent, and cluster.

```
| Week    | Topic                                    | Type          | Target Keyword                   | Intent        | Cluster              | Owner   | Status  |
|---------|------------------------------------------|---------------|----------------------------------|---------------|-----------------------|---------|---------|
| Week 1  | Complete Guide to Invoice Automation     | Pillar guide  | invoice automation               | Informational | Invoice Automation   | @sarah  | Draft   |
| Week 2  | Invoice Automation vs Manual Processing  | Comparison    | invoice automation vs manual     | Commercial    | Invoice Automation   | @sarah  | Outline |
| Week 3  | How to Automate Invoice Data Extraction  | How-to        | automate invoice data extraction | Informational | Invoice Automation   | @mike   | Planned |
| Week 4  | 7 Common Invoice Automation Mistakes     | List post     | invoice automation mistakes      | Informational | Invoice Automation   | @sarah  | Idea    |
| Week 5  | How to Choose Invoice Automation Software| Comparison    | best invoice automation software | Commercial    | Invoice Automation   | @mike   | Idea    |
```

Publish the pillar page first, then supporting articles. After 3-4 supporting articles are live, go back and add internal links from every supporting article to the pillar and between related supporting articles.

## Quality checklist

Before publishing any content, verify:

- [ ] Target keyword and search intent are identified and documented
- [ ] Content type matches the search intent (guide for informational, comparison for commercial, etc.)
- [ ] Article opens with a direct answer in the first 150-200 words (TLDR first)
- [ ] Every H2 section is self-contained and makes sense if extracted independently
- [ ] All statistics and claims cite specific sources with dates
- [ ] Author byline links to a complete author page with credentials
- [ ] Internal links connect the article to its pillar page and related cluster articles
- [ ] At least one element of original value exists (your own data, framework, case study, or unique perspective)

## Common mistakes to avoid

- **Chasing rankings instead of revenue.** Traffic that does not convert is vanity. Prioritize keywords with commercial intent or clear paths to business goals over high-volume informational queries that attract the wrong audience.
- **Publishing AI-generated content without editing.** Unedited LLM output is undifferentiated commodity content. It reads like everything else, contains no original value, and gives neither Google nor AI engines a reason to rank or cite it. Use AI to draft; use humans to add experience, data, and perspective.
- **Ignoring search intent.** A keyword match without an intent match is worthless. If Google shows comparison posts for a keyword and you publish a tutorial, you will not rank regardless of quality.
- **No topic cluster strategy.** Isolated articles on random topics do not build topical authority. One well-structured cluster of 8 interlinked articles outperforms 20 disconnected posts.
- **Vague claims without data.** "AI improves marketing results" is not citable. "AI-personalized email campaigns achieve 26% higher open rates (Salesforce State of Marketing, 2025)" is. GEO requires specific, sourced data.
- **No content refresh cadence.** A guide published in 2024 with 2023 statistics loses to a 2026 article covering the same topic. Schedule quarterly reviews of your top-performing pages.
- **Writing for search engines, not humans.** Keyword-stuffed content that reads like it was written for a crawler will not earn links, citations, or conversions. Write for humans first, optimize for machines second.
- **Expecting overnight results.** SEO compounds over 3-6 months. GEO citation can appear faster but fluctuates as AI models update. Set a 6-month evaluation window before concluding a content strategy is not working.
- **Missing author attribution.** E-E-A-T depends on visible expertise signals. An article without a named author, bio, and credentials is at a disadvantage for both Google rankings and AI citation selection.
- **Starting multiple clusters simultaneously.** Depth beats breadth. Finish one topic cluster (pillar + 5 supporting articles, fully interlinked) before starting the next. Spreading effort across 5 clusters with 1 article each builds zero topical authority.

## Available scripts

The key feedback loop: run `scripts/score-content-geo.py` on existing content to get a GEO score (0-40), then optimize based on the element-by-element breakdown. Run it again after changes to measure improvement.

| Script | What it does | Run it when |
|--------|-------------|-------------|
| `research-keywords.py` | Expands seed keywords via WebSearch, classifies intent, estimates difficulty | Starting keyword research (Step 1) |
| `classify-intent.py` | Analyzes top 5 SERP results per keyword to classify search intent | Verifying intent for your keyword list (Step 2) |
| `analyze-serp-competitors.py` | Extracts word counts, headings, schema, and content format from top 10 results | Analyzing what competitors do for a target keyword |
| `score-content-geo.py` | **Scores content against the 8-element GEO framework (0-40)** | Before and after optimizing any content (Step 4) — the key feedback loop |
| `check-eeat-signals.py` | Checks author byline, author page, credentials, citations, dates, editorial policy | Auditing E-E-A-T compliance (Step 6) |
| `audit-content-freshness.py` | Extracts dates from sitemap/pages, flags stale content, identifies refresh candidates | Planning content refreshes (Step 7) |
| `plan-topic-cluster.py` | Discovers subtopics via WebSearch and generates cluster structure with link map | Planning a new topic cluster (Step 3) — generative, creates content plans |

All scripts output JSON, accept `--tools` for tool inventory, and fall back to free methods (WebFetch/WebSearch) when paid tools are unavailable. Run `--help` on any script for usage details.
