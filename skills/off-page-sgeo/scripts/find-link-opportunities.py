#!/usr/bin/env python3
"""
Find Link Opportunities

Discovers link-building opportunities for a topic/niche using WebSearch:
resource pages, guest post targets, broken link candidates, journalist queries,
and roundup/list posts.

Usage:
    python find-link-opportunities.py --topic "AI analytics"
    python find-link-opportunities.py --topic "AI analytics" --domain example.com
    python find-link-opportunities.py --topic "AI analytics" --tools tools.json
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


def build_opportunity_queries(topic, domain):
    """Build search queries for each type of link opportunity."""
    queries = {
        "resource_pages": [
            {
                "query": f'intitle:"resources" {topic}',
                "purpose": "Find resource/link pages for the topic",
            },
            {
                "query": f'intitle:"useful links" {topic}',
                "purpose": "Find curated link collections",
            },
            {
                "query": f'intitle:"recommended" {topic} tools OR resources',
                "purpose": "Find recommendation pages",
            },
        ],
        "guest_post_targets": [
            {
                "query": f'{topic} "write for us"',
                "purpose": "Find sites accepting guest contributions",
            },
            {
                "query": f'{topic} "guest post" OR "guest article"',
                "purpose": "Find sites with guest post programs",
            },
            {
                "query": f'{topic} "contribute" OR "submission guidelines"',
                "purpose": "Find contributor programs",
            },
        ],
        "roundups_and_lists": [
            {
                "query": f'{topic} "best tools" OR "top tools"',
                "purpose": "Find tool roundup posts for potential inclusion",
            },
            {
                "query": f'{topic} "top resources" OR "best resources"',
                "purpose": "Find resource roundups",
            },
            {
                "query": f'{topic} roundup OR "weekly roundup" OR "monthly roundup"',
                "purpose": "Find recurring roundup posts",
            },
        ],
        "journalist_queries": [
            {
                "query": f'site:qwoted.com {topic} OR site:featured.com {topic} OR site:terkel.io {topic}',
                "purpose": "Find current journalist queries on Qwoted, Featured.com, or Terkel (HARO and Connectively were discontinued in 2023-2024)",
            },
            {
                "query": f'{topic} "looking for sources" OR "seeking experts"',
                "purpose": "Find journalist source requests",
            },
        ],
        "broken_link_candidates": [
            {
                "query": f'{topic} resources inurl:links',
                "purpose": "Find link pages that may have broken links (verify manually)",
                "note": "Broken link detection requires checking each link — approximate without Ahrefs.",
            },
        ],
    }

    # If domain provided, add competitor-gap queries
    if domain:
        queries["competitor_links"] = [
            {
                "query": f'{topic} -site:{domain} inurl:blog',
                "purpose": "Find topic blogs that link to competitors but not you",
            },
        ]

    return queries


def build_output(topic, domain, queries):
    """Build the standardized output JSON."""
    total_queries = sum(len(v) for v in queries.values())

    return {
        "topic": topic,
        "domain": domain,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "queries_prepared",
        "total_search_queries": total_queries,
        "opportunity_queries": queries,
        "analysis_instructions": [
            "Execute each query via WebSearch.",
            "For each result, extract: URL, title, domain, snippet.",
            "Classify each result by opportunity type (resource page, guest post target, roundup, etc.).",
            "Estimate authority level based on domain recognition: high (major publications, .edu), medium (established blogs), low (small/unknown sites).",
            "Prioritize by: relevance to topic > site authority > opportunity type.",
            "For resource pages: note the specific section where your content could fit.",
            "For guest post targets: note any submission guidelines found.",
            "For roundups: note the publication cadence (weekly, monthly, annual).",
            "For broken link candidates: flag for manual verification — WebSearch cannot detect broken links directly.",
        ],
        "output_template": {
            "topic": topic,
            "total_found": "TO_BE_FILLED",
            "opportunities": [
                {
                    "type": "resource_page|guest_post|roundup|journalist_query|broken_link",
                    "url": "TO_BE_FILLED",
                    "title": "TO_BE_FILLED",
                    "domain": "TO_BE_FILLED",
                    "estimated_authority": "high|medium|low",
                    "action": "Specific action to take for this opportunity",
                    "notes": "Any additional context",
                }
            ],
            "by_type": {
                "resource_pages": "TO_BE_FILLED",
                "guest_post_targets": "TO_BE_FILLED",
                "roundups": "TO_BE_FILLED",
                "journalist_queries": "TO_BE_FILLED",
                "broken_link_candidates": "TO_BE_FILLED",
            },
        },
        "outreach_priority": [
            "1. Journalist queries (time-sensitive — respond within 2 hours)",
            "2. Resource pages on high-authority sites (highest conversion rate: 8-12%)",
            "3. Broken link replacements (you're solving a problem — 10-15% conversion)",
            "4. Roundup inclusion (if your product/content qualifies)",
            "5. Guest post pitches (longer process but builds ongoing relationships)",
        ],
        "next_steps": [
            "Execute all search queries and collect results",
            "Deduplicate and prioritize opportunities",
            "Build an outreach list with contact information",
            "See references/backlink-strategy.md for outreach email templates",
            "Track outreach status in a CRM or spreadsheet",
            "Send 5-10 personalized pitches per day — not more",
        ],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Find link-building opportunities for a topic/niche. "
        "Discovers resource pages, guest post targets, roundups, "
        "journalist queries, and broken link candidates via WebSearch.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python find-link-opportunities.py --topic "AI analytics"
    python find-link-opportunities.py --topic "developer tools" --domain example.com
    python find-link-opportunities.py --topic "SaaS marketing" --tools tools.json

Output: JSON with categorized link opportunity queries and analysis framework.
        """,
    )
    parser.add_argument(
        "--topic",
        required=True,
        help="Topic or niche to find link opportunities for",
    )
    parser.add_argument(
        "--domain",
        default=None,
        help="Your domain (used to exclude from results and find competitor gaps)",
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

    tools = load_tools(args.tools)
    queries = build_opportunity_queries(args.topic, domain)
    output = build_output(args.topic, domain, queries)

    # Add paid tool enhancements if available
    if tools.get("ahrefs_api"):
        output["enhanced_methods"] = {
            "ahrefs": {
                "broken_backlinks": "Use Ahrefs Broken Backlinks report for accurate broken link discovery.",
                "content_gap": "Use Content Gap tool to find sites linking to competitors but not you.",
                "dr_da_scores": "Get Domain Rating for all discovered opportunities.",
            }
        }
    if tools.get("dataforseo_api"):
        output.setdefault("enhanced_methods", {})["dataforseo"] = {
            "bulk_authority": "Use DataForSEO for bulk DR/DA scoring of discovered opportunities."
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
