#!/usr/bin/env python3
"""
Analyze Competitor Authority

Compares authority signals across your domain and 3-5 competitor domains.
Estimates backlink profiles, brand mentions, content volume, and platform presence.
Outputs a competitive authority matrix identifying gaps and strengths.

Usage:
    python analyze-competitor-authority.py --domain example.com --competitors "comp1.com,comp2.com,comp3.com"
    python analyze-competitor-authority.py --domain example.com --competitors "comp1.com,comp2.com" --tools tools.json
"""

import argparse
import json
import sys
import os
from datetime import datetime


def load_tools(tools_path):
    """Load tool inventory from JSON file."""
    if tools_path and os.path.exists(tools_path):
        with open(tools_path, "r") as f:
            return json.load(f)
    return {}


def build_domain_queries(domain):
    """Build the set of authority estimation queries for a single domain."""
    brand_name = domain.split(".")[0].capitalize()

    return {
        "domain": domain,
        "queries": {
            "backlink_estimate": {
                "query": f'"{domain}" -site:{domain}',
                "purpose": "Estimate referring domains by counting pages mentioning/linking to domain",
                "metric": "Result count as proxy for backlink volume",
            },
            "brand_mentions": {
                "query": f'"{brand_name}"',
                "purpose": "Estimate total brand mention volume",
                "metric": "Result count indicates brand awareness",
            },
            "content_volume": {
                "query": f"site:{domain}",
                "purpose": "Estimate total indexed pages",
                "metric": "Result count shows content investment",
            },
            "reddit_presence": {
                "query": f'site:reddit.com "{brand_name}" OR "{domain}"',
                "purpose": "Check Reddit mention volume",
                "metric": "Result count indicates community presence",
            },
            "youtube_presence": {
                "query": f'site:youtube.com "{brand_name}"',
                "purpose": "Check YouTube presence",
                "metric": "Result count indicates video content investment",
            },
            "linkedin_presence": {
                "query": f'site:linkedin.com "{brand_name}"',
                "purpose": "Check LinkedIn presence",
                "metric": "Result count indicates professional content activity",
            },
        },
    }


def build_output(user_domain, competitors):
    """Build the standardized output JSON."""
    all_domains = [user_domain] + competitors

    domain_queries = []
    for domain in all_domains:
        domain_queries.append(build_domain_queries(domain))

    return {
        "user_domain": user_domain,
        "competitors": competitors,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "queries_prepared",
        "domain_queries": domain_queries,
        "analysis_instructions": [
            "Execute all queries for all domains via WebSearch.",
            "Record result counts for each query per domain.",
            "Calculate platform_score (0-7) for each domain: +1 for each platform with meaningful presence.",
            "Build the competitive matrix comparing all domains.",
            "Identify gaps: areas where competitors significantly outperform the user domain.",
            "Identify strengths: areas where the user domain outperforms competitors.",
            "Generate prioritized recommendations based on the largest gaps.",
        ],
        "output_template": {
            "user_domain": user_domain,
            "user_metrics": {
                "backlink_estimate": "TO_BE_FILLED",
                "mention_estimate": "TO_BE_FILLED",
                "content_volume": "TO_BE_FILLED",
                "platform_score": "TO_BE_FILLED (0-7)",
            },
            "competitors": [
                {
                    "domain": "competitor.com",
                    "backlink_estimate": "TO_BE_FILLED",
                    "mention_estimate": "TO_BE_FILLED",
                    "content_volume": "TO_BE_FILLED",
                    "platform_score": "TO_BE_FILLED (0-7)",
                }
            ],
            "gaps": [
                "Description of areas where competitors outperform user"
            ],
            "strengths": [
                "Description of areas where user outperforms competitors"
            ],
            "recommendations": [
                "Prioritized list of actions to close authority gaps"
            ],
        },
        "scoring_guide": {
            "backlink_estimate": "WebSearch result count for domain mentions. Relative comparison matters more than absolute numbers.",
            "mention_estimate": "Brand name search results. Higher = more brand awareness.",
            "content_volume": "Indexed pages via site: operator. More pages = more content investment.",
            "platform_score": "Count of platforms with meaningful presence (>5 results). Max 7 (Reddit, YouTube, LinkedIn, Wikipedia, GitHub, Stack Overflow, forums).",
        },
        "next_steps": [
            "Execute all queries and build the competitive matrix",
            "Focus on closing the largest gap first",
            "Use specific scripts for deeper analysis:",
            "  - check-backlink-profile.py for detailed backlink analysis",
            "  - audit-platform-presence.py for detailed platform audits",
            "  - probe-ai-visibility.py for AI citation comparison",
            "Repeat quarterly to track competitive position changes",
        ],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze competitor authority by comparing backlink profiles, "
        "brand mentions, content volume, and platform presence across "
        "your domain and 3-5 competitor domains.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python analyze-competitor-authority.py --domain example.com --competitors "comp1.com,comp2.com"
    python analyze-competitor-authority.py --domain example.com --competitors "a.com,b.com,c.com" --tools tools.json

Output: JSON with competitive authority queries and analysis framework.
        """,
    )
    parser.add_argument(
        "--domain",
        required=True,
        help="Your domain to analyze",
    )
    parser.add_argument(
        "--competitors",
        required=True,
        help="Comma-separated list of competitor domains (3-5 recommended)",
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

    user_domain = args.domain.replace("https://", "").replace("http://", "").strip("/")
    competitors = [
        c.strip().replace("https://", "").replace("http://", "").strip("/")
        for c in args.competitors.split(",")
        if c.strip()
    ]

    if not competitors:
        print("Error: At least one competitor domain is required.", file=sys.stderr)
        sys.exit(1)

    if len(competitors) > 10:
        print(
            "Warning: More than 10 competitors specified. Results may be slow.",
            file=sys.stderr,
        )

    output = build_output(user_domain, competitors)

    # Add paid tool methods if available
    tools = load_tools(args.tools)
    if tools.get("dataforseo_api"):
        output["enhanced_methods"] = {
            "dataforseo": {
                "domain_analytics": "Use DataForSEO Domain Analytics API for precise metrics.",
                "backlinks": "Use Backlinks API for exact referring domain counts.",
            }
        }
    if tools.get("ahrefs_api"):
        output.setdefault("enhanced_methods", {})["ahrefs"] = {
            "domain_comparison": "Use Ahrefs Domain Comparison for side-by-side metrics."
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
