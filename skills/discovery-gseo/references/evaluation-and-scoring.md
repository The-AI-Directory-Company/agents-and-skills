# Evaluation and Scoring

This reference covers the complete evaluation pipeline: volume and KD interpretation, intent classification, GEO scoring, filtering rules, topic clustering, the 4-dimension prioritization framework, and quick win identification.

## Volume interpretation

Search volume is the estimated number of times people search for a keyword per month.

| Volume range | Label | Guidance |
|-------------|-------|----------|
| 10,000+ | High | Very competitive. Hard to rank for as a new site. Target only if you have strong domain authority or a unique angle. |
| 1,000-10,000 | Medium | Good target for sites with some authority. Often the sweet spot for high-value commercial queries. |
| 100-1,000 | Low-medium | Sweet spot for new sites. Enough traffic to matter, low enough competition to win. |
| <100 | Low | Still worth targeting when intent is strong. Buyer keywords with 30 monthly searches can be more valuable than informational keywords with 3,000. |
| 0 | Below threshold | Tools cannot measure, but real people search it. Evaluate on intent and business relevance, not volume. |

**Critical nuance:** Volume numbers vary across tools. Ahrefs, Semrush, and Ubersuggest will show different numbers for the same keyword. Do not obsess over the exact number. Focus on the order of magnitude: is this a 100/mo keyword or a 10,000/mo keyword?

## Keyword Difficulty interpretation

KD is an estimate of how hard it will be to rank in the top 10. All tools use a 0-100 scale but calibrate differently.

| KD range | Difficulty | What it takes |
|----------|-----------|--------------|
| 0-20 | Easy | Good content can rank in weeks to a few months. New sites can target these immediately. |
| 21-40 | Medium | Needs good content plus some backlinks. Realistic for sites with some authority. |
| 41-60 | Hard | Needs excellent content, strong backlinks, and established domain authority. |
| 61-80 | Very hard | Dominated by major websites. Very difficult for sites under DA 50. |
| 81-100 | Extreme | Only the biggest brands rank. Avoid unless you have very high authority. |

**The SERP reality check:** KD is an estimate, not a guarantee. The actual difficulty depends on your specific niche. A KD of 30 in a niche dominated by weak blogs is much easier than a KD of 30 in a niche dominated by Forbes and HubSpot. Always manually check the actual SERP for your target keywords.

**Cross-tool warning:** Ahrefs KD 30 is not the same as Semrush KD 30. They use different algorithms. Never compare KD numbers across tools. Use one tool consistently.

**Free KD proxy:** If you have no paid tools, search the keyword and count high-authority domains in the top 10. All Forbes and Wikipedia? Very high difficulty. Mix of small blogs and niche sites? Likely manageable.

## Search intent classification

Intent is the most important dimension of keyword evaluation. Creating the wrong content type for a keyword means you will not rank, regardless of content quality.

### The 4 intent types

**Informational — "I want to learn."**
- **Signals:** "how to", "what is", "why", "guide", "tutorial", "tips", "examples", "explained."
- **Content type:** Blog posts, guides, tutorials, explainer articles, educational content.
- **Examples:** "how to write an invoice", "what is double-entry bookkeeping."
- **Business value:** Lower direct conversion, but builds awareness, trust, and topical authority. Top of funnel.

**Navigational — "I want a specific site."**
- **Signals:** Brand names, product names, "login", "pricing page", specific URLs.
- **Content type:** Your homepage, product pages. You only rank for your own brand's navigational queries.
- **Examples:** "FreshBooks login", "Stripe dashboard."
- **Business value:** Very high for your own brand. Not worth targeting for other brands.

**Commercial — "I'm comparing options."**
- **Signals:** "best [category]", "[product] review", "[A] vs [B]", "[product] alternatives", "top [category] for [use case]."
- **Content type:** Comparison pages, alternatives pages, review roundups, "best of" lists.
- **Examples:** "best invoicing software for freelancers", "FreshBooks vs Wave."
- **Business value:** High. Close to purchase decision. You can influence the outcome.

**Transactional — "I'm ready to act."**
- **Signals:** "buy", "pricing", "free trial", "sign up", "download", "[product] coupon", "free [tool type]."
- **Content type:** Product pages, pricing pages, landing pages, free tools, sign-up pages.
- **Examples:** "invoicing software free trial", "free invoice template download."
- **Business value:** Highest. Direct conversion opportunity.

### The SERP test

The definitive way to determine intent is to search the keyword on Google and look at what ranks:

1. Open an incognito browser window.
2. Search for the keyword.
3. Look at the top 5-10 results.
4. Blog posts = informational. Product pages = transactional. Comparison articles = commercial. Brand homepages = navigational.

Google has already figured out the intent. The content types that rank are the content types Google has determined match what searchers want. Match the format, or do not bother targeting the keyword.

Run `scripts/classify-intent-live.py --keywords keywords.txt` to automate SERP-based intent classification via Playwright.

### The AI-answerable flag

A keyword is "AI-answerable" when AI platforms provide a direct answer to the query instead of deferring entirely to search results.

