#!/usr/bin/env python3
"""
Monitor Brand Mentions

Searches for brand mentions across web, Reddit, Hacker News, and LinkedIn.
Classifies mentions as linked/unlinked and by sentiment.
Prioritizes unlinked mentions on high-authority sites as link conversion candidates.

Usage:
    python monitor-brand-mentions.py --brand "Acme Corp"
    python monitor-brand-mentions.py --brand "Acme Corp" --domain acme.com --products "AcmeDB,AcmeCloud"
    python monitor-brand-mentions.py --brand "Acme Corp" --tools tools.json
"""

import argparse
import json
import sys
import os
from datetime import datetime


POSITIVE_SIGNALS = [
    "recommend",
    "great",
    "love",
    "excellent",
    "best",
    "amazing",
    "fantastic",
    "impressed",
    "helpful",
    "solid",
    "reliable",
    "outstanding",
]

NEGATIVE_SIGNALS = [
    "avoid",
    "disappointed",
    "issue",
    "problem",
    "terrible",
    "worst",
    "broken",
    "unusable",
    "frustrated",
    "regret",
    "scam",
    "overpriced",
]


def load_tools(tools_path):
    """Load tool inventory from JSON file."""
    if tools_path and os.path.exists(tools_path):
        with open(tools_path, "r") as f:
            return json.load(f)
    return {}


def classify_sentiment(text):
    """Classify sentiment based on signal words in text."""
    text_lower = text.lower()
    pos_count = sum(1 for word in POSITIVE_SIGNALS if word in text_lower)
    neg_count = sum(1 for word in NEGATIVE_SIGNALS if word in text_lower)

    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    return "neutral"


def build_search_queries(brand, domain, products):
    """Build the search queries for brand mention monitoring."""
    queries = []

    # Core brand mention search
    queries.append(
        {
            "query": f'"{brand}" -site:{domain}' if domain else f'"{brand}"',
            "platform": "web",
            "purpose": "General web mentions of the brand",
        }
    )

    # Reddit mentions
    queries.append(
        {
            "query": f'site:reddit.com "{brand}"',
            "platform": "reddit",
            "purpose": "Reddit mentions and discussions",
        }
    )

    # Hacker News mentions
    queries.append(
        {
            "query": f'site:news.ycombinator.com "{brand}"',
            "platform": "hn",
            "purpose": "Hacker News mentions",
        }
    )

    # LinkedIn mentions
    queries.append(
        {
            "query": f'site:linkedin.com "{brand}"',
            "platform": "linkedin",
            "purpose": "LinkedIn mentions",
        }
    )

    # Product-specific searches
    if products:
        for product in products:
            product = product.strip()
            if product:
                queries.append(
                    {
                        "query": f'"{product}" -site:{domain}'
                        if domain
                        else f'"{product}"',
                        "platform": "web",
                        "purpose": f"Mentions of product: {product}",
                    }
                )

    return queries


def build_analysis_instructions(brand, domain):
    """Build instructions for processing search results."""
    return [
        "Execute each query via WebSearch and collect all results.",
        "For each result, extract: URL, domain, title, snippet.",
        f"Classify as LINKED (snippet or page contains href to {domain}) or UNLINKED."
        if domain
        else "Classify as LINKED or UNLINKED based on whether a link to the brand's site is present.",
        "Classify sentiment for each mention using snippet text: positive, negative, or neutral.",
        "Identify high-authority unlinked mentions (DA/DR >40 or well-known domains) as conversion candidates.",
        "Deduplicate results by URL.",
        "Group results by platform (web, reddit, linkedin, hn).",
    ]


def build_output(brand, domain, products, queries):
    """Build the standardized output JSON."""
    return {
        "brand": brand,
        "domain": domain,
        "products": products if products else [],
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "queries_prepared",
        "queries": queries,
        "analysis_instructions": build_analysis_instructions(brand, domain),
        "output_template": {
            "total_mentions": "TO_BE_FILLED",
            "linked": "TO_BE_FILLED",
            "unlinked": "TO_BE_FILLED",
            "sentiment": {
                "positive": "TO_BE_FILLED",
                "neutral": "TO_BE_FILLED",
                "negative": "TO_BE_FILLED",
            },
            "conversion_candidates": [
                {
                    "url": "example URL",
                    "domain": "example.com",
                    "estimated_authority": "high|medium|low",
                    "context": "snippet showing the mention",
                }
            ],
            "platforms": {
                "reddit": "TO_BE_FILLED",
                "web": "TO_BE_FILLED",
                "linkedin": "TO_BE_FILLED",
                "hn": "TO_BE_FILLED",
            },
        },
        "sentiment_keywords": {
            "positive": POSITIVE_SIGNALS,
            "negative": NEGATIVE_SIGNALS,
        },
        "next_steps": [
            "Execute all prepared queries via WebSearch",
            "Process results using the analysis instructions",
            "Fill in the output template with actual data",
            "Prioritize unlinked high-authority mentions for outreach",
            "Flag negative mentions for reputation management review",
        ],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Monitor brand mentions across web, Reddit, HN, and LinkedIn. "
        "Classifies mentions by link status and sentiment. "
        "Identifies high-authority unlinked mentions for link conversion.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python monitor-brand-mentions.py --brand "Acme Corp"
    python monitor-brand-mentions.py --brand "Acme Corp" --domain acme.com
    python monitor-brand-mentions.py --brand "Acme Corp" --products "AcmeDB,AcmeCloud"

Output: JSON with search queries and analysis instructions for agent execution.
        """,
    )
    parser.add_argument(
        "--brand",
        required=True,
        help="Brand name to search for (use quotes for multi-word names)",
    )
    parser.add_argument(
        "--domain",
        default=None,
        help="Brand's domain (e.g., acme.com) — used to exclude own site and identify linked mentions",
    )
    parser.add_argument(
        "--products",
        default=None,
        help="Comma-separated product names to also search for",
    )
    parser.add_argument(
        "--tools",
        default=None,
        help="Path to tools.json inventory file",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: stdout)",
    )

    args = parser.parse_args()

    domain = args.domain
    if domain:
        domain = domain.replace("https://", "").replace("http://", "").strip("/")

    products = args.products.split(",") if args.products else []

    queries = build_search_queries(args.brand, domain, products)
    output = build_output(args.brand, domain, products, queries)

    output_json = json.dumps(output, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
