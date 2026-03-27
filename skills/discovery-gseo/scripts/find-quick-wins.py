#!/usr/bin/env python3
"""
find-quick-wins.py — Identify striking-distance keywords, low-CTR pages, variant keywords, and GEO gaps.

For existing sites with traffic data. Analyzes GSC data (or approximates via WebSearch)
to find keywords that are close to page 1, pages with poor CTR, unexpected keyword
rankings, and keywords where you rank in search but aren't cited by AI.

Usage:
    python3 find-quick-wins.py --domain yourdomain.com
    python3 find-quick-wins.py --domain yourdomain.com --gsc-data gsc-export.csv
    python3 find-quick-wins.py --domain yourdomain.com --geo-data geo-results.json

AI Agent Usage:
    If GSC API available:
    1. Pull queries for last 3 months via GSC API
    2. Striking distance: filter positions 8-20, sort by impressions descending
    3. Low CTR: filter CTR < 3%, sort by impressions descending
    4. Variant keywords: find queries ranking for pages not targeting them
    5. For each quick win: identify the ranking page, recommend action

    Fallback (no GSC):
    1. WebSearch("site:{domain}") for various seed keywords
    2. Identify which pages exist and roughly where they rank
    3. Note limitations: no impression/CTR data without GSC

    GEO quick wins (if --geo-data provided):
    1. Match top-ranking keywords to probe-ai-discovery.py output
    2. Keywords where you rank but aren't AI-cited = GEO gap
    3. Recommend: apply on-page-sgeo and content-sgeo for AI citation optimization
"""

import argparse
import json
import sys
import csv


def find_wins_from_gsc(gsc_data):
    """
    Analyze GSC data for quick wins.

    Expected format: list of dicts with keys:
    query, page, clicks, impressions, ctr, position
    """
    striking_distance = []
    low_ctr = []
    variant_keywords = []

    for row in gsc_data:
        position = float(row.get("position", 0))
        impressions = int(row.get("impressions", 0))
        ctr = float(row.get("ctr", 0))
        query = row.get("query", "")
        page = row.get("page", "")

        # Striking distance: positions 8-20
        if 8 <= position <= 20 and impressions > 100:
            striking_distance.append({
                "keyword": query,
                "position": round(position, 1),
                "impressions": impressions,
                "page": page,
                "action": "Improve content depth, add internal links, optimize title tag for this keyword",
            })

        # Low CTR: CTR < 3% with significant impressions
        if ctr < 0.03 and impressions > 500:
            low_ctr.append({
                "keyword": query,
                "position": round(position, 1),
                "impressions": impressions,
                "ctr": round(ctr, 4),
                "page": page,
                "action": "Rewrite title and meta description for higher CTR. Check if SERP features push result down.",
            })

    # Sort by impressions descending
    striking_distance.sort(key=lambda x: x["impressions"], reverse=True)
    low_ctr.sort(key=lambda x: x["impressions"], reverse=True)

    return striking_distance[:20], low_ctr[:20], variant_keywords


def find_wins_websearch(domain):
    """
    Fallback: approximate quick win analysis using WebSearch.

    Agent: WebSearch("site:{domain}") to catalog pages.
    WebSearch("site:{domain} {seed}") for specific topics.
    Cannot determine: impressions, CTR, exact positions.
    """
    # Agent fills with real WebSearch data
    return [], [], []


def find_geo_gaps(quick_wins, geo_data):
    """
    Cross-reference top-ranking keywords with GEO data to find citation gaps.
    Keywords where you rank well but AI doesn't cite you = GEO quick win.
    """
    geo_gaps = []

    if not geo_data or "results" not in geo_data:
        return geo_gaps

    # Build lookup from geo data
    geo_lookup = {}
    for r in geo_data.get("results", []):
        query = r.get("query", "").lower().strip()
        geo_lookup[query] = r

    # Check striking distance and high-impression keywords
    all_keywords = quick_wins.get("striking_distance", []) + quick_wins.get("low_ctr", [])

    for kw_entry in all_keywords:
        keyword = kw_entry.get("keyword", "").lower().strip()
        geo_result = geo_lookup.get(keyword)

        if geo_result:
            if not geo_result.get("user_brand_cited", False) and geo_result.get("ai_answers"):
                geo_gaps.append({
                    "keyword": kw_entry["keyword"],
                    "position": kw_entry.get("position"),
                    "ai_cited": False,
                    "action": "Apply on-page-sgeo optimization for AI citation: direct-answer formatting, data density, structured data",
                })

    return geo_gaps


def load_gsc_csv(filepath):
    """Load GSC export CSV."""
    data = []
    try:
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        return None
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Identify quick wins: striking distance, low CTR, variants, GEO gaps."
    )
    parser.add_argument(
        "--domain",
        type=str,
        required=True,
        help="Domain to analyze (e.g., yourdomain.com)",
    )
    parser.add_argument(
        "--gsc-data",
        type=str,
        help="Path to GSC export CSV (queries + pages with impressions, clicks, CTR, position)",
    )
    parser.add_argument(
        "--geo-data",
        type=str,
        help="Path to JSON output from probe-ai-discovery.py for GEO gap detection",
    )
    parser.add_argument("--tools", type=str, help="Path to tools.json inventory file")

    args = parser.parse_args()

    geo_data = None
    if args.geo_data:
        try:
            with open(args.geo_data, "r") as f:
                geo_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load GEO data: {e}", file=sys.stderr)

    if args.gsc_data:
        gsc_data = load_gsc_csv(args.gsc_data)
        if gsc_data is None:
            print(json.dumps({"error": f"GSC data file not found: {args.gsc_data}"}))
            sys.exit(1)
        striking, low_ctr, variants = find_wins_from_gsc(gsc_data)
        method = "gsc_export"
    else:
        # Agent should use GSC API directly or fall back to WebSearch
        striking, low_ctr, variants = find_wins_websearch(args.domain)
        method = "websearch"

    quick_wins = {
        "striking_distance": striking,
        "low_ctr": low_ctr,
        "variant_keywords": variants,
    }

    # GEO quick wins
    geo_gaps = find_geo_gaps(quick_wins, geo_data)

    total = len(striking) + len(low_ctr) + len(variants) + len(geo_gaps)

    result = {
        "domain": args.domain,
        "method": method,
        "quick_wins": {
            "striking_distance": striking,
            "low_ctr": low_ctr,
            "variant_keywords": variants,
            "geo_gaps": geo_gaps,
        },
        "total_quick_wins": total,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
