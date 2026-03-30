---
name: off-page-sgeo
description: Build authority and reputation signals for both search engine rankings and AI platform citations — covering backlink strategy, brand mention development, multi-platform presence on AI-cited sources, digital PR, community engagement, and AI visibility measurement.
metadata:
  displayName: "Off-Page SGEO Authority"
  categories: ["business"]
  tags: ["SEO", "GEO", "SGEO", "backlinks", "authority", "digital-PR", "brand-mentions", "AI-visibility", "link-building"]
  worksWellWithAgents: ["content-strategist", "developer-advocate", "growth-engineer", "marketing-strategist", "seo-specialist"]
  worksWellWithSkills: ["content-sgeo", "discovery-gseo", "go-to-market-plan", "on-page-sgeo", "technical-sgeo"]
---

# Off-Page SGEO Authority

## Before you start

Gather the following from the user. If anything is missing, ask before proceeding:

1. **What is the business domain and URL?** (Primary website to build authority for)
2. **What is the current backlink profile?** (Number of referring domains, domain authority/rating if known — check Ahrefs, Moz, or Semrush)
3. **Where does the brand already have presence?** (LinkedIn, Reddit, YouTube, Twitter/X, GitHub, industry forums — list all active accounts)
4. **What content assets are available for promotion?** (Guides, free tools, original research, data studies, templates)
5. **Who are the main competitors?** (3-5 domains that already have authority in your space)
6. **What is the budget for outreach and PR?** (None, small <$500/mo, moderate $500-2000/mo, significant >$2000/mo)
7. **Is AI citation a priority?** (Whether appearing in ChatGPT, Perplexity, Claude, Gemini responses matters for the business)
8. **What is the industry/niche?** (Determines which communities, publications, and platforms matter most)

## Tool discovery

Before gathering project details, confirm which tools are available.
Ask the user directly — do not assume access to any external service.

**Free tools (no API key required):**
- [ ] WebFetch (fetch any public URL — robots.txt, sitemaps, pages)
- [ ] WebSearch (search engine queries for competitive analysis)
- [ ] Google PageSpeed Insights API (CWV data, no key needed for basic usage)
- [ ] Google Rich Results Test (structured data validation)
- [ ] Playwright MCP or Chrome DevTools MCP (browser automation)

**Paid tools (API key or MCP required):**
- [ ] Google Search Console API (requires OAuth)
- [ ] DataForSEO MCP (SERP data, keyword metrics, backlinks)
- [ ] Ahrefs API (backlink profiles, keyword research)
- [ ] Semrush API (competitive analysis, keyword data)

**The agent must:**
1. Present this checklist to the user
2. Record which tools are available
3. Pass the inventory to scripts as context
4. Fall back gracefully — every check has a free-tier path using WebFetch/WebSearch

## Off-page SGEO procedure

### Step 1: Backlink Strategy

> **Scripts:** Run `scripts/check-backlink-profile.py --domain yourdomain.com` for baseline. Run `scripts/find-link-opportunities.py --topic 'your niche'` for prospects.
> **Reference:** See `references/backlink-strategy.md` for outreach templates and anchor text guidelines.

Quality over quantity — one link from a respected industry site is worth more than 100 from random directories. Search engines use backlinks as trust signals. AI engines use the same publications as training and retrieval sources, so a backlink from a high-authority site doubles as an AI citation pathway.

**Linkable asset types** (in order of effectiveness):

1. **Original research** — Surveys, benchmarks, data studies. Journalists and bloggers cite these naturally. AI engines frequently quote statistics from original research.
2. **Free tools** — Calculators, analyzers, generators. People link to useful tools. Tool pages get referenced in AI answers to "how do I..." queries.
3. **Comprehensive guides** — The definitive resource on a topic. Others reference it instead of recreating it. AI engines prefer citing single authoritative sources over fragmented ones.
4. **Data visualizations** — Infographics, interactive charts. Embeddable content earns links passively.
5. **Frameworks and templates** — Reusable assets people reference and share in communities.

**Link acquisition methods:**

