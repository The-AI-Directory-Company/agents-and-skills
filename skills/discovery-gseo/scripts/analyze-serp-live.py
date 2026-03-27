#!/usr/bin/env python3
"""
analyze-serp-live.py — Flagship SERP analysis: organic results, features, AI Overview, screenshots.

Searches a keyword on Google via Playwright MCP, extracts organic results, detects all
SERP features (AI Overview, Featured Snippet, PAA, Knowledge Panel, Video carousel,
Local pack, Shopping, Sitelinks), classifies search intent from SERP composition,
flags AI-answerable queries, and captures a screenshot.

Usage:
    python3 analyze-serp-live.py --keyword "invoicing software"
    python3 analyze-serp-live.py --keywords keywords.txt
    python3 analyze-serp-live.py --keyword "invoicing software" --no-browser

AI Agent Usage (Playwright MCP — primary path):
    1. browser_navigate to https://www.google.com/search?q={keyword}&gl=us&hl=en&pws=0
    2. Wait 3 seconds for full SERP load (AI Overview, SERP features are JS-rendered)
    3. browser_snapshot — extract:
       a. Organic results: position, title, URL, description snippet
       b. SERP features present: AI Overview (source count), Featured Snippet (type),
          PAA (question count), Knowledge Panel, Video carousel, Local pack,
          Shopping results, Sitelinks, Image pack
       c. Feature positions relative to organic results (above/below fold)
    4. browser_take_screenshot — capture full SERP image
    5. For each organic result: classify content type from URL/title patterns
       (blog, product_page, comparison, tool, documentation, category_page)
    6. Determine search intent from SERP composition:
       - Majority blog posts → informational
       - Majority product pages → transactional
       - Majority comparison/review → commercial
       - Brand homepages → navigational
    7. Flag as AI-answerable if AI Overview is present
    Anti-detection: 5-8s between keywords if processing a list.

AI Agent Usage (--no-browser fallback):
    Use WebSearch for organic results. Cannot detect SERP features, AI Overview,
    or take screenshots. Intent classification from titles/URLs only. Note all
    limitations in output.
"""

import argparse
import json
import sys
import random
import time
import re
from datetime import date


CONTENT_TYPE_PATTERNS = {
    "blog": [r"/blog/", r"/article/", r"/post/", r"how-to", r"guide", r"tutorial"],
    "product_page": [r"/product", r"/pricing", r"/features", r"/plans"],
    "comparison": [r"-vs-", r"/compare", r"/alternative", r"/best-", r"review"],
    "tool": [r"/tool", r"/calculator", r"/generator", r"/template", r"/free-"],
    "documentation": [r"/docs/", r"/help/", r"/support/", r"/faq"],
    "category_page": [r"/category/", r"/solutions/", r"/use-case"],
}


def classify_content_type(url, title):
    """Classify a SERP result's content type from URL and title patterns."""
    text = f"{url} {title}".lower()
    for ctype, patterns in CONTENT_TYPE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return ctype
    return "other"


def determine_intent(content_types):
    """Determine search intent from the dominant content type in SERP results."""
    if not content_types:
        return "unknown"

    counts = {}
    for ct in content_types:
        counts[ct] = counts.get(ct, 0) + 1

    # Map content types to intent
    intent_map = {
        "blog": "informational",
        "documentation": "informational",
        "comparison": "commercial",
        "product_page": "transactional",
        "tool": "transactional",
        "category_page": "commercial",
    }

    intent_counts = {}
    for ct, count in counts.items():
        intent = intent_map.get(ct, "informational")
        intent_counts[intent] = intent_counts.get(intent, 0) + count

    return max(intent_counts, key=intent_counts.get)


