#!/usr/bin/env python3
"""
Track AI Referrers

Generates GA4 custom channel group configuration for AI referrer tracking
and provides step-by-step setup instructions. This is an instructional/config
generation script, not a data-fetching script.

If GSC API credentials are available, queries for referrer data showing AI traffic.

Usage:
    python track-ai-referrers.py
    python track-ai-referrers.py --tools tools.json
    python track-ai-referrers.py --output ai-referrer-config.json
"""

import argparse
import json
import sys
import os
from datetime import datetime


# Known AI referrer domains as of 2026
AI_REFERRERS = [
    {
        "domain": "chat.openai.com",
        "platform": "ChatGPT",
        "notes": "Largest AI assistant by user base. 800M+ weekly users.",
    },
    {
        "domain": "perplexity.ai",
        "platform": "Perplexity",
        "notes": "AI search engine. 780M+ queries/month. Most transparent citations.",
    },
    {
        "domain": "gemini.google.com",
        "platform": "Gemini",
        "notes": "Google's AI assistant. Integrated with Google search index.",
    },
    {
        "domain": "claude.ai",
        "platform": "Claude",
        "notes": "Anthropic's AI assistant. Strong for technical and business queries.",
    },
    {
        "domain": "copilot.microsoft.com",
        "platform": "Microsoft Copilot",
        "notes": "Microsoft's AI assistant. Integrated with Bing.",
    },
    {
        "domain": "you.com",
        "platform": "You.com",
        "notes": "AI search engine with citation-forward design.",
    },
    {
        "domain": "poe.com",
        "platform": "Poe",
        "notes": "Quora's multi-model AI platform.",
    },
]


def load_tools(tools_path):
    """Load tool inventory from JSON file."""
    if tools_path and os.path.exists(tools_path):
        with open(tools_path, "r") as f:
            return json.load(f)
    return {}


def build_ga4_config():
    """Build the GA4 custom channel group configuration."""
    conditions = []
    for referrer in AI_REFERRERS:
        conditions.append(
            {
                "type": "referrer_contains",
                "value": referrer["domain"],
                "platform": referrer["platform"],
            }
        )

    return {
        "channel_group_name": "AI Assistants",
        "conditions": conditions,
        "setup_steps": [
            "1. Open Google Analytics 4 for your property.",
            "2. Click the gear icon (Admin) in the bottom-left.",
            "3. Go to Data Display > Custom Channel Groups (under your property settings).",
            "4. Click 'Create custom channel group'.",
            "5. Name it 'AI Assistants'.",
            "6. Add a new channel named 'AI Assistants'.",
            "7. Set the condition: Source matches regex:",
            f"   {build_referrer_regex()}",
            "8. Save the channel group.",
            "9. View AI traffic in: Reports > Acquisition > Traffic Acquisition.",
            "10. Select your custom channel group from the channel grouping dropdown.",
        ],
        "alternative_setup_utm": {
            "description": "If you want to track AI referrers without custom channel groups, you can monitor them in the default Source/Medium report.",
            "steps": [
                "Go to Reports > Acquisition > Traffic Acquisition.",
                "Change the primary dimension to 'Session source'.",
                "Search for 'chat.openai.com', 'perplexity.ai', etc.",
                "This works immediately but requires manual filtering each time.",
            ],
        },
    }


def build_referrer_regex():
    """Build a regex pattern matching all known AI referrers."""
    domains = [r["domain"].replace(".", "\\.") for r in AI_REFERRERS]
    return "(" + "|".join(domains) + ")"


def build_bot_filtering_warning():
    """Build instructions to prevent GA4 from filtering AI referrer traffic."""
    return {
        "warning": "GA4 may classify AI referrer traffic as bot traffic and filter it out.",
        "check_steps": [
            "1. Go to Admin > Data Streams > select your web stream.",
            "2. Click 'Configure tag settings' > 'Show all'.",
            "3. Check 'Define internal traffic' — ensure AI referrer domains are NOT listed here.",
            "4. Go to Admin > Data Settings > Data Filters.",
            "5. Check that no active filter excludes traffic from AI referrer domains.",
            "6. If 'Exclude all hits from known bots and spiders' is enabled in your analytics setup, AI referrers might be partially filtered. Monitor actual vs expected volumes.",
        ],
    }


def build_output(tools):
    """Build the standardized output JSON."""
    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ga4_config": build_ga4_config(),
        "bot_filtering_warning": build_bot_filtering_warning(),
        "known_ai_referrers": AI_REFERRERS,
        "referrer_regex": build_referrer_regex(),
        "context": {
            "growth_rate": "AI-referred sessions grew 527% YoY in early 2025.",
            "recommendation": "Track now even if volumes are small. This traffic source is compounding.",
            "typical_characteristics": {
                "bounce_rate": "Lower than organic — AI sends qualified visitors.",
                "pages_per_session": "Often higher — visitors arrive with specific intent.",
                "conversion_rate": "Frequently higher than organic search — AI pre-qualifies the recommendation.",
            },
        },
        "monitoring_checklist": [
            "Set up GA4 custom channel group (one-time)",
            "Check AI referrer traffic weekly in Acquisition report",
            "Track week-over-week and month-over-month growth trends",
            "Identify top landing pages from AI referrers — these are your cited pages",
            "Compare AI referrer conversion rate against other channels",
            "Update referrer list quarterly as new AI platforms emerge",
        ],
    }

    # Add GSC data query if API credentials available
    if tools.get("gsc_api"):
        output["gsc_query"] = {
            "description": "Query GSC API for search analytics data filtered by AI referrers.",
            "instructions": [
                "Use the Search Analytics API to query for traffic from AI-related sources.",
                "Note: GSC primarily tracks Google Search traffic, not direct AI referrers.",
                "For AI referrer data, GA4 is the primary source.",
                "GSC can show if Google AI Overviews are driving impressions for your pages.",
            ],
        }

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Generate GA4 custom channel group configuration for tracking "
        "AI referrer traffic. Outputs setup instructions and referrer domains. "
        "AI-referred sessions grew 527%% YoY in 2025 — set this up now.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python track-ai-referrers.py
    python track-ai-referrers.py --output ai-referrer-config.json
    python track-ai-referrers.py --tools tools.json

Output: JSON with GA4 configuration, setup steps, and known AI referrer list.
        """,
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
    output = build_output(tools)

    output_json = json.dumps(output, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output_json)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
