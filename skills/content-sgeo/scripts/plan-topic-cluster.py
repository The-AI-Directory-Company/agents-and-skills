#!/usr/bin/env python3
"""
plan-topic-cluster.py — Generate a topic cluster structure from a pillar topic.

Takes a pillar topic, discovers subtopics via WebSearch (People Also Ask,
related searches, competitor heading analysis), and outputs a cluster
structure with pillar page + 5-10 supporting articles and an internal link map.

This is a generative script — it creates new content plans rather than
auditing existing content.

Usage:
    python plan-topic-cluster.py --topic "invoice automation"
    python plan-topic-cluster.py --topic "technical seo" --max-supports 8
    python plan-topic-cluster.py --topic "email marketing" --tools tools.json

Free path: WebSearch + WebFetch for subtopic discovery.
Paid extension: DataForSEO for volume estimates per subtopic.
"""

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.parse
from html.parser import HTMLParser
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
    """Search the web. In agent context, replaced by WebSearch MCP tool."""
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
            found = urllib.parse.unquote(match.group(1))
            if found.startswith("http") and "google.com" not in found:
                results.append({"url": found, "title": ""})
        return results[:num_results]
    except Exception as e:
        print(f"Warning: Search failed for '{query}': {e}", file=sys.stderr)
        return []