- **Guest posting** on relevant industry blogs. Provide genuine value — a unique angle, original data, or expert perspective. Not link drops disguised as articles.
- **Resource page outreach.** Find "useful links" or "resources" pages in your niche using search operators like `intitle:"resources" [your topic]`. Suggest your content where it genuinely fits.
- **Broken link building.** Use Ahrefs or Check My Links to find broken links on relevant sites. Create or identify your content that serves as a replacement. Contact the site owner with the fix.
- **Journalist query platforms (Qwoted, Featured.com, Terkel).** Journalists post queries seeking expert quotes. Respond within 2 hours with a concise, quotable answer and your credentials. Include 1-2 data points. (Note: HARO and Connectively, previously the dominant platforms in this space, were discontinued in 2023-2024.)
- **Skyscraper technique.** Find the top-ranking content for your target keyword. Create something measurably better (more current data, broader scope, better examples). Outreach to sites linking to the original with a specific reason yours is more useful.

**Backlink tracking template:**

```
| Target Site | DA/DR | Contact Person | Asset Offered | Outreach Date | Status | Link Acquired | Follow-up Date |
|-------------|-------|----------------|---------------|---------------|--------|---------------|----------------|
|             |       |                |               |               |        |               |                |
```

Status values: Not contacted, Pitched, Replied, Negotiating, Published, Declined, No response.

### Step 2: Brand Mention Development

> **Script:** Run `scripts/monitor-brand-mentions.py --brand 'Your Brand'` to find and classify mentions.
> **Reference:** See `references/brand-mentions.md` for monitoring setup and mention-to-link conversion workflow.

Unlinked mentions of your brand contribute to perceived authority for both search engines and AI systems. Google's entity recognition treats brand mentions as implicit endorsements. AI engines weigh brand mentions across diverse sources when deciding what to cite.

**Monitoring setup:**

- Set up Google Alerts for your brand name, product names, and founder/CEO names
- Configure Ahrefs Alerts or Semrush Brand Monitoring for web mentions
- Use social listening (Mention.com, Brand24, or free Twitter/Reddit search) for social mentions
- Track mentions weekly — categorize as linked, unlinked, positive, negative, neutral

**Mention-to-link conversion:**

1. Export unlinked mentions from your monitoring tool
2. Prioritize by site authority (DA/DR > 40 first)
3. Find the author's contact (Twitter, LinkedIn, or site contact page)
4. Send a brief, friendly request: "Thanks for mentioning [brand] — would you mind linking to [URL] so readers can find us easily?"
5. Conversion rate expectation: 5-15% of outreach attempts result in added links

**Building mentionable authority:**

- Publish quotable statistics and frameworks that get attributed by name ("According to [Brand]'s 2025 report...")
- Participate in industry surveys and roundups where your brand appears alongside competitors
- Contribute expert commentary to publications — each quote is a brand mention
- Create named methodologies or scores (e.g., "[Brand] Readiness Score") that others reference

### Step 3: Multi-Platform Presence for AI Citation

> **Script:** Run `scripts/audit-platform-presence.py --brand 'Your Brand'` to check presence across all 7 platforms.
> **Reference:** See `references/ai-citation-platforms.md` for platform-by-platform tactical guides.

This is the key GEO differentiator. AI engines cite sources beyond your website. If your brand only exists on your domain, you limit citation potential to a single source. Building presence on platforms that AI engines frequently retrieve from expands your citation surface area.

**Platforms AI engines frequently cite** (ordered by observed citation frequency):

1. **Reddit** — Extremely high AI citation rate. AI engines treat Reddit threads as authentic user opinions and recommendations.
   - Identify 3-5 subreddits where your target audience asks questions
   - Participate genuinely: answer questions with expertise, share experiences, provide helpful context
   - Build karma and post history before any brand mentions
   - Never spam or overtly self-promote — Reddit communities detect and punish this immediately

2. **YouTube** — Transcripts are indexed by AI engines. Video content with detailed spoken explanations gets cited.
   - Create tutorial and explainer videos with clear, keyword-rich spoken content
   - Write detailed video descriptions (AI reads these even when it cannot watch the video)
   - Use chapters with descriptive titles

3. **LinkedIn** — Professional content gets cited for business, industry, and career topics.
   - Publish long-form articles (not just short posts) — articles have permanent URLs that AI can cite
   - Share original data and analysis relevant to your industry
   - Comment substantively on industry discussions

