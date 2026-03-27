#!/usr/bin/env python3
"""Check freshness signals on a page.

Searches for visible dates, extracts datePublished/dateModified from
JSON-LD schema, checks for author bylines, and scores overall freshness.

Usage:
    python check-freshness.py --url https://example.com/page
    python check-freshness.py --url https://example.com/page --tools tools.json

Output: JSON with visible dates, schema dates, author info, and freshness score.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import Optional


# ---------------------------------------------------------------------------
# HTML Parser
# ---------------------------------------------------------------------------

class FreshnessExtractor(HTMLParser):
    """Extract date elements, author info, and JSON-LD from HTML."""

    def __init__(self):
        super().__init__()
        # JSON-LD
        self.jsonld_blocks: list[str] = []
        self._in_jsonld = False
        self._jsonld_buf = ""

        # Dates from <time> elements
        self.time_elements: list[dict] = []

        # Text accumulation for date/author search
        self._text_parts: list[str] = []
        self._skip_depth = 0

        # Author links
        self.author_links: list[dict] = []
        self._in_author_link = False
        self._author_link_href = ""
        self._author_link_text = ""

    def handle_starttag(self, tag: str, attrs):
        attr_dict = {k: v for k, v in attrs}

        if tag in ("script",):
            t = (attr_dict.get("type") or "").lower()
            if t == "application/ld+json":
                self._in_jsonld = True
                self._jsonld_buf = ""
            else:
                self._skip_depth += 1
        elif tag in ("style", "noscript"):
            self._skip_depth += 1

        if tag == "time":
            self.time_elements.append({
                "datetime": attr_dict.get("datetime", ""),
                "text": "",
            })

        if tag == "a":
            href = attr_dict.get("href", "")
            rel = attr_dict.get("rel", "")
            if "author" in rel.lower() or any(p in href.lower() for p in ["/author/", "/team/", "/about/", "/people/"]):
                self._in_author_link = True
                self._author_link_href = href
                self._author_link_text = ""

    def handle_data(self, data: str):
        if self._in_jsonld:
            self._jsonld_buf += data
            return
        if self._skip_depth > 0:
            return

        self._text_parts.append(data)

        if self.time_elements and not self.time_elements[-1]["text"]:
            self.time_elements[-1]["text"] = data.strip()

        if self._in_author_link:
            self._author_link_text += data

    def handle_endtag(self, tag: str):
        if tag == "script":
            if self._in_jsonld:
                self._in_jsonld = False
                if self._jsonld_buf.strip():
                    self.jsonld_blocks.append(self._jsonld_buf.strip())
            elif self._skip_depth > 0:
                self._skip_depth -= 1
        elif tag in ("style", "noscript") and self._skip_depth > 0:
            self._skip_depth -= 1

        if tag == "a" and self._in_author_link:
            self._in_author_link = False
            self.author_links.append({
                "href": self._author_link_href,
                "text": self._author_link_text.strip(),
            })

    def get_text(self) -> str:
        return " ".join(self._text_parts)


# ---------------------------------------------------------------------------
# Date parsing
# ---------------------------------------------------------------------------

DATE_PATTERNS = [
    # "Last updated March 20, 2026" / "Updated: Jan 5, 2025"
    (r"(?:last )?updated[:\s]*(\w+ \d{1,2},?\s*\d{4})", None),
    (r"(?:last )?updated[:\s]*(\d{4}-\d{2}-\d{2})", None),
    # "Published on March 20, 2026"
    (r"published (?:on )?(\w+ \d{1,2},?\s*\d{4})", None),
    (r"published (?:on )?(\d{4}-\d{2}-\d{2})", None),
    # ISO dates
    (r"(\d{4}-\d{2}-\d{2})", None),
    # "March 20, 2026"
    (r"(\w+ \d{1,2},?\s*\d{4})", None),
]

MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def try_parse_date(text: str) -> Optional[str]:
    """Try to parse a date string into YYYY-MM-DD format."""
    text = text.strip().rstrip(",")

    # ISO format
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", text)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

    # "March 20, 2026" or "March 20 2026"
    m = re.match(r"^(\w+)\s+(\d{1,2}),?\s*(\d{4})$", text)
    if m:
        month_str = m.group(1).lower()
        month = MONTH_MAP.get(month_str)
        if month:
            return f"{m.group(3)}-{month:02d}-{int(m.group(2)):02d}"

    return None


def find_visible_dates(text: str) -> list[dict]:
    """Search visible text for date mentions."""
    found = []
    for pattern, _ in DATE_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            raw = m.group(1)
            parsed = try_parse_date(raw)
            if parsed:
                # Get some surrounding context
                start = max(0, m.start() - 30)
                end = min(len(text), m.end() + 10)
                context = text[start:end].strip()
                found.append({"text": context, "parsed_date": parsed})
    # Deduplicate
    seen = set()
    unique = []
    for d in found:
        if d["parsed_date"] not in seen:
            seen.add(d["parsed_date"])
            unique.append(d)
    return unique


# ---------------------------------------------------------------------------
# Schema date extraction
# ---------------------------------------------------------------------------

def extract_schema_dates(blocks: list[str]) -> dict:
    """Extract datePublished and dateModified from JSON-LD."""
    dates = {"datePublished": None, "dateModified": None}
    for block in blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue

        items = []
        if isinstance(data, dict):
            if "@graph" in data:
                items.extend(data["@graph"])
            else:
                items.append(data)
        elif isinstance(data, list):
            items.extend(data)

        for item in items:
            if not isinstance(item, dict):
                continue
            t = item.get("@type", "")
            if isinstance(t, list):
                t = t[0] if t else ""
            if t in ("Article", "BlogPosting", "NewsArticle", "WebPage"):
                if item.get("datePublished"):
                    dates["datePublished"] = str(item["datePublished"])[:10]
                if item.get("dateModified"):
                    dates["dateModified"] = str(item["dateModified"])[:10]
    return dates


# ---------------------------------------------------------------------------
# Author detection
# ---------------------------------------------------------------------------

AUTHOR_PATTERNS = [
    r"\bby\s+([A-Z][a-z]+ [A-Z][a-z]+)",
    r"[Aa]uthor:\s*([A-Z][a-z]+ [A-Z][a-z]+)",
    r"[Ww]ritten by\s+([A-Z][a-z]+ [A-Z][a-z]+)",
]


def find_author(text: str, author_links: list[dict]) -> dict:
    """Search for author information."""
    # Check author links first
    if author_links:
        best = author_links[0]
        return {
            "found": True,
            "name": best["text"] or "Unknown",
            "has_author_page_link": True,
            "author_page_url": best["href"],
        }

    # Fall back to text pattern matching
    for pattern in AUTHOR_PATTERNS:
        m = re.search(pattern, text)
        if m:
            return {
                "found": True,
                "name": m.group(1),
                "has_author_page_link": False,
                "author_page_url": None,
            }

    return {
        "found": False,
        "name": None,
        "has_author_page_link": False,
        "author_page_url": None,
    }


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def compute_freshness_score(
    visible_dates: list[dict],
    schema_dates: dict,
    author: dict,
) -> str:
    """Compute an overall freshness score."""
    now = datetime.now(timezone.utc).date()
    issues: list[str] = []

    # Check most recent date
    all_dates = [d["parsed_date"] for d in visible_dates]
    if schema_dates["dateModified"]:
        all_dates.append(schema_dates["dateModified"])
    if schema_dates["datePublished"]:
        all_dates.append(schema_dates["datePublished"])

    most_recent = None
    if all_dates:
        all_dates.sort(reverse=True)
        most_recent = all_dates[0]

    days_ago = None
    if most_recent:
        try:
            d = datetime.strptime(most_recent, "%Y-%m-%d").date()
            days_ago = (now - d).days
        except ValueError:
            pass

    if days_ago is None:
        score = "poor"
        issues.append("No dates found on page")
    elif days_ago <= 90:
        score = "good"
    elif days_ago <= 180:
        score = "fair"
    elif days_ago <= 365:
        score = "stale"
    else:
        score = "poor"
        issues.append(f"Most recent date is {days_ago} days ago")

    if not schema_dates["dateModified"]:
        issues.append("No dateModified in schema — add it for freshness signals")

    if not visible_dates:
        issues.append("No visible date on page — display 'Last updated' for users and AI")

    if not author["found"]:
        issues.append("No author byline found — author signals feed E-E-A-T and GEO credibility")

    if author["found"] and not author["has_author_page_link"]:
        issues.append("Author has no linked author page — add link to bio/team page")

    # Check date consistency
    if schema_dates["dateModified"] and visible_dates:
        schema_mod = schema_dates["dateModified"]
        visible_latest = max(d["parsed_date"] for d in visible_dates)
        if schema_mod != visible_latest:
            issues.append(
                f"Schema dateModified ({schema_mod}) differs from latest visible date ({visible_latest})"
            )

    return score, days_ago, issues


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def fetch_html(url: str) -> str:
    from urllib.request import Request, urlopen
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; on-page-sgeo-audit/1.0)"})
    with urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


def main():
    ap = argparse.ArgumentParser(description="Check freshness signals on a page")
    ap.add_argument("--url", required=True, help="Page URL to analyze")
    ap.add_argument("--tools", default=None, help="Path to tools.json inventory file")
    args = ap.parse_args()

    try:
        html = fetch_html(args.url)
    except Exception as e:
        print(json.dumps({"error": f"Failed to fetch URL: {e}", "url": args.url}), file=sys.stderr)
        sys.exit(1)

    parser = FreshnessExtractor()
    parser.feed(html)

    full_text = parser.get_text()
    visible_dates = find_visible_dates(full_text)
    schema_dates = extract_schema_dates(parser.jsonld_blocks)
    author = find_author(full_text, parser.author_links)
    score, days_ago, issues = compute_freshness_score(visible_dates, schema_dates, author)

    result = {
        "url": args.url,
        "visible_dates": visible_dates[:5],  # Cap output
        "schema_dates": schema_dates,
        "dates_match": (
            schema_dates["dateModified"] == visible_dates[0]["parsed_date"]
            if schema_dates["dateModified"] and visible_dates
            else None
        ),
        "author": author,
        "days_since_update": days_ago,
        "freshness_score": score,
        "issues": issues,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
