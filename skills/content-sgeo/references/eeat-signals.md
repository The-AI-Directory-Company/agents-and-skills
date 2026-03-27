# E-E-A-T Implementation Guide

How to build Experience, Expertise, Authoritativeness, and Trustworthiness signals into every piece of content — for both Google rankings and AI citation selection.

---

## What quality raters actually look for

Google employs thousands of quality raters who evaluate search results using the Search Quality Evaluator Guidelines. Their assessments don't directly affect rankings, but they train the algorithms that do. Understanding what raters look for tells you what the algorithms are learning to detect.

### Experience

First-hand involvement with the topic. Raters ask: "Has this person actually done what they're writing about?"

**Strong signals:**
- Original photos or screenshots from real projects (not stock images)
- Specific results: "We tested this on 3 client sites and saw a 40% increase in organic traffic over 4 months"
- Nuanced observations that only come from direct involvement: "The vendor's documentation says setup takes 30 minutes. In practice, expect 2-3 hours because their API rate limits aren't mentioned anywhere."
- Named clients or case studies (with permission)

**Weak signals:**
- "In our experience..." without specific details
- Generic advice that could come from reading other articles
- Stock photography accompanying first-person claims

### Expertise

Deep domain knowledge demonstrated through the content itself — not just claimed in a bio.

**Strong signals:**
- Covers edge cases and exceptions, not just the happy path
- Addresses counterarguments and explains why they don't apply (or when they do)
- Technical accuracy at a level that practitioners would recognize and respect
- Explains "why" behind recommendations, not just "what" to do
- Correctly uses domain-specific terminology

**Weak signals:**
- Surface-level summaries that a 10-minute search could produce
- Incorrect use of technical terms
- Missing obvious edge cases that any practitioner would know about

### Authoritativeness

Recognition from others in the field. Raters ask: "Is this person/site a recognized authority on this topic?"

**Strong signals:**
- Backlinks from other authoritative sites in the same domain
- Author published in recognized industry publications
- Author cited by other experts
- Site recognized as a go-to resource in its niche
- Author holds relevant certifications or professional credentials

**Weak signals:**
- Self-proclaimed authority ("We're the leading...")
- Authority in an unrelated field (a dentist writing about software architecture)
- Backlinks from irrelevant or low-quality sites

### Trustworthiness

Transparency, accuracy, and accountability. The overarching factor — a site can have experience, expertise, and authority but fail on trust.

**Strong signals:**
- All claims cite primary sources with dates
- Content transparently acknowledges limitations: "This approach works best for B2B SaaS — results may differ for e-commerce."
- Clear contact information accessible from every page
- Editorial policy describing how content is researched, fact-checked, and updated
- Corrections policy — what happens when content is found to be incorrect
- HTTPS (non-negotiable baseline)
- "Last updated" dates that are visible and accurate

**Weak signals:**
- Unsourced statistics
- No acknowledgment of limitations or exceptions
- No visible contact information
- Dates that appear updated but content hasn't substantively changed

## December 2025 update impact

Google's December 2025 core algorithm update extended E-E-A-T evaluation to ALL competitive queries, not just YMYL (Your Money or Your Life) topics. Previously, E-E-A-T scrutiny was heaviest on health, finance, and legal content. Now, every topic where multiple sites compete for rankings gets the same level of E-E-A-T assessment.

What this means in practice:
- A blog post about "best project management tools" now gets the same E-E-A-T scrutiny as a blog post about "best investment accounts"
- Author credentials matter for technology, marketing, design, and every other competitive niche
- Sites without visible expertise signals are losing rankings to sites that have them — even when the content quality is similar

## How AI engines assess author credibility

AI engines build entity graphs. When they encounter an author name, they cross-reference it across:
- Other publications by the same author
- LinkedIn profile and credentials
- Social media presence and engagement
- Citations by other recognized sources
- Conference presentations and podcast appearances

An author with a consistent, visible presence across multiple credible platforms is more likely to have their content cited by AI engines. An anonymous article from "Admin" has no entity signal for the AI to evaluate.

This is why author pages matter. They create a centralized node in the AI's entity graph for your author, connecting their identity to their expertise, publications, and credentials.

## Author page template

Every author who publishes on your site needs a dedicated author page. Minimum viable author page:

```
# [Full Name]

[Photo — professional headshot, not an avatar or stock image]

## About [First Name]

[2-3 paragraphs covering:]
- Current role and company
- Relevant experience (years in field, specific achievements)
- Areas of expertise (what topics they're qualified to write about)
- Notable projects or results

## Credentials

- [Job title] at [Company] (current)
- [Previous relevant role] at [Previous company]
- [Certification or degree relevant to the content area]
- [Industry award or recognition, if applicable]

## Connect

- [LinkedIn](URL)
- [Twitter/X](URL)
- [GitHub](URL) (if relevant)
- [Personal website](URL)

## Published Work

- [Article title 1](internal link)
- [Article title 2](internal link)
- [External publication: "Article Title"](external link)
```

