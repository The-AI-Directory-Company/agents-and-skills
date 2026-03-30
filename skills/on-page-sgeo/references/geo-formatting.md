# GEO Formatting: Direct Answers, Knowledge Blocks, and Citation-Worthy Content

AI engines don't cite entire pages. They extract passages — typically 50-150 words — and present them as part of a synthesized answer. If your best content is buried in paragraph 5 after a lengthy intro, it's invisible to every AI platform.

This reference covers the three core GEO on-page formatting techniques and the scoring rubric used by `scripts/check-direct-answer.py`.

## Direct-Answer-First Pattern

**The rule:** the first 200 words of the page — and of each major H2 section — must directly and completely answer the primary question. Lead with the TLDR. Then elaborate.

AI engines synthesize answers from opening content. ChatGPT, Perplexity, and Gemini all weight the first sentences of a page or section heavily when selecting text to cite. A meandering introduction wastes the most citation-valuable real estate on the page.

### Before/after: Blog post

**Before (meandering):**
```
Search engine optimization has evolved significantly over the past decade.
With the rise of AI-powered search, marketers face new challenges. In this
comprehensive guide, we will explore the many facets of technical SEO and
help you understand why it matters for your business. Before we dive in,
let's take a step back and consider the history of search engines...

[The actual answer appears 600 words later]
```

**After (direct answer):**
```
Technical SEO is the practice of optimizing a website's infrastructure so
search engines can crawl, index, and render its pages efficiently. It covers
server configuration, site architecture, structured data, page speed, and
mobile usability — everything that is not content or backlinks.

Why it matters: if search engines cannot access your pages, no amount of
content quality or link building will help you rank.
```

The direct-answer version gives an AI engine a self-contained, citable passage in the first two sentences.

### Before/after: Product page

**Before:**
```
Welcome to Acme Invoice Automation! We've been helping businesses streamline
their accounting workflows since 2019. Our team of experts has decades of
combined experience in fintech. We're proud to offer a solution that
thousands of companies trust...
```

**After:**
```
Acme Invoice Automation extracts data from incoming invoices, matches them
to purchase orders, and routes approvals automatically — reducing manual
processing time by 80% on average. It integrates with QuickBooks, Xero,
and NetSuite.
```

### Before/after: Documentation

**Before:**
```
This section covers the configuration options available in the settings
panel. As you learned in the previous chapter, there are many ways to
customize the behavior of the system. Let's look at each option in detail.
```

**After:**
```
The settings panel controls three behaviors: data retention (default 90
days, max 365), notification channels (email, Slack, webhook), and access
permissions (admin, editor, viewer). Each setting takes effect immediately
after saving — no restart required.
```

## Self-Contained Knowledge Blocks

Each H2 section should function as a standalone knowledge block — a 50-150 word passage that makes complete sense if extracted by an AI without any surrounding context.

### The anaphoric reference problem

Anaphoric references point to something said earlier. They make extracted passages incoherent.

**Red flags at the start of a section:**
- "As mentioned above..."
- "This approach..."
- "It..." (when "it" refers to something in the previous section)
- "The above..."
- "See previous section..."
- "Using the same method..."
- "Building on this..."

### Before/after: Dependent to self-contained

**Before (dependent on context):**
```
## Benefits

As we discussed in the previous section, this approach can significantly
improve your results. Many companies have seen positive outcomes using it.
The advantages are numerous and well-documented.
```

**After (self-contained):**
```
## What Are the Benefits of Internal Linking?

Internal linking passes PageRank between pages and helps search engines
discover content. Sites that increase internal links to key pages by 40%
see a median ranking improvement of 3.2 positions within 60 days, according
to a 2025 Ahrefs study of 14,000 domains. Internal links also help AI
engines map your site's knowledge structure, increasing citation likelihood
for any individual page.
```

**Before (vague):**
```
## Results

The results were impressive. Our clients saw major improvements across
the board. The data clearly shows that this strategy works for businesses
of all sizes.
```

**After (specific):**
```
## What Results Does Invoice Automation Deliver?

Companies using automated invoice processing report 80% faster processing
times, 65% fewer data entry errors, and $4.50 saved per invoice on average.
A 2025 Ardent Partners study of 450 enterprises found that full automation
reduces the cost per invoice from $15.97 (manual) to $2.36 (automated) —
an 85% cost reduction.
```

**Before (context-dependent):**
```
## Implementation

To implement this, follow the steps outlined above but apply them to your
specific situation. The process is straightforward if you've understood
the concepts from Section 2.
```

