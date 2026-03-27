#!/usr/bin/env python3
"""
audit-content-freshness.py — Audit content freshness across a site.

Takes a sitemap URL or list of URLs, extracts dates, calculates age,
and flags pages by freshness tier. Identifies position 4-15 refresh
candidates for highest-ROI updates.

Usage:
    python audit-content-freshness.py --sitemap https://example.com/sitemap.xml
    python audit-content-freshness.py --urls urls.txt
    python audit-content-freshness.py --sitemap https://example.com/sitemap.xml --tools tools.json

Free path: WebFetch + WebSearch for date extraction and position sampling.
Paid extension: DataForSEO for bulk ranking position data.
"""

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from typing import Any
from xml.etree import ElementTree


def load_tools(tools_path: str | None) -> dict[str, Any]:
    """Load tool inventory from JSON file if provided."""
    if tools_path:
        try:
            with open(tools_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load tools file: {e}", file=sys.stderr)
    return {}


def fetch_url(url: str) -> str:
    """Fetch a URL's content."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Warning: Failed to fetch {url}: {e}", file=sys.stderr)
        return ""


def web_search(query: str) -> list[dict[str, str]]:
    """Search the web. In agent context, replaced by WebSearch MCP tool."""
    try:
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}&num=10"
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
                results.append({"url": found})
        return results[:10]
    except Exception:
        return []


def parse_sitemap(xml_content: str) -> list[dict[str, Any]]:
    """Parse XML sitemap and extract URLs with lastmod dates."""
    urls = []
    try:
        # Handle namespace
        xml_content = re.sub(r'xmlns="[^"]*"', '', xml_content)
        root = ElementTree.fromstring(xml_content)

        # Check if this is a sitemap index
        if root.tag == "sitemapindex" or root.find(".//sitemap") is not None:
            # Sitemap index — extract child sitemap URLs
            for sitemap in root.findall(".//sitemap"):
                loc = sitemap.find("loc")
                if loc is not None and loc.text:
                    child_xml = fetch_url(loc.text.strip())
                    if child_xml:
                        urls.extend(parse_sitemap(child_xml))
                        time.sleep(0.3)
        else:
            # Regular sitemap
            for url_elem in root.findall(".//url"):
                loc = url_elem.find("loc")
                lastmod = url_elem.find("lastmod")
                if loc is not None and loc.text:
                    entry: dict[str, Any] = {"url": loc.text.strip()}
                    if lastmod is not None and lastmod.text:
                        entry["sitemap_lastmod"] = lastmod.text.strip()
                    urls.append(entry)

    except ElementTree.ParseError as e:
        print(f"Warning: Failed to parse sitemap XML: {e}", file=sys.stderr)

    return urls


def extract_dates_from_page(html: str) -> dict[str, Any]:
    """Extract publication and modification dates from a page."""
    dates: dict[str, Any] = {
        "schema_published": None,
        "schema_modified": None,
        "visible_date": None,
        "visible_date_text": None,
    }

    # Check JSON-LD
    json_ld_pattern = r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>'
    for match in re.finditer(json_ld_pattern, html, re.DOTALL | re.IGNORECASE):
        try:
            data = json.loads(match.group(1))
            if isinstance(data, dict):
                if "datePublished" in data:
                    dates["schema_published"] = data["datePublished"]
                if "dateModified" in data:
                    dates["schema_modified"] = data["dateModified"]
        except json.JSONDecodeError:
            pass

    # Check for visible dates
    visible_patterns = [
        (r'(?:last\s+)?(?:updated|modified)\s*:?\s*(?:on\s+)?'
         r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})', "updated"),
        (r'(?:published|posted)\s*:?\s*(?:on\s+)?'
         r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})', "published"),
        (r'(?:last\s+)?(?:updated|modified)\s*:?\s*(?:on\s+)?'
         r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})',
         "updated"),
        (r'(?:published|posted)\s*:?\s*(?:on\s+)?'
         r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})',
         "published"),
    ]

    for pattern, dtype in visible_patterns:
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            dates["visible_date_text"] = match.group(0).strip()
            dates["visible_date"] = match.group(1).strip()
            break

    return dates


def parse_date(date_str: str) -> datetime | None:
    """Parse a date string into a datetime object."""
    if not date_str:
        return None

    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%B %d, %Y",
        "%B %d %Y",
        "%b %d, %Y",
        "%b %d %Y",
    ]

    # Clean the string
    date_str = date_str.strip()
    # Remove timezone offset for simpler parsing
    date_str = re.sub(r'[+-]\d{2}:\d{2}$', '', date_str)

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    return None


def classify_freshness(days_ago: int) -> str:
    """Classify content freshness by age in days."""
    if days_ago < 180:
        return "fresh"
    elif days_ago < 365:
        return "aging"
    elif days_ago < 548:  # 18 months
        return "stale"
    else:
        return "needs_rewrite"


def recommend_action(freshness: str, estimated_position: int | None) -> str:
    """Recommend refresh action based on freshness and position."""
    if estimated_position and 4 <= estimated_position <= 15:
        return "upgrade (high priority — position 4-15 quick win)"
    if freshness == "needs_rewrite":
        return "rewrite"
    if freshness == "stale":
        return "upgrade"
    if freshness == "aging":
        return "upgrade"
    if freshness == "fresh":
        return "optimization (if needed)"
    return "review"


def estimate_position(url: str) -> int | None:
    """
    Estimate ranking position via site: search.

    This is a rough proxy. For accurate positions, use GSC or DataForSEO.
    """
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.strip("/")
    if not path:
        return None

    # Extract likely keyword from URL path
    slug = path.split("/")[-1]
    keyword = slug.replace("-", " ").replace("_", " ")

    if len(keyword) < 3:
        return None

    results = web_search(keyword)
    domain = parsed.netloc.lower()

    for i, result in enumerate(results):
        if domain in result.get("url", "").lower():
            return i + 1

    return None


def main():
    parser = argparse.ArgumentParser(
        description="Audit content freshness across a site.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Freshness tiers:
  fresh: <6 months since last update
  aging: 6-12 months
  stale: 12-18 months
  needs_rewrite: >18 months

Examples:
    python audit-content-freshness.py --sitemap https://example.com/sitemap.xml
    python audit-content-freshness.py --urls urls.txt
    python audit-content-freshness.py --sitemap https://example.com/sitemap.xml --sample 10
        """,
    )
    parser.add_argument(
        "--sitemap",
        help="URL of XML sitemap to audit",
    )
    parser.add_argument(
        "--urls",
        help="Path to file with URLs (one per line)",
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=20,
        help="Max pages to fully analyze (default: 20)",
    )
    parser.add_argument(
        "--check-positions",
        action="store_true",
        help="Estimate ranking positions via WebSearch (slower, adds rate limiting)",
    )
    parser.add_argument(
        "--tools",
        help="Path to tools.json inventory file",
    )
    args = parser.parse_args()

    if not args.sitemap and not args.urls:
        parser.error("Provide --sitemap or --urls")

    tools = load_tools(args.tools)

    # Gather URLs
    url_entries: list[dict[str, Any]] = []

    if args.sitemap:
        print(f"Fetching sitemap: {args.sitemap}", file=sys.stderr)
        xml_content = fetch_url(args.sitemap)
        if xml_content:
            url_entries = parse_sitemap(xml_content)
            print(f"Found {len(url_entries)} URLs in sitemap", file=sys.stderr)
        else:
            print("Error: Could not fetch sitemap", file=sys.stderr)
            sys.exit(1)
    elif args.urls:
        try:
            with open(args.urls, "r") as f:
                for line in f:
                    url = line.strip()
                    if url and url.startswith("http"):
                        url_entries.append({"url": url})
        except FileNotFoundError:
            print(f"Error: File not found: {args.urls}", file=sys.stderr)
            sys.exit(1)

    # Process pages (sample if too many)
    now = datetime.now()
    pages: list[dict[str, Any]] = []
    sample_entries = url_entries[:args.sample]

    for i, entry in enumerate(sample_entries):
        url = entry["url"]
        print(f"Analyzing {i + 1}/{len(sample_entries)}: {url}", file=sys.stderr)

        page_data: dict[str, Any] = {"url": url}

        # Get sitemap lastmod if available
        sitemap_lastmod = entry.get("sitemap_lastmod")
        if sitemap_lastmod:
            page_data["sitemap_lastmod"] = sitemap_lastmod

        # Fetch page and extract dates
        html = fetch_url(url)
        if html:
            dates = extract_dates_from_page(html)
            page_data.update(dates)

        # Determine the most recent date
        best_date = None
        date_candidates = [
            page_data.get("schema_modified"),
            page_data.get("schema_published"),
            page_data.get("visible_date"),
            page_data.get("sitemap_lastmod"),
        ]

        for candidate in date_candidates:
            if candidate:
                parsed = parse_date(str(candidate))
                if parsed:
                    if best_date is None or parsed > best_date:
                        best_date = parsed

        if best_date:
            days_ago = (now - best_date).days
            page_data["last_updated"] = best_date.strftime("%Y-%m-%d")
            page_data["days_ago"] = max(days_ago, 0)
            page_data["freshness"] = classify_freshness(days_ago)
        else:
            page_data["last_updated"] = None
            page_data["days_ago"] = None
            page_data["freshness"] = "unknown"

        # Estimate position if requested
        estimated_position = None
        if args.check_positions:
            estimated_position = estimate_position(url)
            page_data["estimated_position"] = estimated_position
            time.sleep(0.5)  # Rate limiting

        # Determine priority and action
        if page_data["freshness"] == "unknown":
            page_data["refresh_priority"] = "medium"
            page_data["recommended_action"] = "review (no dates found)"
        else:
            freshness = page_data["freshness"]
            page_data["recommended_action"] = recommend_action(
                freshness, estimated_position
            )
            if estimated_position and 4 <= estimated_position <= 15:
                page_data["refresh_priority"] = "high"
            elif freshness in ("stale", "needs_rewrite"):
                page_data["refresh_priority"] = "high"
            elif freshness == "aging":
                page_data["refresh_priority"] = "medium"
            else:
                page_data["refresh_priority"] = "low"

        pages.append(page_data)
        time.sleep(0.3)  # Rate limiting

    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    pages.sort(key=lambda p: priority_order.get(p.get("refresh_priority", "low"), 3))

    # Summary
    summary = {
        "total_in_sitemap": len(url_entries),
        "total_analyzed": len(pages),
        "fresh": sum(1 for p in pages if p.get("freshness") == "fresh"),
        "aging": sum(1 for p in pages if p.get("freshness") == "aging"),
        "stale": sum(1 for p in pages if p.get("freshness") == "stale"),
        "needs_rewrite": sum(1 for p in pages if p.get("freshness") == "needs_rewrite"),
        "unknown": sum(1 for p in pages if p.get("freshness") == "unknown"),
    }

    output = {
        "pages": pages,
        "summary": summary,
        "tools_used": {
            "webfetch": True,
            "websearch": args.check_positions,
            "dataforseo": bool(tools.get("dataforseo")),
        },
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
