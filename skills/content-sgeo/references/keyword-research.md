# Keyword Research Methodology

Complete reference for finding, expanding, and prioritizing keywords that serve both SEO rankings and GEO citations.

---

## Start with what you already have

Before hunting for new keywords, check Google Search Console (GSC). The Performance report shows every query your site already appears for. Sort by position and filter to positions 4-15. These are your cheapest wins — you're already visible, and small content improvements can push you into the top 3.

Export this list. It is the starting point for everything that follows.

If you don't have GSC connected, stop here and set it up. Keyword research without GSC data is guessing with extra steps.

## Seed keyword generation

List 5-10 terms directly related to the product or service. Use the language your customers use, not internal jargon. Two techniques to get customer language right:

1. **Customer conversations.** Read support tickets, sales call transcripts, and chat logs. The exact phrases customers use are your seeds.
2. **Competitor navigation.** Visit 3-5 competitor homepages. Read their nav menus, page titles, and H1 headings. These reveal the terminology the market uses.

Bad seeds: "enterprise resource planning solution" (jargon). Good seeds: "how to manage business operations" (customer language).

## Expansion techniques

### Google Autocomplete

Type each seed into Google and note the suggestions. Then type `{seed} a`, `{seed} b`, through `{seed} z` to surface long-tail variants. Each letter reveals a different cluster of queries.

Example: "invoice automation" yields "invoice automation software", "invoice automation for small business", "invoice automation benefits". Adding "invoice automation a" yields "invoice automation api", "invoice automation accounts payable".

### People Also Ask (PAA)

Search each seed and expand every PAA box. Each expansion triggers new questions. Click 3-4 and you'll collect 15-20 question-format keywords — these are gold for GEO because they match how users query AI engines.

### Related searches

Scroll to the bottom of the SERP. Google shows 8 related searches. Click one. Scroll to the bottom again. Repeat 2-3 times. You'll find long-tail variations Google considers semantically connected to your seed.

### AnswerThePublic

Enter your seed. AnswerThePublic visualizes questions (who, what, where, when, why, how), prepositions (for, with, without, near), and comparisons (vs, or, and, like). The free tier allows 3 searches per day — use them on your highest-priority seeds.

### Search operators

Run these operator-based searches for each seed to find specific content types:

- `[seed] vs` — reveals comparison intent keywords
- `[seed] alternative` — reveals competitor-aware searchers
- `best [seed]` — reveals commercial intent keywords
- `how to [seed]` — reveals informational intent keywords
- `[seed] for [audience]` — reveals audience-segmented keywords (e.g., "invoice automation for nonprofits")

## Tool-specific guidance

### Free tools

| Tool | What you get | Limitation |
|------|-------------|------------|
| **Google Keyword Planner** | Volume ranges (not exact), CPC data, competition level | Designed for ads, not SEO. Volume ranges are wide (1K-10K). Still useful for CPC signals. |
| **GSC Performance report** | Exact queries you rank for, impressions, clicks, CTR, position | Only shows your own data. No competitor keywords. |
| **Google Trends** | Relative interest over time, regional breakdown, related queries | No absolute volume numbers. Best for comparing seasonal patterns and trend direction. |

### Paid tools

| Tool | What you get | When to invest |
|------|-------------|----------------|
| **Ahrefs Keywords Explorer** | Exact volume, keyword difficulty (KD), clicks data, SERP features, parent topic | When content is your primary growth channel and you're publishing 4+ pieces/month. |
| **Semrush Keyword Magic Tool** | Volume, KD, intent classification, SERP features, keyword groups | Same threshold as Ahrefs — pick one, not both. |
| **DataForSEO Keyword Data API** | Programmatic access to volume, CPC, competition, difficulty | When you need bulk keyword data for automation or large-scale research. |

## Difficulty score interpretation

Difficulty scores are not comparable across tools. Ahrefs KD estimates how many backlinks you need to rank in the top 10. Semrush KD measures competitive density on a 0-100 scale. A KD of 30 in Ahrefs is very different from 30 in Semrush.

**Free difficulty proxy:** Search the keyword. Count how many results on page 1 are from well-known, high-authority domains (Wikipedia, major publications, government sites, Fortune 500 companies). More than 7 = very hard. Fewer than 3 = low competition.

**Practical thresholds for new sites:**
- Target keywords with difficulty <25 (Ahrefs) or <40 (Semrush) initially
- After 20+ published pages and some backlinks, expand to difficulty <40 (Ahrefs) or <55 (Semrush)
- Avoid difficulty >60 until you have established topical authority

## CPC as a commercial intent proxy

Cost-per-click data reveals what advertisers are willing to pay for a click. High CPC signals commercial value — someone is profiting from this keyword.

- **CPC > $8:** High commercial intent. These keywords drive revenue. Prioritize if they match your product.
- **CPC $3-8:** Moderate commercial intent. Mix of informational and commercial queries.
- **CPC < $3:** Usually informational. Still valuable for topical authority and GEO citation building, but don't expect direct conversions.

Low CPC does not mean low value. "What is invoice automation" (low CPC) builds awareness and topical authority. It may never convert directly, but it feeds the topic cluster that supports "invoice automation software" (high CPC).

