#!/usr/bin/env python3
"""
analyze-serp-competitors.py — Analyze top SERP results for a keyword.

Fetches top 10 results, extracts title patterns, word counts, heading
structures, schema types, and content formats. Identifies gaps between
competitors and your content.

Usage:
    python analyze-serp-competitors.py --keyword "invoice automation"
    python analyze-serp-competitors.py --keyword "seo guide" --tools tools.json

Free path: WebSearch + WebFetch for result analysis.
Paid extension: DataForSEO + Ahrefs for backlink counts per result.
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
        print(f"Warning: Search failed: {e}", file=sys.stderr)
        return []


def fetch_page(url: str) -> str:
    """Fetch a page's HTML. In agent context, replaced by WebFetch MCP tool."""
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
    """Extract headings and text from HTML."""

    def __init__(self):
        super().__init__()
        self.headings: list[dict[str, Any]] = []
        self.current_heading: dict[str, Any] | None = None
        self.title: str = ""
        self.in_title = False
        self.in_script = False
        self.in_style = False
        self.text_parts: list[str] = []
        self.json_ld_blocks: list[str] = []
        self.in_json_ld = False
        self.json_ld_buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        tag_lower = tag.lower()
        if tag_lower == "title":
            self.in_title = True
        elif tag_lower == "script":
            attr_dict = dict(attrs)
            if attr_dict.get("type") == "application/ld+json":
                self.in_json_ld = True
                self.json_ld_buffer = []
            else:
                self.in_script = True
        elif tag_lower == "style":
            self.in_style = True
        elif tag_lower in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(tag_lower[1])
            self.current_heading = {"level": level, "text": ""}

    def handle_endtag(self, tag: str):
        tag_lower = tag.lower()
        if tag_lower == "title":
            self.in_title = False
        elif tag_lower == "script":
            if self.in_json_ld:
                self.json_ld_blocks.append("".join(self.json_ld_buffer))
                self.in_json_ld = False
            self.in_script = False
        elif tag_lower == "style":
            self.in_style = False
        elif tag_lower in ("h1", "h2", "h3", "h4", "h5", "h6"):
            if self.current_heading:
                self.headings.append(self.current_heading)
                self.current_heading = None

    def handle_data(self, data: str):
        if self.in_json_ld:
            self.json_ld_buffer.append(data)
        elif self.in_title:
            self.title += data
        elif self.current_heading is not None:
            self.current_heading["text"] += data
        elif not self.in_script and not self.in_style:
            self.text_parts.append(data)


def analyze_page(url: str, html: str) -> dict[str, Any]:
    """Analyze a page's content structure."""
    parser = HeadingExtractor()
    try:
        parser.feed(html)
    except Exception:
        pass

    # Word count from visible text
    full_text = " ".join(parser.text_parts)
    word_count = len(full_text.split())

    # Heading counts
    h1_count = sum(1 for h in parser.headings if h["level"] == 1)
    h2_count = sum(1 for h in parser.headings if h["level"] == 2)
    h3_count = sum(1 for h in parser.headings if h["level"] == 3)

    # Question-format H2s
    question_h2s = sum(
        1 for h in parser.headings
        if h["level"] == 2 and re.match(
            r'^(what|how|why|when|where|is|can|does|will|should|which)',
            h["text"].strip().lower()
        )
    )

    # Schema types
    schema_types = []
    for block in parser.json_ld_blocks:
        try:
            data = json.loads(block)
            if isinstance(data, dict):
                stype = data.get("@type", "")
                if stype:
                    schema_types.append(stype)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        stype = item.get("@type", "")
                        if stype:
                            schema_types.append(stype)
        except json.JSONDecodeError:
            pass

    # Detect content format
    content_format = detect_format(parser.headings, word_count, url, parser.title)

    # Detect dates
    date_patterns = re.findall(
        r'(?:20\d{2}[-/]\d{1,2}[-/]\d{1,2})|'
        r'(?:(?:January|February|March|April|May|June|July|August|'
        r'September|October|November|December)\s+\d{1,2},?\s+20\d{2})',
        html
    )
    last_updated = date_patterns[0] if date_patterns else None

    return {
        "url": url,
        "title": parser.title.strip(),
        "title_length": len(parser.title.strip()),
        "word_count": word_count,
        "h1_count": h1_count,
        "h2_count": h2_count,
        "h3_count": h3_count,
        "question_h2_ratio": round(question_h2s / h2_count, 2) if h2_count > 0 else 0,
        "schema_types": list(set(schema_types)),
        "format": content_format,
        "last_updated": last_updated,
    }


