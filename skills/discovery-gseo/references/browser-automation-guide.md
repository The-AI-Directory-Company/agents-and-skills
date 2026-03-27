# Browser Automation Guide

Browser automation is the superpower that turns this skill from keyword research into live market intelligence. WebSearch gives you results. Playwright gives you the SERP.

Google's SERP is a dynamic, JavaScript-rendered application. Autocomplete, People Also Ask, AI Overviews, Related Searches, Knowledge Panels — these features are not available through simple HTTP fetches or search APIs. They require a real browser. Browser automation gives you the same data a human researcher sees, at scale.

## Why browser automation matters for discovery

**What browser automation captures that WebSearch cannot:**
- Google Autocomplete suggestions (real-time, localized, typed character by character)
- People Also Ask expansion (click to reveal, cascading new questions)
- AI Overview presence and content (JavaScript-rendered overlay)
- Related Searches (bottom of SERP, dynamic content)
- SERP feature detection (Featured Snippets, Knowledge Panels, Video carousels, Local packs)
- Visual SERP layout (above/below fold positioning, feature placement relative to organic results)
- Full-page screenshots for documentation and change tracking

WebSearch returns structured results — useful, but limited. It misses the dynamic, interactive elements that contain the highest-value discovery data.

## Playwright MCP tool reference

These are the exact Playwright MCP tool calls used throughout this skill's scripts.

### Core tools

**`browser_navigate`** — Navigate to a URL.
```
Tool: browser_navigate
Args: {"url": "https://www.google.com/search?q=invoicing+software&gl=us&hl=en"}
```
Use for: opening Google, navigating to search results, visiting competitor pages.

**`browser_click`** — Click an element on the page.
```
Tool: browser_click
Args: {"element": "search input", "ref": "s1e3"}
```
Use for: clicking the search input, expanding PAA questions, clicking Related Searches links.

**`browser_type`** — Type text into a focused element.
```
Tool: browser_type
Args: {"text": "invoicing software", "submit": false}
```
Use for: typing search queries, entering seed keywords for Autocomplete capture. Set `submit: false` when capturing Autocomplete (do not press Enter). Set `submit: true` when executing a search.

**`browser_snapshot`** — Get a text representation of the current page.
```
Tool: browser_snapshot
Args: {}
```
Use for: extracting page content, reading SERP results, capturing Autocomplete suggestion text, reading PAA questions and answers.

**`browser_evaluate`** — Execute JavaScript on the page.
```
Tool: browser_evaluate
Args: {"expression": "window.scrollTo(0, document.body.scrollHeight)"}
```
Use for: scrolling to bottom of SERP (Related Searches), extracting specific DOM elements, counting result elements, measuring page dimensions.

**`browser_take_screenshot`** — Capture a screenshot.
```
Tool: browser_take_screenshot
Args: {}
```
Use for: full SERP screenshots, documenting SERP features, visual analysis, before/after comparisons.

### Supporting tools

**`browser_press_key`** — Press a keyboard key.
```
Tool: browser_press_key
Args: {"key": "Backspace"}
```
Use for: clearing characters in the search input during Autocomplete a-z cycling.

**`browser_wait_for`** — Wait for a condition.
```
Tool: browser_wait_for
Args: {"selector": "[data-attrid='PeopleAlsoAsk']", "timeout": 5000}
```
Use for: waiting for PAA box to load, waiting for Autocomplete dropdown to appear, waiting for SERP features to render.

**`browser_hover`** — Hover over an element.
```
Tool: browser_hover
Args: {"element": "autocomplete suggestion", "ref": "s2e5"}
```
Use for: triggering hover-dependent UI elements.

## Chrome DevTools MCP alternative

Chrome DevTools MCP provides equivalent capabilities with different tool names. Use this mapping if Playwright MCP is unavailable but Chrome DevTools MCP is available.

| Playwright MCP | Chrome DevTools MCP | Notes |
|---------------|-------------------|-------|
| `browser_navigate` | `navigate_page` | Same parameters |
| `browser_click` | `click` | Same parameters |
| `browser_type` | `type_text` | Same parameters |
| `browser_snapshot` | `take_snapshot` | Same — text representation |
| `browser_evaluate` | `evaluate_script` | Same — JS execution |
| `browser_take_screenshot` | `take_screenshot` | Same parameters |
| `browser_press_key` | `press_key` | Same parameters |
| `browser_wait_for` | `wait_for` | Same parameters |
| `browser_hover` | `hover` | Same parameters |

All scripts in this skill document Playwright MCP tool names. When using Chrome DevTools MCP, substitute the tool names using this mapping. The parameters and behavior are equivalent.

## Google navigation patterns

### Incognito / clean session

Always start with a clean browser state. Previous search history, logged-in accounts, and cookies influence what Google shows. Incognito mode eliminates personalization and gives you the "neutral" SERP that most users see.

