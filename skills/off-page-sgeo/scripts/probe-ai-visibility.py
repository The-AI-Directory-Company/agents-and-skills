#!/usr/bin/env python3
"""
Probe AI Visibility

Tests queries against AI platforms and records brand citations.
This is the key measurement script for off-page SGEO — run it to establish
a baseline and then monthly to track the impact of authority-building efforts.

Free path: WebFetch to check Perplexity results, WebSearch for cached AI answers.
Paid path: DataForSEO AI visibility endpoints, ChatGPT scraper API.

Usage:
    python probe-ai-visibility.py --brand "Acme Corp" --queries queries.txt
    python probe-ai-visibility.py --brand "Acme Corp" --queries queries.txt --tools tools.json
    python probe-ai-visibility.py --brand "Acme Corp" --queries queries.txt --output results.json
"""

import argparse
import json
import sys
import os
from datetime import datetime
from urllib.parse import quote_plus


def load_tools(tools_path):
    """Load tool inventory from JSON file."""
    if tools_path and os.path.exists(tools_path):
        with open(tools_path, "r") as f:
            return json.load(f)
    return {}


def load_queries(queries_path):
    """Load queries from a text file, one per line."""
    if not os.path.exists(queries_path):
        print(f"Error: Queries file not found: {queries_path}", file=sys.stderr)
        sys.exit(1)

    with open(queries_path, "r") as f:
        queries = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not queries:
        print("Error: No queries found in file.", file=sys.stderr)
        sys.exit(1)

    return queries


def build_query_checks(queries, brand):
    """Build the check plan for each query across available platforms."""
    checks = []

    for query in queries:
        encoded_query = quote_plus(query)

        check = {
            "query": query,
            "platforms": [
                {
                    "name": "Perplexity",
                    "method": "webfetch",
                    "url": f"https://www.perplexity.ai/search?q={encoded_query}",
                    "instructions": [
                        "Fetch the Perplexity search page via WebFetch.",
                        "Parse the response HTML for citations and source URLs.",
                        f'Search the response text for "{brand}" (case-insensitive).',
                        "Extract cited source URLs from the response.",
                        "Note any competitor brand names mentioned.",
                    ],
                    "fallback": {
                        "method": "websearch",
                        "query": f'site:perplexity.ai "{query}"',
                        "instructions": [
                            "If direct fetch fails, search for cached Perplexity results.",
                            f'Check if "{brand}" appears in any cached results.',
                        ],
                    },
                },
                {
                    "name": "ChatGPT",
                    "method": "manual_or_api",
                    "instructions": [
                        f'Ask ChatGPT: "{query}"',
                        f'Record whether "{brand}" is mentioned in the response.',
                        "List any competitor brands mentioned.",
                        "Note the source URLs if ChatGPT provides citations.",
                    ],
                    "automated_fallback": {
                        "method": "websearch",
                        "query": f'site:chat.openai.com "{query}" OR "{query}" chatgpt answer',
                        "instructions": [
                            "Search for cached or reported ChatGPT responses to this query.",
                        ],
                    },
                },
                {
                    "name": "Claude",
                    "method": "manual_or_api",
                    "instructions": [
                        f'Ask Claude: "{query}"',
                        f'Record whether "{brand}" is mentioned in the response.',
                        "List any competitor brands mentioned.",
                    ],
                },
                {
                    "name": "Gemini",
                    "method": "manual_or_api",
                    "instructions": [
                        f'Ask Gemini: "{query}"',
                        f'Record whether "{brand}" is mentioned in the response.',
                        "List any competitor brands mentioned.",
                        "Note any source citations provided.",
                    ],
                },
            ],
            "result_template": {
                "query": query,
                "platforms_checked": [],
                "brand_cited": False,
                "brand_citation_context": "",
                "competitors_cited": [],
                "cited_sources": [],
            },
        }
        checks.append(check)

    return checks


def build_output(brand, queries, checks):
    """Build the standardized output JSON."""
    return {
        "brand": brand,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "checks_prepared",
        "queries_count": len(queries),
        "checks": checks,
        "analysis_instructions": [
            "Execute each platform check for each query.",
            "Perplexity is the most accessible via WebFetch — prioritize it.",
            "For ChatGPT, Claude, and Gemini: use manual testing or API access if available.",
            f'For each response, search for "{brand}" (case-insensitive).',
            "Record all competitor brands mentioned in each response.",
            "Extract source URLs when platforms provide citations.",
            "Calculate citation rate: (queries where brand cited) / (total queries tested).",
            "Calculate competitor citation rates for comparison.",
        ],
        "output_template": {
            "brand": brand,
            "queries_tested": len(queries),
            "citations_found": "TO_BE_FILLED",
            "citation_rate": "TO_BE_FILLED (0.0-1.0)",
            "results": [
                {
                    "query": "example query",
                    "platforms_checked": ["perplexity", "chatgpt"],
                    "brand_cited": False,
                    "competitors_cited": ["competitor1", "competitor2"],
                    "cited_sources": ["reddit.com", "competitor1.com"],
                }
            ],
            "competitor_citation_rates": {
                "competitor1": "TO_BE_FILLED",
                "competitor2": "TO_BE_FILLED",
            },
            "recommendation": "TO_BE_FILLED",
        },
        "interpretation_guide": {
            "citation_rate_0_to_10pct": "Not visible. AI does not associate your brand with these queries. Focus on building platform presence and content authority.",
            "citation_rate_10_to_25pct": "Emerging visibility. Some queries trigger citations. Analyze which queries cite you and double down on those topics.",
            "citation_rate_25_to_50pct": "Established visibility. You appear regularly. Focus on expanding to queries where competitors are cited but you are not.",
            "citation_rate_50pct_plus": "Strong visibility. You are a primary source. Focus on maintaining freshness and expanding to adjacent query categories.",
        },
        "next_steps": [
            "Execute all checks and fill in the output template",
            "Save results with timestamp for trend tracking",
            "Compare against competitor citation rates",
            "Identify queries where competitors are cited but you are not — these are priority gaps",
            "Repeat monthly to track the impact of authority-building efforts",
        ],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Probe AI visibility by testing queries against AI platforms "
        "and recording brand citations. This is the key measurement script "
        "for off-page SGEO — run it to establish a baseline and then monthly.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python probe-ai-visibility.py --brand "Acme Corp" --queries queries.txt
    python probe-ai-visibility.py --brand "Acme Corp" --queries queries.txt --output results.json

Query file format (one query per line, # for comments):
    What is the best analytics tool for startups?
    # This is a comment
    How do I track website performance?
    Which analytics platforms do professionals recommend?

Output: JSON with prepared checks for each query across AI platforms.
        """,
    )
    parser.add_argument(
        "--brand",
        required=True,
        help="Brand name to check AI visibility for",
    )
    parser.add_argument(
        "--queries",
        required=True,
        help="Path to text file with queries (one per line)",
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

    tools = load_tools(args.tools)
    queries = load_queries(args.queries)
    checks = build_query_checks(queries, args.brand)
    output = build_output(args.brand, queries, checks)

    # If paid tools available, add enhanced check methods
    if tools.get("dataforseo_api"):
        output["enhanced_methods"] = {
            "dataforseo": {
                "endpoint": "https://api.dataforseo.com/v3/serp/ai_overview/live",
                "instructions": [
                    "Use DataForSEO AI Overview endpoint for automated checking.",
                    "This provides structured citation data without manual testing.",
                ],
            }
        }

    output_json = json.dumps(output, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
