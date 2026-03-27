#!/usr/bin/env python3
"""
classify-intent.py — Classify search intent for a list of keywords.

For each keyword, analyzes top 5 search results to determine whether
the intent is informational, navigational, commercial, or transactional.
Assigns confidence based on result-type unanimity.

Usage:
    python classify-intent.py --keywords keywords.txt
    echo "invoice automation software" | python classify-intent.py --from-stdin
    python classify-intent.py --keywords keywords.txt --tools tools.json

Free path: WebSearch to analyze top results.
Paid extension: DataForSEO SERP API for richer SERP feature data.
"""

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.parse
from typing import Any


def load_tools(tools_path: str | None) -> dict[str, Any]:
    """Load tool inventory from JSON file if provided."""
    if tools_path:
        try:
            with open(tools_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load tools file: {e}", file=sys.stderr)
    return {}


def web_search(query: str, num_results: int = 5) -> list[dict[str, str]]:
    """
    Search the web and return top results with URLs and titles.

    In agent context, replaced by the WebSearch MCP tool.
    """
    try:
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}&num={num_results}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        results = []
        for match in re.finditer(r'<a href="/url\?q=([^&"]+)', html):
            found_url = urllib.parse.unquote(match.group(1))
            if found_url.startswith("http") and "google.com" not in found_url:
                results.append({"url": found_url, "title": ""})
        return results[:num_results]
    except Exception as e:
        print(f"Warning: Search failed for '{query}': {e}", file=sys.stderr)
        return []


def classify_result_type(url: str, title: str) -> str:
    """
    Classify a search result into a page type based on URL and title patterns.

    Returns: guide, comparison, product, tool, docs, listicle, video,
             forum, news, other
    """
    url_lower = url.lower()
    title_lower = title.lower()
    combined = f"{url_lower} {title_lower}"

    # Video platforms
    if any(d in url_lower for d in ["youtube.com", "vimeo.com", "tiktok.com"]):
        return "video"

    # Forums / community
    if any(d in url_lower for d in ["reddit.com", "quora.com",
                                      "stackexchange.com", "stackoverflow.com"]):
        return "forum"

    # News
    if any(d in url_lower for d in ["news.", "/news/", "techcrunch.com",
                                      "theverge.com", "wired.com"]):
        return "news"

    # Product / pricing pages
    if any(p in combined for p in ["/pricing", "/plans", "/buy", "/product",
                                     "/free-trial", "pricing", "get started"]):
        return "product"

    # Documentation
    if any(p in url_lower for p in ["/docs/", "/documentation/", "/api/",
                                      "/reference/"]):
        return "docs"

    # Comparison posts
    if any(p in combined for p in [" vs ", " versus ", "comparison",
                                     "compare", "alternative"]):
        return "comparison"

    # Listicles
    if re.search(r'\b\d+\s+(best|top|ways|tips|tools|examples)', combined):
        return "listicle"

    # How-to guides
    if any(p in combined for p in ["how to", "guide", "tutorial",
                                     "step-by-step", "complete guide",
                                     "beginner", "learn"]):
        return "guide"

    return "other"


def infer_intent(result_types: list[str]) -> tuple[str, float]:
    """
    Infer search intent from the distribution of result types.

    Returns: (intent, confidence)
    """
    if not result_types:
        return "informational", 0.0

    # Map result types to intents
    intent_map = {
        "guide": "informational",
        "docs": "informational",
        "video": "informational",
        "forum": "informational",
        "comparison": "commercial",
        "listicle": "commercial",
        "product": "transactional",
        "news": "informational",
        "other": "informational",
    }

    intent_counts: dict[str, int] = {}
    for rt in result_types:
        intent = intent_map.get(rt, "informational")
        intent_counts[intent] = intent_counts.get(intent, 0) + 1

    total = len(result_types)
    dominant_intent = max(intent_counts, key=intent_counts.get)  # type: ignore[arg-type]
    confidence = round(intent_counts[dominant_intent] / total, 2)

    return dominant_intent, confidence


def recommend_content_type(intent: str, result_types: list[str]) -> str:
    """Recommend what content type to create based on intent and SERP."""
    if intent == "transactional":
        return "product/pricing page"
    if intent == "commercial":
        if "comparison" in result_types:
            return "comparison post"
        if "listicle" in result_types:
            return "listicle/roundup"
        return "comparison or review post"
    if intent == "informational":
        if "guide" in result_types:
            return "comprehensive guide"
        if "video" in result_types:
            return "tutorial (consider video + written)"
        return "how-to guide or explainer"
    return "comprehensive guide"


