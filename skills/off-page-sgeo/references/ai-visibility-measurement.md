# AI Visibility Measurement

You cannot improve what you do not measure. AI citation is a new metric that most competitors are not tracking yet. Starting now gives you a structural advantage — you'll have baseline data and trend lines while competitors are still guessing.

This reference covers the complete measurement framework: manual testing, tool-based tracking, GA4 setup, server log analysis, and competitive benchmarking.

---

## Manual Testing Protocol

Manual testing is the free baseline. Everyone should do this regardless of budget.

### Query Design

Compile 10-20 queries your target audience would ask AI assistants. Mix three types:

**Informational queries (5-8):**
- "What is [concept in your domain]?"
- "How does [process you help with] work?"
- "What are the best practices for [your topic]?"

**Commercial queries (3-5):**
- "What is the best [category] tool?"
- "Which [product type] should I use for [use case]?"
- "[Your product] vs [competitor] — which is better?"

**Brand-adjacent queries (3-5):**
- "What are the top [your niche] companies?"
- "Who are the leaders in [your space]?"
- "What tools do professionals use for [your domain]?"

Write queries in the way your audience actually talks to AI — conversational, specific, sometimes informal.

### Platform Coverage

Test on a minimum of 3 platforms. Ideally all 4:

| Platform | URL | Notes |
|----------|-----|-------|
| ChatGPT | chat.openai.com | Largest user base. Use GPT-4 or latest model. |
| Perplexity | perplexity.ai | Most transparent citations — shows sources inline. |
| Claude | claude.ai | Strong for technical and business queries. |
| Gemini | gemini.google.com | Integrated with Google's search index. |

### Recording Methodology

For each query on each platform, record:

| Field | What to Record |
|-------|---------------|
| Query | The exact text you asked |
| Platform | Which AI platform |
| Brand cited | Yes/No — was your brand mentioned by name or your content cited? |
| Citation context | Direct quote, mention by name, link to your site, or no citation |
| Competitors cited | List of competitor brands mentioned in the response |
| Source URLs | If the platform shows sources, capture the URLs it cited |
| Date | When you ran the test |

### Tracking Spreadsheet

Maintain a simple spreadsheet:

```
| Query | Platform | Brand Cited? | Competitors Cited | Source URLs | Date |
|-------|----------|-------------|-------------------|-------------|------|
| | | | | | |
```

Run this monthly at minimum. Weekly for high-priority queries if you're actively optimizing.

### Trend Analysis

After 3+ months of data, analyze:
- Which queries cite you? What's different about those queries vs. ones that don't?
- Which competitors appear most often? What authority signals do they have that you lack?
- Are citations increasing or decreasing month over month?
- Which platforms cite you more frequently? Focus optimization efforts there.

---

## Tool Comparison

These tools automate what manual testing does by hand. They're worth the investment once manual testing confirms that AI visibility matters for your business.

### Cairrot (~$40/mo)

Best value for small-to-mid sites.

**What it tracks:** ChatGPT, Perplexity, Claude, Gemini citations. AI bot crawl activity via WordPress plugin. Includes llms.txt generator.

**Strengths:**
- Broadest platform coverage at this price point
- WordPress plugin provides server-side AI bot tracking — see which AI crawlers visit your site and how often
- Tracks citation trends over time with visual dashboards
- llms.txt generator (low impact but free to set up)

**Limitations:**
- Citation data can lag 1-2 weeks behind real-time
- WordPress plugin required for bot tracking — non-WordPress sites miss this feature
- Newer tool — feature set evolving rapidly

**Best for:** Most businesses starting to track AI visibility. The WordPress plugin alone justifies the cost if you're on WordPress.

### AIclicks (~$39/mo)

Good for prompt-level tracking and content recommendations.

**What it tracks:** AI visibility score, prompt-level citation tracking, content optimization recommendations.

**Strengths:**
- AI visibility score provides a single benchmark number useful for reporting
- Content recommendations suggest specific improvements to increase citation likelihood
- Prompt research shows what queries trigger AI answers in your space

**Limitations:**
- Fewer platforms tracked than Cairrot
- Recommendations can be generic — verify against your specific content before acting
- Visibility score methodology is proprietary — hard to validate independently

**Best for:** Teams that want a single score to track and content-level recommendations.

### Peec AI (Varies)

Competitive benchmarking focus.

**What it tracks:** AI visibility across platforms, competitive benchmarking, share-of-voice metrics.

**Strengths:**
- Strong competitive comparison features
- Useful if you need to benchmark against specific competitors regularly
- Category-level analysis shows where your brand fits in AI's understanding

**Limitations:**
- Pricing is opaque — requires sales conversation
- Less focused on individual content optimization
- Better for brands that already have some AI visibility to benchmark

**Best for:** Mid-size brands in competitive categories that need to track share-of-voice against specific competitors.

### Semrush AI Add-On (Included in Semrush Subscription)

Fine if you already pay for Semrush. Don't buy Semrush just for AI tracking.

**What it tracks:** AI visibility score, prompt research, some citation tracking bolted onto the existing Semrush platform.

**Strengths:**
- No additional cost if you already use Semrush
- Integrated with your existing SEO workflow
- Prompt research is useful for discovering what queries trigger AI answers

**Limitations:**
- AI features are secondary to Semrush's core SEO toolkit
- Less depth than dedicated AI visibility tools
- Feature set is playing catch-up with dedicated AI tools

**Best for:** Existing Semrush customers who want AI visibility data without adding another tool.

### Profound (Enterprise)

Overkill for most sites. Built for large brands with enterprise budgets.

**What it tracks:** Deep citation analytics, share-of-voice tracking, competitive intelligence across AI platforms.

**Strengths:**
- Most comprehensive AI citation analytics available
- Enterprise-grade reporting and integrations
- White-glove support and custom analysis

