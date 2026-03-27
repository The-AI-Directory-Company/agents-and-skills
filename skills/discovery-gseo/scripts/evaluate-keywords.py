#!/usr/bin/env python3
"""
evaluate-keywords.py — Enrich raw keyword list with volume/KD estimates and GEO scores.

Takes a raw keyword list, estimates volume and keyword difficulty for each,
merges GEO score data if available, and applies configurable filters to remove
noise (high KD, low relevance, duplicates).

Usage:
    python3 evaluate-keywords.py --keywords raw-keywords.txt
    python3 evaluate-keywords.py --keywords raw-keywords.txt --max-kd 50 --min-volume 10
    python3 evaluate-keywords.py --keywords raw-keywords.txt --geo-data geo-results.json
    python3 evaluate-keywords.py --keywords raw-keywords.txt --api dataforseo

AI Agent Usage:
    For each keyword in the list:
    1. Estimate volume:
       - If DataForSEO available: call keyword data API for exact volume
       - If Ahrefs/Semrush available: call keyword metrics API
       - Fallback: WebSearch the keyword, use total result count as rough proxy
         (>1B results ≈ high volume, <10M results ≈ low volume)
    2. Estimate KD:
       - If paid tool available: use its KD score directly
       - Fallback: WebSearch the keyword, analyze top 10 results:
         count high-DA domains (Forbes, HubSpot, Wikipedia, etc.)
         0-2 strong domains → easy, 3-5 → medium, 6+ → hard
    3. Merge GEO score:
       - If --geo-data file provided: match keywords to probe-ai-discovery.py output
       - Otherwise: mark as "unscored" (agent should run probe-ai-discovery.py first)
    4. Apply filters:
       - Remove KD > --max-kd threshold
       - Remove volume < --min-volume threshold
       - Flag near-duplicates (fuzzy match on keyword text)
"""

import argparse
import json
import sys
import re
from collections import defaultdict


# High-authority domains — used for free KD estimation
HIGH_AUTHORITY_DOMAINS = [
    "forbes.com", "hubspot.com", "wikipedia.org", "nytimes.com",
    "techcrunch.com", "wired.com", "theverge.com", "cnet.com",
    "pcmag.com", "g2.com", "capterra.com", "gartner.com",
    "shopify.com", "salesforce.com", "microsoft.com", "google.com",
    "amazon.com", "apple.com", "ibm.com", "oracle.com",
]


def normalize_keyword(kw):
    """Normalize a keyword for deduplication."""
    return re.sub(r"\s+", " ", kw.lower().strip())


def find_near_duplicates(keywords):
    """Identify near-duplicate keywords (e.g., 'invoice software' vs 'invoicing software')."""
    normalized = {}
    duplicates = set()

    for kw in keywords:
        norm = normalize_keyword(kw)
        # Simple stemming: remove trailing 'ing', 's', 'ed'
        stem = re.sub(r"(ing|ed|s)\b", "", norm)
        stem = re.sub(r"\s+", " ", stem).strip()

        if stem in normalized:
            duplicates.add(kw)
        else:
            normalized[stem] = kw

    return duplicates


def evaluate_keywords(keywords, max_kd=100, min_volume=0, geo_data=None):
    """
    Evaluate and filter keywords.

    In actual execution, the AI agent fills volume/KD with real data from
    APIs or WebSearch analysis. This function documents the expected structure.
    """
    evaluated = []
    duplicates = find_near_duplicates(keywords)
    duplicates_removed = 0
    filtered_kd = 0
    filtered_volume = 0

    # Build GEO score lookup
    geo_lookup = {}
    if geo_data and "results" in geo_data:
        for r in geo_data["results"]:
            query = r.get("query", "").lower().strip()
            if r.get("gap_opportunity") == "high":
                geo_lookup[query] = 3
            elif r.get("ai_answers"):
                geo_lookup[query] = 2
            else:
                geo_lookup[query] = 1

    for kw in keywords:
        kw = kw.strip()
        if not kw:
            continue

        # Skip near-duplicates
        if kw in duplicates:
            duplicates_removed += 1
            continue

        # Agent fills these with real data:
        volume_estimate = None  # Agent: from API or WebSearch proxy
        kd_estimate = None  # Agent: from API or SERP analysis
        intent = None  # Agent: from classify-intent-live.py or heuristic

        # GEO score from probe-ai-discovery.py output
        geo_score = geo_lookup.get(kw.lower(), None)

        entry = {
            "keyword": kw,
            "volume_estimate": volume_estimate,
            "kd_estimate": kd_estimate,
            "intent": intent,
            "geo_score": geo_score,
            "source": "evaluation",
            "priority_score": None,  # Filled in prioritize-opportunities.py
        }

        # Apply filters (when agent has filled real data)
        if kd_estimate is not None and kd_estimate > max_kd:
            filtered_kd += 1
            continue

        if volume_estimate is not None and volume_estimate < min_volume:
            filtered_volume += 1
            continue

        evaluated.append(entry)

    return evaluated, duplicates_removed, filtered_kd, filtered_volume


def main():
    parser = argparse.ArgumentParser(
        description="Enrich raw keyword list with volume/KD estimates and GEO scores."
    )
    parser.add_argument(
        "--keywords",
        type=str,
        required=True,
        help="Path to file with keywords, one per line",
    )
    parser.add_argument(
        "--max-kd",
        type=int,
        default=100,
        help="Maximum keyword difficulty threshold (default: 100 = no filter)",
    )
    parser.add_argument(
        "--min-volume",
        type=int,
        default=0,
        help="Minimum volume threshold (default: 0 = no filter)",
    )
    parser.add_argument(
        "--geo-data",
        type=str,
        help="Path to JSON output from probe-ai-discovery.py for GEO score merging",
    )
    parser.add_argument(
        "--api",
        type=str,
        choices=["websearch", "dataforseo", "ahrefs", "semrush"],
        default="websearch",
        help="Data source for volume/KD data (default: websearch)",
    )
    parser.add_argument("--tools", type=str, help="Path to tools.json inventory file")

    args = parser.parse_args()

    try:
        with open(args.keywords, "r") as f:
            keywords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(json.dumps({"error": f"Keywords file not found: {args.keywords}"}))
        sys.exit(1)

    geo_data = None
    if args.geo_data:
        try:
            with open(args.geo_data, "r") as f:
                geo_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load GEO data: {e}", file=sys.stderr)

    evaluated, dupes_removed, kd_filtered, vol_filtered = evaluate_keywords(
        keywords,
        max_kd=args.max_kd,
        min_volume=args.min_volume,
        geo_data=geo_data,
    )

    result = {
        "total_input": len(keywords),
        "total_after_filter": len(evaluated),
        "keywords": evaluated,
        "filters_applied": {
            "max_kd": args.max_kd,
            "min_volume": args.min_volume,
            "duplicates_removed": dupes_removed,
            "kd_filtered": kd_filtered,
            "volume_filtered": vol_filtered,
        },
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
