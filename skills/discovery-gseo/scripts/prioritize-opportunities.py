#!/usr/bin/env python3
"""
prioritize-opportunities.py — 4-dimension scoring (max 12) with tiered content plan and schedule.

Takes clustered keyword data, scores each keyword/page on 4 dimensions (Business Value,
Ranking Feasibility, Traffic Potential, GEO Opportunity), assigns tiers, and generates
a prioritized content calendar.

Usage:
    python3 prioritize-opportunities.py --clusters clusters.json
    python3 prioritize-opportunities.py --clusters clusters.json --business-keywords biz.txt

AI Agent Usage:
    This script runs locally. The agent may need to interactively ask the user for
    business value assessments (which keywords are directly product-relevant?).
    1. Load cluster data (JSON from build-topic-clusters.py)
    2. For each keyword across all clusters:
       a. Score Business Value (1-3):
          - 3 = directly product-relevant (matches --business-keywords or user confirms)
          - 2 = indirectly relevant (solves related problem)
          - 1 = tangentially related
       b. Score Ranking Feasibility (1-3):
          - 3 = KD < 20
          - 2 = KD 20-40
          - 1 = KD 40+
       c. Score Traffic Potential (1-3):
          - 3 = volume > 1000
          - 2 = volume 200-1000
          - 1 = volume < 200
       d. Score GEO Opportunity (1-3): from geo_score data
       e. Total = BV + RF + TP + GEO (max 12)
       f. Assign tier: 10-12 golden, 7-9 strong, 4-6 moderate, 1-3 skip
    3. Sort by total score descending
    4. Generate monthly plan:
       - Month 1: golden-tier, pillar pages first
       - Month 2: supporting pages + internal links
       - Month 3: optimize Month 1 with GSC data + continue publishing
       - Ongoing: 2-4 pages/month
"""

import argparse
import json
import sys
import math


def score_business_value(keyword, business_keywords=None):
    """
    Score business value 1-3.

    If business_keywords list provided, keywords matching the list get 3.
    Otherwise, agent should interactively assess with the user.
    """
    if business_keywords:
        kw_lower = keyword.lower()
        for bk in business_keywords:
            if bk.lower() in kw_lower or kw_lower in bk.lower():
                return 3
    # Default: agent should override with user input
    return 2


def score_ranking_feasibility(kd):
    """Score ranking feasibility 1-3 based on keyword difficulty."""
    if kd is None:
        return 2  # Unknown KD defaults to medium
    if kd < 20:
        return 3
    elif kd <= 40:
        return 2
    else:
        return 1


def score_traffic_potential(volume):
    """Score traffic potential 1-3 based on search volume."""
    if volume is None:
        return 1  # Unknown volume defaults to low
    if isinstance(volume, str):
        try:
            volume = int(volume)
        except ValueError:
            return 1
    if volume > 1000:
        return 3
    elif volume >= 200:
        return 2
    else:
        return 1


def score_geo_opportunity(geo_score):
    """Score GEO opportunity 1-3 from existing GEO score data."""
    if geo_score is None:
        return 1  # Unknown GEO defaults to low
    return max(1, min(3, int(geo_score)))


def assign_tier(total_score):
    """Assign tier based on total score."""
    if total_score >= 10:
        return "golden"
    elif total_score >= 7:
        return "strong"
    elif total_score >= 4:
        return "moderate"
    else:
        return "skip"


def prioritize(clusters_data, business_keywords=None):
    """Score and prioritize all keywords across clusters."""
    content_plan = []

    for cluster in clusters_data:
        cluster_name = cluster.get("name", "Unknown")

        # Process pillar
        pillar = cluster.get("pillar", {})
        if pillar.get("keyword"):
            entry = _score_entry(
                pillar, cluster_name, "pillar", business_keywords
            )
            content_plan.append(entry)

        # Process supports
        for support in cluster.get("supports", []):
            if support.get("keyword"):
                entry = _score_entry(
                    support, cluster_name, support.get("page_type", "guide"),
                    business_keywords
                )
                content_plan.append(entry)

    # Sort by total score descending
    content_plan.sort(key=lambda x: x["total_score"], reverse=True)

    # Assign priority numbers
    for i, entry in enumerate(content_plan):
        entry["priority"] = i + 1

    return content_plan


