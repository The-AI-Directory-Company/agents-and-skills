# Heading Hierarchy and Page Structure

Headings define your page's information architecture for three audiences simultaneously: human readers scanning the page, search engine crawlers parsing topic relationships, and AI engines extracting specific sections to cite.

## The Rules

**One H1 per page.** The H1 is the page's primary topic declaration. It should closely align with the title tag — not an exact match, but clearly about the same thing. Two H1s confuse crawlers about which topic is primary.

**H2s for major sections.** Each H2 introduces a distinct subtopic. Think of them as chapter titles.

**H3s for subsections within an H2.** Never skip levels — going from H1 to H3 without an H2 breaks the hierarchy and signals sloppy structure to crawlers.

**Never use headings for visual styling.** If you want big bold text that isn't a section header, use CSS. Headings are semantic, not decorative.

## H1 and Title Tag Alignment

The H1 and title tag serve different contexts but should be clearly related:

```
Title tag: "Invoice Automation Software: Cut Processing Time 80% | Acme"
H1:        "Invoice Automation That Cuts Processing Time by 80%"

Title tag: "What Is Technical SEO? A 15-Point Checklist for 2026"
H1:        "What Is Technical SEO?"
```

The title tag is optimized for SERP display (character limits, brand suffix). The H1 is optimized for on-page readability (can be longer, no brand suffix needed).

## GEO Question-Format Pattern

AI engines match user queries to headings. A heading phrased as a question directly matches how users ask AI platforms. When someone asks ChatGPT "how much does Salesforce cost?", the AI searches for headings and content that match that query pattern. A heading "How Much Does Salesforce Cost?" is a near-exact match. A heading "Pricing" is not.

**Use question-format H2s for informational and commercial intent sections.** These are the sections where users are asking questions — and AI engines are looking for answers.

**Use declarative headings for procedural and reference sections.** "Step 1: Install the CLI" reads better than "How Do You Install the CLI?" in a procedure. Reference tables, changelogs, and API docs also work better with declarative headings.

**Target 40-60% question-format H2s on content pages.** Not every heading should be a question — that reads unnaturally. Mix questions where they serve discovery with declarative headings where they serve clarity.

## H2 Templates by Intent Type

### Informational intent

When users want to learn:

- "What Is [X]?"
- "How Does [X] Work?"
- "Why Is [X] Important?"
- "What Are the Types of [X]?"
- "When Should You Use [X]?"
- "Who Needs [X]?"

### Commercial intent

When users are evaluating options:

- "How Much Does [X] Cost?"
- "[X] vs [Y]: Which Is Better?"
- "Is [X] Worth It in 2026?"
- "What Are the Best [X] Tools?"
- "What Are the Pros and Cons of [X]?"

### Transactional intent

When users are ready to act:

- "How to Get Started with [X]"
- "Where to Buy [X]"
- "How to Sign Up for [X]"

### Procedural content

When content is step-by-step (declarative is better here):

- "Step 1: [Action]"
- "Prerequisites"
- "Installation"
- "Configuration Options"

## Before/After Heading Rewrites

Here are 15 real-world heading rewrites. The "before" versions are what most sites use. The "after" versions match query patterns and increase AI citation likelihood.

### SaaS

| Before | After | Why |
|--------|-------|-----|
| Pricing | How Much Does [Product] Cost in 2026? | Matches commercial query pattern |
| Features | What Can [Product] Do? | Matches exploratory question |
| Getting Started | How to Set Up [Product] in 5 Minutes | Specific, actionable, time-bounded |
| Benefits | Why Do Teams Switch to [Product]? | Social proof framing, matches real query |
| Integrations | What Does [Product] Integrate With? | Question format for discovery |

### E-commerce

| Before | After | Why |
|--------|-------|-----|
| Product Description | What Makes [Product] Different? | Differentiation angle |
| Size Guide | How to Find Your [Product] Size | Actionable, matches "how to" queries |
| Reviews | What Do Customers Say About [Product]? | Social proof, question format |
| Shipping | How Long Does Shipping Take? | Matches the actual question buyers ask |
| Returns | What Is the Return Policy? | Direct question match |

### Content / Publishing

| Before | After | Why |
|--------|-------|-----|
| Overview | What Is [Topic] and Why Does It Matter? | Two-part question covers basics |
| Best Practices | How to [Topic] the Right Way | Actionable, avoids generic label |
| Tools | What Tools Do You Need for [Topic]? | Question format for discovery |
| Examples | What Does Good [Topic] Look Like? | Frames examples as answers |
| FAQ | Frequently Asked Questions | Keep as-is — already a recognized pattern that search and AI engines handle well |

## When NOT to Use Question Format

- **Reference tables** — Column headers should be labels, not questions
- **Changelogs** — Version numbers and dates are the correct format
- **Legal pages** — "Terms of Service", "Privacy Policy" are standard labels
- **API documentation** — Endpoint names, method signatures, parameter lists
- **Step-by-step procedures** — "Step 1:", "Step 2:" reads cleaner than questions for sequential instructions
- **Navigation-heavy pages** — Category pages, directory listings, dashboards

## Heading Hierarchy Validation

A valid hierarchy follows these rules:

1. Exactly one H1
2. H2s follow the H1 (no H3 before the first H2)
3. H3s are children of the preceding H2
4. No level skips (H1 -> H3, H2 -> H4)
5. Headings are not empty
6. Headings are not used purely for styling (check: does removing the heading lose section meaning?)

Run `scripts/analyze-headings.py` against any page to validate the hierarchy automatically and get a GEO heading score based on the question-format ratio.
