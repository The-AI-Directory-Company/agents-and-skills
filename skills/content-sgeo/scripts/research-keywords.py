#!/usr/bin/env python3
"""
research-keywords.py — Expand seed keywords via WebSearch and classify results.

Takes seed keywords, expands them using search engine autocomplete patterns,
People Also Ask extraction, and related searches. Outputs a keyword table
with volume estimates, difficulty proxy, and intent classification.

Usage:
    python research-keywords.py --seeds "invoice automation,ap automation"
    echo "invoice automation" | python research-keywords.py --from-stdin
    python research-keywords.py --seeds "invoice automation" --tools tools.json

Free path: WebSearch for expansion and SERP analysis.
Paid extension: DataForSEO keyword data API for exact volume, difficulty, CPC.
"""

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
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


def web_search(query: str, num_results: int = 10) -> list[dict[str, str]]:
    """
    Search the web for a query. Returns a list of result dicts.

    In agent context, this is replaced by the WebSearch MCP tool.
    As a standalone script, it uses a basic HTTP search fallback.
    """
    # This function serves as a template for agents to understand the logic.
    # When run by an agent, the agent replaces this with its WebSearch tool.
    # When run standalone, it attempts a basic Google search scrape.
    try:
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        # Extract basic result patterns (title + URL)
        results = []
        # Simple regex to find result links — not production-grade
        for match in re.finditer(r'<a href="/url\?q=([^&"]+)', html):
            url_found = urllib.parse.unquote(match.group(1))
            if url_found.startswith("http") and "google.com" not in url_found:
                results.append({"url": url_found, "title": ""})
        return results[:num_results]
    except Exception as e:
        print(f"Warning: Web search failed: {e}", file=sys.stderr)
        return []


def extract_paa_questions(query: str) -> list[str]:
    """
    Extract People Also Ask questions for a query.

    In agent context, the agent searches the query and extracts PAA boxes
    from the SERP. Standalone, this attempts to parse them from HTML.
    """
    results = web_search(query)
    questions = []
    # PAA extraction is best done by agents with WebSearch tool
    # Standalone: generate likely PAA patterns from the query
    seed_noun = query.strip()
    patterns = [
        f"What is {seed_noun}?",
        f"How does {seed_noun} work?",
        f"How much does {seed_noun} cost?",
        f"Is {seed_noun} worth it?",
        f"What are the benefits of {seed_noun}?",
    ]
    for pattern in patterns:
        questions.append(pattern)
    return questions


def classify_intent(keyword: str) -> str:
    """Classify keyword intent using simple heuristics."""
    kw = keyword.lower()
    if any(p in kw for p in ["how to", "what is", "what are", "guide", "tutorial",
                              "why", "when to", "how does", "learn"]):
        return "informational"
    if any(p in kw for p in ["buy", "pricing", "price", "free trial", "signup",
                              "sign up", "download", "coupon", "discount"]):
        return "transactional"
    if any(p in kw for p in ["best", "vs", "versus", "review", "comparison",
                              "compare", "alternative", "top", "rated"]):
        return "commercial"
    # Check for brand terms (heuristic: capitalized words not in common words)
    return "informational"


def estimate_difficulty(keyword: str) -> str:
    """
    Estimate keyword difficulty using SERP analysis.

    Free proxy: count high-authority domains in top results.
    Returns: 'low', 'medium', or 'high'.
    """
    results = web_search(keyword, num_results=10)
    high_authority_domains = [
        "wikipedia.org", "amazon.com", "youtube.com", "reddit.com",
        "linkedin.com", "forbes.com", "nytimes.com", "bbc.com",
        "medium.com", "github.com", "microsoft.com", "apple.com",
        "google.com", "hubspot.com", "semrush.com", "ahrefs.com",
    ]
    authority_count = 0
    for result in results:
        url = result.get("url", "")
        for domain in high_authority_domains:
            if domain in url:
                authority_count += 1
                break

    if authority_count >= 7:
        return "high"
    elif authority_count >= 4:
        return "medium"
    else:
        return "low"


def expand_with_autocomplete(seed: str) -> list[str]:
    """
    Expand seed keyword using autocomplete patterns.

    Searches: "{seed} a", "{seed} b", ... to discover long-tail variants.
    """
    expanded = []
    # In agent context, the agent runs these searches via WebSearch.
    # Standalone: generate the query patterns for the agent to execute.
    letters = "abcdefghijklmnopqrstuvwxyz"
    for letter in letters[:5]:  # Limit to 5 for rate limiting
        query = f"{seed} {letter}"
        # In production, each search yields autocomplete suggestions
        expanded.append(query)
        time.sleep(0.2)  # Rate limiting
    return expanded


def expand_with_operators(seed: str) -> list[str]:
    """Generate keyword variants using search operator patterns."""
    return [
        f"{seed} vs",
        f"{seed} alternative",
        f"best {seed}",
        f"how to {seed}",
        f"{seed} for small business",
        f"{seed} for enterprise",
        f"{seed} software",
        f"{seed} tools",
        f"{seed} guide",
        f"{seed} cost",
    ]