4. **Wikipedia** — Extremely high authority for AI citation. If your brand or topic qualifies for a Wikipedia article, it carries outsized weight.
   - Do NOT edit your own brand's article — this violates Wikipedia policy and edits get reverted
   - Contribute genuine expertise to related topic articles where you have knowledge
   - Ensure your brand is cited in reliable secondary sources first (Wikipedia requires these for notability)

5. **GitHub** — Critical for developer-focused products.
   - README quality directly affects AI citation. Write comprehensive READMEs with clear explanations, not just installation instructions.
   - Maintain documentation that answers common questions
   - Participate in relevant open-source projects

6. **Stack Overflow / industry forums** — Expert answers get cited when AI encounters technical questions.
   - Answer questions in your domain with thorough, well-structured responses
   - Include code examples, links to documentation, and explanations of why (not just how)

7. **Industry publications** — Guest articles on respected publications extend your brand's citation surface.
   - Target publications that rank for queries your audience searches
   - Prioritize evergreen content over news — AI engines cite reference material more than dated articles

**Platform audit template:**

```
| Platform         | Account Exists | Last Active | Content Pieces | Content Quality (1-5) | AI Citation Potential | Priority |
|------------------|----------------|-------------|----------------|-----------------------|-----------------------|----------|
| Reddit           |                |             |                |                       |                       |          |
| YouTube          |                |             |                |                       |                       |          |
| LinkedIn         |                |             |                |                       |                       |          |
| Wikipedia        |                |             |                |                       |                       |          |
| GitHub           |                |             |                |                       |                       |          |
| Stack Overflow   |                |             |                |                       |                       |          |
| [Industry forum] |                |             |                |                       |                       |          |
```

AI Citation Potential: High (platform frequently cited by AI for this topic), Medium (occasionally cited), Low (rarely cited for this niche).

### Step 4: Digital PR

> **Reference:** See `references/digital-pr.md` for pitch templates, journalist identification workflow, and podcast guesting strategy.

Getting featured in publications, podcasts, and roundups builds both traditional authority (backlinks, brand mentions) and AI citation surface area. Journalists produce content that AI engines treat as authoritative sources.

**Tactics:**

- **Create newsworthy content.** Trend reports, benchmark studies, industry surveys with original data. Journalists need data to write stories — be the source.
- **Build journalist relationships.** Follow reporters covering your niche on Twitter/X. Engage with their work before pitching. Use tools like Muck Rack or manual research to find relevant journalists.
- **Pitch data-driven stories.** Lead with the most surprising statistic. Journalists get hundreds of pitches — yours needs a compelling number in the subject line.
- **Participate in podcasts.** Reach out to podcasts in your niche as a guest. Podcast show notes with backlinks persist indefinitely. Transcripts get indexed by AI.
- **Submit to industry awards and lists.** "Best of" lists, "Top 50" roundups, and award programs generate high-authority mentions and links.
- **Speak at events and conferences.** Speaker pages link to your site. Conference content gets cited. Recorded talks become searchable content.

**PR pitch template:**

```
Subject: [Key Statistic or Angle] — for [Publication Name]

Hi [First Name],

[One sentence: why this matters to their specific audience — reference a recent article they wrote if possible.]

[Two sentences: what the data or story is, leading with the most interesting finding. Include one specific number.]

[One sentence: why you or your company is credible on this topic — role, years of experience, dataset size.]

Happy to share the full [report/dataset/analysis]. Would you like to take a look?

[Your Name]
[Title, Company]
```

Response rate expectation: 5-10% for cold pitches, 15-25% for warm contacts. Follow up once after 3-5 business days if no response.

### Step 5: Community Engagement

> **Reference:** See `references/ai-citation-platforms.md` (Reddit and forum sections) for community-specific tactics.

Genuine participation in communities drives referral traffic, brand awareness signals, and — for AI citation — creates the kind of authentic, expert-attributed content that AI engines prefer to cite.

**Execution steps:**