**How to check:**
- Search the keyword on Google — does an AI Overview appear at the top?
- Ask the query on Perplexity — does it give a direct, sourced answer?
- Ask the query on ChatGPT — does it answer with specifics, or say "I'd recommend searching for..."?

**Why it matters:** If a keyword is AI-answerable, GEO optimization is critical. The AI answer captures attention before organic results. If your content is not cited in that AI answer, you lose visibility even if you rank #1 organically.

Mark AI-answerable keywords in your spreadsheet. They get a GEO score of at least 2, because AI actively engages with the topic.

## GEO score methodology

For each keyword, assess AI citation potential on a 1-3 scale.

**Score 3 — High GEO opportunity:**
AI answers this query and cites weak or few sources. You can create content that replaces those citations.

How to identify:
- Perplexity cites sources that are outdated, thin, or from low-authority domains.
- AI's answer is incomplete or mentions that information is limited.
- Few sources are cited (1-2 instead of 4-5).

This is the GEO equivalent of finding a low-KD keyword. The competition for AI citation is weak.

**Score 2 — Moderate GEO opportunity:**
AI answers and cites strong, authoritative sources. You can appear alongside them but displacing them is harder.

How to identify:
- Perplexity cites well-known authoritative sources (industry leaders, major publications).
- AI's answer is comprehensive and well-sourced.
- Multiple strong sources are cited.

Still worth targeting — AI citation is not winner-take-all. Multiple sources can be cited.

**Score 1 — Low GEO opportunity:**
AI does not answer this query or defers entirely to search. SEO-only value.

How to identify:
- The query is too niche or too recent for AI to have good training data.
- AI responses say "I'd recommend checking..." or provide generic non-answers.
- No AI Overview appears on Google for this query.

This keyword has organic search value but minimal AI citation potential.

Run `scripts/probe-ai-discovery.py --queries keywords.txt` to assess GEO scores across your keyword list.

## Filtering rules

Apply these filters after enriching your keyword list with volume, KD, intent, and GEO scores.

**Remove irrelevant keywords:** If the searcher would never become your customer, cut the keyword. Be honest. "Concrete invoice" might appear in your expansion, but if you sell software, it is irrelevant.

**Remove branded competitor navigational queries:** "[CompetitorName] login" and "[CompetitorName] support" are navigational — those searchers want that specific competitor. However, KEEP "[CompetitorName] alternative" and "[CompetitorA] vs [CompetitorB]" — these signal comparison intent.

**Remove keywords above your KD threshold:** As a general rule for new sites (DA <20-30), filter out keywords with KD above 40-50. Adjust upward as your authority grows. You can target high-KD keywords later.

**Remove duplicates and near-duplicates:** "Invoice software" and "invoicing software" are the same keyword to Google. Keep the version with higher volume. Google understands synonyms and will rank your page for both.

## Spreadsheet structure

After evaluation and filtering, organize your keywords:

```
| Keyword | Volume | KD | Intent | GEO Score | Source | Priority | Target URL | Status |
|---------|--------|----|----|-----------|--------|----------|------------|--------|
| invoice generator free | 2,400 | 18 | Trans. | 3 | Expansion | — | /tools/generator | To create |
| how to create an invoice | 6,600 | 35 | Info. | 3 | Google PAA | — | /blog/create-invoice | To create |
| FreshBooks alternative | 1,300 | 22 | Comm. | 2 | Gap analysis | — | /compare/freshbooks | To create |
```

The Priority column stays empty until Phase 9 (4-dimension scoring). Source tracks where the keyword came from. Status tracks your content creation progress.

## Topic clustering

### Cluster structure

A topic cluster is a set of related keywords targeted by interconnected pages that build topical authority together.

**Pillar page:** Comprehensive, broad coverage of the cluster topic. Targets the highest-volume, broadest keyword.

**Supporting pages:** Specific, deep coverage of subtopics. Each targets a narrower keyword within the cluster.

**Internal links:** Every support links to the pillar. The pillar links to every support. Related supports link to each other. This web of content signals expertise to Google.

### The "own page" test

Does a keyword deserve its own dedicated page, or should it be an H2 section in a larger page?

A keyword gets its own page when:
- It has a **distinct intent** from other keywords in the cluster (a comparison keyword vs an informational keyword).
- The topic is **deep enough** for 800+ words of dedicated content.
- The **SERP test** shows standalone pages ranking (not subsections of comprehensive guides).

Otherwise, target the keyword as an H2 section within a pillar or supporting page.

### GEO citation mapping within clusters

Within each cluster, rank supporting topics by GEO score. Create highest-GEO topics first:

1. They get cited by AI sooner, building your brand's AI visibility.
2. AI citations create a virtuous cycle — cited content gets more traffic, which strengthens organic rankings.
3. Early AI visibility for supporting topics can boost the pillar's GEO score over time.

## 4-dimension prioritization framework (max 12 points)

This framework extends the traditional 3-dimension SEO prioritization (Business Value + Feasibility + Traffic) with a 4th dimension: GEO Opportunity. The GEO dimension ensures AI citation potential is a real factor in content planning, not an afterthought.