**After (self-contained):**
```
## How to Implement Schema Markup on Your Site

Add a JSON-LD script tag to your page's <head> section containing
structured data that describes the page's content type. For an article,
include headline, author (with name and jobTitle), datePublished, and
dateModified. Validate the markup using Google's Rich Results Test at
search.google.com/test/rich-results before deploying to production.
```

## Citation-Worthy Passage Construction

A citation-worthy passage follows a three-part formula:

**[Topic sentence with key claim] + [Specific data point with source] + [Implication or context]**

### Weak vs strong passages

**Weak:**
```
Internal linking is important for SEO. It helps search engines find your
pages and can improve your rankings. Many experts recommend using internal
links on your website.
```
Problems: No specific data, no named source, "many experts" is unfalsifiable vagueness.

**Strong:**
```
Internal linking passes PageRank between pages and reduces average crawl
depth. A 2024 Botify analysis of 6.2 billion pages found that pages at
crawl depth 3 or less were indexed 5x faster than pages at depth 6+,
and reducing crawl depth by two levels increased page discovery rate by 31%.
```
Why it works: Topic sentence names the mechanism. Data point is specific (5x faster, 31%, depth thresholds). Source is named (Botify, 6.2 billion pages).

**Weak:**
```
Page speed is becoming more important. Google has said it matters for
rankings. Slow sites provide a bad user experience and may rank lower.
```
Problems: "Becoming more important" is vague. No thresholds. No data.

**Strong:**
```
Google's Core Web Vitals are a confirmed ranking factor since June 2021.
Pages with LCP under 2.5 seconds, INP under 200 milliseconds, and CLS
under 0.1 are classified as "good." A 2024 Semrush analysis of 1 million
URLs found that pages meeting all three thresholds ranked 2.1 positions
higher on average than pages failing any one metric.
```
Why it works: Named ranking factor with date. Three specific thresholds. Quantified impact with source.

**Weak:**
```
AI search is growing fast. More people are using AI to find information
online. This trend is expected to continue.
```

**Strong:**
```
According to BrightEdge research, AI-referred website sessions grew over
500% year-over-year in the first half of 2025. ChatGPT alone reaches
800+ million weekly users, and
Perplexity processes 780+ million queries per month. Meanwhile, ~60% of
Google searches now end without a click, driven partly by AI Overviews
appearing in 18.5% of commercial queries.
```
Why it works: Five specific data points. Named platforms. Time-bounded claims.

## Per-Section GEO Scoring Rubric (0-8 Scale)

This rubric is used by `scripts/check-direct-answer.py` to score individual page sections. It evaluates whether a single H2 section is citation-ready.

**Note:** This is distinct from the full-article GEO score (0-40 scale, 8 elements at 0-5 each) used by content-sgeo's `score-content-geo.py`. This rubric focuses on per-section extraction quality.

### Scoring criteria

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| **Direct answer present** | Section opens with filler, question, or context-dependent reference | Section has an answer but it's buried after 2+ introductory sentences | First 1-2 sentences directly state the key point |
| **Self-contained** | Section relies on prior context to make sense (anaphoric references, "this approach") | Section is mostly self-contained but has minor dependencies ("as noted" once) | Section stands completely alone — any reader or AI could understand it without prior sections |
| **Specific data** | No numbers, no named entities, no dates — pure opinion or vague claims | Some specifics but imprecise ("many companies", "significant improvement") | Concrete numbers, percentages, dates, or named entities with precision |
| **Source attribution** | No sources cited | Vague attribution ("studies show", "experts say", "research indicates") | Named source with specifics (organization name, study size, date, or URL) |

### Score interpretation

- **0-2:** Not citable. The section is too vague, too dependent on context, or too devoid of specifics for any AI engine to extract a useful passage. Needs a full rewrite.
- **3-5:** Partially citable. The section has some useful content but structural or specificity issues reduce citation likelihood. Targeted improvements can push it to citation-ready.
- **6-8:** Citation-ready. The section opens with a direct answer, stands alone, contains specific data, and attributes sources. AI engines can extract a useful passage from this section.

### Applying the rubric

Walk through each H2 section of a page:

1. Read the first 2-3 sentences. Do they directly answer the section's implicit question?
2. Copy the section into a blank document. Does it make sense without the rest of the page?
3. Count the specific data points (numbers, dates, named entities). Are there at least 2?
4. Check source attribution. Is at least one claim backed by a named source?

Score each criterion 0-2 and sum for the section's total (0-8). Average across all H2 sections for a page-level GEO formatting score.

Run `scripts/check-direct-answer.py --url <URL>` to automate this analysis for the page's opening section.