1. Identify 3-5 communities where your target audience actively asks questions and discusses problems
2. Spend 2-4 weeks contributing value before any brand mentions — answer questions, share expertise, provide feedback
3. Build reputation as a domain expert, not a marketer. Your profile and post history are visible.
4. Share your content only when it directly answers someone's question or request
5. Track community referral traffic in GA4 (Acquisition > Traffic acquisition > filter by source)

**Community platforms by niche:**

```
| Niche            | Primary Communities                                                          |
|------------------|------------------------------------------------------------------------------|
| Developer tools  | Hacker News, Reddit (r/programming, r/webdev), Dev.to, Stack Overflow       |
| SaaS / Business  | LinkedIn, Reddit (r/SaaS, r/startups), Product Hunt, Indie Hackers          |
| Marketing        | Reddit (r/SEO, r/marketing), Twitter/X, LinkedIn, GrowthHackers             |
| Design           | Dribbble, Behance, Reddit (r/design), Figma Community                        |
| AI / ML          | Reddit (r/MachineLearning, r/LocalLLaMA), Hacker News, Hugging Face, GitHub |
| E-commerce       | Reddit (r/ecommerce, r/shopify), Twitter/X, Shopify Community                |
| Finance          | Reddit (r/fintech), LinkedIn, Twitter/X FinTwit                              |
```

**Community engagement tracking:**

```
| Community     | Posts/Comments This Month | Helpful Responses | Brand Mentions | Referral Traffic | Engagement Trend |
|---------------|---------------------------|--------------------|----------------|------------------|------------------|
|               |                           |                    |                |                  |                  |
```

### Step 6: AI Visibility Measurement

> **Scripts:** Run `scripts/probe-ai-visibility.py` for baseline measurement. Run `scripts/analyze-competitor-authority.py` for competitive comparison. Run `scripts/track-ai-referrers.py` for GA4 setup instructions.
> **Reference:** See `references/ai-visibility-measurement.md` for the complete measurement framework.

Track whether your authority-building efforts translate into AI citations. This is the GEO feedback loop — without measurement, you cannot optimize.

**Manual testing method:**

1. Compile 10-20 queries your target audience would ask AI assistants (e.g., "What is the best [category] tool?", "How do I [problem your product solves]?", "What are the top [your niche] companies?")
2. Ask each query on ChatGPT, Perplexity, Claude, and Gemini
3. Record whether your brand or content is cited in the response
4. Record which competitors are cited instead
5. Analyze what the cited sources have that yours does not (more backlinks? presence on cited platform? better content?)
6. Repeat monthly to track trends over time

**AI visibility tracking template:**

```
| Query                          | ChatGPT Cited? | Perplexity Cited? | Claude Cited? | Gemini Cited? | Competitors Cited | Notes | Date       |
|--------------------------------|----------------|-------------------|---------------|---------------|-------------------|-------|------------|
|                                |                |                   |               |               |                   |       |            |
```

**Tool-based tracking:**

```
| Tool                   | Approx. Price | What It Tracks                                                    |
|------------------------|---------------|-------------------------------------------------------------------|
| Cairrot                | ~$40/mo       | ChatGPT, Perplexity, Claude, Gemini citations; AI bot crawl logs  |
| AIclicks               | ~$39/mo       | Prompt-level tracking, AI visibility score                        |
| Peec AI                | Varies        | AI visibility across platforms, competitive benchmarking           |
| Semrush AI add-on      | Included      | AI visibility score, prompt research                              |
```

**GA4 referrer tracking for AI traffic:**

- Add these referrers to a custom channel group or monitor in Acquisition reports:
  - `chat.openai.com`
  - `perplexity.ai`
  - `gemini.google.com`
  - `claude.ai`
- AI-referred sessions grew 527% year-over-year in early 2025. This traffic source is compounding — track it now even if volumes are small.

### Step 7: Measurement Cadence

```
| Frequency  | What to Check                                                                                    |
|------------|--------------------------------------------------------------------------------------------------|
| Weekly     | New backlinks acquired, keyword ranking movements, GSC for crawl errors, community engagement     |
| Monthly    | Backlink profile growth, content performance by referral source, AI visibility manual checks      |
| Quarterly  | Full backlink audit (toxic link review), competitor authority comparison, platform strategy review |
| Biannually | Tool stack assessment, budget reallocation, strategy pivot decisions based on 6-month trends      |
```