**Limitations:**
- Enterprise pricing (typically $1K+/mo)
- More features than most businesses need
- Sales-driven process

**Best for:** Large brands where AI visibility is a board-level priority.

### Recommendation

- **Starting out:** Manual testing (free) for 2-3 months
- **Confirmed AI visibility matters:** Cairrot ($40/mo) — best value
- **Already on Semrush:** Enable the AI add-on — it's included
- **Competitive category:** Add Peec AI for benchmarking
- **Enterprise:** Profound if budget allows

---

## GA4 AI Referrer Setup

AI-referred traffic is growing 527% year-over-year. Set this up now even if volumes are small — you want baseline data.

### Step-by-Step Setup

1. **Go to GA4 Admin** (gear icon in bottom-left)
2. **Navigate to:** Data Streams > Web > Configure tag settings
3. **Define internal traffic:** Ensure AI referrers are NOT excluded from your bot filtering. Some GA4 setups inadvertently filter AI-referred traffic as bot traffic.
4. **Go to:** Admin > Custom Definitions > Custom Channel Groups
5. **Create a new channel group** named "AI Assistants"
6. **Add conditions** (Source/Medium contains):
   - `chat.openai.com`
   - `perplexity.ai`
   - `gemini.google.com`
   - `claude.ai`
   - `copilot.microsoft.com`
7. **Save** the channel group
8. **View data in:** Acquisition > Traffic Acquisition report, then select your custom channel group

### What to Track

Once set up, monitor:
- **Session count:** How many visits come from AI platforms
- **Pages per session:** Are AI-referred visitors engaged?
- **Conversion rate:** Do AI-referred visitors convert? (Often higher than organic — AI sends highly qualified traffic)
- **Top landing pages:** Which pages are being cited by AI?
- **Growth trend:** Week-over-week and month-over-month AI traffic growth

### Known AI Referrers (2026)

Keep this list updated as new AI platforms emerge:

| Referrer Domain | AI Platform |
|----------------|-------------|
| `chat.openai.com` | ChatGPT |
| `perplexity.ai` | Perplexity |
| `gemini.google.com` | Gemini |
| `claude.ai` | Claude |
| `copilot.microsoft.com` | Microsoft Copilot |
| `you.com` | You.com |
| `poe.com` | Poe (Quora) |

---

## Server Log Analysis

Server logs show you which AI bots crawl your site — independently of whether they cite you.

### AI Bot User-Agent Strings

Look for these in your access logs:

| User-Agent Contains | AI Platform |
|--------------------|-------------|
| `GPTBot` | OpenAI (ChatGPT) |
| `ChatGPT-User` | ChatGPT browsing |
| `ClaudeBot` | Anthropic (Claude) |
| `PerplexityBot` | Perplexity |
| `Google-Extended` | Google AI (Gemini, AI Overviews) |
| `Bytespider` | ByteDance AI |
| `cohere-ai` | Cohere |

### What to Check

- **Are AI bots visiting?** If not, check robots.txt and CDN settings — you may be blocking them.
- **Visit frequency:** Daily? Weekly? Rarely? More frequent crawling suggests your content is being actively indexed.
- **Which pages?** Are AI bots crawling your most important content or getting stuck on irrelevant pages?
- **Response codes:** Are they getting 200s? If they're getting 403s or 503s, your CDN or WAF is blocking them.

### Log Analysis Commands

For Apache/Nginx access logs:

```bash
# Count AI bot visits by user-agent
grep -iE "GPTBot|ClaudeBot|PerplexityBot|Google-Extended|ChatGPT-User" access.log | wc -l

# See which pages AI bots request most
grep -iE "GPTBot|ClaudeBot|PerplexityBot" access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head -20

# Check response codes for AI bots
grep -iE "GPTBot|ClaudeBot|PerplexityBot" access.log | awk '{print $9}' | sort | uniq -c | sort -rn
```

---

## Share of Model Metric

Share of Model measures your brand's percentage of AI answers in your category. It's the AI equivalent of share of voice.

### How to Calculate

1. Define your category with 15-20 representative queries
2. Run each query on 3-4 AI platforms
3. Count how many responses mention your brand vs. total responses
4. Your share = (responses mentioning your brand) / (total responses tested)
5. Calculate the same for each competitor

### Interpreting Results

| Share of Model | Interpretation |
|---------------|---------------|
| 0-5% | Not visible. AI doesn't know about you for this category. |
| 5-15% | Emerging. Occasional citations but inconsistent. |
| 15-30% | Established. Regular citations across platforms. |
| 30-50% | Dominant. You're a primary source for this category. |
| 50%+ | Category leader. AI defaults to citing you. |

### Benchmarking Against Competitors

Run the same query set for your brand and 3-5 competitors. Build a comparison:

```
| Brand | Share of Model | Top Citation Platform | Trend |
|-------|---------------|----------------------|-------|
| You | 12% | Perplexity | Up |
| Competitor A | 35% | ChatGPT | Stable |
| Competitor B | 22% | Claude | Up |
| Competitor C | 8% | Perplexity | Down |
```

Track quarterly. Meaningful changes in Share of Model take 3-6 months of sustained authority-building work to materialize.

---

## Measurement Cadence

| Frequency | What to Check |
|-----------|---------------|
| Weekly | GA4 AI referrer traffic, new backlinks (if tool available) |
| Monthly | Manual AI visibility test (full query set), Share of Model calculation, brand mention count |
| Quarterly | Full competitive benchmark, tool stack assessment, strategy adjustment based on trends |
| Biannually | Budget reallocation, platform priority review, 6-month trend analysis |

Start measuring before you start optimizing. The baseline is the most important data point you'll collect — without it, you can't prove improvement.