def detect_format(headings: list[dict], word_count: int,
                  url: str, title: str) -> str:
    """Detect the content format of a page."""
    combined = f"{url.lower()} {title.lower()}"

    # Check for numbered lists in title
    if re.search(r'\b\d+\s+(best|top|ways|tips|tools)', combined):
        return "listicle"

    # Check for comparison
    if any(p in combined for p in [" vs ", "versus", "comparison", "compare"]):
        return "comparison"

    # Check for FAQ
    question_headings = sum(1 for h in headings if "?" in h.get("text", ""))
    if question_headings >= 5:
        return "faq"

    # Check for glossary/definition
    if any(p in combined for p in ["glossary", "definition", "what is"]):
        return "definition"

    # Check for guide based on length and heading count
    if word_count > 2000 and len(headings) > 8:
        return "comprehensive_guide"

    if word_count > 1000:
        return "guide"

    return "other"


def main():
    parser = argparse.ArgumentParser(
        description="Analyze top SERP results for a keyword.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python analyze-serp-competitors.py --keyword "invoice automation"
    python analyze-serp-competitors.py --keyword "seo tools" --top 5
        """,
    )
    parser.add_argument(
        "--keyword",
        required=True,
        help="Target keyword to analyze SERP for",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top results to analyze (default: 10)",
    )
    parser.add_argument(
        "--tools",
        help="Path to tools.json inventory file",
    )
    args = parser.parse_args()

    tools = load_tools(args.tools)

    # Search for the keyword
    print(f"Searching for: {args.keyword}", file=sys.stderr)
    search_results = web_search(args.keyword, num_results=args.top)

    if not search_results:
        output = {
            "keyword": args.keyword,
            "error": "No search results found",
            "results": [],
        }
        print(json.dumps(output, indent=2))
        sys.exit(1)

    # Analyze each result
    analyzed = []
    for i, result in enumerate(search_results):
        print(f"Analyzing result {i + 1}/{len(search_results)}: {result['url']}",
              file=sys.stderr)
        html = fetch_page(result["url"])
        if html:
            analysis = analyze_page(result["url"], html)
            analysis["position"] = i + 1
            analyzed.append(analysis)
        time.sleep(0.5)  # Rate limiting

    # Calculate aggregates
    if analyzed:
        word_counts = [a["word_count"] for a in analyzed if a["word_count"] > 0]
        h2_counts = [a["h2_count"] for a in analyzed]
        avg_word_count = round(sum(word_counts) / len(word_counts)) if word_counts else 0
        avg_h2_count = round(sum(h2_counts) / len(h2_counts)) if h2_counts else 0

        # Dominant format
        formats = [a["format"] for a in analyzed]
        format_counts: dict[str, int] = {}
        for fmt in formats:
            format_counts[fmt] = format_counts.get(fmt, 0) + 1
        dominant_format = max(format_counts, key=format_counts.get) if format_counts else "unknown"  # type: ignore[arg-type]

        # Common schema types
        all_schemas: dict[str, int] = {}
        for a in analyzed:
            for st in a["schema_types"]:
                all_schemas[st] = all_schemas.get(st, 0) + 1
        common_schemas = [s for s, c in all_schemas.items() if c >= 2]

        # Identify gaps
        gaps = []
        avg_question_ratio = sum(a["question_h2_ratio"] for a in analyzed) / len(analyzed)
        if avg_question_ratio > 0.3:
            gaps.append("Top results use question-format H2s — match this pattern")
        if "FAQPage" in all_schemas:
            gaps.append("Some competitors use FAQ Schema — consider adding it")
        if avg_word_count > 2500:
            gaps.append(f"Average word count is {avg_word_count} — content needs to be comprehensive")
        if common_schemas and "Article" in common_schemas:
            gaps.append("Competitors use Article Schema — ensure you have it")
    else:
        avg_word_count = 0
        avg_h2_count = 0
        dominant_format = "unknown"
        common_schemas = []
        gaps = []

    output = {
        "keyword": args.keyword,
        "results_analyzed": len(analyzed),
        "results": analyzed,
        "averages": {
            "word_count": avg_word_count,
            "h2_count": avg_h2_count,
        },
        "dominant_format": dominant_format,
        "common_schemas": common_schemas,
        "gaps": gaps,
        "tools_used": {
            "websearch": True,
            "webfetch": True,
            "dataforseo": bool(tools.get("dataforseo")),
            "ahrefs": bool(tools.get("ahrefs")),
        },
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
