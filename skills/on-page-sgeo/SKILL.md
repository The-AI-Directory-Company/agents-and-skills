---
name: on-page-sgeo
description: Optimize individual pages for both search engine ranking and AI citation — covering title tags, meta descriptions, heading hierarchy, URL structure, internal linking, image optimization, structured data, direct-answer formatting, and knowledge block structure.
metadata:
  displayName: "On-Page SGEO Optimization"
  categories: ["business", "communication"]
  tags: ["SEO", "GEO", "SGEO", "on-page-SEO", "meta-tags", "headings", "internal-linking", "AI-citation", "structured-data"]
  worksWellWithAgents: ["seo-specialist", "content-strategist", "frontend-engineer", "copywriter"]
  worksWellWithSkills: ["technical-sgeo", "content-sgeo", "off-page-sgeo", "technical-seo-audit"]
---

# On-Page SGEO Optimization

On-page SGEO (Search Generative Engine Optimization) is the practice of optimizing individual page elements so the page both ranks in traditional search results and gets cited by AI platforms (ChatGPT, Perplexity, Gemini, Copilot). Every section below addresses both dimensions together — SEO impact and GEO impact are not separate concerns.

This is skill 2 of 4 in the SGEO series: technical-sgeo > **on-page-sgeo** > content-sgeo > off-page-sgeo.

## Tool discovery

Before gathering project details, confirm which tools are available. Ask the user directly — do not assume access to any external service.

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

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **Target page URL** — The live URL being optimized, or a description of the page being created.
2. **Primary keyword / topic** — The main query or subject the page should rank for and be cited on.
3. **Search intent** — Informational, navigational, commercial, or transactional. This determines the optimal page structure.
4. **Target audience** — Who this page is for (developers, marketers, executives, general consumers, etc.).
5. **Existing performance data** — Google Search Console impressions, average position, CTR, and top queries if the page already exists. Omit for new pages.
6. **AI citation priority** — Whether this page should be optimized for AI citation (high, medium, low). High priority pages get extra GEO formatting.
7. **Related pages on the site** — Pages that should link to/from this one. Needed for internal linking recommendations.
8. **Competitor pages ranking for the same keyword** — Top 3-5 URLs currently ranking, for gap analysis.

## On-page optimization template

### 1. Title Tag & Meta Description

> **Automate:** Run `scripts/extract-meta-tags.py --url <URL>` to extract and validate all meta tags. See `references/meta-optimization.md` for industry-specific examples and OG tag requirements.

The title tag is the single strongest on-page ranking signal. The meta description does not directly affect ranking but controls CTR from search results and is often extracted by AI engines as a page summary.

**Title tag rules:**

- Include the primary keyword within the first 50 characters
- Keep total length under 60 characters (Google truncates at ~580px)
- Front-load the most important words
- Make it specific and outcome-oriented — avoid vague labels
- Do not stuff multiple keywords separated by pipes

**Meta description rules:**

- Summarize the page's value proposition in under 155 characters
- Include the primary keyword naturally (Google bolds matching terms)
- Use active voice and a clear benefit statement
- For GEO: write the description as a complete, factual sentence — AI engines sometimes pull meta descriptions as summary text

**Examples:**

```
BAD title:  "SEO Guide | Best SEO Tips 2026 | SEO Company"
WHY:        Keyword-stuffed, no specificity, no compelling reason to click.

GOOD title: "Technical SEO Checklist: 15 Fixes That Improve Crawlability"
WHY:        Specific topic, concrete number, clear outcome, keyword up front.
```

```
BAD meta:   "We are the best SEO company. Learn about SEO on our blog."
WHY:        Self-promotional, no value proposition, no keyword alignment.

GOOD meta:  "A 15-point technical SEO checklist covering crawl errors, indexation,
             Core Web Vitals, and structured data — with fix instructions for each."
WHY:        Describes exactly what the reader gets. Complete sentence an AI could cite.
```

### 2. URL Structure

URLs are a minor ranking factor but a major usability and crawlability signal. AI engines also parse URLs to understand page topic.

**Rules:**

- Keep it short: 3-5 words after the domain
- Use hyphens to separate words (not underscores or camelCase)
- Include the primary keyword naturally
- Use lowercase only
- No dates, IDs, session parameters, or query strings
- Match the URL to the page's core topic, not its category hierarchy

