# Structured Data: Schema.org JSON-LD Implementation Guide

Structured data helps search engines understand page content precisely and enables rich results. For AI systems, structured data provides machine-readable facts that are easier to extract and cite accurately than unstructured text. FAQ Schema is your single best GEO investment for structured data — pre-package Q&A pairs and AI engines extract them directly.

## Why JSON-LD

Google explicitly recommends JSON-LD as the preferred structured data format. It lives in a `<script type="application/ld+json">` tag in your HTML `<head>` (or `<body>`), separate from your markup. This makes it easier to maintain, less error-prone than Microdata or RDFa, and trivial to generate server-side.

Do not use Microdata for new implementations. It mixes data into HTML attributes, is harder to maintain, and JSON-LD has feature parity with better tooling.

## Templates by page type

### Organization (homepage)

Every site should have Organization schema on the homepage. This feeds Knowledge Panels and gives AI engines your canonical entity information.

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Your Company Name",
  "url": "https://example.com",
  "logo": {
    "@type": "ImageObject",
    "url": "https://example.com/logo.png",
    "width": 600,
    "height": 60
  },
  "sameAs": [
    "https://twitter.com/yourcompany",
    "https://linkedin.com/company/yourcompany",
    "https://github.com/yourcompany"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-555-5555",
    "contactType": "customer service",
    "availableLanguage": ["English"]
  },
  "foundingDate": "2020-01-15",
  "numberOfEmployees": {
    "@type": "QuantitativeValue",
    "minValue": 10,
    "maxValue": 50
  }
}
```

### Product

Product schema enables rich snippets with price, availability, and ratings in search results. AI systems use it to answer product comparison queries accurately.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Widget Pro 3000",
  "description": "Professional-grade widget with 5-year warranty.",
  "image": [
    "https://example.com/photos/widget-pro-front.jpg",
    "https://example.com/photos/widget-pro-side.jpg"
  ],
  "brand": {
    "@type": "Brand",
    "name": "WidgetCorp"
  },
  "sku": "WP3000",
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/widget-pro-3000",
    "priceCurrency": "USD",
    "price": 299.99,
    "availability": "https://schema.org/InStock",
    "priceValidUntil": "2026-12-31",
    "seller": {
      "@type": "Organization",
      "name": "WidgetCorp"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": 4.6,
    "reviewCount": 247
  },
  "review": [
    {
      "@type": "Review",
      "author": {"@type": "Person", "name": "Jane Smith"},
      "datePublished": "2026-02-10",
      "reviewRating": {"@type": "Rating", "ratingValue": 5},
      "reviewBody": "Best widget I have ever used. Build quality is exceptional."
    }
  ]
}
```

### Article

Article schema is essential for blog posts, news, and editorial content. The `author` and `dateModified` fields are particularly important for E-E-A-T and AI citation — AI systems prefer content with clear attribution and recent updates.

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Optimize Core Web Vitals in 2026",
  "datePublished": "2026-01-15T08:00:00+00:00",
  "dateModified": "2026-03-20T14:30:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Alex Chen",
    "jobTitle": "Senior Performance Engineer",
    "url": "https://example.com/team/alex-chen"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Example Corp",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "image": "https://example.com/images/cwv-guide-hero.jpg",
  "description": "A practitioner's guide to fixing LCP, INP, and CLS with specific techniques for Next.js, WordPress, and Shopify."
}
```

### FAQPage

FAQ Schema is the highest-value structured data for GEO. The Q&A format maps directly to how users query AI assistants. When you publish a genuine FAQ with properly structured schema, you are pre-packaging extractable knowledge blocks for AI engines.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the maximum URL count for an XML sitemap?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Each XML sitemap file can contain up to 50,000 URLs and must be under 50MB uncompressed. For sites with more URLs, use a sitemap index file that references multiple sitemap files."
      }
    },
    {
      "@type": "Question",
      "name": "Does blocking AI crawlers in robots.txt remove existing AI citations?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Not immediately. Blocking prevents future crawling, but AI systems retain previously crawled data. Over time, citations will decay as the cached content becomes stale and competitors publish fresher material. Unblocking is the correct action if AI visibility matters."
      }
    }
  ]
}
```

**Google reduced FAQ rich result eligibility** in 2023 to government and health sites only. But FAQPage schema still benefits you because: (1) AI engines read it regardless of Google's rich result policy, and (2) Bing and other search engines may still display FAQ snippets.

### HowTo

