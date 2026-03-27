# GEO Content Creation Framework

The 8-element method for creating content that ranks in search AND gets cited by AI platforms. This is the definitive reference — it includes the scoring rubric used by `scripts/score-content-geo.py` and detailed guidance for each element.

---

## The core principle

AI engines don't link to your page. They extract passages from it and quote them in synthesized answers. Content that ranks in Google but isn't structured for extraction gets search traffic but zero AI citations. Content structured for both gets traffic AND citation — compounding visibility across channels.

Every element below serves one purpose: making your content extractable, citable, and preferred by AI systems when they choose which 2-7 sources to quote.

---

## Element 1: TLDR First (0-5 points)

### Why it matters

AI engines frequently extract opening content. If your page's first 200 words directly answer the primary question, they become a citation candidate for every query that matches. If your first 200 words are a meandering introduction ("In today's rapidly evolving landscape..."), the AI skips to a competitor who gets to the point.

Search engines also reward this pattern. Google's passage ranking system can surface individual passages, and a strong opening paragraph is the most frequently surfaced passage.

### Before/after example 1: Blog post

**Before (meandering):**
> In today's fast-paced business environment, companies of all sizes are looking for ways to streamline their operations. One area that has seen significant attention is the automation of financial processes. As technology continues to evolve, many organizations are exploring...

**After (TLDR first):**
> Invoice automation reduces manual processing time by 80% and cuts per-invoice costs from $15-40 to $1-3 (Ardent Partners, 2025). It works by using OCR and machine learning to extract data from invoices, match them against purchase orders, and route them for approval — replacing manual data entry, physical routing, and paper-based approvals.

### Before/after example 2: Product page

**Before:**
> Welcome to our platform. We believe in helping businesses grow. Our solution has been trusted by thousands of companies worldwide since 2019...

**After:**
> Acme automates invoice processing end-to-end — from receipt to payment approval in under 2 minutes. It integrates with QuickBooks, Xero, and NetSuite. Plans start at $49/month for up to 500 invoices. 14-day free trial, no credit card required.

### Common failure pattern

Introductions that establish credibility before providing value. "As a leading provider of..." or "With over 10 years of experience..." — nobody cares. Answer the question first, then prove you're credible.

### Quick test

Read only the first 200 words. Do they fully answer the core question someone would ask about this topic? If a colleague who knows nothing about the subject read only those 200 words, would they understand the key point? If no to either, rewrite.

### Scoring criteria

- **5:** First 200 words directly, completely answer the primary question with specific data
- **4:** Direct answer present with some specifics, minor fluff
- **3:** Answer present but buried after 50-100 words of setup
- **2:** Answer partially present, significant filler before it
- **1:** Some relevant content in opening but not a direct answer
- **0:** Meandering intro with no answer in first 200 words

---

## Element 2: Question-Format Headers (0-5 points)

### Why it matters

When users ask AI a question, the engine searches for content with headings that match the query structure. "What Is Invoice Automation?" matches the query "what is invoice automation" directly. "Invoice Automation Overview" requires the AI to infer the match — possible, but the question-format heading wins in tie-breaking.

PAA (People Also Ask) data confirms this: Google surfaces questions because users think in questions. AI engines inherit this pattern.

### Before/after examples

| Before (declarative) | After (question-format) |
|----------------------|------------------------|
| Pricing | How Much Does Invoice Automation Cost in 2026? |
| Features | What Can Invoice Automation Do? |
| Getting Started | How to Set Up Invoice Automation in 5 Minutes |
| Benefits | Why Do Finance Teams Switch to Invoice Automation? |
| Implementation | How Long Does Invoice Automation Take to Implement? |
| Comparison | Invoice Automation vs Manual Processing: Which Saves More? |
| Use Cases | Who Benefits Most from Invoice Automation? |
| Troubleshooting | What to Do When Invoice Automation Fails |

### Common failure pattern

Converting every heading to a question, including procedures and reference tables. "How to Read This Table?" is worse than "Pricing Comparison." Use questions for informational and commercial sections. Use declarative headings for procedures, reference tables, changelogs, and legal content.

### Quick test