def _score_entry(kw_data, cluster_name, page_type, business_keywords):
    """Score a single keyword entry on all 4 dimensions."""
    keyword = kw_data.get("keyword", "")
    kd = kw_data.get("kd") or kw_data.get("kd_estimate")
    volume = kw_data.get("volume") or kw_data.get("volume_estimate")
    geo = kw_data.get("geo_score")

    bv = score_business_value(keyword, business_keywords)
    rf = score_ranking_feasibility(kd)
    tp = score_traffic_potential(volume)
    geo_opp = score_geo_opportunity(geo)
    total = bv + rf + tp + geo_opp

    # Generate target URL from keyword
    slug = keyword.lower().replace(" ", "-")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")

    return {
        "keyword": keyword,
        "volume": volume,
        "kd": kd,
        "intent": kw_data.get("intent", "unknown"),
        "geo_score": geo,
        "scores": {
            "business_value": bv,
            "ranking_feasibility": rf,
            "traffic_potential": tp,
            "geo_opportunity": geo_opp,
        },
        "total_score": total,
        "tier": assign_tier(total),
        "page_type": page_type,
        "target_url": f"/{slug}",
        "cluster": cluster_name,
        "publish_by": "",  # Filled in monthly plan generation
    }


def generate_monthly_plan(content_plan):
    """Assign publishing schedule based on tiers."""
    golden = [e for e in content_plan if e["tier"] == "golden"]
    strong = [e for e in content_plan if e["tier"] == "strong"]
    moderate = [e for e in content_plan if e["tier"] == "moderate"]

    month_1 = []
    month_2 = []
    month_3 = []

    # Month 1: golden-tier, up to 5 pages, pillars first
    golden_pillars = [e for e in golden if e["page_type"] == "pillar"]
    golden_others = [e for e in golden if e["page_type"] != "pillar"]
    month_1_candidates = golden_pillars + golden_others

    for i, entry in enumerate(month_1_candidates[:5]):
        entry["publish_by"] = f"Month 1 Week {min(i + 1, 4)}"
        month_1.append(entry)

    remaining_golden = month_1_candidates[5:]

    # Month 2: remaining golden + top strong, up to 5 pages
    month_2_candidates = remaining_golden + strong
    for i, entry in enumerate(month_2_candidates[:5]):
        entry["publish_by"] = f"Month 2 Week {min(i + 1, 4)}"
        month_2.append(entry)

    # Month 3: remaining strong + optimization
    month_3_candidates = month_2_candidates[5:]
    for i, entry in enumerate(month_3_candidates[:5]):
        entry["publish_by"] = f"Month 3 Week {min(i + 1, 4)}"
        month_3.append(entry)

    return {
        "month_1": [e["keyword"] for e in month_1],
        "month_2": [e["keyword"] for e in month_2],
        "month_3": [e["keyword"] for e in month_3],
    }


def main():
    parser = argparse.ArgumentParser(
        description="4-dimension scoring (max 12), tiered content plan with schedule."
    )
    parser.add_argument(
        "--clusters",
        type=str,
        required=True,
        help="Path to JSON file from build-topic-clusters.py",
    )
    parser.add_argument(
        "--business-keywords",
        type=str,
        help="Path to file with business-relevant keywords (one per line) for BV scoring",
    )
    parser.add_argument("--tools", type=str, help="Path to tools.json inventory file")

    args = parser.parse_args()

    try:
        with open(args.clusters, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(json.dumps({"error": f"Clusters file not found: {args.clusters}"}))
        sys.exit(1)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON in clusters file."}))
        sys.exit(1)

    # Support both raw cluster list and build-topic-clusters.py output format
    if isinstance(data, list):
        clusters_data = data
    elif isinstance(data, dict) and "clusters" in data:
        clusters_data = data["clusters"]
    else:
        print(json.dumps({"error": "Unexpected JSON format."}))
        sys.exit(1)

    business_keywords = None
    if args.business_keywords:
        try:
            with open(args.business_keywords, "r") as f:
                business_keywords = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Warning: Business keywords file not found.", file=sys.stderr)

    content_plan = prioritize(clusters_data, business_keywords)
    monthly_plan = generate_monthly_plan(content_plan)

    # Count tiers
    tier_dist = {}
    for entry in content_plan:
        tier = entry["tier"]
        tier_dist[tier] = tier_dist.get(tier, 0) + 1

    result = {
        "total_opportunities": len(content_plan),
        "content_plan": content_plan,
        "tier_distribution": tier_dist,
        "monthly_plan": monthly_plan,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
