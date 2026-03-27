#!/usr/bin/env python3
"""
Audit Platform Presence

Checks brand presence on the 7 AI-cited platforms:
Reddit, YouTube, LinkedIn, Wikipedia, GitHub, Stack Overflow, and industry forums.
Outputs a platform audit with presence status, activity level, and AI citation potential.

Usage:
    python audit-platform-presence.py --brand "Acme Corp"
    python audit-platform-presence.py --brand "Acme Corp" --forums "shopify.community,producthunt.com"
    python audit-platform-presence.py --brand "Acme Corp" --tools tools.json
"""

import argparse
import json
import sys
import os
from datetime import datetime


# Default platform definitions with search patterns and AI citation metadata
PLATFORMS = [
    {
        "name": "Reddit",
        "search_query_template": 'site:reddit.com "{brand}"',
        "presence_query_template": 'site:reddit.com/user "{brand}"',
        "ai_citation_frequency": "very_high",
        "description": "AI engines heavily cite Reddit for authentic opinions and recommendations.",
        "optimization_priority": "high",
    },
    {
        "name": "YouTube",
        "search_query_template": 'site:youtube.com "{brand}"',
        "presence_query_template": 'site:youtube.com/c "{brand}" OR site:youtube.com/@"{brand}"',
        "ai_citation_frequency": "high",
        "description": "Video transcripts and descriptions are indexed by AI engines.",
        "optimization_priority": "high",
    },
    {
        "name": "LinkedIn",
        "search_query_template": 'site:linkedin.com "{brand}"',
        "presence_query_template": 'site:linkedin.com/company "{brand}"',
        "ai_citation_frequency": "high",
        "description": "Professional content cited for business and industry topics.",
        "optimization_priority": "high",
    },
    {
        "name": "Wikipedia",
        "search_query_template": 'site:wikipedia.org "{brand}"',
        "presence_query_template": 'site:en.wikipedia.org "{brand}"',
        "ai_citation_frequency": "very_high",
        "description": "Extremely high authority. AI models trained extensively on Wikipedia.",
        "optimization_priority": "medium",
        "note": "Do NOT edit your own article. Build notability through media coverage first.",
    },
    {
        "name": "GitHub",
        "search_query_template": 'site:github.com "{brand}"',
        "presence_query_template": 'site:github.com/{brand_slug}',
        "ai_citation_frequency": "high",
        "description": "Critical for developer-focused products. READMEs directly cited.",
        "optimization_priority": "high_if_technical",
    },
    {
        "name": "Stack Overflow",
        "search_query_template": 'site:stackoverflow.com "{brand}"',
        "presence_query_template": 'site:stackoverflow.com "{brand}"',
        "ai_citation_frequency": "medium",
        "description": "Expert answers cited for technical questions.",
        "optimization_priority": "medium_if_technical",
    },
]


def load_tools(tools_path):
    """Load tool inventory from JSON file."""
    if tools_path and os.path.exists(tools_path):
        with open(tools_path, "r") as f:
            return json.load(f)
    return {}


def build_platform_queries(brand, forums):
    """Build search queries for each platform."""
    brand_slug = brand.lower().replace(" ", "").replace(".", "")
    platform_queries = []

    for platform in PLATFORMS:
        queries = {
            "platform": platform["name"],
            "mention_query": platform["search_query_template"].format(
                brand=brand, brand_slug=brand_slug
            ),
            "presence_query": platform["presence_query_template"].format(
                brand=brand, brand_slug=brand_slug
            ),
            "ai_citation_frequency": platform["ai_citation_frequency"],
            "description": platform["description"],
            "optimization_priority": platform["optimization_priority"],
        }
        if "note" in platform:
            queries["note"] = platform["note"]
        platform_queries.append(queries)

    # Add custom industry forums
    if forums:
        for forum in forums:
            forum = forum.strip()
            if forum:
                platform_queries.append(
                    {
                        "platform": f"Forum: {forum}",
                        "mention_query": f'site:{forum} "{brand}"',
                        "presence_query": f'site:{forum} "{brand}"',
                        "ai_citation_frequency": "varies",
                        "description": f"Industry forum: {forum}",
                        "optimization_priority": "assess",
                    }
                )

    return platform_queries


def build_output(brand, platform_queries):
    """Build the standardized output JSON."""
    return {
        "brand": brand,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "queries_prepared",
        "platforms_to_check": platform_queries,
        "analysis_instructions": [
            "Execute each mention_query via WebSearch. Record result count per platform.",
            "Execute each presence_query to determine if an official account/page exists.",
            "For platforms with results, assess activity level: active (recent content), dormant (exists but inactive), none (no presence).",
            "Rate content quality 1-5 based on: depth of content, engagement, recency.",
            "Assess AI citation potential: high (platform frequently cited for this brand's topic), medium (occasionally), low (rarely).",
            "Identify missing platforms as priority gaps.",
            "Generate prioritized recommendations for platform presence building.",
        ],
        "output_template": {
            "platforms": [
                {
                    "name": "Platform Name",
                    "presence": "true|false",
                    "estimated_activity": "active|dormant|none",
                    "mention_count": "TO_BE_FILLED",
                    "content_quality": "1-5 or N/A",
                    "ai_citation_potential": "high|medium|low",
                    "priority": "maintain|build|create|skip",
                }
            ],
            "missing_platforms": ["list of platforms with no presence"],
            "recommendation": "TO_BE_FILLED — prioritized action list",
        },
        "priority_framework": {
            "create_first": "Platforms with high AI citation frequency where brand has no presence",
            "build_next": "Platforms with existing presence but low activity or content quality",
            "maintain": "Platforms with active, quality presence — keep contributing",
            "skip_if_irrelevant": "Platforms not relevant to your niche (e.g., GitHub for non-technical brands)",
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Audit brand presence on 7 AI-cited platforms. "
        "Checks Reddit, YouTube, LinkedIn, Wikipedia, GitHub, Stack Overflow, "
        "and configurable industry forums.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python audit-platform-presence.py --brand "Acme Corp"
    python audit-platform-presence.py --brand "Acme Corp" --forums "shopify.community,producthunt.com"

Output: JSON with platform audit queries and analysis instructions.
        """,
    )
    parser.add_argument(
        "--brand",
        required=True,
        help="Brand name to audit platform presence for",
    )
    parser.add_argument(
        "--forums",
        default=None,
        help="Comma-separated list of industry forum domains to also check",
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

    forums = args.forums.split(",") if args.forums else []
    platform_queries = build_platform_queries(args.brand, forums)
    output = build_output(args.brand, platform_queries)

    output_json = json.dumps(output, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
