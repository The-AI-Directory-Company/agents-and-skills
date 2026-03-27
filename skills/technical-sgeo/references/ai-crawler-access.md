# AI Crawler Access: Complete Bot Management Guide

AI crawlers follow similar mechanics to search engine crawlers — they request pages via HTTP and read the response. But they have different user-agents, different CDN treatment, and in many cases, no JavaScript execution capability. Many robots.txt files inherited AI blocks from 2023 panic. Review yours — those blocks are now costing you AI visibility.

## AI crawler user-agent table

| Bot | User-Agent String | Operator | What It Feeds | Recommended Action |
|-----|-------------------|----------|---------------|--------------------|
| GPTBot | `GPTBot/1.0` | OpenAI | ChatGPT training + browsing | Allow |
| ChatGPT-User | `ChatGPT-User/1.0` | OpenAI | ChatGPT live browsing only | Allow |
| OAI-SearchBot | `OAI-SearchBot/1.0` | OpenAI | ChatGPT search results | Allow |
| ClaudeBot | `ClaudeBot/1.0` | Anthropic | Claude training + retrieval | Allow |
| PerplexityBot | `PerplexityBot/1.0` | Perplexity | Perplexity search answers | Allow |
| Google-Extended | `Google-Extended` | Google | Gemini training (separate from Googlebot) | Allow |
| Bytespider | `Bytespider` | ByteDance | TikTok AI features | Evaluate — high crawl volume, aggressive rate |

**Note:** `Google-Extended` controls only Gemini training. Blocking it does not affect Google Search indexing (that is `Googlebot`). Similarly, blocking `GPTBot` does not affect ChatGPT's live browsing feature — that uses `ChatGPT-User`. These are distinct user-agents with distinct purposes.

## robots.txt configurations

### Allow all AI bots (recommended for most sites)

```
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /
```

### Allow specific bots, block others

```
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Bytespider
Disallow: /

User-agent: Google-Extended
Disallow: /
```

### Block all AI bots (not recommended if you want AI visibility)

```
User-agent: GPTBot
Disallow: /

User-agent: ChatGPT-User
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: PerplexityBot
Disallow: /

User-agent: Google-Extended
Disallow: /
```

**If no rule exists for a specific bot:** The `User-agent: *` rules apply. If `*` allows access, AI bots can crawl. But explicit rules are better practice — they document your intent and make auditing straightforward.

## CDN configuration per provider

### Cloudflare

Cloudflare is the most common source of accidental AI bot blocking.

**Bot Fight Mode** (free plans):
- Location: Security > Bots > Bot Fight Mode toggle
- Default: ON — actively challenges/blocks automated traffic
- Impact: AI crawlers receive CAPTCHAs or 403 responses
- Fix: Toggle OFF, or create a WAF custom rule: `(http.user_agent contains "GPTBot") or (http.user_agent contains "ClaudeBot") or (http.user_agent contains "PerplexityBot")` with action "Skip" (skip all remaining rules)

**Super Bot Fight Mode** (Pro/Business plans):
- More aggressive than Bot Fight Mode
- Has separate toggles for "Definitely automated" and "Likely automated"
- AI crawlers may fall into either category
- Fix: Set "Definitely automated" to "Allow" or create specific WAF exceptions

**Cloudflare AI Audit** (newer feature):
- Some Cloudflare plans now include AI bot analytics
- Check Analytics > Security > Bot traffic to see which AI bots are visiting and their treatment

### AWS CloudFront + WAF

- **WAF Bot Control**: AWS categorizes bots into "Common" and "Targeted" rule groups
- AI crawlers may be classified under the Common bot category as "unverified"
- Fix: Add a custom rule that allows requests matching AI bot user-agent strings before the Bot Control rule evaluates
- Example WAF rule: Match `User-Agent` header against a regex containing known AI bot strings, with action Allow

### Akamai

