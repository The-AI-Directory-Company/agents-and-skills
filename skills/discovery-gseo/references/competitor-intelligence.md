# Competitor Intelligence

Competitor analysis is the single highest-ROI activity in the entire discovery process. Other websites have done the research for you. They have tested keywords, created content, built authority, and proven what works. Use their work as a shortcut.

## SEO competitor identification

Your SEO competitors are not necessarily your business competitors. They are the websites that rank for the keywords you want to rank for.

**How to find them:**
1. Search Google for 5-10 of your seed keywords (in incognito mode).
2. Note which domains appear repeatedly in the top 10 results across multiple seeds.
3. These are your SEO competitors, even if they sell different products.

**Example:** If you sell invoicing software, your SEO competitors might include FreshBooks, Wave, Zoho Invoice (direct product competitors), HubSpot (content competitor — their blog ranks for invoicing keywords), and G2 or Capterra (aggregator competitors — review sites that dominate comparison queries).

**Pick 3-5 competitors for analysis.** Include a mix:
- 1-2 direct product competitors (sell similar products)
- 1-2 content competitors (rank for informational keywords in your space)
- 1 aggregator or review site (if they dominate your SERP)

SEO competitors ≠ business competitors. A blog that outranks you for every informational keyword in your space is a more important SEO competitor than a direct product rival with no organic presence.

## Keyword gap analysis methodology

A keyword gap analysis reveals keywords your competitors rank for that you do not. These represent validated opportunities — someone has already proven these keywords drive traffic in your space.

### Ahrefs Content Gap

1. Go to Competitive Analysis > Content Gap.
2. Enter your domain in the "Target" field.
3. Enter 3-5 competitor domains in the "Competitor" fields.
4. Click "Show keyword opportunities."
5. The tool shows keywords competitors rank for and you do not. These are your "missing" keywords.
6. Filter by KD (set a max based on your domain authority) and volume (minimum threshold for relevance).
7. Export the list. Sort by volume and business relevance.

### Semrush Keyword Gap

1. Go to the Keyword Gap tool.
2. Enter your domain and up to 4 competitor domains.
3. Select your target country. Click "Compare."
4. **"Missing" tab:** Keywords ALL your competitors rank for but you do not. Highest priority.
5. **"Weak" tab:** Keywords where your competitors rank higher. Optimization opportunity.
6. **"Strong" tab:** Keywords where you outrank competitors. Protect these.
7. Export Missing and Weak lists for your master spreadsheet.

### SE Ranking

1. Go to Competitive Research > enter a competitor's domain.
2. View their organic keywords — every keyword they rank for with position, volume, and traffic share.
3. Use the Keyword Gap analysis to compare with your domain.
4. Focus on keywords where the competitor ranks well and you have no presence.

### Free alternative (no paid tools)

When no paid tool is available, approximate gap analysis using WebSearch:

1. For each competitor: `site:competitor.com` to see total indexed pages.
2. For each competitor: `site:competitor.com [seed keyword]` to find their relevant pages.
3. Catalog their pages: list the topics they cover (blog posts, landing pages, comparison pages, tools).
4. Compare against your own site: `site:yourdomain.com` to catalog your pages.
5. Identify gaps: topics competitors cover that you do not.

Run `scripts/competitor-gap-analysis.py --domain yourdomain.com --competitors comp1.com,comp2.com` to automate this process.

This free method lacks volume and KD data but still reveals topic gaps. You can estimate volume using Google Keyword Planner for the gap keywords you discover.

## Top pages analysis

Understanding which competitor pages drive the most traffic reveals where the proven opportunities are.

**In Ahrefs:**
1. Site Explorer > enter competitor domain > Top Pages.
2. Sort by Traffic (descending).
3. Note the top 20 pages: their URLs, the keywords they target, the traffic they receive.
4. Look for patterns: are their highest-traffic pages blog posts? Comparison pages? Free tools? Templates?

**What to learn from top pages:**
- **Content format:** What type of page drives the most traffic? If their top page is a free tool, that is the format Google rewards for that keyword.
- **Depth:** How comprehensive is the content? Word count, section count, number of examples.
- **Angle:** Beginner guide? Expert deep-dive? Comparison? Review? The angle tells you what resonates with the audience.
- **Keyword targeting:** What is the primary keyword in the title, H1, and URL? Are they targeting a single keyword per page or multiple related terms?
- **Structured data:** Do they use FAQ schema, How-To schema, or other structured data that wins SERP features?

## Analyzing why competitors rank

For the most interesting gap keywords, manually visit the ranking pages and conduct a detailed analysis.

**Questions to answer for each competing page:**

- **Page type:** Blog post, landing page, comparison page, free tool, tutorial, documentation, category page?
- **Content depth:** Rough word count. Number of sections. Breadth of subtopics covered. Quality of examples.
- **Visual aids:** Screenshots, diagrams, videos, charts? Pages with strong visual content tend to rank better for informational queries.
- **Angle/perspective:** Beginner guide aimed at novices? Technical deep-dive for experts? Product comparison for buyers? The angle determines the audience and intent match.
- **Weaknesses to exploit:**
  - Outdated information (dates, statistics, tool versions)
  - Poor content structure (wall of text, no headings, no clear hierarchy)
  - Thin coverage (mentions a topic but does not explain it in depth)
  - No examples or templates
  - No original data or unique perspective
  - Bad user experience (intrusive ads, slow loading, aggressive popups)

Your goal: create content that is strictly better on every dimension that matters for this keyword.

## GEO competitor analysis

Traditional competitor analysis asks "who ranks in Google?" GEO competitor analysis asks "who gets cited by AI?"

These are different questions with different answers. A site ranking #1 in Google may not be cited by any AI platform. A site ranking #8 might be cited by all of them. Understanding this gap is critical for GEO-aware discovery.

### Who gets cited by AI?

For your target queries, check which competitors AI platforms cite:

**Perplexity:** Search your target queries on Perplexity. It explicitly shows sources for each claim. Record:
- Which domains appear as sources
- Which specific pages are cited
- How many citations each competitor receives across your queries

**ChatGPT (with Browse):** Ask your target queries. When ChatGPT provides answers with citations, record the sources.

**Gemini:** Same queries. Note which sources are cited.

Run `scripts/probe-ai-discovery.py --queries target-queries.txt --brand YourBrand` to automate this across queries.

### What do cited pages have in common?

Pages that get cited by AI tend to share characteristics:
- **Direct-answer formatting:** Clear, concise answers to specific questions in the first paragraph or a dedicated section.
- **Data density:** Specific numbers, statistics, comparisons, and quantified claims. AI prefers citable facts over vague prose.
- **Author attribution:** Named authors with credentials. AI platforms factor in source authority.
- **Structured content:** Well-organized with clear headings, lists, and tables that AI can parse.
- **Recency:** Recently updated content with current dates and statistics.
- **Unique information:** Original research, proprietary data, or expert analysis that cannot be found elsewhere.

### Identifying GEO gaps

A GEO gap exists when:
- AI answers a query but cites weak or outdated sources. You can create better content and replace those citations.
- AI answers a query but does not cite any source in your competitive space. No competitor has optimized for this.
- Your competitor ranks in Google but is not cited by AI. Their content is not structured for AI consumption.

These gaps are high-opportunity targets. A keyword with a GEO gap is easier to win AI visibility for than a keyword where AI cites strong, authoritative sources.

Map GEO gaps to your keyword spreadsheet. They directly feed the GEO Opportunity dimension in Phase 9 prioritization.
