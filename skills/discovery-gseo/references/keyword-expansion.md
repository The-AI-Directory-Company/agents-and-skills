# Keyword Expansion

Expansion is where 15-30 seeds become 200-1000+ keyword candidates. The goal is volume and breadth — you want every possible variation, question, and angle. Filtering comes later.

Google Keyword Planner gives you ranges. Ubersuggest gives you estimates. Ahrefs gives you data. Use whichever you can afford — the process works with any of them.

## Tool-by-tool expansion guides

### Google Keyword Planner (free)

The baseline tool everyone has access to through a Google Ads account.

**Step by step:**
1. Go to Google Ads > Tools > Keyword Planner > "Discover new keywords."
2. Enter one seed keyword (e.g., "invoicing software").
3. Set your target country and language.
4. Click "Get results."
5. View related keywords with average monthly search volume ranges and competition level.
6. Download as CSV. Repeat for each seed.

**What you get:** Related keyword suggestions with volume ranges (e.g., "1K-10K"), competition level (Low/Medium/High — based on ad competition, not organic SEO), and suggested bid (useful as a proxy for commercial value).

**Limitations:**
- Volume is a range, not an exact number. "1K-10K" is a massive spread.
- Competition metric reflects ad competition, not organic ranking difficulty. A keyword with "Low" ad competition can still have high organic difficulty.
- Suggestions are biased toward commercial queries (Google wants you to buy ads).
- No click data — some high-volume keywords have low clicks due to zero-click SERP features.

**When to use it:** Always, as a baseline. Even if you have paid tools, Keyword Planner sometimes surfaces suggestions others miss.

### Ahrefs Keywords Explorer

The most intuitive paid tool for keyword expansion.

**Key features for expansion:**
- **Matching terms:** Keywords containing your exact seed phrase. "invoicing software" → "free invoicing software", "best invoicing software for freelancers."
- **Related terms:** Semantically related keywords that may not contain your seed. "invoicing software" → "billing tool", "send receipts online."
- **Questions:** Queries phrased as questions. "How to create an invoice", "what is the best invoicing app."
- **Also rank for:** Other keywords that pages ranking for your seed also rank for. Often reveals tangential opportunities.

**Pro tip:** The "Clicks" metric is unique to Ahrefs. Some high-volume keywords have low clicks because of Featured Snippets or zero-click results. Always check Clicks alongside Volume to assess real traffic potential.

Export each view. Repeat for all seeds.

### Semrush Keyword Magic Tool

The largest keyword database (20B+ keywords). Best for discovering long-tail variations.

**Key features:**
- Enter a seed, get thousands of variations organized by subtopics.
- Auto-grouped into clusters — helpful for Phase 8 (topic clustering).
- Intent classification built in (Informational, Navigational, Commercial, Transactional).
- Keyword Gap tool: compare up to 5 domains at once to find missing keywords.

**Pro tip:** The subtopic grouping in Keyword Magic Tool gives you a head start on clustering. Export the groups, not just the flat list.

### Ubersuggest

Budget-friendly with a strong lifetime deal (~$120 one-time).

**Key features:**
- Keyword Ideas: related keywords with volume, KD, and CPC.
- Questions: question-based keywords for informational content.
- Related: semantically connected terms.
- Content Ideas: top-performing content for your keyword (useful for competitor analysis too).

**Limitation:** Data accuracy is lower than Ahrefs or Semrush. Volume estimates can be off by 30-50%. KD scores tend to be optimistic (showing keywords as easier than they are).

**When to use it:** When paid tools are the only option and budget is tight. The data is less precise but still sufficient for the process.

### AnswerThePublic

Specialized in question and preposition expansions. 3 free searches per day.

**What it generates:**
- Questions: who/what/where/when/why/how + your keyword
- Prepositions: "[keyword] for [use case]", "[keyword] with [feature]", "[keyword] without [limitation]"
- Comparisons: "[keyword] vs [alternative]", "[keyword] or [alternative]"
- Alphabetical: "[keyword] a", "[keyword] b"... through z

**Best for:** Finding question-based content ideas and comparison angle keywords. Use your broadest seed keywords to maximize the 3 free daily searches.

## Browser automation expansion

Browser automation is the expansion technique that no other tool replicates. You get real-time, localized, intent-rich suggestions directly from Google's own systems.

### Autocomplete technique

Google Autocomplete shows real-time suggestions based on what people actually search. These suggestions are localized, personalized (in non-incognito), and updated frequently.

**How it works:**
1. Open Google in an incognito browser via Playwright MCP.
2. Focus the search input.
3. Type your seed keyword character by character (with 100-200ms delays to trigger suggestions).
4. After typing the full seed: wait 500ms, capture the suggestion dropdown.
5. Append each letter a-z: type 'a', wait, capture suggestions, clear the letter, type 'b', repeat.
6. Prepend question words: "how to [seed]", "what is [seed]", "best [seed]", "why [seed]" — capture suggestions for each.

**Why this beats WebSearch:** WebSearch returns search results, not Autocomplete suggestions. Autocomplete data is a different signal — it reflects real-time query patterns that tools cannot replicate. You get suggestions that keyword tools miss because the volume is too low for tools to register, but real people are searching.

Run `scripts/harvest-autocomplete.py --seeds 'seed1,seed2,seed3'` to automate this entire process.

**Rate limiting:** Wait 2-5 seconds between searches to avoid triggering captchas. Do not exceed 20-30 unique seed expansions per session. If a captcha appears, pause for 5 minutes, clear cookies, and restart.

