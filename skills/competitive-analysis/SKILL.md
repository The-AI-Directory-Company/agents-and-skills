---
name: competitive-analysis
description: Structured market research template for identifying competitors, analyzing positioning, comparing features, assessing strengths and weaknesses, and finding market opportunities.
metadata:
  displayName: "Competitive Analysis"
  categories: ["business", "product-management"]
  tags: ["competitive-analysis", "market-research", "positioning", "strategy"]
  worksWellWithAgents: ["business-analyst", "marketing-strategist", "pricing-strategist", "product-marketing-manager", "vp-product"]
  worksWellWithSkills: ["go-to-market-plan", "prd-writing", "pricing-analysis", "product-launch-brief", "startup-pitch-deck"]
---

# Competitive Analysis

## Before you start

Gather the following from the user:

1. **What is your product/service?** (One-sentence description and primary value proposition)
2. **Who are your known competitors?** (Direct and indirect — list at least 3)
3. **What market segment?** (Enterprise, SMB, consumer, developer tools, etc.)
4. **What decision are you informing?** (Pricing, positioning, feature roadmap, GTM strategy, fundraising)
5. **What data sources are available?** (Public websites, G2/Capterra reviews, pricing pages, job postings, SEC filings)

If the user says "we have no competitors," push back: "Every product competes with something — even if it's spreadsheets, manual processes, or doing nothing. Who are customers using today to solve this problem?"

## Competitor identification

Start by mapping the competitive landscape into three tiers.

```
| Tier     | Definition                                              | Example               |
|----------|--------------------------------------------------------|-----------------------|
| Direct   | Same problem, same customer segment, same approach     | Competitor A vs You   |
| Indirect | Same problem, different approach or different segment   | Spreadsheets, agencies|
| Adjacent | Different problem today, could expand into your space   | Platform with overlap |
```

List 3-5 direct competitors, 2-3 indirect, and 1-2 adjacent. For each, capture:

```
| Competitor     | Tier     | Founded | Funding/Revenue | HQ       | Est. Customers |
|---------------|----------|---------|-----------------|----------|----------------|
| Competitor A  | Direct   | 2019    | $50M Series B   | SF, USA  | ~5,000 SMBs    |
| Competitor B  | Direct   | 2017    | $120M ARR       | London   | ~2,000 Ent.    |
| Manual process| Indirect | N/A     | N/A             | N/A      | Everyone else  |
```

## Feature comparison matrix

Compare features that matter for the purchase decision. Use a clear rating system.

```
Rating: Y = Yes | P = Partial | N = No | ? = Unknown

| Feature              | Your Product | Comp A | Comp B | Comp C |
|---------------------|-------------|--------|--------|--------|
| Core feature 1      | Y           | Y      | P      | N      |
| Core feature 2      | Y           | Y      | Y      | Y      |
| Integration X       | P           | Y      | N      | Y      |
| Self-serve onboard  | Y           | N      | Y      | N      |
| Enterprise SSO      | N           | Y      | Y      | Y      |
| API access          | Y           | Y      | P      | N      |
```

Weight features by importance to the target buyer. A feature your buyer does not care about is not a competitive advantage.

## Positioning analysis

For each direct competitor, map their positioning using this template.

```
## [Competitor Name]

Tagline:        [From their homepage]
Target buyer:   [Who they sell to — title, company size]
Primary value:  [Their #1 claimed benefit]
Pricing model:  [Free tier? Per seat? Usage-based?]
Key message:    [Core narrative from marketing — "the X for Y" or "unlike Z, we..."]
Differentiator: [What they emphasize as unique]
Weakness signal: [Complaints from reviews, missing features, churn patterns]
```

## Strengths and weaknesses assessment

Use a structured SWOT-style analysis per competitor. Focus on observable evidence, not speculation.

```
## [Competitor Name] — Assessment

Strengths (what they do well):
- [Evidence-backed strength — cite source: G2 review, pricing page, job posting]
- [Evidence-backed strength]

Weaknesses (where they fall short):
- [Evidence-backed weakness — cite source]
- [Evidence-backed weakness]

Opportunities for you (gaps they leave open):
- [Specific gap you can exploit]

Threats from them (risks to your position):
- [Specific risk — e.g., they're hiring for your feature area]
```

## Opportunity mapping

Synthesize the analysis into actionable opportunities ranked by impact and feasibility.

```
| Opportunity                          | Evidence                              | Impact | Effort |
|--------------------------------------|---------------------------------------|--------|--------|
| Underserved SMB segment              | Comp A/B focus on enterprise only     | High   | Medium |
| No competitor offers self-serve      | All require demo/sales call           | High   | Low    |
| Integration gap with [Tool X]        | Top-requested in G2 reviews           | Medium | Low    |
| Price point gap at $X-Y/month        | Comp A is $100+, no mid-tier option   | High   | Medium |
```

## Quality checklist

Before delivering the analysis, verify:

- [ ] At least 3 direct competitors are profiled with evidence, not just names
- [ ] Feature comparison is weighted by buyer importance, not just feature count
- [ ] Positioning analysis uses actual competitor messaging, not your interpretation
- [ ] Weaknesses cite observable evidence (reviews, missing features), not assumptions
- [ ] Opportunities are ranked by impact and effort
- [ ] The analysis answers the specific decision the user needs to make
- [ ] Sources are noted (pricing pages, review sites, job boards, press releases)

## Common mistakes

- **Listing features without weighting.** Having 50 features vs. a competitor's 30 means nothing if the buyer only cares about 5. Weight the comparison by what drives purchase decisions.
- **Relying on competitor marketing copy as truth.** Their homepage says "enterprise-grade security." Their G2 reviews say "no SOC 2." Use third-party evidence, not self-reported claims.
- **Ignoring indirect competitors.** The biggest competitor for most products is "do nothing" or "use a spreadsheet." Include the status quo in your analysis.
- **Analysis without actionable recommendations.** A competitive matrix that doesn't lead to "so we should do X" is an academic exercise. End with ranked opportunities tied to decisions.
- **One-time snapshot instead of ongoing tracking.** Competitors change pricing, ship features, and pivot positioning. Schedule quarterly updates to the analysis.
