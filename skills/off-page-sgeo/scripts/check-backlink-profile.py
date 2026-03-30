#!/usr/bin/env python3
"""
Check Backlink Profile

Estimates a domain's backlink profile using available tools.
Free path: WebSearch to find pages mentioning/linking to the domain.
Paid path: DataForSEO backlink API or Ahrefs API for full profile data.

Usage:
    python check-backlink-profile.py --domain example.com
    python check-backlink-profile.py --domain example.com --tools tools.json
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


def check_via_websearch(domain):
    """
    Estimate backlink profile via WebSearch queries.

    This function generates the search queries and instructions for the agent
    to execute via WebSearch, then process the results.
    """
    queries = [
        {
            "query": f'"{domain}" -site:{domain}',
            "purpose": "Find pages that mention or link to the domain",
        },
        {
            "query": f'link:{domain} -site:{domain}',
            "purpose": "Find pages linking to the domain (supported by some engines)",
        },
        {
            "query": f'"{domain}" inurl:resources OR inurl:links',
            "purpose": "Find resource pages linking to the domain",
        },
    ]

    return {
        "method": "websearch",
        "status": "queries_prepared",
        "queries": queries,
        "instructions": [
            f"Execute each query via WebSearch and collect results.",
            "For each result, extract: URL, domain, title, snippet.",
            "Deduplicate by referring domain.",
            "Identify high-authority sources (known major publications, .edu, .gov domains).",
            "Count total unique referring domains found.",
            "Note: WebSearch estimates are a lower bound — actual backlink counts are typically 5-10x higher.",
        ],
    }


def check_via_dataforseo(domain, api_credentials):
    """
    Check backlink profile via DataForSEO API.

    Returns the API call configuration for the agent to execute.
    """
    return {
        "method": "dataforseo",
        "status": "api_call_prepared",
        "endpoint": "https://api.dataforseo.com/v3/backlinks/summary/live",
        "request_body": {
            "target": domain,
            "internal_list_limit": 0,
            "backlinks_status_type": "live",
        },
        "expected_response_fields": [
            "total_backlinks",
            "referring_domains",
            "referring_domains_nofollow",
            "broken_backlinks",
            "referring_ips",
            "referring_subnets",
        ],
        "instructions": [
            "Execute the API call with provided credentials.",
            "Parse response for backlink summary metrics.",
            "Follow up with anchor text distribution endpoint if needed.",
        ],
    }


def check_via_ahrefs(domain, api_credentials):
    """
    Check backlink profile via Ahrefs API.

    Returns the API call configuration for the agent to execute.
    """
    return {
        "method": "ahrefs",
        "status": "api_call_prepared",
        "endpoint": f"https://api.ahrefs.com/v3/site-explorer/backlinks?target={domain}&mode=domain",
        "instructions": [
            "Execute the API call with Ahrefs API token.",
            "Parse response for: backlinks count, referring domains, domain rating.",
            "Request anchor text report separately if detailed analysis needed.",
        ],
    }


def build_output(domain, method_result):
    """Build the standardized output JSON."""
    return {
        "domain": domain,
        "method": method_result.get("method", "unknown"),
        "status": method_result.get("status", "unknown"),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "data": method_result,
        "output_template": {
            "referring_domains_estimate": "TO_BE_FILLED",
            "top_sources": [
                {
                    "domain": "example.com",
                    "context": "mentioned in article about...",
                }
            ],
            "anchor_text_sample": [],
            "issues": [],
            "recommendation": "TO_BE_FILLED",
        },
        "next_steps": [
            "Execute the prepared queries/API calls",
            "Fill in the output template with actual results",
            "Compare referring domain count against competitors",
            "Identify gaps in anchor text distribution",
            "Flag any toxic links for disavow consideration",
        ],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Check backlink profile for a domain. "
        "Free path uses WebSearch to estimate referring domains. "
        "Paid path uses DataForSEO or Ahrefs for comprehensive data.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python check-backlink-profile.py --domain example.com
    python check-backlink-profile.py --domain example.com --tools tools.json

Output: JSON with backlink profile data or prepared queries for agent execution.
        """,
    )
    parser.add_argument(
        "--domain",
        required=True,
        help="Domain to check backlink profile for (e.g., example.com)",
    )
    parser.add_argument(
        "--tools",
        default=None,
        help="Path to tools.json inventory file (from inventory-tools.py)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: stdout)",
    )

    args = parser.parse_args()

    # Strip protocol if provided
    domain = args.domain.replace("https://", "").replace("http://", "").strip("/")

    tools = load_tools(args.tools)

    # Determine best available method
    if tools.get("ahrefs_api"):
        result = check_via_ahrefs(domain, tools["ahrefs_api"])
    elif tools.get("dataforseo_api"):
        result = check_via_dataforseo(domain, tools["dataforseo_api"])
    else:
        result = check_via_websearch(domain)

    output = build_output(domain, result)

    output_json = json.dumps(output, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