### PAA technique

People Also Ask boxes are a goldmine. Each question reveals 2-3 more questions when clicked, creating an expanding tree of related queries.

**How it works:**
1. Search for a seed keyword (press Enter).
2. Wait for the results page to fully load.
3. Find the PAA box (usually between organic results 2-4).
4. Click each question to expand it — the answer appears, AND Google adds more questions below.
5. After each click, wait 1-2 seconds for new questions to load.
6. Keep clicking newly revealed questions until no new ones appear or you have 50+.
7. Extract: question text, answer snippet, source URL.

**Why this matters:** PAA questions are real queries that real people ask. Each one is a potential H2 heading in a guide, a standalone blog post, or an FAQ entry. The source URLs show you who currently answers these questions — your competition for that specific question.

Run `scripts/extract-paa.py --seeds 'seed1,seed2'` to automate PAA expansion.

### Related Searches chaining

Related Searches appear at the bottom of Google SERPs. Clicking one takes you to a new SERP with its own Related Searches — creating a chain of lateral keyword ideas.

**How it works:**
1. Search for a seed keyword.
2. Scroll to the bottom of the SERP.
3. Extract all Related Searches (typically 8 links).
4. Click each Related Search (level 2).
5. Scroll to the bottom of each level-2 SERP, extract those Related Searches.
6. Deduplicate across all levels.

**Why this matters:** Related Searches reveal lateral keyword ideas — terms that are semantically connected to your seed but might not contain any of the same words. This is how you discover angles that tools miss.

Run `scripts/scrape-related-searches.py --seeds 'seed1,seed2'` for 2-level chaining.

**Rate limiting:** Wait 3-5 seconds between page navigations. Related Searches chaining requires multiple page loads per seed, so limit to 5-10 seeds per session.

## Volume and KD interpretation across tools

Different tools use different scales. Do not compare numbers cross-tool.

**Ahrefs KD vs Semrush KD:** Both use 0-100 but calibrate differently. Ahrefs KD 30 is not the same as Semrush KD 30. Ahrefs bases KD primarily on the number of backlinks needed to rank in the top 10. Semrush uses a broader set of signals. In general, Ahrefs KD scores tend to run slightly lower than Semrush for the same keyword.

**Google Keyword Planner ranges vs paid tool exact data:** Keyword Planner says "1K-10K." Ahrefs might show 2,400. Ubersuggest might show 3,100. The exact number does not matter much — what matters is the relative scale (is this a 100/mo keyword or a 10,000/mo keyword?).

**Free proxy for KD:** If you have no paid tools, search the keyword on Google and count how many high-DA domains appear in the top 10. If the top 10 is all Forbes, HubSpot, and Wikipedia, difficulty is very high regardless of what any tool says. If the top 10 includes small blogs with modest design, difficulty is likely manageable.

**Ahrefs "Clicks" metric:** Unique to Ahrefs and underappreciated. Some keywords have high volume but low clicks because Google answers the query directly (Featured Snippet, Knowledge Panel, calculator, etc.). Always check Clicks alongside Volume.

## Zero-volume keywords

Tools show 0 because the volume is too low to measure — not because nobody searches for them. Real people do search these terms.

Zero-volume keywords are valuable when:
- **Intent is strong:** "invoicing software for freelancers who use Stripe" has perfect buyer intent even if tools show zero volume.
- **They aggregate:** 50 zero-volume keywords targeting the same topic, grouped into one comprehensive page, can collectively drive meaningful traffic.
- **They are emerging:** New trends start as zero-volume keywords before tools pick them up. Community listening (Phase 5) often surfaces these first.

Do not filter out zero-volume keywords automatically. Evaluate them on intent and business relevance, not just volume.

## Expansion output management

### Deduplication during expansion

As you pull keywords from multiple tools and techniques, duplicates accumulate fast. Deduplicate continuously:
- Normalize case (lowercase everything)
- Normalize spacing (remove extra spaces, trim)
- Merge near-synonyms: "invoice software" and "invoicing software" target the same SERP. Keep the higher-volume version.
- Flag but do not delete plural variants: "invoice template" vs "invoice templates" — Google treats these similarly but not identically. Keep both during expansion, merge during evaluation.

### Tracking keyword sources

Tag every keyword with its source as you collect them. This matters for two reasons:
1. **Quality assessment:** Keywords from competitor gap analysis are pre-validated (someone already ranks). Keywords from your brain are unvalidated assumptions. Knowing the source helps prioritize.
2. **Coverage gaps:** If 90% of your keywords come from one tool, you are missing what the other sources reveal. Aim for keywords from at least 3 of the 5 sources.

Source tags: `brain`, `competitor_gap`, `tool_expansion`, `google_autocomplete`, `google_paa`, `google_related`, `community`, `answerthepublic`.

### When to stop expanding

Stop when you hit 200-1000+ raw keyword candidates. The exact number depends on your niche:
- **Narrow niche** (HIPAA-compliant form builders): 200-400 keywords is a full universe.
- **Broad category** (project management software): 1000+ keywords is normal.
- **Multi-product business:** Run the expansion for each product line separately.

More keywords is not always better. Beyond 1000, you spend more time filtering than discovering. If you have 500 quality candidates, move to evaluation.

### GEO expansion layer

After tool-based expansion, cross-reference your expanded list with GEO data from Phase 1. Keywords that match topics mentioned by AI platforms get a GEO flag. During evaluation (Phase 6), these flags become GEO scores. This is not extra work — it is connecting data you already have from the seed validation step.