def classify_with_heuristics(keyword: str) -> tuple[str, float]:
    """
    Classify intent using keyword pattern heuristics (no search needed).

    Returns: (intent, confidence)
    """
    kw = keyword.lower()

    # Strong transactional signals
    if any(p in kw for p in ["buy", "pricing", "price", "free trial",
                               "sign up", "signup", "download", "coupon",
                               "discount", "order", "subscribe"]):
        return "transactional", 0.85

    # Strong commercial signals
    if any(p in kw for p in ["best", " vs ", "versus", "review", "comparison",
                               "compare", "alternative", "top rated",
                               "top 10", "which is better"]):
        return "commercial", 0.80

    # Strong navigational signals (brand-specific)
    if any(p in kw for p in ["login", "dashboard", "account", "support"]):
        return "navigational", 0.85

    # Strong informational signals
    if any(p in kw for p in ["how to", "what is", "what are", "why",
                               "guide", "tutorial", "learn", "meaning",
                               "definition", "example", "how does"]):
        return "informational", 0.80

    return "informational", 0.40  # Default with low confidence


def classify_keyword(keyword: str, use_search: bool = True) -> dict:
    """Classify a single keyword's search intent."""
    # Start with heuristic classification
    heuristic_intent, heuristic_conf = classify_with_heuristics(keyword)

    if not use_search:
        return {
            "keyword": keyword,
            "intent": heuristic_intent,
            "confidence": heuristic_conf,
            "method": "heuristic_only",
            "top_results": [],
            "recommended_content_type": recommend_content_type(
                heuristic_intent, []
            ),
        }

    # Search-based classification
    results = web_search(keyword, num_results=5)
    result_types = []
    top_results = []

    for result in results:
        rtype = classify_result_type(result["url"], result.get("title", ""))
        result_types.append(rtype)
        top_results.append({
            "url": result["url"],
            "type": rtype,
        })

    if result_types:
        search_intent, search_conf = infer_intent(result_types)

        # If heuristic and search agree, boost confidence
        if heuristic_intent == search_intent:
            final_intent = search_intent
            final_conf = min(round((heuristic_conf + search_conf) / 2 + 0.1, 2), 1.0)
        else:
            # Prefer search-based if confidence is high
            if search_conf > heuristic_conf:
                final_intent = search_intent
                final_conf = search_conf
            else:
                final_intent = heuristic_intent
                final_conf = heuristic_conf
        method = "heuristic_plus_serp"
    else:
        final_intent = heuristic_intent
        final_conf = heuristic_conf
        method = "heuristic_only"

    return {
        "keyword": keyword,
        "intent": final_intent,
        "confidence": final_conf,
        "method": method,
        "top_results": top_results,
        "recommended_content_type": recommend_content_type(
            final_intent, result_types
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Classify search intent for a list of keywords.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python classify-intent.py --keywords keywords.txt
    echo "best invoice automation" | python classify-intent.py --from-stdin
    python classify-intent.py --keyword "how to automate invoices"
        """,
    )
    parser.add_argument(
        "--keyword",
        help="Single keyword to classify",
    )
    parser.add_argument(
        "--keywords",
        help="Path to file with one keyword per line",
    )
    parser.add_argument(
        "--from-stdin",
        action="store_true",
        help="Read keywords from stdin (one per line)",
    )
    parser.add_argument(
        "--heuristic-only",
        action="store_true",
        help="Use only heuristic classification (no web search)",
    )
    parser.add_argument(
        "--tools",
        help="Path to tools.json inventory file",
    )
    args = parser.parse_args()

    # Load tool inventory
    tools = load_tools(args.tools)

    # Gather keywords
    keywords: list[str] = []
    if args.keyword:
        keywords = [args.keyword]
    elif args.keywords:
        try:
            with open(args.keywords, "r") as f:
                keywords = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File not found: {args.keywords}", file=sys.stderr)
            sys.exit(1)
    elif args.from_stdin:
        keywords = [line.strip() for line in sys.stdin if line.strip()]
    else:
        parser.error("Provide --keyword, --keywords, or --from-stdin")

    use_search = not args.heuristic_only

    # Classify each keyword
    classifications = []
    for kw in keywords:
        result = classify_keyword(kw, use_search=use_search)
        classifications.append(result)
        if use_search:
            time.sleep(0.5)  # Rate limiting between searches

    output = {
        "classifications": classifications,
        "total": len(classifications),
        "tools_used": {
            "websearch": use_search,
            "dataforseo": bool(tools.get("dataforseo")),
        },
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