### Location and language parameters

Append URL parameters for localized results:
- `&gl=us` — Geolocation (country code). Use the target country from "Before you start."
- `&hl=en` — Interface language. Match the target audience language.
- `&pws=0` — Disable personalized results.

Example: `https://www.google.com/search?q=invoicing+software&gl=us&hl=en&pws=0`

### Viewport settings

Use a standard desktop viewport to get the full SERP experience:
- **Recommended:** 1280x800 (common laptop) or 1920x1080 (desktop).
- Avoid mobile viewports for SERP analysis — Google shows different SERP features on mobile.
- Consistent viewport across all searches ensures comparable results.

### Page load waiting

After navigating to a search results page, wait for the page to fully load before extracting data. Dynamic elements (AI Overview, PAA box, video carousels) load asynchronously and may not be present in the initial HTML.

**Strategy:** After `browser_navigate`, call `browser_snapshot` and check if expected elements are present. If not, wait 2-3 seconds and snapshot again. Most SERP features load within 3 seconds.

## Avoiding captchas and rate limiting

Google uses rate limiting and captcha challenges to prevent automated querying. These patterns minimize the risk of being blocked.

### Timing patterns

- **Between searches:** Wait 3-8 seconds (randomized). Never use a fixed interval — fixed intervals are a bot fingerprint.
- **Between Autocomplete keystrokes:** Wait 100-200ms between characters. This mimics human typing speed.
- **Between PAA expansions:** Wait 1-2 seconds between clicks. Humans do not click every PAA question in 100ms.
- **Between Related Searches navigations:** Wait 3-5 seconds. Each navigation is a full page load.

### Session limits

- **Maximum searches per session:** 20-30. After that, risk of captcha increases significantly.
- **Session duration:** 10-15 minutes maximum. Take a 5-minute break between sessions.
- **Daily limit:** 3-5 sessions per day per IP/browser profile.

### If a captcha appears

1. Stop all automated actions immediately.
2. Pause for at least 5 minutes.
3. Clear cookies and restart the browser session.
4. Reduce the pace — increase delays between searches.
5. If captchas persist: switch to a different session or fall back to `--no-browser` mode.

### User-Agent

Use a standard Chrome User-Agent string. Unusual or missing User-Agent strings trigger bot detection.

Playwright MCP uses a standard Chromium User-Agent by default. Do not override it with custom strings.

### Search entry points

Vary your search entry points:
- Navigate to `google.com` and type in the search box (more human-like).
- Navigate directly to `google.com/search?q=...` (faster, slightly more detectable).
- Mix both approaches within a session.

## Autocomplete extraction technique

### Full procedure

1. **Navigate** to `google.com` (`browser_navigate`).
2. **Click** the search input (`browser_click` on the search box).
3. **Type** the seed keyword character by character (`browser_type` with `submit: false`). Wait 100-200ms between characters to trigger Autocomplete.
4. **Wait** 500ms after the full seed is typed for the suggestion dropdown to appear.
5. **Capture** suggestions: `browser_snapshot` to read the Autocomplete dropdown text.
6. **Cycle a-z:** For each letter a through z:
   - Type the letter (`browser_type`).
   - Wait 500ms.
   - Capture suggestions (`browser_snapshot`).
   - Delete the letter (`browser_press_key` with Backspace).
7. **Question prefixes:** Clear the search input. Type "how to [seed]", "what is [seed]", "best [seed]", "why [seed]". Capture suggestions for each.
8. **Wait** 3-8 seconds (randomized) before moving to the next seed.
9. **Deduplicate** all collected suggestions.

### What you get

For each seed, you typically capture 50-200+ unique Autocomplete suggestions. Across 15-30 seeds, this generates 750-6000+ raw keyword candidates — far more than any keyword tool provides, and with real-time currency.

Run `scripts/harvest-autocomplete.py --seeds 'seed1,seed2,seed3'` to automate this.

## PAA expansion technique

### Full procedure

1. **Search** for the keyword: type in the search input and submit (`browser_type` with `submit: true`).
2. **Wait** for the results page to fully load (2-3 seconds).
3. **Locate** the PAA box: `browser_snapshot` and identify PAA questions in the page content.
4. **Click** each PAA question (`browser_click`). The question expands to show:
   - The answer snippet
   - The source URL
   - 2-3 new related questions added below
5. **Wait** 1-2 seconds after each click for new questions to load.
6. **Repeat:** Click each newly revealed question. Keep going until no new questions appear or you have captured 50+ questions.
7. **Extract** for each question: question text, answer snippet, source URL, the seed keyword that triggered it.
8. **Wait** 5-8 seconds before searching the next seed keyword.

### What you get

For each seed, PAA expansion typically captures 20-50 unique questions with answer snippets and source URLs. Each question is a content opportunity — a potential H2 section, FAQ entry, or standalone article. The source URLs reveal your competitors for each specific question.