### What makes a good author page

- **Specific credentials.** "10 years in marketing" is weaker than "Led content strategy for 3 B2B SaaS companies, growing organic traffic from 0 to 50K monthly visits at Acme Corp."
- **Real photo.** AI engines can detect stock photos. Use an actual headshot.
- **Active social links.** Links that go to real, active profiles — not dormant accounts created solely for E-E-A-T purposes.
- **Published work list.** Both internal articles and external publications. This creates the cross-reference signals AI engines use to evaluate expertise.

## Editorial policy template

An editorial policy page signals institutional trustworthiness. It tells both quality raters and AI engines: "We have a process for ensuring accuracy."

```
# Editorial Policy

## How we research content

[Describe your research process: primary source review, expert interviews,
data verification steps]

## Fact-checking

[Describe who reviews content before publication, what gets checked,
how claims are verified against sources]

## Author qualifications

[Explain how authors are selected for topics — they must have
relevant experience or credentials]

## Update policy

[How often content is reviewed. Which pages are prioritized for updates.
How you handle outdated statistics.]

## Corrections

[What happens when an error is found. How corrections are communicated.
Whether a correction notice is added to the article.]

## Contact

[How to reach the editorial team with corrections, questions,
or feedback. Email address.]
```

This page doesn't need to be long. It needs to be honest and specific. "We thoroughly research all content" is weak. "Every article is reviewed by a subject matter expert with 5+ years in the relevant field, and all statistics are verified against primary sources" is strong.

## Per-article E-E-A-T checklist

Run this checklist for every article before publishing:

### Author signals
- [ ] Author byline visible near the article title or opening
- [ ] Author name links to a dedicated author page
- [ ] Author page has bio (>100 words), photo, credentials, social links
- [ ] Author is qualified to write about this specific topic (credentials match content area)

### Experience signals
- [ ] Article includes at least one first-hand experience, case study, or original observation
- [ ] Specific results or data from direct involvement (not just industry reports)
- [ ] Original screenshots, photos, or materials (not stock images)

### Expertise signals
- [ ] Article covers edge cases and exceptions, not just the basic scenario
- [ ] Addresses at least one counterargument or limitation
- [ ] Technical accuracy verified by someone with domain knowledge
- [ ] Domain-specific terminology used correctly

### Trust signals
- [ ] All statistics cite primary sources with dates
- [ ] At least 3-5 external citations to authoritative sources per article
- [ ] Article acknowledges limitations or cases where advice doesn't apply
- [ ] "Last updated" date visible and accurate (matches actual last edit)
- [ ] Contact information accessible from the page (footer link or explicit contact)

### Structural signals
- [ ] Article Schema (JSON-LD) includes author (Person type), datePublished, dateModified
- [ ] Author entity in schema links to author page URL
- [ ] Publisher entity in schema links to organization with logo

## Building E-E-A-T over time

E-E-A-T is not a one-time checkbox. It compounds:

1. **Month 1-3:** Establish author pages, editorial policy, and per-article E-E-A-T checklist compliance.
2. **Month 3-6:** Build the author's external presence — guest posts on industry sites, podcast appearances, LinkedIn publishing. These create cross-reference signals.
3. **Month 6-12:** Accumulate citations from other sites, speaking engagements, and original research publications. Track which authors drive the most organic traffic and AI citations.
4. **Ongoing:** Update author pages with new credentials, publications, and achievements. Update articles with fresh data and experiences. The author's entity profile grows stronger with every new signal.

## E-E-A-T for AI citation specifically

AI engines assess E-E-A-T differently from Google's algorithm, but the signals overlap:

- **Author recognition:** If an AI engine has seen the author's name associated with authoritative content across multiple sources, it's more likely to cite them.
- **Source chain quality:** AI engines prefer content that cites its sources, because the AI can trace the claim back to the original data. Unsourced claims are risky for the AI to repeat.
- **Recency of expertise:** An author whose latest publication is from 2022 may be discounted compared to one actively publishing in 2026. Keep author profiles current.
- **Specificity of claims:** "AI improves marketing" (no E-E-A-T signal) vs "AI-personalized email campaigns achieve 26% higher open rates (Salesforce State of Marketing, 2025)" (strong signal). The specific claim with a source is citable. The vague claim is not.

E-E-A-T is not a checklist you bolt on after writing. It's a content philosophy. If you don't have genuine expertise on a topic, find someone who does and put their name on it. Manufactured expertise is detectable — by quality raters, by algorithms, and increasingly by AI engines that cross-reference author entities.