- **Bot Manager**: Uses a bot scoring system with categories
- AI crawlers may receive low (suspicious) scores by default
- Fix: Create custom bot definitions for AI crawler user-agents and assign them an "allow" action
- Check the Bot Manager Analytics dashboard for blocked bot traffic

### Fastly

- **Signal Sciences WAF**: Applies bot detection scoring
- AI crawlers may trigger automated rate limiting or blocking
- Fix: Create an exception rule matching AI bot user-agents
- Monitor the Signal Sciences dashboard for blocked requests from AI bot user-agents

## Server log verification

After configuring robots.txt and CDN settings, you must verify with server logs. Configuration alone does not guarantee access.

### Common log format queries

**Apache/Nginx combined log format:**
```bash
# Count AI bot requests in the last 24 hours
grep -E "(GPTBot|ClaudeBot|PerplexityBot|ChatGPT-User|OAI-SearchBot)" access.log | \
  awk '{print $1, $9}' | sort | uniq -c | sort -rn

# Check response codes for AI bots
grep "GPTBot" access.log | awk '{print $9}' | sort | uniq -c | sort -rn
```

**Expected output:** You should see 200 responses. If you see 403, 503, or zero entries, AI bots are being blocked before reaching your server (CDN/WAF) or by your server configuration.

### What to look for

| Log Pattern | Meaning | Action |
|-------------|---------|--------|
| 200 responses from AI bots | Working correctly | No action needed |
| 403 responses from AI bots | Actively blocked (WAF/CDN or server config) | Check CDN bot management settings |
| 503 responses from AI bots | Rate limited or server overloaded | Check rate limiting rules |
| Zero AI bot entries | CDN is blocking before requests reach your server | Check CDN bot management settings |
| 200 but tiny response body | Serving a CAPTCHA/challenge page instead of content | Disable bot challenges for AI bots |

### Monitoring frequency

Check AI bot access logs weekly at minimum. Set up automated alerts for:
- Any AI bot receiving non-200 responses
- Sudden drop in AI bot request volume (may indicate new CDN rule deployment)
- New AI bot user-agents appearing in logs (new bots emerge regularly)

## Content accessibility for AI consumption

AI crawlers generally cannot:
- **Execute JavaScript.** They read raw HTML responses. Content that requires JS to render is invisible.
- **Authenticate or log in.** Gated content behind login walls will not be crawled.
- **Bypass cookie consent walls.** If a consent banner hides content until accepted, AI bots see only the banner.
- **Process iframes from different origins.** Content loaded in cross-origin iframes is not accessible.
- **Interact with the page.** Content behind click-to-expand, tabs, or infinite scroll is not accessible.

**For AI visibility, ensure:**
1. All substantive content is in the initial HTML response (SSR or static generation)
2. No critical content requires authentication
3. Cookie consent banners do not hide page content from bots (most implementations correctly only block tracking, not content)
4. Content is in the main document, not in iframes

## llms.txt

The llms.txt proposal suggests placing a plain-text markdown file at `/llms.txt` summarizing your site's content for LLMs. The specification defines a structured format with site description, key pages, and content summaries.

### Current research findings

| Study | Scope | Finding |
|-------|-------|---------|
| SE Ranking | 300,000 domains | No correlation between llms.txt presence and AI visibility |
| OtterlyAI | 90-day controlled study | No measurable impact on AI citation rates |
| ALLMO | 94,000+ cited URLs | No statistically significant benefit detected |

No major AI platform has publicly confirmed that they use llms.txt for retrieval or ranking decisions.

### Verdict

Adding an llms.txt file is low effort (30 minutes) and carries no risk. But it should not take priority over the fundamentals covered in this skill — crawlability, rendering, structured data, and content quality drive AI visibility far more than a summary file. If you have spare time after completing all other sections, add it. If you are triaging limited engineering time, skip it.

The one exception: if you publish developer documentation, APIs, or technical content that AI coding assistants consume, an llms.txt can serve as a useful entry point for those specific use cases. But this is a developer-tooling concern, not a general AI visibility strategy.
