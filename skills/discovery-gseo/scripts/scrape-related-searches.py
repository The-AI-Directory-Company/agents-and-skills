#!/usr/bin/env python3
"""
scrape-related-searches.py — Extract Related Searches from Google SERPs with 2-level chaining.

For each seed keyword, searches Google, scrolls to the bottom of the SERP to extract
Related Searches, then clicks each related search for a 2nd-level expansion. Deduplicates
across all levels.

Usage:
    python3 scrape-related-searches.py --seeds "invoicing software,billing software"
    python3 scrape-related-searches.py --seeds "invoicing software" --no-browser
    python3 scrape-related-searches.py --seeds-file seeds.txt

AI Agent Usage (Playwright MCP — primary path):
    For each seed keyword:
    1. browser_navigate to https://www.google.com/search?q={seed}&gl=us&hl=en&pws=0
    2. Wait 2-3 seconds for page load
    3. browser_evaluate(expression="window.scrollTo(0, document.body.scrollHeight)")
    4. browser_snapshot — extract Related Searches links from the bottom section
    5. For each related search (level 1):
       a. browser_click on the related search link
       b. Wait 3-5 seconds for new SERP to load
       c. browser_evaluate to scroll to bottom
       d. browser_snapshot — extract level-2 Related Searches
    6. Deduplicate all collected keywords
    7. Wait 3-5 seconds (randomized) before next seed
    Anti-detection: 3-5s between navigations, max 10 seeds per session (many page loads per seed).

AI Agent Usage (--no-browser fallback):
    Use WebSearch for each seed. Some APIs include related search data.
    No chaining possible — level 1 only, with fewer results.
"""

import argparse
import json
import sys
import random
import time


MAX_SEEDS_PER_SESSION = 10


def scrape_with_browser(seeds):
    """
    Browser-based Related Searches extraction with 2-level chaining.
    """
    all_related = []
    seen = set()

    for i, seed in enumerate(seeds):
        if i >= MAX_SEEDS_PER_SESSION:
            print(
                f"Warning: session limit ({MAX_SEEDS_PER_SESSION}) reached.",
                file=sys.stderr,
            )
            break

        seed = seed.strip()
        if not seed:
            continue

        # --- Agent: Playwright MCP calls ---
        # 1. browser_navigate(url=f"https://www.google.com/search?q={seed}&gl=us&hl=en&pws=0")
        # 2. Wait 2-3 seconds
        # 3. browser_evaluate(expression="window.scrollTo(0, document.body.scrollHeight)")
        # 4. browser_snapshot() → find "Related searches" section, extract link texts
        # 5. For each level-1 related search:
        #      browser_click(element="related search link", ref="...")
        #      Wait 3-5 seconds
        #      browser_evaluate(expression="window.scrollTo(0, document.body.scrollHeight)")
        #      browser_snapshot() → extract level-2 related searches
        # 6. Wait 3-5 seconds before next seed

        # Level 1 placeholder
        level1_keywords = _placeholder_related(seed, level=1)
        for kw in level1_keywords:
            key = kw["keyword"]
            if key not in seen:
                seen.add(key)
                all_related.append(kw)

                # Level 2 chaining
                level2_keywords = _placeholder_related(key, level=2, parent=seed)
                for kw2 in level2_keywords:
                    if kw2["keyword"] not in seen:
                        seen.add(kw2["keyword"])
                        kw2["parent"] = key
                        all_related.append(kw2)

        delay = random.uniform(3.0, 5.0)
        time.sleep(delay)

    return all_related


def scrape_without_browser(seeds):
    """
    Fallback: extract related search data from WebSearch results.
    No chaining — level 1 only.
    """
    all_related = []
    seen = set()

    for seed in seeds:
        seed = seed.strip()
        if not seed:
            continue

        # Agent: WebSearch(query=seed) → parse any "related searches" from results
        placeholder = {
            "keyword": f"{seed} alternatives",
            "level": 1,
            "source_seed": seed,
        }
        if placeholder["keyword"] not in seen:
            seen.add(placeholder["keyword"])
            all_related.append(placeholder)

    return all_related


def _placeholder_related(seed, level=1, parent=None):
    """Placeholder for browser-extracted Related Searches."""
    result = {
        "keyword": f"{seed} related",
        "level": level,
        "source_seed": seed,
    }
    if parent:
        result["parent"] = parent
    return [result]


def main():
    parser = argparse.ArgumentParser(
        description="Extract Related Searches from Google SERPs with 2-level chaining."
    )
    parser.add_argument("--seeds", type=str, help="Comma-separated seed keywords")
    parser.add_argument(
        "--seeds-file", type=str, help="Path to file with seeds, one per line"
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Use WebSearch fallback instead of Playwright MCP",
    )
    parser.add_argument("--tools", type=str, help="Path to tools.json inventory file")

    args = parser.parse_args()

    seeds = []
    if args.seeds:
        seeds = [s.strip() for s in args.seeds.split(",") if s.strip()]
    elif args.seeds_file:
        try:
            with open(args.seeds_file, "r") as f:
                seeds = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(json.dumps({"error": f"Seeds file not found: {args.seeds_file}"}))
            sys.exit(1)

    if not seeds:
        print(json.dumps({"error": "No seeds provided. Use --seeds or --seeds-file."}))
        sys.exit(1)

    if args.no_browser:
        related = scrape_without_browser(seeds)
        method = "fallback"
    else:
        related = scrape_with_browser(seeds)
        method = "playwright"

    result = {
        "seeds_processed": min(len(seeds), MAX_SEEDS_PER_SESSION),
        "total_related": len(related),
        "related": related,
        "method": method,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
