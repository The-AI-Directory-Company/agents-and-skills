#!/usr/bin/env python3
"""Analyze heading hierarchy and GEO heading quality for a URL.

Extracts all headings (H1-H6), validates the hierarchy, classifies H2s
as question-format or declarative, and scores GEO heading quality.

Usage:
    python analyze-headings.py --url https://example.com/page
    python analyze-headings.py --url https://example.com/page --tools tools.json

Output: JSON with heading tree, hierarchy validation, and GEO score.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from typing import Optional


# ---------------------------------------------------------------------------
# HTML Parser
# ---------------------------------------------------------------------------

class HeadingParser(HTMLParser):
    """Extract headings and title from HTML."""

    def __init__(self):
        super().__init__()
        self.headings: list[dict] = []
        self.title = ""
        self._current_tag: Optional[str] = None
        self._current_text = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs):
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._current_tag = tag
            self._current_text = ""
        if tag == "title":
            self._in_title = True

    def handle_data(self, data: str):
        if self._current_tag:
            self._current_text += data
        if self._in_title:
            self.title += data

    def handle_endtag(self, tag: str):
        if tag == self._current_tag:
            level = int(tag[1])
            text = self._current_text.strip()
            text = re.sub(r"\s+", " ", text)
            if text:
                self.headings.append({"level": level, "text": text})
            self._current_tag = None
            self._current_text = ""
        if tag == "title":
            self._in_title = False


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

QUESTION_STARTERS = re.compile(
    r"^(what|how|why|when|where|who|which|is|are|can|does|do|should|will|could)\b",
    re.IGNORECASE,
)


def is_question_heading(text: str) -> bool:
    """Check if a heading is phrased as a question."""
    return bool(QUESTION_STARTERS.match(text.strip())) or text.strip().endswith("?")


def check_hierarchy(headings: list[dict]) -> tuple[bool, list[str]]:
    """Validate heading hierarchy. Return (valid, list of issues)."""
    issues: list[str] = []
    prev_level = 0
    for h in headings:
        level = h["level"]
        if prev_level > 0 and level > prev_level + 1:
            issues.append(f"Skipped level: H{prev_level} -> H{level} (before \"{h['text'][:50]}\")")
        prev_level = level
    return len(issues) == 0, issues


def analyze_headings(headings: list[dict], title: str) -> dict:
    h1s = [h for h in headings if h["level"] == 1]
    h2s = [h for h in headings if h["level"] == 2]

    issues: list[str] = []

    # H1 count
    h1_count = len(h1s)
    if h1_count == 0:
        issues.append("No H1 tag found")
    elif h1_count > 1:
        issues.append(f"Multiple H1 tags found ({h1_count}) — should be exactly 1")

    h1_text = h1s[0]["text"] if h1s else ""

    # Hierarchy validation
    hierarchy_valid, hierarchy_issues = check_hierarchy(headings)
    issues.extend(hierarchy_issues)

    # Question-format analysis for H2s
    question_h2s = 0
    heading_details = []
    for h in headings:
        detail = {
            "level": h["level"],
            "text": h["text"],
        }
        if h["level"] == 2:
            q = is_question_heading(h["text"])
            detail["is_question"] = q
            if q:
                question_h2s += 1
        heading_details.append(detail)

    question_ratio = question_h2s / len(h2s) if h2s else 0

    # GEO heading score
    if not h2s:
        geo_score = "no_h2s"
    elif question_ratio >= 0.4:
        geo_score = "good"
    elif question_ratio >= 0.2:
        geo_score = "fair"
    else:
        geo_score = "poor"

    # Empty headings
    empty = [h for h in headings if not h["text"].strip()]
    if empty:
        issues.append(f"{len(empty)} empty heading(s) found")

    return {
        "h1_count": h1_count,
        "h1_text": h1_text,
        "title_tag": title.strip(),
        "headings": heading_details,
        "total_headings": len(headings),
        "h2_count": len(h2s),
        "question_h2_count": question_h2s,
        "question_heading_ratio": round(question_ratio, 2),
        "geo_heading_score": geo_score,
        "hierarchy_valid": hierarchy_valid,
        "skipped_levels": hierarchy_issues,
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------

def fetch_html(url: str) -> str:
    from urllib.request import Request, urlopen

    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; on-page-sgeo-audit/1.0)"})
    with urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Analyze heading hierarchy and GEO heading quality")
    ap.add_argument("--url", required=True, help="Page URL to analyze")
    ap.add_argument("--tools", default=None, help="Path to tools.json inventory file")
    args = ap.parse_args()

    try:
        html = fetch_html(args.url)
    except Exception as e:
        print(json.dumps({"error": f"Failed to fetch URL: {e}", "url": args.url}), file=sys.stderr)
        sys.exit(1)

    parser = HeadingParser()
    parser.feed(html)

    result = analyze_headings(parser.headings, parser.title)
    result["url"] = args.url
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
