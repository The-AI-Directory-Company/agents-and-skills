# Meta Tag Optimization

Title tags and meta descriptions are the first impression your page makes — in search results, social shares, and AI summaries. Get them wrong and you lose clicks before anyone reads a word of your content.

## Title Tag

The title tag is the single strongest on-page ranking signal. It appears in browser tabs, search result headlines, and social shares. AI engines use it to understand page topic and sometimes pull it verbatim into citations.

**Hard constraints:**

- 60 characters max (Google truncates at ~580px — 60 chars is the safe ceiling)
- Front-load the primary keyword — the first 3-5 words carry the most weight
- One keyword, one page — do not stuff multiple keywords separated by pipes
- Be specific and outcome-oriented — vague labels get ignored

**Pixel width matters more than character count.** Uppercase letters and wide characters (W, M) eat more pixels. "MAMMOGRAM SCREENING" is wider than "technical seo checklist" at the same character count. Use SERP preview tools (Mangools SERP Simulator, Portent's Title Tag Preview) to check actual rendering.

**If your title starts with your brand name, you're wasting the most valuable real estate on the page — unless you're Nike.** Brand goes at the end, separated by a dash or pipe, and only if you have room.

### Good vs bad by industry

**SaaS:**
```
BAD:  "Acme | Invoice | Automation | Software | Best"
WHY:  Pipe-separated keyword stuffing. No value proposition. Spam signal.

GOOD: "Invoice Automation Software: Cut Processing Time 80% | Acme"
WHY:  Keyword front-loaded, specific outcome (80%), brand at end.
```

**E-commerce:**
```
BAD:  "Buy Shoes Online — Best Shoes — Running Shoes Sale"
WHY:  Three keyword variations crammed together. Reads like spam.

GOOD: "Women's Running Shoes — Free Shipping Over $50 | BrandName"
WHY:  Specific product, clear benefit (free shipping), brand last.
```

**Content / Blog:**
```
BAD:  "SEO Guide | Best SEO Tips | SEO Company"
WHY:  Three repetitions of "SEO" in one title. No specificity.

GOOD: "What Is Technical SEO? A 15-Point Checklist for 2026"
WHY:  Question format (GEO-friendly), concrete number, date signals freshness.
```

## Meta Description

Meta descriptions do not directly affect ranking — Google confirmed this years ago. But they control CTR from search results and are often extracted by AI engines as page summary text. Treat them as ad copy for your page.

**Rules:**

- 155 characters max (Google truncates around 920px on desktop)
- Write it as a complete, factual sentence — AI engines sometimes cite meta descriptions verbatim
- Include the primary keyword naturally (Google bolds matching terms in results)
- Use active voice and a clear benefit statement
- Do not duplicate descriptions across pages — unique per page or leave blank (Google will auto-generate)

**Good vs bad:**

```
BAD:  "We are the best SEO company. Learn about SEO on our blog."
WHY:  Self-promotional, no value proposition, no keyword alignment.

GOOD: "A 15-point technical SEO checklist covering crawl errors, indexation,
       Core Web Vitals, and structured data — with fix instructions for each."
WHY:  Describes exactly what the reader gets. Complete sentence an AI could cite.
```

## Open Graph Tags

OG tags control how your page appears when shared on social platforms, messaging apps, and some AI interfaces that render cards.

**Required OG tags:**

| Tag | Purpose | Rules |
|-----|---------|-------|
| `og:title` | Social share headline | Can differ from `<title>` — optimize for social context, not search |
| `og:description` | Social share summary | Can be longer than meta description (up to 300 chars) |
| `og:image` | Share image | 1200x630px minimum, under 8MB, absolute URL |
| `og:type` | Content type | `website` for homepages, `article` for blog/content pages |
| `og:url` | Canonical URL | Must match `<link rel="canonical">` |

**Twitter card tags** (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`) overlap with OG tags. If both are set, Twitter uses its own. If only OG is set, Twitter falls back to OG values. Set both when you want different messaging for Twitter vs other platforms.

## Canonical Tag

The canonical tag tells search engines which URL is the "official" version of a page when duplicates exist.

**Rules:**

- Every indexable page should have a self-referencing canonical: `<link rel="canonical" href="https://example.com/current-page">`
- Always use absolute URLs (not relative)
- Place in `<head>`, as early as possible
- The canonical URL must return a 200 status code
- If content exists at multiple URLs (HTTP/HTTPS, www/non-www, parameterized), all versions should canonical to one

**Common mistake:** CMS generates canonical tags pointing to the wrong URL — pagination pages canonicalizing to page 1, filtered views canonicalizing to the unfiltered page. Audit these with your structured data script.

## Meta Robots Tag

The `<meta name="robots">` tag controls whether search engines index a page and follow its links.

**Common directives:**

- `index, follow` — Default behavior (can omit the tag entirely)
- `noindex, follow` — Don't index this page, but follow links on it (useful for tag pages, internal search results)
- `noindex, nofollow` — Don't index, don't follow links (staging pages, admin pages)
- `max-snippet:-1` — Allow search engines to show any length snippet (good for GEO — lets AI engines extract longer passages)

**GEO consideration:** If you set `max-snippet:0` or short snippet lengths, you're telling AI engines they cannot extract text from your page. For pages you want AI to cite, use `max-snippet:-1` or omit snippet restrictions entirely.
