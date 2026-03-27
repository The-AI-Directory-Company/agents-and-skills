#!/usr/bin/env python3
"""
harvest-autocomplete.py — Harvest Google Autocomplete suggestions for seed keywords.

Types each seed keyword into Google with a-z letter suffixes and question prefixes
(how/what/why/best), capturing every Autocomplete suggestion. Uses Playwright MCP
for live browser interaction with Google Autocomplete.

Usage:
    python3 harvest-autocomplete.py --seeds "invoicing software,billing software"
    python3 harvest-autocomplete.py --seeds "invoicing software" --no-browser
    python3 harvest-autocomplete.py --seeds-file seeds.txt

AI Agent Usage (Playwright MCP — primary path):
    For each seed keyword:
    1. browser_navigate to https://www.google.com
    2. browser_click on the search input
    3. browser_type the seed keyword (submit: false) — wait 500ms
    4. browser_snapshot to capture Autocomplete dropdown suggestions
    5. For each letter a-z:
       - browser_type the letter (submit: false) — wait 500ms
       - browser_snapshot to capture suggestions
       - browser_press_key Backspace to remove the letter
    6. Clear input, type "how to [seed]", "what is [seed]", "best [seed]", "why [seed]"
       - browser_snapshot for each prefix
    7. Wait 3-8 seconds (randomized) before next seed
    Anti-detection: randomized delays 3-8s between seeds, 100-200ms between keystrokes,
    standard viewport 1280x800, max 25 seeds per session.

AI Agent Usage (--no-browser fallback):
    Use WebSearch for "[seed] a", "[seed] b", etc. Results approximate Autocomplete
    but miss real-time, localized suggestions. Quality is significantly reduced.
"""

import argparse
import json
import sys
import random
import time


QUESTION_PREFIXES = ["how to", "what is", "best", "why"]
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
MAX_SEEDS_PER_SESSION = 25


def harvest_with_browser(seeds):
    """
    Browser-based Autocomplete harvesting via Playwright MCP.

    This function documents the procedure for AI agents. The agent should
    execute the Playwright MCP tool calls described in the module docstring,
    collecting suggestions at each step.

    Returns a list of suggestion dicts.
    """
    suggestions = []
    seen = set()

    for i, seed in enumerate(seeds):
        if i >= MAX_SEEDS_PER_SESSION:
            print(
                f"Warning: session limit ({MAX_SEEDS_PER_SESSION}) reached. "
                f"Remaining seeds skipped to avoid captchas.",
                file=sys.stderr,
            )
            break

        seed = seed.strip()
        if not seed:
            continue

        # --- Agent: execute these Playwright MCP calls ---
        # 1. browser_navigate(url="https://www.google.com")
        # 2. browser_click(element="search input")
        # 3. browser_type(text=seed, submit=False)
        # 4. Wait 500ms, then browser_snapshot() → parse Autocomplete suggestions
        # 5. For letter in a-z:
        #      browser_type(text=letter, submit=False)
        #      Wait 500ms, browser_snapshot() → parse suggestions
        #      browser_press_key(key="Backspace")
        # 6. Clear input (select all + delete), then for each prefix in QUESTION_PREFIXES:
        #      browser_type(text=f"{prefix} {seed}", submit=False)
        #      Wait 500ms, browser_snapshot() → parse suggestions
        #      Clear input
        # 7. Wait random 3-8 seconds before next seed

        # Base seed suggestions
        base_suggestions = _placeholder_suggestions(seed, "autocomplete_base")
        for s in base_suggestions:
            if s["keyword"] not in seen:
                seen.add(s["keyword"])
                suggestions.append(s)

        # a-z suffix suggestions
        for letter in ALPHABET:
            letter_suggestions = _placeholder_suggestions(
                f"{seed} {letter}", f"autocomplete_{letter}"
            )
            for s in letter_suggestions:
                if s["keyword"] not in seen:
                    seen.add(s["keyword"])
                    suggestions.append(s)

        # Question prefix suggestions
        for prefix in QUESTION_PREFIXES:
            prefix_suggestions = _placeholder_suggestions(
                f"{prefix} {seed}", f"autocomplete_prefix_{prefix.replace(' ', '_')}"
            )
            for s in prefix_suggestions:
                if s["keyword"] not in seen:
                    seen.add(s["keyword"])
                    suggestions.append(s)

        # Rate limiting
        delay = random.uniform(3.0, 8.0)
        time.sleep(delay)

    return suggestions


def harvest_without_browser(seeds):
    """
    Fallback: approximate Autocomplete data using WebSearch.

    AI Agent: For each seed, run WebSearch queries for "[seed] a", "[seed] b", etc.
    Parse the result titles and snippets for keyword phrases. Quality is significantly
    lower than browser-based Autocomplete — many suggestions will be missed.
    """
    suggestions = []
    seen = set()

    for seed in seeds:
        seed = seed.strip()
        if not seed:
            continue

        # Agent: WebSearch("[seed]") → extract keyword phrases from titles/snippets
        # Agent: WebSearch("[seed] a"), WebSearch("[seed] b"), ... through z
        # Agent: WebSearch("how to [seed]"), WebSearch("best [seed]"), etc.
        # Parse result titles for keyword candidates.

        placeholder = {
            "keyword": seed,
            "source_seed": seed,
            "expansion_type": "fallback_websearch",
        }
        if seed not in seen:
            seen.add(seed)
            suggestions.append(placeholder)

    return suggestions


def _placeholder_suggestions(query, expansion_type):
    """
    Placeholder for browser-extracted suggestions.

    In actual execution, the AI agent replaces this with real data from
    browser_snapshot parsing. This function exists so the script can run
    standalone for testing and to document the expected output format.
    """
    # In real execution, the agent collects suggestions from browser_snapshot
    # and returns them in this format.
    return [
        {
            "keyword": query,
            "source_seed": query.split()[0] if query else "",
            "expansion_type": expansion_type,
        }
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Harvest Google Autocomplete suggestions for seed keywords."
    )
    parser.add_argument(
        "--seeds",
        type=str,
        help="Comma-separated seed keywords (e.g., 'invoicing software,billing software')",
    )
    parser.add_argument(
        "--seeds-file",
        type=str,
        help="Path to file with seed keywords, one per line",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Use WebSearch fallback instead of Playwright MCP browser automation",
    )
    parser.add_argument(
        "--tools",
        type=str,
        help="Path to tools.json inventory file",
    )

    args = parser.parse_args()

    # Parse seeds
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

    # Harvest
    if args.no_browser:
        suggestions = harvest_without_browser(seeds)
        method = "fallback"
    else:
        suggestions = harvest_with_browser(seeds)
        method = "playwright"

    # Output
    result = {
        "seeds_processed": min(len(seeds), MAX_SEEDS_PER_SESSION),
        "total_suggestions": len(suggestions),
        "suggestions": suggestions,
        "method": method,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