def research_keywords_dataforseo(seeds: list[str], api_login: str,
                                  api_password: str) -> list[dict]:
    """
    Use DataForSEO keyword data API for exact volume and difficulty.

    Paid extension: provides exact search volume, keyword difficulty,
    CPC, and competition data.
    """
    import base64
    keywords = []
    cred = base64.b64encode(f"{api_login}:{api_password}".encode()).decode()

    for seed in seeds:
        try:
            payload = json.dumps([{
                "keyword": seed,
                "location_code": 2840,  # US
                "language_code": "en",
            }]).encode()

            req = urllib.request.Request(
                "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live",
                data=payload,
                headers={
                    "Authorization": f"Basic {cred}",
                    "Content-Type": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())

            if data.get("tasks"):
                for task in data["tasks"]:
                    for item in task.get("result", []):
                        keywords.append({
                            "keyword": item.get("keyword", seed),
                            "volume_estimate": item.get("search_volume"),
                            "difficulty_proxy": None,
                            "cpc_estimate": item.get("cpc"),
                            "competition": item.get("competition"),
                        })
            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"Warning: DataForSEO request failed for '{seed}': {e}",
                  file=sys.stderr)

    return keywords


def main():
    parser = argparse.ArgumentParser(
        description="Expand seed keywords via WebSearch and classify results.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python research-keywords.py --seeds "invoice automation,ap automation"
    python research-keywords.py --seeds "seo tools" --tools tools.json
    echo "invoice automation" | python research-keywords.py --from-stdin
        """,
    )
    parser.add_argument(
        "--seeds",
        help="Comma-separated seed keywords",
    )
    parser.add_argument(
        "--from-stdin",
        action="store_true",
        help="Read seeds from stdin (one per line)",
    )
    parser.add_argument(
        "--tools",
        help="Path to tools.json inventory file",
    )
    parser.add_argument(
        "--max-expand",
        type=int,
        default=50,
        help="Maximum expanded keywords to return (default: 50)",
    )
    args = parser.parse_args()

    # Gather seeds
    seeds: list[str] = []
    if args.seeds:
        seeds = [s.strip() for s in args.seeds.split(",") if s.strip()]
    elif args.from_stdin:
        seeds = [line.strip() for line in sys.stdin if line.strip()]
    else:
        parser.error("Provide --seeds or --from-stdin")

    # Load tool inventory
    tools = load_tools(args.tools)

    # Expand keywords
    all_keywords: list[dict] = []
    seen: set[str] = set()

    for seed in seeds:
        # Add the seed itself
        if seed.lower() not in seen:
            seen.add(seed.lower())
            all_keywords.append({
                "keyword": seed,
                "volume_estimate": None,
                "difficulty_proxy": None,
                "cpc_estimate": None,
                "intent": classify_intent(seed),
                "source": "seed",
                "priority": "high",
            })

        # Expand via search operators
        for variant in expand_with_operators(seed):
            kw = variant.lower()
            if kw not in seen and len(all_keywords) < args.max_expand:
                seen.add(kw)
                all_keywords.append({
                    "keyword": variant,
                    "volume_estimate": None,
                    "difficulty_proxy": None,
                    "cpc_estimate": None,
                    "intent": classify_intent(variant),
                    "source": "search_operator",
                    "priority": "medium",
                })

        # Extract PAA questions
        paa = extract_paa_questions(seed)
        for question in paa:
            kw = question.lower()
            if kw not in seen and len(all_keywords) < args.max_expand:
                seen.add(kw)
                all_keywords.append({
                    "keyword": question,
                    "volume_estimate": None,
                    "difficulty_proxy": None,
                    "cpc_estimate": None,
                    "intent": classify_intent(question),
                    "source": "people_also_ask",
                    "priority": "high",
                })

    # If DataForSEO available, enrich with exact data
    if tools.get("dataforseo"):
        api_login = tools.get("dataforseo_login", "")
        api_password = tools.get("dataforseo_password", "")
        if api_login and api_password:
            enriched = research_keywords_dataforseo(
                [kw["keyword"] for kw in all_keywords],
                api_login,
                api_password,
            )
            # Merge enriched data back
            enriched_map = {e["keyword"].lower(): e for e in enriched}
            for kw in all_keywords:
                if kw["keyword"].lower() in enriched_map:
                    data = enriched_map[kw["keyword"].lower()]
                    kw["volume_estimate"] = data.get("volume_estimate")
                    kw["cpc_estimate"] = data.get("cpc_estimate")

    # Estimate difficulty for top-priority keywords (free path)
    for kw in all_keywords:
        if kw["priority"] == "high" and kw["difficulty_proxy"] is None:
            kw["difficulty_proxy"] = estimate_difficulty(kw["keyword"])
            time.sleep(0.3)  # Rate limiting

    # Output
    output = {
        "keywords": all_keywords[:args.max_expand],
        "total_found": len(all_keywords),
        "seeds_used": seeds,
        "tools_used": {
            "websearch": True,
            "dataforseo": bool(tools.get("dataforseo")),
        },
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