Count your H2 headings. What percentage are question-format? For content pages, target 40-60%. Below 30% means you're missing GEO opportunities. Above 70% starts feeling forced.

### Scoring criteria

- **5:** >60% of H2s are question-format, well-phrased, matching real user queries
- **4:** 50-60% question-format, good phrasing
- **3:** 30-50% question-format
- **2:** 15-30% question-format
- **1:** A few question headers present but minority
- **0:** No question-format headers

---

## Element 3: Data Density (0-5 points)

### Why it matters

AI engines preferentially cite content with specific, verifiable data. "Companies reduce costs by 60-80% (Ardent Partners, 2025)" is citable. "Companies reduce costs significantly" is not. The difference is specificity.

Data gives the AI something concrete to quote. Vague claims are interchangeable — any source says the same thing. Specific data with attribution makes your content uniquely citable.

### Before/after example

**Before (vague):**
> Invoice automation significantly reduces processing times and costs for businesses of all sizes.

**After (data-rich):**
> Invoice automation cuts average processing time from 14.6 days to 2.9 days and reduces per-invoice costs from $15.96 to $2.36 (Ardent Partners AP Metrics Report, 2025). Companies processing 10,000+ invoices annually save $136,000 per year on average.

### Common failure pattern

Including data without sources. Unsourced statistics are less citable than sourced ones because AI engines evaluate source reliability. "60% of companies..." (unsourced) < "60% of companies (McKinsey Global Survey, 2025)" (sourced).

### Quick test

Count the specific statistics, percentages, dollar amounts, or dated facts in each 500-word section. Fewer than 2 per section means the content is too vague for AI citation.

### Scoring criteria

- **5:** >3 sourced statistics per 500 words, all with named sources and dates
- **4:** 2-3 sourced statistics per 500 words
- **3:** 1-2 statistics per 500 words, most sourced
- **2:** Some statistics but few sources
- **1:** Occasional numbers without sources
- **0:** No specific data

---

## Element 4: Self-Contained Sections (0-5 points)

### Why it matters

AI engines extract individual sections, not entire articles. Each H2 section must make complete sense if read in isolation. If a section requires reading the previous section to understand, the AI can't cite it — because it would be quoting something incoherent.

### Before/after example 1: Anaphoric reference

**Before (dependent on context):**
> As mentioned in the previous section, this approach works particularly well when combined with the technique described above. It also addresses the limitations we discussed earlier.

**After (self-contained):**
> Three-way matching — comparing invoice data against both the purchase order and receiving report — catches 94% of duplicate payment errors (IOFM, 2025). This technique works because it validates the same transaction from three independent data sources, making it nearly impossible for a fraudulent or duplicate invoice to pass all three checks.

### Before/after example 2: Pronoun-heavy opener

**Before:**
> They found that it reduced costs dramatically. This was consistent across all the industries they studied.

**After:**
> The Ardent Partners 2025 study found that invoice automation reduced processing costs by 60-80% across all industries surveyed, including manufacturing, healthcare, financial services, and technology. The cost reduction was consistent regardless of company size.

### Common failure pattern

Sections that begin with "Additionally..." or "Furthermore..." or "As we saw..." — all of which assume the reader has context from earlier content. Every section opener should restate enough context to stand alone.

### Quick test

Read each H2 section independently, without reading anything before or after it. Does it make sense? Does it provide a complete thought? If you need to scroll up to understand it, restructure.

**Anaphoric reference checklist — eliminate these from section openers:**
- "As mentioned above"
- "This approach" (with no preceding definition in the same section)
- "It" at section start (with unclear referent)
- "The above"
- "See previous section"
- "Furthermore..." / "Additionally..." (implies unstated prior content)
- "As we discussed"

### Scoring criteria

- **5:** Every section stands completely alone, no anaphoric references, clear topic sentences
- **4:** Most sections self-contained, 1-2 minor dependencies
- **3:** Some sections self-contained, some depend on prior context
- **2:** Mixed — some effort at self-containment but frequent references to other sections
- **1:** Most sections depend on prior context
- **0:** Sections are a continuous narrative that only works read sequentially

---