def analyze_with_browser(keywords):
    """
    Browser-based SERP analysis via Playwright MCP.
    The agent executes tool calls per the module docstring.
    """
    results = []

    for i, keyword in enumerate(keywords):
        keyword = keyword.strip()
        if not keyword:
            continue

        # --- Agent: Playwright MCP calls ---
        # 1. browser_navigate(url=f"https://www.google.com/search?q={kw}&gl=us&hl=en&pws=0")
        # 2. Wait 3 seconds
        # 3. browser_snapshot() → parse organic results and SERP features
        # 4. browser_take_screenshot() → save as serp-{keyword}-{date}.png
        # 5. Classify each result's content type
        # 6. Determine intent from SERP composition
        # 7. Check for AI Overview presence → ai_answerable flag

        today = date.today().isoformat()
        result = {
            "keyword": keyword,
            "method": "playwright",
            "organic_results": [],
            "serp_features": {
                "ai_overview": {"present": False, "source_count": 0},
                "featured_snippet": {"present": False, "type": None},
                "paa": {"present": False, "question_count": 0},
                "knowledge_panel": {"present": False},
                "video_carousel": {"present": False},
                "local_pack": {"present": False},
                "shopping_results": {"present": False},
                "sitelinks": {"present": False},
                "image_pack": {"present": False},
            },
            "intent_classification": "unknown",
            "ai_answerable": False,
            "screenshot_path": f"serp-{keyword.replace(' ', '-')}-{today}.png",
        }

        # Agent fills organic_results from browser_snapshot data:
        # [{"position": 1, "title": "...", "url": "...",
        #   "description": "...", "content_type": "blog"}, ...]
        # Agent fills serp_features from browser_snapshot analysis.
        # Agent sets ai_answerable = True if AI Overview is detected.

        results.append(result)

        if i < len(keywords) - 1:
            delay = random.uniform(5.0, 8.0)
            time.sleep(delay)

    return results


def analyze_without_browser(keywords):
    """
    Fallback: SERP analysis via WebSearch.
    Cannot detect SERP features or AI Overview. Intent from titles/URLs only.
    """
    results = []

    for keyword in keywords:
        keyword = keyword.strip()
        if not keyword:
            continue

        # Agent: WebSearch(query=keyword) → parse organic results
        # Classify content types from URLs/titles
        # Cannot detect: AI Overview, Featured Snippet, PAA, Knowledge Panel, etc.

        result = {
            "keyword": keyword,
            "method": "fallback",
            "organic_results": [],
            "serp_features": {
                "ai_overview": {"present": None, "source_count": None},
                "featured_snippet": {"present": None},
                "paa": {"present": None},
                "knowledge_panel": {"present": None},
                "video_carousel": {"present": None},
                "local_pack": {"present": None},
                "shopping_results": {"present": None},
                "sitelinks": {"present": None},
                "image_pack": {"present": None},
            },
            "intent_classification": "unknown",
            "ai_answerable": None,
            "screenshot_path": None,
            "limitations": [
                "SERP features not detectable without browser",
                "AI Overview presence unknown",
                "No screenshot available",
                "Intent classification based on result titles/URLs only",
            ],
        }

        results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Flagship SERP analysis with organic results, features, and AI Overview."
    )
    parser.add_argument("--keyword", type=str, help="Single keyword to analyze")
    parser.add_argument(
        "--keywords", type=str, help="Path to file with keywords, one per line"
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Use WebSearch fallback instead of Playwright MCP",
    )
    parser.add_argument("--tools", type=str, help="Path to tools.json inventory file")

    args = parser.parse_args()

    keywords = []
    if args.keyword:
        keywords = [args.keyword]
    elif args.keywords:
        try:
            with open(args.keywords, "r") as f:
                keywords = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(json.dumps({"error": f"Keywords file not found: {args.keywords}"}))
            sys.exit(1)

    if not keywords:
        print(
            json.dumps(
                {"error": "No keywords provided. Use --keyword or --keywords."}
            )
        )
        sys.exit(1)

    if args.no_browser:
        analyses = analyze_without_browser(keywords)
    else:
        analyses = analyze_with_browser(keywords)

    if len(analyses) == 1:
        print(json.dumps(analyses[0], indent=2))
    else:
        print(json.dumps({"total_analyzed": len(analyses), "results": analyses}, indent=2))


if __name__ == "__main__":
    main()
