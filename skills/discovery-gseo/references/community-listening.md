# Community Listening

Keyword tools rely on historical data. Communities show you what people are asking right now. The language they use maps directly to both search queries and AI prompts — making community-sourced keywords doubly valuable for GSEO discovery.

## Platform-by-platform guide

### Reddit

The richest source of customer language for most B2B and consumer categories.

**How to use it:**
1. Search reddit.com for your product category or industry.
2. Identify relevant subreddits (e.g., r/smallbusiness, r/SaaS, r/webdev, r/freelance).
3. Sort by Top (past year) and New to see both proven topics and emerging questions.
4. Read post titles AND top comments — the real language is in the comments.

**What to watch for:**
- **Repeated questions:** If 5 different people ask "how do I send automated payment reminders," that is a keyword candidate.
- **Complaints about tools:** "FreshBooks is too expensive for solo freelancers" → "FreshBooks alternative freelancers", "cheap invoicing software."
- **Comparison language:** "Has anyone switched from X to Y?" → "[X] vs [Y]", "[X] alternative."
- **Pain point descriptions:** The raw, unfiltered language of someone with a problem. These map directly to long-tail search queries.

**Browser automation:** Run `scripts/scrape-community-keywords.py --topic 'invoicing software' --platforms reddit` to automate extraction. The script navigates Reddit via Playwright, searches your topic, and extracts post titles, popular comment phrases, and question patterns from the top 50 results.

### Hacker News

Technical audiences. Especially valuable for developer tools, SaaS, and infrastructure products.

**How to use it:**
1. Search hn.algolia.com for your product category.
2. Filter by date (last year) and sort by points (popularity).
3. Read "Ask HN" threads — these are direct tool recommendation requests. "Ask HN: What do you use for invoicing?"
4. Read "Show HN" comments on competing products — people describe what they like, what is missing, and what they would prefer.

**What to capture:** Technical terminology, integration needs ("works with Stripe", "connects to QuickBooks"), workflow descriptions ("I need to automate the invoice-to-payment pipeline").

### Twitter/X

Real-time pulse. Best for emerging trends and public complaints.

**How to use it:**
1. Search for your product category, competitor names, and problem descriptions.
2. Look at replies and quote tweets — conversations reveal pain points.
3. Watch for trending topics in your space.

**What to capture:** Short, punchy problem descriptions. Comparison requests. Product frustrations that drive switching behavior.

### Quora

Questions on Quora mirror Google searches directly. The format is almost identical to how people phrase search queries.

**How to use it:**
1. Search Quora for your product category.
2. Read the questions — not the answers. The questions are the keyword candidates.
3. Look at "Related Questions" in the sidebar for additional ideas.

**What to capture:** Question phrasing that matches search query patterns. "What is the best invoicing software for freelancers?" maps directly to "best invoicing software for freelancers."

### Product Hunt

New products and launches in your space. Comments reveal what people want.

**How to use it:**
1. Search Product Hunt for products similar to yours.
2. Read the launch comments — people describe their needs, compare alternatives, and express frustrations.
3. Look at "Alternatives" sections for competitor landscape.

**What to capture:** Feature requests, comparison language, use-case descriptions.

### Industry forums, Discord, and Slack groups

Every niche has dedicated communities. These are often the most valuable sources because the language is hyper-specific to your audience.

**How to find them:**
- Search Google: "[your industry] forum", "[your industry] community", "[your industry] Discord."
- Check product documentation for community links.
- Look for Slack groups listed in industry newsletters.

**How to use them:**
- Lurk before extracting. Understand the community norms.
- Search internal archives for your category keywords.
- Pay attention to recurring questions and complaints.
- Note terminology that is specific to the community — these become niche keyword targets.

## Language pattern extraction

You are not looking for keyword data in communities. You are looking for **language patterns** — how real people describe problems in their own words.

### Pain point to keyword candidate mapping

Turn community observations into keyword candidates by identifying the search query someone would type if they were looking for a solution:

| Community observation | Suggested keyword |
|----------------------|------------------|
| "I need a way to automatically send payment reminders" | automatic payment reminder software |
| "Is there a Stripe alternative that handles invoicing too?" | Stripe alternative with invoicing |
| "How do I set up recurring billing without a developer?" | recurring billing no code |
| "FreshBooks is way too expensive for what it does" | FreshBooks alternative cheaper |
| "I just want to create an invoice and send it — nothing else" | simple invoice tool |
| "Does anyone know a form builder that handles HIPAA compliance?" | HIPAA compliant form builder |

### Zero-volume opportunities

Community-sourced keywords often show zero volume in keyword tools. This does not mean nobody searches for them. It means the volume is below the tool's measurement threshold.

These keywords are valuable when:
- **Intent is perfect:** The person expressing this need is exactly your target customer.
- **Competition is zero:** Nobody has created content targeting this exact query.
- **They aggregate:** 20 zero-volume keywords targeting the same topic can drive meaningful traffic when grouped into one comprehensive page.
- **They are emerging:** Community discussions often surface trends 3-6 months before keyword tools register volume.

## Browser automation for community scraping

### Why browser automation for communities?

Community platforms use dynamic loading (Reddit's infinite scroll), JavaScript rendering (forum software), and pagination (HN) that simple HTTP fetches cannot handle. Browser automation via Playwright gives you the same experience a human researcher would have.

**Playwright technique for Reddit:**
1. Navigate to `reddit.com/search?q=[topic]&sort=relevance&t=year`
2. Wait for results to load (dynamic content)
3. Extract post titles and upvote counts
4. Click into top posts, extract comment text
5. Identify repeated phrases and question patterns

**Rate limiting:** Respect community platforms. Wait 3-5 seconds between page loads. Do not scrape aggressively. These are communities, not data feeds.

Run `scripts/scrape-community-keywords.py --topic 'your category' --platforms reddit,hn` to automate extraction with built-in rate limiting.

## GEO dimension of community listening

Community language maps directly to AI query language. This is the insight that makes community listening doubly valuable for GSEO.

**The pattern:**
- Questions people ask on Reddit → questions people ask ChatGPT
- Pain points described in forums → problems people describe to AI assistants
- Comparison requests in communities → comparison queries to AI platforms
- Feature wishlists in product discussions → capability questions to AI

When someone writes on Reddit: "I need a simple invoicing tool that works with Stripe and doesn't cost a fortune" — that same person will eventually ask ChatGPT: "What's a simple invoicing tool that integrates with Stripe for under $20/month?"

Community-sourced keywords are therefore GEO-validated by default. If a topic generates discussion in communities, it generates queries to AI platforms. Content targeting these topics has built-in AI citation potential.

**Practical implication:** When you find a community-sourced keyword, give it a GEO score of at least 2 in your evaluation. Community-validated topics almost always have AI query counterparts.