## Element 5: Expert Quotations (0-5 points)

### Why it matters

Named expert quotes serve two functions. For Google, they signal E-E-A-T — the content contains recognized authority voices. For AI engines, they provide pre-formatted citation material. A named quote is the easiest thing for an AI to extract and attribute.

### Before/after example

**Before (unsourced claim):**
> Companies that implement automation see major improvements in their finance operations.

**After (expert quote):**
> "We cut our invoice cycle from 14 days to 2 days after implementing automation. The biggest surprise was the error rate — it dropped from 3.5% to 0.2% in the first quarter." — Mary Chen, VP of Finance at Acme Corp

### Common failure pattern

Generic quotes without specifics. "AI is changing everything" — attributed to a named expert — is still valueless. Quotes must contain specific claims, data, or insights that contribute substance.

### Quick test

For each expert quote: does it contain at least one specific fact, data point, or concrete observation? Would the article be weaker without it? If the quote adds nothing that the surrounding text doesn't already say, replace it with a quote that does.

### Scoring criteria

- **5:** 3+ expert quotes with named attribution, specific credentials, and substantive content
- **4:** 2-3 expert quotes with good attribution
- **3:** 1-2 quotes with named sources
- **2:** Quotes present but vague or poorly attributed
- **1:** One generic quote
- **0:** No expert quotations

---

## Element 6: Source Citations (0-5 points)

### Why it matters

AI engines track source chains. Content that cites its own sources — linking to studies, official documentation, and datasets — signals reliability. The AI reasons: "This content backs up its claims, so I can trust what it says and cite it to my users."

Unsourced content is a liability. If the AI cites you and you're wrong, the AI looks bad. The AI's training/RLHF teaches it to prefer sources that are themselves well-sourced.

### Before/after example

**Before (no sources):**
> AI visibility in search has increased dramatically and many businesses are starting to pay attention.

**After (sourced):**
> AI-referred sessions to websites increased 527% year-over-year in the first five months of 2025 (Brightedge, 2025). ChatGPT alone now reaches 800+ million weekly active users (OpenAI, 2025). This shift has driven 64% of enterprise SEO teams to add GEO-specific strategies to their 2026 plans (Search Engine Land / Conductor survey, 2025).

### Common failure pattern

Citing only your own content or competitor content. External citations should point to primary sources: academic studies, industry reports, official documentation, government data. Self-citations are fine for internal linking but don't build the trust signal that external citations do.

### Quick test

Count external links per article. At least 3-5 external citations to primary sources per 1,500 words. If you can't find sources for your claims, the claims may not be specific enough.

### Scoring criteria

- **5:** 5+ external citations to primary sources (studies, reports, official docs) with dates
- **4:** 3-5 external citations, most to primary sources
- **3:** 2-3 external citations
- **2:** 1-2 citations, some to secondary sources
- **1:** Minimal external references
- **0:** No external citations

---

## Element 7: Original Value (0-5 points)

### Why it matters

Original data is the only unfakeable GEO advantage. If you can run a survey, scrape a dataset, benchmark something, or publish results from direct experience — do it. Everything else can be commoditized. A hundred sites can rewrite the same industry report. Only you can publish your own data.

AI engines have a unique-source preference. When choosing among 10 articles that all cite the same Ardent Partners study, the AI will favor the one that also includes original data — because it adds information the AI can't get elsewhere.

### Before/after example

**Before (commodity content):**
> According to various industry sources, invoice automation typically reduces processing costs by 60-80%.

**After (original value):**
> We analyzed 147 invoices processed before and after implementing automated matching at three client companies (a 200-person manufacturer, a 50-person SaaS company, and a 2,000-person hospital system). Average processing time dropped from 12.3 days to 1.8 days. Cost per invoice fell from $18.40 to $2.10. The hospital system saw the largest improvement — their complex approval chains benefited most from automated routing.

### Common failure pattern

Claiming originality without demonstrating it. "Our unique approach" or "our proprietary methodology" without actually sharing the data or method. Show, don't tell.

### Quick test

Remove all externally-sourced content from your article. What's left? If the answer is "generic connecting sentences," the article has no original value. If the answer includes your own data, framework, case study results, or unique perspective — that's original value.