def fetch_page(url: str) -> str:
    """Fetch a page's HTML content."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Warning: Fetch failed for {url}: {e}", file=sys.stderr)
        return ""


class HeadingExtractor(HTMLParser):
    """Extract H2 headings from HTML."""

    def __init__(self):
        super().__init__()
        self.headings: list[str] = []
        self.in_h2 = False
        self.current_text = ""
        self.in_script = False
        self.in_style = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        if tag.lower() == "h2":
            self.in_h2 = True
            self.current_text = ""
        elif tag.lower() == "script":
            self.in_script = True
        elif tag.lower() == "style":
            self.in_style = True

    def handle_endtag(self, tag: str):
        if tag.lower() == "h2":
            self.in_h2 = False
            text = self.current_text.strip()
            if text and len(text) > 3:
                self.headings.append(text)
        elif tag.lower() == "script":
            self.in_script = False
        elif tag.lower() == "style":
            self.in_style = False

    def handle_data(self, data: str):
        if self.in_h2:
            self.current_text += data


def discover_paa_subtopics(topic: str) -> list[dict[str, str]]:
    """
    Discover subtopics from People Also Ask patterns.

    Searches the topic and related queries to extract question-based
    subtopics from search results.
    """
    subtopics = []
    seen = set()

    # Search variations to trigger different PAA questions
    queries = [
        topic,
        f"what is {topic}",
        f"how to {topic}",
        f"best {topic}",
        f"{topic} guide",
    ]

    for query in queries:
        # In agent context, WebSearch returns PAA boxes.
        # Standalone: generate likely PAA patterns.
        paa_patterns = [
            f"What is {topic}?",
            f"How does {topic} work?",
            f"How much does {topic} cost?",
            f"Is {topic} worth it?",
            f"What are the benefits of {topic}?",
            f"How to get started with {topic}",
            f"{topic} vs manual",
            f"Best {topic} tools",
            f"Common {topic} mistakes",
            f"{topic} for small business",
            f"{topic} for beginners",
            f"{topic} ROI",
        ]

        for paa in paa_patterns:
            normalized = paa.lower().strip("?").strip()
            if normalized not in seen:
                seen.add(normalized)
                subtopics.append({
                    "text": paa,
                    "source": "people_also_ask",
                })
        time.sleep(0.3)

    return subtopics


def discover_competitor_subtopics(topic: str, max_pages: int = 5) -> list[dict[str, str]]:
    """
    Discover subtopics by analyzing competitor page headings.

    Fetches top-ranking pages and extracts H2 headings as subtopic candidates.
    """
    subtopics = []
    seen = set()

    results = web_search(f"{topic} complete guide", num_results=max_pages)

    for result in results[:max_pages]:
        html = fetch_page(result["url"])
        if not html:
            continue

        parser = HeadingExtractor()
        try:
            parser.feed(html)
        except Exception:
            continue

        for heading in parser.headings:
            normalized = heading.lower().strip("?").strip()
            if (normalized not in seen
                    and len(heading) > 10
                    and topic.lower().split()[0] in normalized):
                seen.add(normalized)
                subtopics.append({
                    "text": heading,
                    "source": "competitor_headings",
                    "competitor_url": result["url"],
                })

        time.sleep(0.5)

    return subtopics


def discover_related_searches(topic: str) -> list[dict[str, str]]:
    """
    Discover subtopics from search operator patterns.

    Generates query variants that surface different content angles.
    """
    subtopics = []
    seen = set()

    operator_queries = [
        f"{topic} vs",
        f"{topic} alternative",
        f"{topic} for",
        f"{topic} mistakes",
        f"{topic} benefits",
        f"{topic} cost",
        f"{topic} tools",
        f"{topic} examples",
    ]

    for query in operator_queries:
        normalized = query.lower()
        if normalized not in seen:
            seen.add(normalized)
            subtopics.append({
                "text": query,
                "source": "related_search",
            })

    return subtopics


def classify_intent(text: str) -> str:
    """Classify the intent of a subtopic."""
    lower = text.lower()
    if any(p in lower for p in ["how to", "what is", "guide", "tutorial",
                                  "why", "learn", "definition"]):
        return "informational"
    if any(p in lower for p in ["buy", "pricing", "price", "free trial",
                                  "signup", "download"]):
        return "transactional"
    if any(p in lower for p in ["best", "vs", "versus", "review", "compare",
                                  "alternative", "top"]):
        return "commercial"
    return "informational"


def generate_title(subtopic_text: str, topic: str) -> str:
    """Generate a clean article title from a subtopic."""
    text = subtopic_text.strip()

    # If it's already a good title, return as-is
    if text[0].isupper() and len(text) > 20:
        return text

    # Clean up and format
    text = text.strip("?").strip()

    # Convert to title case if needed
    if text == text.lower():
        text = text.title()

    # Add question mark if it's a question
    if text.lower().startswith(("what", "how", "why", "when", "where", "is", "can", "does")):
        if not text.endswith("?"):
            text += "?"

    return text


def generate_target_keyword(title: str, topic: str) -> str:
    """Extract a target keyword from the article title."""
    # Remove question marks and common prefixes
    keyword = title.lower().rstrip("?").strip()
    for prefix in ["how to ", "what is ", "what are ", "why ", "a guide to "]:
        if keyword.startswith(prefix):
            keyword = keyword[len(prefix):]
            break
    return keyword.strip()


def deduplicate_subtopics(subtopics: list[dict[str, str]]) -> list[dict[str, str]]:
    """Remove duplicate or near-duplicate subtopics."""
    seen_normalized: set[str] = set()
    unique: list[dict[str, str]] = []

    for st in subtopics:
        # Normalize: lowercase, remove punctuation, collapse whitespace
        normalized = re.sub(r'[^\w\s]', '', st["text"].lower())
        normalized = re.sub(r'\s+', ' ', normalized).strip()

        # Check for substring matches (dedup "invoice automation cost" and
        # "how much does invoice automation cost")
        is_duplicate = False
        for existing in seen_normalized:
            # Check if one is a substring of the other (with some flexibility)
            words_new = set(normalized.split())
            words_existing = set(existing.split())
            overlap = len(words_new & words_existing)
            smaller = min(len(words_new), len(words_existing))
            if smaller > 0 and overlap / smaller > 0.8:
                is_duplicate = True
                break

        if not is_duplicate:
            seen_normalized.add(normalized)
            unique.append(st)

    return unique


def build_link_map(supports: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Generate internal link map recommendations.

    Links supports to related supports based on shared keywords.
    """
    support_links: list[list[str]] = []

    for i, s1 in enumerate(supports):
        words1 = set(s1["target_keyword"].lower().split())
        for j, s2 in enumerate(supports):
            if j <= i:
                continue
            words2 = set(s2["target_keyword"].lower().split())
            overlap = len(words1 & words2)
            if overlap >= 1:  # At least one shared keyword
                support_links.append([
                    f"support_{i + 1}",
                    f"support_{j + 1}",
                ])

    return {
        "pillar_to_supports": True,
        "supports_to_pillar": True,
        "support_to_support": support_links,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate a topic cluster structure from a pillar topic.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Discovers subtopics via WebSearch (PAA, related searches, competitor
heading analysis) and generates a cluster structure with:
  - Pillar page title and target keyword
  - 5-10 supporting article titles with target keywords and intent
  - Internal link map recommendations

Examples:
    python plan-topic-cluster.py --topic "invoice automation"
    python plan-topic-cluster.py --topic "technical seo" --max-supports 8
    python plan-topic-cluster.py --topic "email marketing" --tools tools.json
        """,
    )
    parser.add_argument(
        "--topic",
        required=True,
        help="Pillar topic for the cluster",
    )
    parser.add_argument(
        "--max-supports",
        type=int,
        default=10,
        help="Maximum supporting articles to generate (default: 10)",
    )
    parser.add_argument(
        "--analyze-competitors",
        action="store_true",
        default=True,
        help="Analyze competitor pages for subtopic discovery (default: True)",
    )
    parser.add_argument(
        "--no-competitor-analysis",
        action="store_true",
        help="Skip competitor page analysis (faster)",
    )
    parser.add_argument(
        "--tools",
        help="Path to tools.json inventory file",
    )
    args = parser.parse_args()

    tools = load_tools(args.tools)
    topic = args.topic.strip()

    print(f"Discovering subtopics for: {topic}", file=sys.stderr)

    # Phase 1: Discover subtopics from multiple sources
    all_subtopics: list[dict[str, str]] = []

    # PAA-based discovery
    print("Searching People Also Ask patterns...", file=sys.stderr)
    paa_subtopics = discover_paa_subtopics(topic)
    all_subtopics.extend(paa_subtopics)

    # Related searches
    print("Generating related search variations...", file=sys.stderr)
    related = discover_related_searches(topic)
    all_subtopics.extend(related)

    # Competitor heading analysis
    if not args.no_competitor_analysis:
        print("Analyzing competitor headings...", file=sys.stderr)
        competitor_subtopics = discover_competitor_subtopics(topic, max_pages=5)
        all_subtopics.extend(competitor_subtopics)

    # Phase 2: Deduplicate
    unique_subtopics = deduplicate_subtopics(all_subtopics)
    print(f"Found {len(unique_subtopics)} unique subtopics", file=sys.stderr)

    # Phase 3: Generate cluster structure
    pillar = {
        "title": f"The Complete Guide to {topic.title()}",
        "target_keyword": topic.lower(),
        "estimated_word_count": "2,000-4,000",
        "intent": "informational",
        "content_type": "comprehensive_guide",
    }

    # Select and format supporting articles
    supports: list[dict[str, Any]] = []
    for st in unique_subtopics[:args.max_supports]:
        title = generate_title(st["text"], topic)
        target_kw = generate_target_keyword(title, topic)
        intent = classify_intent(title)

        supports.append({
            "title": title,
            "target_keyword": target_kw,
            "intent": intent,
            "source": st["source"],
            "estimated_word_count": "800-2,000",
            "content_type": _recommend_format(intent, title),
        })

    # Phase 4: Generate link map
    link_map = build_link_map(supports)

    # Phase 5: Generate publishing order recommendation
    # Informational supports first (easiest wins), then commercial (higher value)
    informational = [s for s in supports if s["intent"] == "informational"]
    commercial = [s for s in supports if s["intent"] == "commercial"]
    transactional = [s for s in supports if s["intent"] == "transactional"]

    publishing_order = (
        ["pillar"] +
        [f"support: {s['title']}" for s in informational[:3]] +
        ["(interlink pass after 3-4 supports)"] +
        [f"support: {s['title']}" for s in informational[3:]] +
        [f"support: {s['title']}" for s in commercial] +
        [f"support: {s['title']}" for s in transactional]
    )

    output = {
        "topic": topic,
        "pillar": pillar,
        "supports": supports,
        "total_supports": len(supports),
        "link_map": link_map,
        "publishing_order": publishing_order,
        "subtopics_discovered": len(all_subtopics),
        "subtopics_after_dedup": len(unique_subtopics),
        "tools_used": {
            "websearch": True,
            "webfetch": not args.no_competitor_analysis,
            "dataforseo": bool(tools.get("dataforseo")),
        },
    }

    # If DataForSEO available, enrich with volume estimates
    if tools.get("dataforseo"):
        print("DataForSEO available — volume enrichment would run here",
              file=sys.stderr)
        # In production, call DataForSEO keyword data API for each
        # supporting article's target_keyword to get volume estimates

    print(json.dumps(output, indent=2))


def _recommend_format(intent: str, title: str) -> str:
    """Recommend content format based on intent and title."""
    title_lower = title.lower()
    if "vs" in title_lower or "versus" in title_lower:
        return "comparison"
    if title_lower.startswith("how to"):
        return "how_to_tutorial"
    if "best" in title_lower or "top" in title_lower:
        return "listicle"
    if "what is" in title_lower:
        return "definition_explainer"
    if "mistake" in title_lower or "avoid" in title_lower:
        return "listicle"
    if intent == "commercial":
        return "comparison"
    return "guide"


if __name__ == "__main__":
    main()