### Dimension 1 — Business Value (1-3)

How directly does this keyword relate to revenue?

| Score | Definition | Examples |
|-------|-----------|----------|
| 3 | Direct product relevance. Searcher could become a customer. | "[category] software", "[competitor] alternative", "pricing" |
| 2 | Indirect relevance. Builds awareness with target audience. | "how to [solve problem]", "[topic] guide" |
| 1 | Tangential. Drives traffic, weak revenue connection. | General industry news, broad educational content |

### Dimension 2 — Ranking Feasibility (1-3)

Can you realistically rank in the top 10?

| Score | Definition |
|-------|-----------|
| 3 | KD under 20 AND you have relevant existing content or expertise |
| 2 | KD 20-40 OR requires building backlinks |
| 1 | KD 40+ OR dominated by major brands with high authority |

### Dimension 3 — Traffic Potential (1-3)

How much search traffic can this bring?

| Score | Definition |
|-------|-----------|
| 3 | Volume over 1,000/month |
| 2 | Volume 200-1,000/month |
| 1 | Volume under 200/month |

### Dimension 4 — GEO Opportunity (1-3)

What is the AI citation potential?

| Score | Definition |
|-------|-----------|
| 3 | AI cites weak/few sources for this query. Replacement opportunity. |
| 2 | AI cites strong sources. Worth targeting, harder to displace. |
| 1 | AI does not answer this query. SEO-only value. |

### Scoring and tiers

**Total = Business Value + Ranking Feasibility + Traffic Potential + GEO Opportunity (max 12)**

| Score range | Tier | Action |
|------------|------|--------|
| 10-12 | Golden | Do these first. Highest combined impact. |
| 7-9 | Strong | Do these second. Solid opportunities. |
| 4-6 | Moderate | Do eventually. Lower priority but still valuable. |
| 1-3 | Skip | Not worth the effort right now. |

### Worked scoring example (form builder SaaS)

| Keyword | BV | RF | TP | GEO | Total | Tier |
|---------|----|----|----|----|-------|------|
| Typeform alternative | 3 | 2 | 3 | 3 | 11 | Golden |
| NPS survey template | 3 | 3 | 2 | 2 | 10 | Golden |
| form builder with payment | 3 | 3 | 1 | 3 | 10 | Golden |
| how to create online form | 2 | 2 | 3 | 3 | 10 | Golden |
| event registration form | 3 | 3 | 3 | 1 | 10 | Golden |
| best online form builder | 3 | 1 | 2 | 2 | 8 | Strong |
| HIPAA compliant form builder | 3 | 3 | 1 | 1 | 8 | Strong |
| conditional logic form | 2 | 3 | 1 | 1 | 7 | Strong |
| drag and drop form builder | 2 | 2 | 1 | 2 | 7 | Strong |

Notice how "form builder with payment" scores Golden (10) despite low traffic potential (1) because GEO opportunity is high (3). Traditional 3-dimension scoring would give it a 7 (Strong). The GEO dimension changes prioritization.

## Quick win identification

Quick wins apply to sites with existing traffic and GSC data. They are the fastest path to more traffic because they optimize what already partially works.

### Striking distance (positions 8-20)

**What it is:** Keywords where you rank on positions 8-20. You are close to page 1 but not there yet.

**How to find them:**
1. GSC > Performance > Queries.
2. Set date range to last 3 months.
3. Filter: Average position between 8 and 20.
4. Sort by impressions descending.

**What to do:**
- Identify the ranking page (click keyword > Pages tab).
- Improve that page: add depth to the section covering the keyword, optimize the title tag, add internal links.
- Consider whether a dedicated page would serve the keyword better.

### High impressions, low CTR

**What it is:** Keywords where Google shows your page but people do not click. Your listing is not compelling.

**How to find them:**
1. Same GSC Performance view.
2. Filter: CTR below 2-3%.
3. Sort by impressions descending.

**What to do:**
- Rewrite the title tag: more specific, include the keyword, add a clear benefit or hook.
- Rewrite the meta description: active voice, value proposition, clear benefit of clicking.
- Check if a SERP feature (PAA, Featured Snippet) pushes your result down.

### Variant keywords

**What it is:** Keywords your pages rank for that you did not deliberately target.

**How to find them:**
1. In GSC, look at the queries for each page.
2. Find queries with significant impressions that are not your primary target.

**What to do:**
- If the variant has higher volume or better intent: shift your primary target.
- At minimum: add a section covering the variant, include it in an H2 or the body text.

### GEO quick wins

**What it is:** Keywords where you rank in organic search but AI platforms do not cite your content.

**How to find them:**
1. Take your top-ranking keywords (positions 1-10).
2. Run `scripts/probe-ai-discovery.py` with those keywords.
3. Identify keywords where you rank but are not cited.

**What to do:**
- Apply on-page-sgeo: optimize content structure for AI consumption (direct-answer formatting, data density, structured data).
- Apply content-sgeo: enhance content with citable facts, statistics, and expert attribution.
- The content already ranks — it just needs GEO formatting to get cited.

These are often the fastest GEO wins because the content already has search authority.