## Competitor gap analysis workflow

1. **Export your keyword list.** GSC Performance report, filtered to the last 3 months.
2. **Export competitor keywords.** Ahrefs > Site Explorer > Organic keywords. Or Semrush > Organic Research > Positions. Do this for 3-5 competitors.
3. **Find the gaps.** Keywords competitors rank for that you don't. In Ahrefs: Content Gap tool. In Semrush: Keyword Gap tool. Without paid tools: search `site:competitor.com` and browse their content — every published page targets at least one keyword.
4. **Filter for feasibility.** Remove keywords with difficulty >40 (for newer sites). Remove keywords outside your topic area. Remove branded competitor keywords.
5. **Prioritize by intent.** Commercial and informational keywords with CPC > $3 go to the top. Informational keywords with low CPC but high volume go to a separate "topical authority" list.

## Quick win identification

The fastest ROI from keyword research comes from keywords you already rank for at positions 4-15. These pages are already indexed, already have some authority, and already appear in search results. Small improvements compound:

- Position 8 to position 3: CTR jumps from ~3% to ~11% (3.6x more traffic, zero new content needed)
- Position 12 to position 8: moves you from page 2 (near-zero clicks) to page 1

**How to find quick wins:**
1. GSC > Performance > Sort by position ascending
2. Filter to positions 4-15
3. Filter to impressions > 100/month (enough volume to matter)
4. For each: review the page. Is the content comprehensive? Does it match the search intent? Can you add a section, update data, or improve the title?

These improvements often show results within 2-4 weeks, compared to 3-6 months for new content.

## Output format

For every keyword research session, produce this table:

```
| Keyword                          | Volume | Difficulty | CPC   | Intent        | Current Pos. | Priority | Source      |
|----------------------------------|--------|-----------|-------|---------------|-------------|----------|-------------|
| how to automate invoices         | 1,200  | 22        | $4.50 | Informational | Not ranking | High     | Autocomplete|
| invoice automation software      | 880    | 45        | $12.80| Commercial    | Position 18 | High     | Seed        |
| best invoice automation tools    | 720    | 38        | $9.20 | Commercial    | Not ranking | Medium   | PAA         |
```

Include the Source column — it tells you where the keyword came from, which helps you replicate the process and verify the data.

## Keyword grouping and clustering

Raw keyword lists are unwieldy. Group keywords by topic and intent before planning content.

**Grouping process:**
1. Sort all keywords alphabetically. Similar keywords cluster naturally.
2. Group by shared root topic. "Invoice automation cost," "invoice automation pricing," and "how much does invoice automation cost" all belong to a pricing subtopic.
3. Within each group, identify the head keyword (highest volume) and long-tail variants.
4. Map each group to a single piece of content. One page should target one group, not one keyword.

**Avoid cannibalization.** If two pages target keywords in the same group, search engines can't decide which to rank. One comprehensive page targeting a keyword group outperforms two thin pages targeting individual keywords from the same group.

**Example grouping:**

```
Group: Invoice Automation Cost
  Head keyword: invoice automation cost (volume: 880)
  Long-tail: how much does invoice automation cost (320)
  Long-tail: invoice automation pricing (260)
  Long-tail: invoice automation ROI (440)
  → One content piece: "How Much Does Invoice Automation Cost in 2026?"
  → Content type: Commercial guide with pricing data, ROI calculator
```

## Keyword prioritization matrix

When you have 50+ keywords, use a 2x2 matrix to prioritize:

```
                    HIGH INTENT (commercial/transactional)
                    |
        Quick wins  |  Strategic targets
        (low diff,  |  (high diff,
         high ROI)  |   high ROI)
  LOW  ------------|------------ HIGH
  DIFF             |             DIFF
        Easy fills  |  Backburner
        (low diff,  |  (high diff,
         low value) |   low value)
                    |
                    LOW INTENT (pure informational)
```

- **Quick wins (top-left):** Do these first. Low difficulty + high intent = fastest revenue impact.
- **Strategic targets (top-right):** Build toward these. Need topical authority and backlinks before you can compete.
- **Easy fills (bottom-left):** Good for building topical authority and GEO citation volume. Low effort.
- **Backburner (bottom-right):** Save for later. High difficulty informational keywords are expensive to rank for and convert poorly.

## GEO considerations for keyword research

AI engines process queries differently from Google. They decompose complex questions into sub-queries and synthesize answers from multiple sources. This means:

- **Long-tail, question-format keywords are disproportionately valuable for GEO.** "What is the average cost of invoice automation for a 50-person company?" is a query an AI engine will decompose and answer — and it will cite content that specifically addresses this question.
- **Comparison keywords trigger AI synthesis.** "X vs Y" queries make AI engines pull from multiple sources. If your comparison post covers both sides thoroughly, you're more likely to be cited.
- **Definition keywords are GEO entry points.** "What is [term]" queries are the simplest for AI to answer, and they cite the clearest, most authoritative definition. A well-crafted glossary entry can be cited thousands of times.

Treat keyword research as serving two audiences: search engine users (click-through traffic) and AI engines (citation potential). The same keyword list serves both, but prioritize question-format and definition keywords slightly higher than you would for pure SEO.
