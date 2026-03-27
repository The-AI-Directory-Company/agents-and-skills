# Content Refresh Strategy

How to identify, prioritize, and execute content updates that maintain rankings and citation eligibility.

---

## Why content decays

Published content loses value over time through four mechanisms:

1. **Data aging.** Statistics from 2024 in a 2026 article signal staleness to both search engines and AI. AI engines specifically prefer recent data — a "2025 report" cited in March 2026 beats a "2023 study" every time.
2. **Competitive displacement.** Competitors publish newer, more comprehensive articles on the same topic. If they cover angles you missed or include fresher data, they rank above you.
3. **Intent shift.** The search intent behind a keyword can change. "Remote work tools" in 2020 was informational. By 2026 it's commercial. Content that matched the old intent stops ranking.
4. **Freshness signal decay.** Google and AI engines track content age. A page with no updates in 18 months is deprioritized against one updated 2 months ago — even if the underlying content is equivalent.

Maintenance is as important as creation. A 2024 guide loses to a 2026 article on the same topic, every time.

## 3-tier refresh model

### Tier 1: Optimizations (under 15% changes)

Small, continuous updates that maintain existing performance.

**What to change:**
- Update meta title and description (refresh the value proposition, add current year)
- Add internal links to content published after the original article
- Improve CTAs based on current conversion data
- Fix broken outbound links
- Add FAQ Schema if not present
- Update the "Last modified" date in schema (only after making substantive changes)

**When:** Continuously, as new content is published. Budget 15 minutes per page.

**Expected impact:** Maintains existing rankings, slightly improves CTR from refreshed titles.

### Tier 2: Upgrades (15-70% changes)

Substantive improvements to strengthen competitive position.

**What to change:**
- Refresh all statistics with 2025-2026 data
- Add 1-2 new sections covering developments since original publication
- Replace or supplement expert quotes with current sources
- Improve visual content (add diagrams, update screenshots)
- Enhance GEO elements: strengthen TLDR opening, convert declarative H2s to questions, add source citations
- Add original data or insights accumulated since publication

**When:** Every 3-6 months for pages that rank in positions 1-20. Priority to pages at positions 4-15 (cheapest wins).

**Expected impact:** Position improvements of 2-5 places within 2-4 weeks. Renewed AI citation eligibility.

### Tier 3: Rewrites (70%+ changes)

Complete overhauls for content that no longer works.

**When to rewrite:**
- The page's angle no longer matches search intent (intent has shifted)
- The topic has fundamentally changed (regulations, technology, market conditions)
- The content was never good enough (thin, poorly structured, no original value)
- Competitor content is so far ahead that incremental updates can't close the gap

**How to rewrite without losing existing equity:**
- Keep the same URL (never change it during a rewrite)
- Keep the same primary keyword target
- 301 redirect if URL change is absolutely necessary
- Resubmit to GSC after publishing the rewrite

**Expected impact:** Treat as new content. 3-6 months to see ranking effects.

## Identifying refresh candidates from GSC data

### Position decay

GSC > Performance > Pages > Compare last 3 months to previous 3 months. Sort by position change. Pages that dropped from positions 1-10 to 11-20 are your highest priority — they were ranking well and lost ground.

**Action:** Tier 2 upgrade. Find what competitors published that displaced you. Match or exceed their coverage.

### CTR decay

Filter to pages with stable impressions but declining CTR. The page appears in results as often as before, but fewer people click. The title and description are fatiguing.

**Action:** Tier 1 optimization. Rewrite the meta title and description. Test a new angle or add a current-year qualifier.

### High impressions, low position

Pages at positions 4-15 with high impression counts. These pages are visible but not winning clicks. Small improvements yield disproportionate returns because CTR jumps significantly between positions 10 and 3.

**Action:** Tier 2 upgrade. This is the highest-ROI refresh work you can do.

### Stale by age

Pages older than 12 months that have never been updated. Even if ranking well today, these are vulnerable to newer competitors.

**Action:** Tier 2 upgrade minimum. Check competitor content published in the last 6 months on the same topic.

## Refresh prioritization framework

Process refresh candidates in this order:

1. **Position 4-15 pages** — cheapest wins, highest ROI
2. **Position-declining pages** — catch decay before it becomes a rewrite
3. **High-impression, low-CTR pages** — title/description optimization
4. **Pages >12 months without updates** — proactive decay prevention
5. **Pages with new internal linking opportunities** — quick optimization when new cluster content is published

## Update workflow that preserves rankings

Follow this process to update content without risking existing rankings:

1. **Don't change the URL.** Ever. If you must, 301 redirect.
2. **Keep the core topic and primary keyword the same.** Changing the topic angle can confuse Google about what the page is about.
3. **Add content, don't remove ranking content.** A section that ranks for a long-tail keyword should be kept and improved, not deleted. Use GSC to check which queries drive traffic to this specific page before removing anything.
4. **Update visible dates honestly.** Change "Last updated" to today's date. Update dateModified in schema. Only do this when you've made substantive changes.
5. **Update data and sources.** Replace 2024 statistics with 2025-2026 data. Replace dead source links.
6. **Resubmit URL to GSC.** After publishing updates, use GSC > URL Inspection > Request Indexing. This prompts a re-crawl.

## Substantive vs cosmetic changes

Search engines can detect cosmetic-only updates. Changing only the date, moving paragraphs around, or adding a single sentence is not a substantive update and can erode trust if detected.

**Substantive changes include:**
- New sections with original content (200+ words)
- Updated statistics with new sources
- New expert quotes
- Fresh examples or case studies
- Additional data points

**Cosmetic changes (don't qualify as a real update):**
- Changing the "Last updated" date without other changes
- Reordering existing paragraphs
- Rewording sentences without adding information
- Adding a single internal link

Updating the date without changing substance is worse than doing nothing — Google can detect it and it erodes trust.

## Refresh tracking template

Track all content refreshes in a single document:

```
| URL                          | Current Pos. | Last Updated | Traffic Trend | Refresh Type  | Priority | Status  |
|------------------------------|-------------|-------------|---------------|---------------|----------|---------|
| /guide/invoice-automation    | 6           | 2025-08-14  | Declining     | Upgrade       | High     | Planned |
| /blog/ap-best-practices      | 14          | 2025-03-20  | Flat          | Optimization  | High     | Done    |
| /glossary/three-way-matching | 3           | 2025-11-01  | Growing       | None needed   | Low      | --      |
```

Review this table monthly. Update statuses. Reprioritize based on current GSC data.

## GEO freshness considerations

AI engines weigh recency heavily. A page updated in the last 3 months with current-year statistics is significantly more likely to be cited than one with 2024 data. This creates a specific GEO incentive for regular refreshes:

- **Update statistics quarterly** in your highest-value pages
- **Add "Last updated" timestamps** to every content page (visible to users, not just in schema)
- **Reference current-year data** explicitly: "In 2026..." signals freshness to AI engines
- **Remove or update outdated predictions** — if your 2024 article predicted "by 2025, AI will..." and that year has passed, update the prediction to reflect what actually happened