**Examples:**

```
BAD:  /blog/2026/03/27/post-id-4827
WHY:  Date will make the URL look stale. ID is meaningless. Deeply nested.

BAD:  /resources/guides/seo/technical-seo-comprehensive-beginners-advanced-guide
WHY:  Too long. Redundant words. Dilutes keyword signal.

GOOD: /technical-seo-checklist
WHY:  Short, descriptive, keyword-inclusive, no unnecessary nesting.
```

### 3. Heading Hierarchy

> **Automate:** Run `scripts/analyze-headings.py --url <URL>` to validate the hierarchy and get a GEO heading score. See `references/heading-and-structure.md` for question-format templates and 15 before/after heading rewrites.

Headings define page structure for both search crawlers and AI parsers. A well-structured heading hierarchy helps search engines understand topic relationships and helps AI engines extract specific sections.

**Rules:**

- One H1 per page — it should match the primary topic and closely align with the title tag
- H2s for major sections — each should cover a distinct subtopic
- H3s for subsections within an H2
- Never skip heading levels (H1 > H3 without an H2)
- Do not use headings for visual styling — use CSS instead

**GEO-specific rule: use question-format H2s where natural.** AI engines match user queries to headings. A heading phrased as a question directly matches how users ask AI platforms.

**Examples:**

```
WEAK heading:   "## Technical SEO Overview"
WHY:            Generic. Does not match any natural query pattern.

STRONG heading: "## What Is Technical SEO?"
WHY:            Matches "what is technical seo" — a common AI query.
                Perplexity, ChatGPT, and Gemini will pull the content
                under this heading when answering that question.
```

```
WEAK heading:   "## Pricing"
STRONG heading: "## How Much Does [Product] Cost?"
WHY:            Matches commercial query format AI users actually type.
```

Not every heading should be a question — use questions for informational and commercial intent sections, and declarative headings for procedural or reference sections.

### 4. Direct-Answer-First Pattern (GEO)

> **Automate:** Run `scripts/check-direct-answer.py --url <URL>` to score the opening content on the 0-8 GEO rubric. See `references/geo-formatting.md` for the scoring criteria and before/after examples.

This is the most important GEO on-page technique. AI engines synthesize answers from the opening content of a page. If your answer is buried in paragraph 5 after a lengthy introduction, it will not be cited.

**The rule: the first 200 words of the page (or of each major section) must directly and completely answer the primary question.**

Lead with the TLDR. Then elaborate.

**Bad — meandering introduction:**

```
Search engine optimization has evolved significantly over the past decade.
With the rise of AI-powered search, marketers face new challenges. In this
comprehensive guide, we will explore the many facets of technical SEO and
help you understand why it matters for your business. Before we dive in,
let's take a step back and consider the history of search engines...

[The actual answer appears 600 words later]
```

**Good — direct answer first:**

```
Technical SEO is the practice of optimizing a website's infrastructure so
search engines can crawl, index, and render its pages efficiently. It
covers server configuration, site architecture, structured data, page
speed, and mobile usability — everything that is not content or backlinks.

Why it matters: if search engines cannot access your pages, no amount of
content quality or link building will help you rank.

[Elaboration, details, and supporting sections follow]
```

The direct-answer version gives an AI engine a self-contained, citable passage in the first two sentences. The meandering version gives it nothing usable.

**Apply this pattern to every H2 section**, not just the page opening. Each section should open with its key point, then expand.

### 5. Self-Contained Knowledge Blocks (GEO)

> See `references/geo-formatting.md` for the self-contained knowledge block rubric, anaphoric reference checklist, and citation-worthy passage construction formula.

AI engines do not always cite an entire page. They extract specific passages — typically 50-150 words — and present them as part of a synthesized answer. Each H2 section on your page should function as a standalone knowledge block that makes sense without surrounding context.

**Rules for knowledge blocks:**

- Each H2 section should be 50-150 words of self-contained, factual content (before elaboration)
- Include specific, citable data points within each block — numbers, percentages, named entities
- Avoid anaphoric references ("As mentioned above...", "This approach...", "It...") in the opening sentences of a section
- Front-load the most important fact or definition

**Examples:**

```
WEAK (not self-contained):
"As we discussed in the previous section, this approach can significantly
improve your results. Many companies have seen positive outcomes."

WHY: An AI extracting this passage has no idea what "this approach" refers
     to or what "positive outcomes" means. Zero citation value.
```