### Scoring criteria

- **5:** Original data, proprietary framework, or detailed case study with specific results from direct experience
- **4:** Strong original perspective with some supporting original data
- **3:** Some original observations or analysis, beyond just summarizing others
- **2:** Minor original commentary on externally sourced material
- **1:** Attempts at original framing but no unique data or experience
- **0:** Pure aggregation of external sources with no original contribution

---

## Element 8: Author Attribution (0-5 points)

### Why it matters

E-E-A-T depends on visible expertise signals. Google's quality raters check who wrote the content and whether they're qualified. AI engines perform similar credibility assessments — they cross-reference authors across publications to build entity profiles.

An article with a named author, linked bio page, and visible credentials is more likely to rank AND be cited than identical content without attribution.

### Before/after example

**Before:**
> Posted by Admin | March 15, 2026

**After:**
> By [Sarah Chen](https://example.com/team/sarah-chen), Director of Finance Automation at Acme Corp. Sarah has led AP automation projects for 50+ companies since 2019.
> Last updated: March 15, 2026

### Common failure pattern

Author page exists but contains only a name and headshot. The page must include: bio (2-3 paragraphs), credentials, links to social profiles (LinkedIn, Twitter), and links to other published work by the same author.

### Quick test

Can you answer these three questions by looking at the article?
1. Who wrote it? (name visible)
2. Why are they qualified? (credentials visible)
3. What else have they written? (link to author page with more work)

If any answer is no, author attribution is incomplete.

### Scoring criteria

- **5:** Named author with linked bio page containing photo, credentials, social links, and other published work
- **4:** Named author with linked bio page, most details present
- **3:** Named author with some credentials visible
- **2:** Named author but no link to bio or credentials
- **1:** Generic attribution ("Team" or "Admin")
- **0:** No author attribution

---

## Scoring Rubric Summary

This rubric is implemented by `scripts/score-content-geo.py`.

| Element | Points | What it measures |
|---------|--------|-----------------|
| TLDR first | 0-5 | Does the opening answer the question directly? |
| Question headers | 0-5 | Do H2s match how users ask questions? |
| Data density | 0-5 | Are claims backed by specific, sourced data? |
| Self-contained sections | 0-5 | Can each section be extracted independently? |
| Expert quotations | 0-5 | Are recognized authorities quoted with attribution? |
| Source citations | 0-5 | Does the content cite primary external sources? |
| Original value | 0-5 | Does the content add something no competitor has? |
| Author attribution | 0-5 | Is the author named, credentialed, and linked? |
| **Total** | **0-40** | |

### Score interpretation

| Score | Rating | What it means |
|-------|--------|--------------|
| 0-10 | Not citable | Content is too vague, unsourced, or poorly structured for AI citation. Major rework needed. |
| 11-20 | Partially citable | Some elements present but significant gaps. AI may cite if no better source exists, but won't prefer you. |
| 21-30 | Good — citation-ready | Solid content that AI engines will cite for relevant queries. Focus on weak elements to push higher. |
| 31-40 | Excellent — high citation potential | Well-structured, data-rich, authoritative content. Top-tier citation candidate. |

### The feedback loop

Run `scripts/score-content-geo.py` on your content before publishing. Fix the lowest-scoring elements. Run it again. Repeat until you hit 25+. After publishing, run it again in 3 months during your content refresh — scores may change as you add or lose data freshness.

---

## Passage extraction simulation

The ultimate quality test: read each H2 section as if you're an AI engine that needs to quote exactly 2-3 sentences from it to answer a user's question.

For each section, ask:
1. **Can I extract 2-3 sentences that fully answer a question?** If not, the section needs restructuring.
2. **Do those sentences make sense without the rest of the article?** If not, add context to make them self-contained.
3. **Do those sentences contain specific, verifiable information?** If not, add data and sources.
4. **Is a human expert's perspective represented?** If not, consider adding a quote or first-hand observation.

If every section passes this test, the article is citation-ready. If fewer than half pass, the article needs significant rework before it will earn consistent AI citations.
