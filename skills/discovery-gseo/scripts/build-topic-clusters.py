#!/usr/bin/env python3
"""
build-topic-clusters.py — Group keywords by semantic similarity, identify pillars, generate cluster map.

Pure local processing — no external tools required. Takes an evaluated keyword list
and groups keywords into topic clusters, identifies pillar candidates, assigns
supporting keywords, and generates an internal link topology. Includes GEO citation
mapping to prioritize content creation within each cluster.

Usage:
    python3 build-topic-clusters.py --keywords evaluated-keywords.json
    python3 build-topic-clusters.py --keywords evaluated-keywords.json --min-cluster-size 3

AI Agent Usage:
    This script runs locally. No external API calls needed.
    1. Load evaluated keyword data (JSON from evaluate-keywords.py)
    2. Extract root topics from each keyword (strip modifiers: best, free, how to, etc.)
    3. Group keywords sharing the same root topic
    4. Merge near-duplicate groups (overlapping root topics)
    5. Per group: identify pillar (highest volume, broadest scope)
    6. Assign remaining keywords as supports or H2 sections
    7. Apply "own page" test: distinct intent + deep enough for 800+ words + SERP shows standalone pages
    8. GEO citation mapping: rank supports by GEO score, highest-GEO created first
    9. Generate internal link topology: pillar ↔ supports, related supports ↔ supports
"""

import argparse
import json
import sys
import re
from collections import defaultdict


# Modifier words to strip when extracting root topics
MODIFIERS = [
    "best", "top", "free", "cheap", "affordable", "premium",
    "how to", "what is", "why", "when", "where",
    "guide", "tutorial", "tips", "examples", "template",
    "alternative", "vs", "versus", "comparison", "review",
    "for beginners", "for freelancers", "for small business",
    "online", "software", "tool", "app", "platform", "service",
]


def extract_root_topic(keyword):
    """Extract the root topic from a keyword by stripping common modifiers."""
    kw = keyword.lower().strip()
    for mod in sorted(MODIFIERS, key=len, reverse=True):
        kw = kw.replace(mod, "")
    kw = re.sub(r"\s+", " ", kw).strip()
    return kw if kw else keyword.lower().strip()


def group_keywords(keywords_data):
    """Group keywords by root topic similarity."""
    groups = defaultdict(list)

    for entry in keywords_data:
        kw = entry.get("keyword", "")
        root = extract_root_topic(kw)
        groups[root].append(entry)

    # Merge groups with very similar root topics
    merged = {}
    used = set()
    roots = list(groups.keys())

    for i, root1 in enumerate(roots):
        if root1 in used:
            continue
        merged_group = list(groups[root1])
        used.add(root1)

        for j in range(i + 1, len(roots)):
            root2 = roots[j]
            if root2 in used:
                continue
            # Simple overlap check — if one root contains the other
            if root1 in root2 or root2 in root1:
                merged_group.extend(groups[root2])
                used.add(root2)

        # Use the shortest root as the group name
        merged[root1] = merged_group

    return merged


def identify_pillar(keywords_in_group):
    """Identify the pillar keyword (highest volume, broadest scope)."""
    pillar = None
    max_volume = -1

    for entry in keywords_in_group:
        vol = entry.get("volume_estimate")
        if vol is None:
            vol = 0
        if isinstance(vol, str):
            try:
                vol = int(vol)
            except ValueError:
                vol = 0
        if vol > max_volume:
            max_volume = vol
            pillar = entry

    if pillar is None and keywords_in_group:
        pillar = keywords_in_group[0]

    return pillar


def build_clusters(keywords_data, min_cluster_size=2):
    """Build topic clusters from evaluated keyword data."""
    groups = group_keywords(keywords_data)
    clusters = []
    unassigned = []

    for root_topic, kw_entries in groups.items():
        if len(kw_entries) < min_cluster_size:
            unassigned.extend(kw_entries)
            continue

        pillar = identify_pillar(kw_entries)
        supports = [e for e in kw_entries if e != pillar]

        # Sort supports by GEO score descending for creation priority
        supports.sort(
            key=lambda x: (x.get("geo_score") or 0, x.get("volume_estimate") or 0),
            reverse=True,
        )

        # Assign GEO priority (1 = create first)
        for idx, s in enumerate(supports):
            s["geo_priority"] = idx + 1

        # Determine page type for each support
        for s in supports:
            intent = s.get("intent", "informational")
            if intent == "commercial":
                s["page_type"] = "comparison"
            elif intent == "transactional":
                s["page_type"] = "product page or tool"
            else:
                s["page_type"] = "guide"

        cluster = {
            "name": root_topic.title() if root_topic else "Uncategorized",
            "pillar": {
                "keyword": pillar.get("keyword", ""),
                "volume": pillar.get("volume_estimate"),
                "kd": pillar.get("kd_estimate"),
                "geo_score": pillar.get("geo_score"),
            },
            "supports": [
                {
                    "keyword": s.get("keyword", ""),
                    "volume": s.get("volume_estimate"),
                    "kd": s.get("kd_estimate"),
                    "geo_score": s.get("geo_score"),
                    "page_type": s.get("page_type", "guide"),
                    "geo_priority": s.get("geo_priority", 99),
                }
                for s in supports
            ],
            "internal_links": {
                "pillar_to_supports": True,
                "supports_to_pillar": True,
                "cross_links": [],  # Agent identifies related supports to cross-link
            },
        }

        clusters.append(cluster)

    # Sort clusters by pillar volume descending
    clusters.sort(
        key=lambda c: c["pillar"].get("volume") or 0,
        reverse=True,
    )

    return clusters, unassigned


def main():
    parser = argparse.ArgumentParser(
        description="Group keywords into topic clusters with pillar/support assignments."
    )
    parser.add_argument(
        "--keywords",
        type=str,
        required=True,
        help="Path to JSON file from evaluate-keywords.py",
    )
    parser.add_argument(
        "--min-cluster-size",
        type=int,
        default=2,
        help="Minimum keywords per cluster (default: 2)",
    )

    args = parser.parse_args()

    try:
        with open(args.keywords, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(json.dumps({"error": f"Keywords file not found: {args.keywords}"}))
        sys.exit(1)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON in keywords file."}))
        sys.exit(1)

    # Support both raw list and evaluate-keywords.py output format
    if isinstance(data, list):
        keywords_data = data
    elif isinstance(data, dict) and "keywords" in data:
        keywords_data = data["keywords"]
    else:
        print(json.dumps({"error": "Unexpected JSON format. Expected list or {keywords: [...]}"}))
        sys.exit(1)

    clusters, unassigned = build_clusters(keywords_data, args.min_cluster_size)

    total_assigned = sum(1 + len(c["supports"]) for c in clusters)

    result = {
        "total_clusters": len(clusters),
        "total_keywords_assigned": total_assigned,
        "clusters": clusters,
        "unassigned_keywords": len(unassigned),
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
