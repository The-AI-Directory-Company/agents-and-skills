# Structured Data Types Reference

Schema.org types organized by page type, with validation tools and rich result eligibility. Use this when auditing Section 4 (Structured Data) of the technical SEO audit.

---

## Schema Types by Page Type

### Homepage

| Schema Type | Purpose | Rich Result | Priority |
|-------------|---------|-------------|----------|
| Organization | Identifies the business entity | Knowledge Panel | High |
| WebSite | Declares site-level properties | Sitelinks Search Box | Medium |
| LocalBusiness (if applicable) | Physical location details | Local Pack, Knowledge Panel | High (local businesses) |

**Required properties (Organization):** name, url, logo, contactPoint, sameAs (social profiles).

### Product Pages (E-commerce)

| Schema Type | Purpose | Rich Result | Priority |
|-------------|---------|-------------|----------|
| Product | Product details | Product rich result (price, availability, reviews) | High |
| Offer (nested in Product) | Pricing and availability | Price shown in search results | High |
| AggregateRating (nested) | Review summary | Star rating in search results | High |
| Review (nested) | Individual reviews | Review snippets | Medium |
| BreadcrumbList | Navigation path | Breadcrumb trail in SERP | Medium |

**Required properties (Product):** name, image, description, offers (with price, priceCurrency, availability).

### Blog / Article Pages

| Schema Type | Purpose | Rich Result | Priority |
|-------------|---------|-------------|----------|
| Article / BlogPosting | Identifies article content | Article rich result, Top Stories | High |
| BreadcrumbList | Navigation path | Breadcrumb trail in SERP | Medium |
| Person (author) | Author identification | Author attribution | Medium |
| ImageObject | Article images | Image search enrichment | Low |

**Required properties (Article):** headline, image, datePublished, author.

### FAQ Pages

| Schema Type | Purpose | Rich Result | Priority |
|-------------|---------|-------------|----------|
| FAQPage | Question-answer pairs | FAQ rich result (expandable Q&A in SERP) | High |
| Question + Answer (nested) | Individual Q&A pairs | Displayed inline in search results | High |

**Required properties (FAQPage):** mainEntity array of Question objects, each with name (question text) and acceptedAnswer with text.

**Note:** Google has significantly reduced FAQ rich result visibility since August 2023. They now appear primarily for well-known government and health websites. Still worth implementing for other search engines and potential future eligibility.

### How-To Pages

| Schema Type | Purpose | Rich Result | Priority |
|-------------|---------|-------------|----------|
| HowTo | Step-by-step instructions | How-to rich result with steps | Medium |
| HowToStep (nested) | Individual steps | Step-by-step display | Medium |

**Required properties (HowTo):** name, step (array of HowToStep with text).

### Event Pages

| Schema Type | Purpose | Rich Result | Priority |
|-------------|---------|-------------|----------|
| Event | Event details | Event rich result (date, location, tickets) | High |

**Required properties (Event):** name, startDate, location (Place or VirtualLocation), eventStatus.

### Recipe Pages

| Schema Type | Purpose | Rich Result | Priority |
|-------------|---------|-------------|----------|
| Recipe | Recipe details | Recipe rich result (image, rating, time, ingredients) | High |

**Required properties (Recipe):** name, image, recipeIngredient, recipeInstructions.

### SaaS / Software Pages

| Schema Type | Purpose | Rich Result | Priority |
|-------------|---------|-------------|----------|
| SoftwareApplication | Software details | Software rich result (rating, price) | Medium |
| AggregateRating (nested) | Review summary | Star rating | Medium |
| Offer (nested) | Pricing | Price display | Medium |

### Job Posting Pages

| Schema Type | Purpose | Rich Result | Priority |
|-------------|---------|-------------|----------|
| JobPosting | Job listing details | Google for Jobs listing | High |

**Required properties (JobPosting):** title, description, datePosted, hiringOrganization, jobLocation (or jobLocationType for remote).

---

## Validation Tools

| Tool | URL | What It Checks |
|------|-----|---------------|
| Google Rich Results Test | search.google.com/test/rich-results | Validates structured data and previews rich result eligibility |
| Schema.org Validator | validator.schema.org | Validates against the Schema.org specification (broader than Google's subset) |
| Google Search Console (Enhancements) | search.google.com/search-console | Shows structured data errors/warnings across all indexed pages |
| Bing Markup Validator | bing.com/webmasters/markup-validator | Validates markup for Bing rich results |

### Validation Workflow

1. **Test individual pages** with Google Rich Results Test during development
2. **Monitor at scale** with Google Search Console Enhancements reports
3. **Cross-check** with Schema.org Validator for spec compliance beyond Google's requirements
4. **Audit periodically** with a crawl tool (Screaming Frog, Sitebulb) to catch missing or broken markup across the site

---

## Rich Result Eligibility

Not all structured data produces visible rich results. Google's support varies by type and changes over time.

| Schema Type | Rich Result | Current Status (as of 2025) |
|-------------|-------------|---------------------------|
| Article | Article rich result, Top Stories | Active |
| BreadcrumbList | Breadcrumb trail | Active |
| Event | Event listing | Active |
| FAQPage | Expandable FAQ | Reduced — primarily government/health sites |
| HowTo | Step-by-step display | Reduced visibility |
| JobPosting | Google for Jobs | Active |
| LocalBusiness | Local Pack, Knowledge Panel | Active |
| Organization | Knowledge Panel | Active |
| Product + Offer | Price, availability, reviews | Active (Merchant Center integration expanding) |
| Recipe | Recipe carousel | Active |
| Review / AggregateRating | Star ratings | Active (self-serving reviews restricted) |
| SoftwareApplication | Software info panel | Limited |
| VideoObject | Video carousel, key moments | Active |
| WebSite | Sitelinks Search Box | Active |

### Important Notes

- **Self-serving reviews are restricted.** A business cannot add AggregateRating markup for its own products based on reviews collected on its own site unless it meets Google's review snippet guidelines. Third-party review platforms are preferred.
- **JSON-LD is the recommended format.** Google prefers JSON-LD over Microdata or RDFa. JSON-LD can be placed anywhere in the HTML (typically in `<head>` or end of `<body>`).
- **Structured data must match visible content.** Markup that describes content not visible on the page risks a manual action. If the price in the markup differs from the price on the page, that is a violation.