```
STRONG (self-contained):
"Internal linking passes PageRank between pages and helps search engines
discover content. Sites that increase internal links to key pages by 40%
see a median ranking improvement of 3.2 positions within 60 days,
according to a 2025 Ahrefs study of 14,000 domains."

WHY: Complete topic sentence. Specific data. Named source. An AI can
     extract this passage and it stands alone as a useful answer.
```

### 6. Internal Linking

> **Automate:** Run `scripts/check-internal-links.py --url <URL>` to count links, evaluate anchor text quality, and detect broken links. See `references/internal-linking.md` for anchor text taxonomy and click depth optimization.

Internal links distribute link equity, help crawlers discover pages, establish topical relationships, and guide users through your site. They also help AI engines understand your site's knowledge structure.

**Rules:**

- Aim for 3-5 internal links per 1,000 words of content
- Use descriptive anchor text that tells the reader (and crawlers) what the destination page covers
- Link to your most important pages from your most authoritative pages
- Link contextually within body content — not just in sidebars or footers
- Ensure every important page is reachable within 3 clicks from the homepage

**Anchor text examples:**

```
BAD:  "For more information, click here."
WHY:  "click here" tells crawlers and AI nothing about the destination.

BAD:  "Read our technical SEO guide for a comprehensive overview of
       technical SEO best practices for technical SEO."
WHY:  Over-optimized. Keyword-stuffed anchor text triggers spam signals.

GOOD: "Run a technical SEO audit to identify crawl and indexation issues
       before optimizing individual pages."
WHY:  Descriptive, natural, tells the reader and crawlers what to expect.
```

**GEO consideration:** AI engines follow internal links to build context about your site's expertise. A well-linked site on a topic signals topical authority — making any individual page more likely to be cited.

### 7. Image Optimization

> **Automate:** Run `scripts/check-images.py --url <URL>` to audit alt text, file sizes, formats, dimensions, and lazy loading. See `references/image-and-media.md` for the format decision tree and compression targets.