HowTo schema works well for procedural content. Each step becomes a rich result snippet and an extractable block for AI.

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Submit an XML Sitemap to Google Search Console",
  "totalTime": "PT5M",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Log in to Google Search Console",
      "text": "Navigate to search.google.com/search-console and sign in with the Google account that has verified ownership of the property.",
      "url": "https://example.com/guide#step-1"
    },
    {
      "@type": "HowToStep",
      "name": "Navigate to Sitemaps",
      "text": "In the left sidebar, click 'Sitemaps' under the 'Indexing' section.",
      "url": "https://example.com/guide#step-2"
    },
    {
      "@type": "HowToStep",
      "name": "Submit sitemap URL",
      "text": "Enter your sitemap URL (e.g., /sitemap.xml) in the 'Add a new sitemap' field and click Submit.",
      "url": "https://example.com/guide#step-3"
    }
  ]
}
```

### LocalBusiness

For businesses with a physical location. Feeds the local pack in Google search and provides location data to AI systems.

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Widget Repair Shop",
  "image": "https://example.com/photos/storefront.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "Springfield",
    "addressRegion": "IL",
    "postalCode": "62701",
    "addressCountry": "US"
  },
  "telephone": "+1-555-555-1234",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  ],
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 39.7817,
    "longitude": -89.6501
  }
}
```

### Service

For service pages. No rich result, but provides structured data for AI knowledge extraction.

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Technical SEO Audit",
  "description": "Comprehensive technical audit covering crawlability, indexation, Core Web Vitals, and AI crawler access.",
  "provider": {
    "@type": "Organization",
    "name": "Example Agency"
  },
  "areaServed": {
    "@type": "Country",
    "name": "United States"
  },
  "serviceType": "SEO Consulting"
}
```

### BreadcrumbList

Breadcrumbs help search engines understand site structure and display breadcrumb trails in search results. Implement on every page.

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/"},
    {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://example.com/blog/"},
    {"@type": "ListItem", "position": 3, "name": "Technical SEO Guide", "item": "https://example.com/blog/technical-seo-guide/"}
  ]
}
```

## Nesting patterns

Structured data types nest inside each other. The most common nesting patterns:

- **Organization inside Article** (as `publisher`): Every Article should reference its publisher Organization.
- **Person inside Article** (as `author`): Use a full Person object with `name`, `jobTitle`, and `url` — not just a string name.
- **Offer inside Product**: Products always contain an Offer (or AggregateOffer for multiple variants).
- **AggregateRating inside Product**: Ratings belong inside the Product, not as standalone schema.
- **ImageObject inside Organization** (as `logo`): Use an ImageObject with `url`, `width`, `height` rather than a bare URL string.

**Multiple schemas on one page:** A product page might have Product + BreadcrumbList + Organization. Each goes in its own `<script type="application/ld+json">` tag or combined in a `@graph` array.

## Validation workflow

1. **Google Rich Results Test** (`https://search.google.com/test/rich-results`): Paste a URL or code snippet. Shows which rich results are eligible and flags errors/warnings. This is the authoritative validator for Google-specific rich results.

2. **Schema.org Validator** (`https://validator.schema.org/`): Validates against the full schema.org vocabulary. Catches issues the Rich Results Test might not (non-Google types, missing recommended properties).

3. **GSC Enhancements report**: After deployment, monitor the Enhancements section in Google Search Console. It shows error counts per schema type across your entire site. Fix errors promptly — persistent schema errors can cause Google to ignore your structured data entirely.

4. **Manual JSON validation**: Before deploying, paste your JSON-LD into a JSON validator to catch syntax errors (missing commas, unescaped quotes). A single syntax error invalidates the entire block.

## Common mistakes

| Mistake | Risk | Fix |
|---------|------|-----|
| Schema does not match visible content | Manual action from Google | Schema must reflect exactly what users see |
| Rating in schema differs from page rating | Manual action | Sync aggregateRating with displayed rating |
| Using Microdata instead of JSON-LD | Maintenance burden, harder to debug | Migrate to JSON-LD |
| Missing required properties | Schema ignored, no rich result | Check Rich Results Test, add all required fields |
| Author as string instead of Person object | Weak E-E-A-T signal | Use full Person with name, jobTitle, url |
| Invalid JSON syntax | Entire schema block ignored | Validate JSON before deployment |
| Structured data on non-indexable pages | Wasted effort | Only add schema to indexable, canonical pages |
| Duplicate schema blocks | Confusing signals | One schema per type per page (use @graph for multiples) |