Track the compounding effect: off-page authority builds slowly (expect 3-6 months for measurable backlink impact, 6-12 months for significant AI citation improvements). Document baseline metrics at the start so progress is visible.

## Available scripts

Start with `scripts/probe-ai-visibility.py` to establish your AI citation baseline, then measure monthly to track the impact of your authority-building efforts. The script generates a structured check plan with per-platform instructions. You must execute the manual verification steps for each platform listed in the output.

| Script | What it does | Run it when |
|--------|-------------|-------------|
| `probe-ai-visibility.py` | Generates a structured check plan (JSON) with per-platform instructions for testing AI visibility. Does not execute checks directly — the agent must perform the manual verification steps for ChatGPT, Claude, and Gemini listed in the output. **Key measurement script.** | Baseline + monthly |
| `check-backlink-profile.py` | Estimates backlink profile via WebSearch or paid APIs. Identifies top referring domains. | Baseline + quarterly |
| `monitor-brand-mentions.py` | Finds brand mentions across web, Reddit, HN, LinkedIn. Classifies as linked/unlinked and by sentiment. | Monthly |
| `audit-platform-presence.py` | Checks brand presence on 7 AI-cited platforms. Identifies gaps and priorities. | Baseline + quarterly |
| `analyze-competitor-authority.py` | Compares authority signals across your domain and competitors. Identifies gaps and strengths. | Baseline + quarterly |
| `find-link-opportunities.py` | Discovers resource pages, guest post targets, roundups, and journalist queries for your topic. | Monthly |
| `track-ai-referrers.py` | Generates GA4 custom channel group config for AI referrer tracking. Setup guide included. | One-time setup |

All scripts accept `--tools tools.json` to use paid tool APIs when available. Without it, every script works using WebFetch and WebSearch as free baseline.

## Quality checklist

- [ ] Backlink tracking spreadsheet is set up with target sites prioritized by relevance and authority
- [ ] Brand mention monitoring is active (Google Alerts at minimum, dedicated tool if budget allows)
- [ ] At least 3 platforms from the AI citation list have active, quality profiles
- [ ] One linkable asset (research, tool, or comprehensive guide) exists or is in production
- [ ] Community participation is established in at least 2 relevant communities with value-first contributions
- [ ] AI visibility baseline is recorded (manual test of 10+ queries across 3+ AI platforms)
- [ ] Digital PR pitch list is built with 10+ relevant journalists or publications
- [ ] Measurement cadence is scheduled with calendar reminders for weekly, monthly, and quarterly reviews

## Common mistakes to avoid

- **Buying links or participating in link schemes.** Google penalties are real and recoverable but painful. Purchased links provide zero AI citation benefit because AI engines assess source quality independently.
- **Ignoring multi-platform presence.** AI engines cite Reddit, YouTube, LinkedIn, and Wikipedia — not just your domain. If you only build backlinks to your website, you miss the GEO half of SGEO.
- **Self-promotion without value in communities.** Reddit, Hacker News, and forums have strong norms against marketing. Violating them damages your reputation permanently in that community and can result in bans.
- **Not tracking AI visibility.** You cannot improve what you do not measure. AI citation is a new metric — most competitors are not tracking it yet, which is an advantage if you start now.
- **Focusing only on backlinks, ignoring brand mentions.** AI engines weigh unlinked brand mentions as authority signals. A brand mentioned in 50 articles without links still registers as authoritative.
- **Expecting overnight results.** Authority building is a 6-12 month compounding investment. Backlink campaigns take 3-6 months to show ranking impact. AI citation changes lag further behind.
- **Only existing on your own domain.** If your brand has no presence on Reddit, LinkedIn, YouTube, or industry forums, AI engines have fewer sources to cite you from. Diversify your presence.
- **Neglecting content quality while chasing links.** Authority without fresh, accurate content does not rank or get cited. Links to outdated or thin content waste the authority they pass.
- **Trying to do everything at once.** Pick 2-3 authority channels (e.g., backlinks + Reddit + digital PR) and execute consistently. Spreading effort across all channels simultaneously produces mediocre results everywhere.