Run `scripts/extract-paa.py --seeds 'seed1,seed2'` to automate this.

## Related Searches extraction

### Full procedure

1. **Search** for the seed keyword and wait for results to load.
2. **Scroll** to the bottom of the SERP: `browser_evaluate` with `window.scrollTo(0, document.body.scrollHeight)`.
3. **Capture** the Related Searches section: `browser_snapshot` to read the related search links (typically 8 links).
4. **Level 2 chaining:** Click each Related Search (`browser_click`). On each new SERP:
   - Wait for page load (2-3 seconds).
   - Scroll to bottom.
   - Extract its Related Searches.
5. **Deduplicate** across all levels.
6. **Wait** 3-5 seconds between page navigations.

### What you get

For each seed: 8 level-1 related searches, each producing up to 8 level-2 searches = up to 72 related keyword ideas per seed (after deduplication, typically 30-50 unique). These are lateral keyword ideas — semantically connected but often containing different words.

Run `scripts/scrape-related-searches.py --seeds 'seed1,seed2'` to automate 2-level chaining.

## SERP feature detection

After searching for a keyword, analyze the SERP for features that affect ranking strategy and GEO scoring.

### Features to detect

**AI Overview:**
- JavaScript-rendered answer box at the top of the SERP.
- If present: the keyword is AI-answerable. GEO optimization is critical.
- Look for: source count (how many sources cited), content type (summary, list, table).

**Featured Snippet:**
- Highlighted answer box above organic result #1.
- Types: paragraph (most common), list (numbered/bulleted), table.
- If present: opportunity to win position 0. Structure your content to match the snippet format.

**People Also Ask:**
- Expandable question box, typically between positions 2-4.
- If present: question-based content opportunity. Each question is a potential target.

**Knowledge Panel:**
- Right-side panel with entity information.
- If present: Google recognizes an entity for this query. Structured data and entity SEO matter.

**Video carousel:**
- Horizontal row of video results.
- If present: strong informational signal. Consider video content alongside written content.

**Local pack:**
- Map + business listings.
- If present: local intent. Not relevant for most content-based SEO.

**Shopping results:**
- Product listings with prices.
- If present: strong transactional intent. Product pages and pricing pages should target this keyword.

**Sitelinks:**
- Expanded site links under the top organic result.
- If present: the top result has strong brand authority for this query.

### How feature detection feeds into scoring

- AI Overview present → GEO score is at least 2 (AI engages with this topic)
- Featured Snippet present → content structure opportunity (format content to win the snippet)
- Shopping results present → transactional intent confirmed
- Video carousel present → informational intent signal
- Local pack present → local intent, may not be relevant for content strategy

Run `scripts/analyze-serp-live.py --keyword 'invoicing software'` for comprehensive SERP feature detection.

## Fallback patterns when browser is unavailable

When neither Playwright MCP nor Chrome DevTools MCP is available, all browser-dependent scripts fall back to WebSearch + WebFetch. The fallback is functional but provides lower-quality data.

| Feature | Browser | Fallback | Quality loss |
|---------|---------|----------|-------------|
| Autocomplete | Full a-z + prefix harvesting | Not replicable. Use AnswerThePublic instead. | Severe — no equivalent |
| PAA expansion | Click-expand 50+ questions | WebSearch may return some PAA data. | Significant — 4-8 vs 50+ |
| Related Searches | 2-level chaining, 30-50 per seed | WebSearch may include some. | Moderate — fewer and no chaining |
| SERP features | Full detection (AI Overview, snippets, etc.) | Cannot detect. Classify intent from titles/URLs only. | Significant — blind to features |
| Community scraping | Full page rendering, JS content | `site:reddit.com [topic]` via WebSearch | Moderate — titles only, no comments |
| Screenshots | Full SERP capture | Not available | Complete — no visual analysis |

When operating in fallback mode:
- Use AnswerThePublic (3 free/day) to approximate Autocomplete data.
- Use WebSearch results to approximate intent (titles/URLs suggest content type).
- Note all limitations in your output. The user should know which data is estimated vs observed.
- Consider obtaining Playwright MCP access before running a full discovery process. The quality difference is substantial.

## Session management best practices

**Start clean:** Begin each discovery session with a fresh browser instance. No previous cookies, no logged-in sessions.

**Group by task:** Run all Autocomplete harvesting in one session, all PAA expansion in another, all SERP analysis in a third. This reduces context switching and makes rate limiting easier to manage.

**Save incrementally:** After each search or extraction, save the results. If a session is interrupted (captcha, network issue, timeout), you do not lose previous work.

**Log everything:** Record which keywords were searched, which techniques were used, and what data was captured. This makes it easy to pick up where you left off and prevents duplicate effort.

**Rotate sessions:** If you need to process more than 20-30 searches, split across multiple sessions with 5-minute breaks between them. This dramatically reduces captcha risk.
