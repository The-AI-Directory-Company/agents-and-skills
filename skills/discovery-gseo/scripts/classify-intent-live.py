#!/usr/bin/env python3
"""
classify-intent-live.py — Live SERP analysis for intent classification and AI-answerable flagging.

For each keyword, searches Google via Playwright MCP, analyzes SERP composition
(content types ranking, SERP features present), classifies intent, and flags
AI-answerable queries.

Usage:
    python3 classify-intent-live.py --keywords keywords.txt
    python3 classify-intent-live.py --keywords keywords.txt --no-browser

AI Agent Usage (Playwright MCP — primary path):
    For each keyword:
    1. browser_navigate to https://www.google.com/search?q={keyword}&gl=us&hl=en&pws=0
    2. Wait 3 seconds for full SERP load
    3. browser_snapshot — analyze:
       a. Top 10 result content types: blog, product page, comparison, tool, docs
       b. SERP features: AI Overview, Featured Snippet, PAA, Shopping, Video, Local pack
    4. Classify intent from majority content type:
       - Blog/tutorial/guide → informational
       - Product/pricing/tool → transactional
       - Comparison/review/best-of → commercial
       - Brand homepage → navigational
    5. Flag AI-answerable if AI Overview is present
    6. Record dominant content type and recommended page type
    7. Wait 5-8 seconds (randomized) between keywords
    Anti-detection: 5-8s between searches, max 20 keywords per session.

AI Agent Usage (--no-browser fallback):
    Use WebSearch for each keyword. Classify intent from result titles and URLs.
    Cannot detect SERP features or AI Overview. Note limitations.
"""

import argparse
import json
import sys
import re
import random
import time


MAX_KEYWORDS_PER_SESSION = 20

# URL/title patterns for content type classification
CONTENT_PATTERNS = {
    "blog": [r"/blog/", r"/article/", r"how[\s-]to", r"guide", r"tutorial", r"tips"],
    "product_page": [r"/product", r"/pricing", r"/features", r"/plans", r"/signup"],
    "comparison": [r"-vs-", r"/compare", r"/alternative", r"/best-", r"review", r"top-\d+"],
    "tool": [r"/tool", r"/calculator", r"/generator", r"/template", r"/free-"],
    "documentation": [r"/docs/", r"/help/", r"/support/", r"/api/"],
}

# Content type to intent mapping
INTENT_MAP = {
    "blog": "informational",
    "documentation": "informational",
    "comparison": "commercial",
    "product_page": "transactional",
    "tool": "transactional",
}

# Page type recommendations per intent
PAGE_TYPE_MAP = {
    "informational": "blog post or guide",
    "commercial": "comparison page",
    "transactional": "product page or free tool",
    "navigational": "brand page",
}


def classify_content_type(url, title):
    """Classify content type from URL and title."""
    text = f"{url} {title}".lower()
    for ctype, patterns in CONTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return ctype
    return "other"


def classify_with_browser(keywords):
    """
    Browser-based intent classification via Playwright MCP.
    """
    classifications = []
    intent_counts = {"informational": 0, "commercial": 0, "transactional": 0, "navigational": 0}

    for i, keyword in enumerate(keywords):
        if i >= MAX_KEYWORDS_PER_SESSION:
            print(
                f"Warning: session limit ({MAX_KEYWORDS_PER_SESSION}) reached.",
                file=sys.stderr,
            )
            break

        keyword = keyword.strip()
        if not keyword:
            continue

        # --- Agent: Playwright MCP calls ---
        # 1. browser_navigate(url=f"https://www.google.com/search?q={kw}&gl=us&hl=en&pws=0")
        # 2. Wait 3 seconds
        # 3. browser_snapshot() → analyze SERP:
        #    - Identify content types for each organic result
        #    - Check for AI Overview, Featured Snippet, PAA, Shopping, Video, Local pack
        # 4. Determine intent from dominant content type
        # 5. Set ai_answerable = True if AI Overview detected
        # 6. Wait 5-8 seconds before next keyword

        classification = {
            "keyword": keyword,
            "intent": "unknown",  # Agent fills from SERP analysis
            "confidence": 0.0,  # Agent sets based on SERP consistency
            "ai_answerable": False,  # Agent sets True if AI Overview present
            "ai_overview_present": False,
            "serp_features": [],  # Agent fills: ["paa", "ai_overview", "featured_snippet", ...]
            "dominant_content_type": "unknown",
            "recommended_page_type": "unknown",
        }

        classifications.append(classification)
        intent = classification["intent"]
        if intent in intent_counts:
            intent_counts[intent] += 1

        if i < len(keywords) - 1:
            delay = random.uniform(5.0, 8.0)
            time.sleep(delay)

    return classifications, intent_counts


def classify_without_browser(keywords):
    """
    Fallback: intent classification from WebSearch result titles and URLs.
    Cannot detect SERP features or AI Overview.
    """
    classifications = []
    intent_counts = {"informational": 0, "commercial": 0, "transactional": 0, "navigational": 0}

    for keyword in keywords:
        keyword = keyword.strip()
        if not keyword:
            continue

        # Agent: WebSearch(query=keyword) → get results
        # For each result: classify_content_type(url, title)
        # Determine intent from majority content type

        # Heuristic fallback based on keyword text patterns
        kw_lower = keyword.lower()
        if any(w in kw_lower for w in ["how to", "what is", "why", "guide", "tutorial"]):
            intent = "informational"
        elif any(w in kw_lower for w in ["best", "vs", "alternative", "review", "comparison", "top"]):
            intent = "commercial"
        elif any(w in kw_lower for w in ["buy", "price", "free", "tool", "download", "template"]):
            intent = "transactional"
        else:
            intent = "informational"  # Default

        classification = {
            "keyword": keyword,
            "intent": intent,
            "confidence": 0.5,  # Lower confidence for heuristic
            "ai_answerable": None,  # Cannot determine without browser
            "ai_overview_present": None,
            "serp_features": [],
            "dominant_content_type": "unknown",
            "recommended_page_type": PAGE_TYPE_MAP.get(intent, "unknown"),
            "limitations": [
                "Intent classified from keyword text, not live SERP",
                "AI-answerable status unknown without browser",
                "SERP features not detectable",
            ],
        }

        classifications.append(classification)
        if intent in intent_counts:
            intent_counts[intent] += 1

    return classifications, intent_counts


def main():
    parser = argparse.ArgumentParser(
        description="Live SERP analysis for intent classification and AI-answerable flagging."
    )
    parser.add_argument(
        "--keywords",
        type=str,
        required=True,
        help="Path to file with keywords, one per line",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Use heuristic fallback instead of Playwright MCP",
    )
    parser.add_argument("--tools", type=str, help="Path to tools.json inventory file")

    args = parser.parse_args()

    try:
        with open(args.keywords, "r") as f:
            keywords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(json.dumps({"error": f"Keywords file not found: {args.keywords}"}))
        sys.exit(1)

    if not keywords:
        print(json.dumps({"error": "No keywords found in file."}))
        sys.exit(1)

    if args.no_browser:
        classifications, intent_dist = classify_without_browser(keywords)
        method = "fallback"
    else:
        classifications, intent_dist = classify_with_browser(keywords)
        method = "playwright"

    result = {
        "total_classified": len(classifications),
        "method": method,
        "classifications": classifications,
        "intent_distribution": intent_dist,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