Images affect page speed, accessibility, search visibility (image search), and CLS. AI engines that process visual content (Google's multimodal search, Bing visual search) also use image metadata.

**Rules:**

- **Alt text:** Descriptive, concise (under 125 characters). Include the primary keyword only if the image genuinely relates to it. Do not keyword-stuff alt attributes.
- **File format:** Use WebP or AVIF for photographs, SVG for icons and illustrations. Serve fallback formats for older browsers.
- **File size:** Compress images to under 200KB where possible. Use tools like Squoosh, Sharp, or your build pipeline's image optimization.
- **Lazy loading:** Add `loading="lazy"` to all images below the fold. Do NOT lazy-load the LCP image (usually the hero image).
- **Dimensions:** Always set explicit `width` and `height` attributes (or use CSS `aspect-ratio`) to prevent Cumulative Layout Shift.
- **File names:** Use descriptive, hyphenated file names (`technical-seo-audit-results.webp`, not `IMG_4827.jpg`).

**Examples:**

```
BAD alt:  alt="image" or alt="" (on a meaningful image) or alt="SEO SEO guide SEO tips"
GOOD alt: alt="Screaming Frog crawl report showing 47 pages with redirect chains"
```

### 8. Structured Data Per Page

> **Automate:** Run `scripts/extract-structured-data.py --url <URL>` to extract JSON-LD, identify schema types, and validate required properties.

Structured data (JSON-LD) helps search engines understand page content and enables rich results. For GEO, structured data pre-packages information in a machine-readable format that AI engines can directly parse.

**Page type to schema mapping:**

```
| Page Type       | Schema Type   | Key Properties                                    |
|-----------------|---------------|---------------------------------------------------|
| Homepage        | Organization  | name, url, logo, sameAs (social profiles)         |
| Product page    | Product       | name, price, availability, review, aggregateRating |
| Blog post       | Article       | headline, author, datePublished, dateModified      |
| FAQ page        | FAQPage       | mainEntity (array of Question + acceptedAnswer)    |
| How-to guide    | HowTo         | name, step (array of HowToStep with text + image)  |
| Local business  | LocalBusiness | address, geo, openingHours, telephone              |
| Event page      | Event         | name, startDate, location, offers                  |
| Person/bio page | Person        | name, jobTitle, worksFor, sameAs                   |
```

**Implementation rules:**

- Use JSON-LD format (Google's preferred format), placed in a `<script type="application/ld+json">` tag
- One primary schema type per page — do not overload a single page with unrelated schema types
- Validate every page with Google's Rich Results Test (https://search.google.com/test/rich-results)
- Keep schema data consistent with visible on-page content — mismatches can trigger manual actions

**GEO-specific note:** FAQPage schema is particularly valuable for AI citation. It pre-structures question/answer pairs in exactly the format AI engines consume. If your page answers common questions, implement FAQPage schema even if the page is not a traditional FAQ — blog posts and product pages can include FAQ sections with matching schema.

### 9. Freshness Signals

> **Automate:** Run `scripts/check-freshness.py --url <URL>` to verify visible dates, schema dates, author bylines, and freshness score.

Both search engines and AI engines weight content recency. A page last updated in 2022 is less likely to be cited for a 2026 query than one updated this month — even if the underlying information has not changed.

**Rules:**

- Display a visible "Last updated: [date]" timestamp on content pages — this signals recency to both users and AI crawlers
- Include `dateModified` in your Article schema markup (not just `datePublished`)
- Show author name and credentials on content pages — this feeds E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) signals that both Google and AI engines evaluate
- When updating content, change substantive information — do not just change the date. Search engines can detect superficial updates.
- Review and update high-value pages on a quarterly cycle at minimum

**Example Article schema with freshness signals:**

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Technical SEO Checklist: 15 Fixes That Improve Crawlability",
  "author": {
    "@type": "Person",
    "name": "Jane Smith",
    "jobTitle": "Senior SEO Engineer",
    "url": "https://example.com/team/jane-smith"
  },
  "datePublished": "2025-06-15",
  "dateModified": "2026-03-20",
  "publisher": {
    "@type": "Organization",
    "name": "Example Company",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
```

### 10. On-Page SGEO Audit Table

> **Automate:** Run `scripts/audit-page.py --url <URL> --format md` to generate this table automatically. The orchestrator runs all 7 scripts and aggregates results.

Use this consolidated table to audit any existing page. Walk through each element, note the current state, and flag items that need work.

```
| Element                    | SEO Impact | GEO Impact | What to Check                                              | Status |
|----------------------------|------------|------------|------------------------------------------------------------|--------|
| Title tag                  | High       | Medium     | Under 60 chars, keyword up front, specific and compelling  | [ ]    |
| Meta description           | Medium     | Medium     | Under 155 chars, value proposition, complete sentence      | [ ]    |
| URL structure              | Medium     | Low        | Short, descriptive, keyword-inclusive, no parameters       | [ ]    |
| H1 tag                     | High       | Medium     | One per page, matches primary topic, aligns with title     | [ ]    |
| Heading hierarchy          | Medium     | High       | Logical H2/H3 structure, question-format where natural     | [ ]    |
| Direct-answer opening      | Low        | High       | First 200 words directly answer the primary question       | [ ]    |
| Knowledge blocks           | Low        | High       | Each H2 section is self-contained, 50-150 words, specific  | [ ]    |
| Internal links             | High       | Medium     | 3-5 per 1000 words, descriptive anchors, contextual        | [ ]    |
| Image alt text             | Medium     | Low        | Descriptive, concise, keyword where natural                | [ ]    |
| Image file size & format   | Medium     | Low        | Under 200KB, WebP/AVIF, lazy loading below fold            | [ ]    |
| Image dimensions           | Medium     | Low        | Explicit width/height set, no CLS                          | [ ]    |
| Structured data            | Medium     | High       | Correct schema type for page, validates in Rich Results    | [ ]    |
| FAQPage schema             | Medium     | High       | Applied to pages with Q&A content, matches visible content | [ ]    |
| dateModified in schema     | Low        | High       | Present and reflects actual last substantive update        | [ ]    |
| Visible last-updated date  | Low        | Medium     | Displayed on page, matches schema dateModified             | [ ]    |
| Author & credentials       | Medium     | High       | Name, role, and expertise visible on content pages         | [ ]    |
```

## Quality checklist

Before delivering the optimized page, verify:

- [ ] Title tag is under 60 characters, includes primary keyword, and is specific
- [ ] Meta description is under 155 characters, reads as a complete sentence, and conveys the page's value
- [ ] URL is short, descriptive, and keyword-inclusive
- [ ] Page has exactly one H1 and a logical H2/H3 hierarchy with question-format headings where appropriate
- [ ] The first 200 words directly answer the primary question without preamble
- [ ] Each H2 section opens with a self-contained knowledge block (50-150 words that stand alone)
- [ ] 3-5 internal links per 1,000 words with descriptive anchor text
- [ ] All images have descriptive alt text, are compressed, use modern formats, and have explicit dimensions
- [ ] Correct structured data type is implemented and validates in Rich Results Test
- [ ] Freshness signals are present: visible date, dateModified in schema, author credentials

## Common mistakes to avoid

1. **Keyword stuffing in title tags and headings.** Repeating the keyword 3+ times does not help — it triggers spam signals and reads poorly. Use the keyword once naturally and use semantic variations elsewhere.

2. **Burying the answer below a long introduction.** AI engines extract from the opening content. If your first 200 words are throat-clearing ("In today's digital landscape..."), your page will not be cited. Lead with the answer.

3. **Generic headings instead of question-format headers.** "Overview" and "Introduction" tell crawlers and AI nothing. "What Is [Topic]?" and "How Does [Topic] Work?" match real queries and increase citation likelihood.

4. **Missing structured data for the page type.** A product page without Product schema, a blog post without Article schema, an FAQ without FAQPage schema — each is a missed opportunity for rich results and AI extraction.

5. **Internal links with "click here" or "learn more" as anchor text.** These waste the anchor text signal entirely. Describe the destination: "Run a technical SEO audit" is both more useful to users and more informative to crawlers.

6. **No freshness signals on content pages.** Pages without visible dates, author information, or dateModified schema appear stale to both search engines and AI engines. A 2024 Semrush study found that pages with visible update dates had 23% higher click-through rates in search results.

7. **Ignoring search intent mismatch.** A product page will not rank for "how to" queries. A tutorial will not rank for "buy" queries. Match the page format to the intent: informational queries need guides, commercial queries need comparison pages, transactional queries need product/pricing pages.

8. **Writing H2 sections that depend on prior context.** If an AI extracts a section that starts with "As we saw above..." or "Using the same approach...", the extracted passage is incoherent. Every section must open with enough context to stand alone.

## Available scripts

For a complete page audit, run `scripts/audit-page.py --url <URL>` — it runs all other scripts and aggregates results into the audit table from Section 10.

| Script | What it checks | Run it when |
|--------|---------------|-------------|
| `audit-page.py` | **Orchestrator** — runs all 7 scripts below, outputs audit table | You want a full on-page SGEO audit of any URL |
| `extract-meta-tags.py` | Title, meta description, OG tags, canonical, robots meta | Optimizing title/description or diagnosing CTR issues |
| `analyze-headings.py` | Heading hierarchy, H1 count, question-format ratio, GEO score | Restructuring page headings or evaluating GEO readiness |
| `check-direct-answer.py` | First 200 words, direct-answer scoring (0-8 rubric), meandering patterns | Evaluating whether a page's opening is citation-ready |
| `check-internal-links.py` | Link count per 1000 words, anchor text quality, broken links | Auditing internal link structure or fixing anchor text |
| `check-images.py` | Alt text, formats, file sizes, dimensions, lazy loading | Optimizing images for speed, accessibility, and SEO |
| `extract-structured-data.py` | JSON-LD extraction, schema type validation, required properties | Implementing or auditing structured data markup |
| `check-freshness.py` | Visible dates, schema dates, author bylines, freshness score | Checking freshness signals or planning content updates |

All scripts accept `--url <URL>` and `--tools <tools.json>`. Output is JSON by default. `audit-page.py` also accepts `--format md` for a markdown table.

## References

| File | Covers |
|------|--------|
| `references/meta-optimization.md` | Title/description craft, OG tags, canonical, robots meta, industry examples |
| `references/heading-and-structure.md` | Hierarchy rules, GEO question-format patterns, 15 before/after rewrites |
| `references/geo-formatting.md` | Direct-answer-first, knowledge blocks, citation-worthy passages, 0-8 scoring rubric |
| `references/internal-linking.md` | Link equity, anchor text taxonomy, click depth, audit workflow |
| `references/image-and-media.md` | Format decision tree, compression targets, responsive images, alt text guide |
