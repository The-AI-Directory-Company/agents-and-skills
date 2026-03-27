# Internal Linking Strategy

Internal links distribute link equity, help crawlers discover pages, establish topical relationships, and guide users through your site. They also help AI engines understand your site's knowledge structure — a well-linked site on a topic signals topical authority, making any individual page more likely to be cited.

## How Link Equity Works

Every page on your site has some authority (from external backlinks, age, content quality). Internal links pass a portion of that authority to the pages they link to. This is often called "link juice" or "PageRank flow."

**The practical implication:** your most important pages should receive the most internal links from your most authoritative pages. If your homepage has 50 backlinks and your pricing page has 0, an internal link from the homepage to the pricing page passes some of that authority.

This is not an exact science — Google does not publish the formula. But the directional effect is well-documented: pages with more quality internal links pointing to them tend to rank higher, all else being equal.

## Anchor Text Taxonomy

Anchor text is the clickable text in a link. It tells crawlers, AI engines, and users what the destination page is about. Choosing the right anchor text matters for both SEO and GEO.

| Type | Example | Risk Level | Notes |
|------|---------|------------|-------|
| **Branded** | "Acme Corp" | Safe | Always appropriate. Use for homepage or brand mentions. |
| **Natural/descriptive** | "technical SEO audit guide" | Safe | Most valuable. Describes the destination page's content. |
| **Exact-match keyword** | "technical SEO" | Moderate | Fine in moderation. Over-use (>30% of anchors to one page) looks manipulative. |
| **Generic** | "click here", "learn more", "read this" | Waste | Zero signal value. Tells crawlers and AI nothing about the destination. |
| **Over-optimized** | "best technical SEO audit checklist tool 2026" | High risk | Stuffing multiple keywords into one anchor text triggers spam signals. |
| **Image link (no alt)** | `<a><img src="..."></a>` | Waste | Without alt text, the link passes no anchor signal at all. |

**The rule:** Use natural, descriptive anchor text that tells the reader (and crawlers) what they'll find at the destination. Don't overthink it. Write it as you'd describe the destination page to a colleague.

**Examples:**

```
BAD:  "For more information, click here."
WHY:  "click here" tells crawlers and AI nothing about the destination.

BAD:  "Read our technical SEO guide for a comprehensive overview of
       technical SEO best practices for technical SEO."
WHY:  Over-optimized. Three repetitions of "technical SEO" in one link.

GOOD: "Run a technical SEO audit to identify crawl and indexation issues
       before optimizing individual pages."
WHY:  Descriptive, natural, tells the reader and crawlers what to expect.
```

## Contextual vs Navigational Links

**Contextual links** appear within body content — the middle of a paragraph, within a relevant sentence. These carry the most weight because they're surrounded by topically relevant text that provides additional signal about what the destination page covers.

**Navigational links** appear in headers, sidebars, footers, breadcrumbs, and menus. They're necessary for site usability but carry less ranking signal per link because they appear on every page (site-wide links get their signal diluted).

**Prioritize contextual links.** When you want to boost a page's ranking and citation potential, add in-content links from related articles — not another sidebar widget.

## Links Per Page Target

**Target: 3-5 internal links per 1,000 words of body content.**

- Below 2/1000: Under-linked. You're missing opportunities to distribute equity and help crawlers.
- 3-5/1000: Healthy range. Enough links for discovery and equity flow without overwhelming readers.
- Above 8/1000: Over-linked. Dilutes the signal per link and can feel spammy to readers.

These counts refer to body content links, not navigation/footer/sidebar links which are separate.

## Click Depth Optimization

**Click depth** is the minimum number of clicks from the homepage to reach a page.

- Depth 1: Linked from homepage directly. Maximum authority signal.
- Depth 2: Linked from a page linked from the homepage. Strong.
- Depth 3: Three clicks from homepage. Acceptable for most content.
- Depth 4+: Deep. Search engines may crawl these less frequently. AI engines may underweight them.

**Rule: every important page should be reachable within 3 clicks of the homepage.** Use breadcrumbs, in-content links from high-authority pages, and hub/cluster structures to keep depth shallow.

### Identifying deep pages

Run a site crawl (Screaming Frog, Ahrefs Site Audit) and sort by click depth. Any revenue-generating or high-priority content page at depth 4+ needs additional internal links from shallower pages.

## Link Audit Workflow

1. **Crawl your site** — Use Screaming Frog (free for <500 URLs) or your crawl tool of choice
2. **Map click depth** — Identify pages at depth 4+
3. **Find orphan pages** — Pages with zero internal links pointing to them (only discoverable via sitemap, not via navigation or content links)
4. **Find under-linked pages** — Important pages receiving fewer than 3 internal links
5. **Find over-linked pages** — Pages receiving 50+ internal links (usually navigation/footer links — check if all are necessary)
6. **Audit anchor text** — Flag generic anchors ("click here", "learn more") and over-optimized anchors
7. **Check for broken internal links** — Links pointing to 404 pages waste equity and hurt user experience

Run `scripts/check-internal-links.py --url <URL>` to automate the per-page analysis (link count, anchor text quality, broken link detection).

## GEO Consideration

AI engines follow internal links to build context about your site's expertise. When ChatGPT or Perplexity crawls a page, they also discover linked pages. A well-structured internal link network does two things for GEO:

1. **Increases crawl coverage** — AI bots discover more of your content
2. **Signals topical authority** — A cluster of 10 interlinked pages on "invoice automation" signals deeper expertise than a single standalone page

The practical advice: if you're building topic clusters (and you should be), internal linking is the connective tissue that makes clusters work for both SEO and GEO.
